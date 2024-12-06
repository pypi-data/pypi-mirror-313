from pathlib import Path
from typing import Tuple

from pyPhases.util.Logger import classLogger
from pyPhasesRecordloader.downloader.Downloader import Downloader
from pyPhasesRecordloader.Event import Event
from pyPhasesRecordloader.NormalizeRecordSignal import NormalizeRecordSignal
from pyPhasesRecordloader.RecordSignal import RecordSignal
from pyPhasesRecordloader.util.DynamicModule import DynamicModule

from . import recordLoaders as recordManagerPath


class ParseError(Exception):
    pass


class AnnotationException(Exception):
    path = []
    name = ""

    def __init__(self, path):
        self.path = path
        self.name = path[-1]
        super().__init__(self.getMessage())


class AnnotationNotFound(AnnotationException):
    def getMessage(self):
        return f"Annotation was not found in the XML file: {self.path} -> {self.name}"


class AnnotationInvalid(AnnotationException):
    def getMessage(self):
        return f"Annotation is invalid: {self.path}"


class ChannelsNotPresent(Exception):
    channels = []

    def __init__(self, channels, msg=None, recordid="Unknown"):
        if msg is None:
            msg = f"Channels of record {recordid} where not present: {channels}, you can define 'aliases' for the channelname or make the channel optional"
        super().__init__(msg)
        self.channels = channels


@classLogger
class RecordLoader:
    recordLoader = DynamicModule(recordManagerPath)

    recordLoaders = {
        "EDFRecrodLoader": "pyPhasesRecordloader.recordLoaders",
        "H5RecordLoader": "pyPhasesRecordloader.recordLoaders",
        "MatRecordLoader": "pyPhasesRecordloader.recordLoaders",
        "WFDBRecordLoader": "pyPhasesRecordloader.recordLoaders",
        "XMLAnnotationLoader": "pyPhasesRecordloader.recordLoaders",
    }

    def __init__(
        self,
        filePath="",
        targetSignals=None,
        targetSignalTypes=None,
        optionalSignals=None,
        combineChannels=None,
        downloadOptions=None,
        downloaderConfig=None,
    ) -> None:
        downloadOptions = downloadOptions if downloadOptions is not None else {}
        combineChannels = combineChannels if combineChannels is not None else []
        optionalSignals = optionalSignals if optionalSignals is not None else []
        targetSignalTypes = targetSignalTypes if targetSignalTypes is not None else []
        targetSignals = targetSignals if targetSignals is not None else []

        self.filePath = filePath
        self.optionalSignals = optionalSignals
        self.targetSignals = targetSignals
        self.targetSignalTypes = targetSignalTypes
        # lightOff and lightOn are in seconds !
        self.lightOff = 0
        self.lightOn = None
        self.classificationConfig = {}
        self.exportsEventArray = False
        self.firstSleep = None
        self.lastSleep = None
        self.signalTypeDict = dict(zip(self.targetSignals, self.targetSignalTypes))
        self.useDigitalSignals = False
        self.combineChannels = combineChannels
        self.downloadOptions = downloadOptions
        self.downloaderConfig = downloaderConfig
        self.downloader = None

    def registerRecordLoader(name, path):
        RecordLoader.recordLoaders[name] = path

    def delete(self, recordName):
        pass

    def exist(self, recordName):
        pass

    def getDownloader(self):
        if self.downloader is None:
            self.downloader = Downloader.loadFromConfig(self.downloaderConfig)
        return self.downloader

    def setupRemoteReadOrDownload(self):
        dl = self.getDownloader()
        dl.options = self.downloadOptions
        if dl.canReadRemote:
            self.filePath = dl.basePath
        elif not Path(self.filePath + "/.complete").exists():
            dl.downloadTo(self.filePath)
            Path(self.filePath + "/.complete").touch()

    def getHarmonizedSignal(self, recordName):
        signal = self.getSignal(recordName)
        NormalizeRecordSignal().combine(signal, self.combineChannels, self.targetSignals)
        return signal
    
    def addCombinedChannels(self, combinedChannels):
        combinedNames = [c["name"] for c in self.combineChannels]
        for combinedChannel in combinedChannels:
            if "name" not in combinedChannel:
                raise Exception("Combined channels need a name")
            if "type" not in combinedChannel:
                raise Exception("Combined channels need a type")
            if "channel" not in combinedChannel:
                raise Exception("Combined channels need one or multiple 'channel' defined")
            if "combineType" not in combinedChannel:
                raise Exception("Combined channels need a combineType defined: copy, derived, mean, select or selectByQuality")
            if combinedChannel["name"] in combinedNames:
                self.logWarning(f"combined channel was allready added: {combinedChannel['name']}")
                continue
            self.combineChannels.append(combinedChannel)
    
    def getSignalTypeByName(self, signalName):
        if signalName not in self.signalTypeDict:
            combinedChannelsDict = dict(zip([c["name"] for c in self.combineChannels], self.combineChannels))
            if signalName not in combinedChannelsDict:
                raise ChannelsNotPresent(signalName)
            return combinedChannelsDict[signalName]["type"]
        return self.signalTypeDict[signalName]

    def loadRecord(self, recordName, eventTargetFrequency=1) -> Tuple[RecordSignal, Tuple[Event]]:
        # self.downloadOnDemand(recordName)
        signal = self.getHarmonizedSignal(recordName)
        eventList = self.getEventList(recordName, targetFrequency=eventTargetFrequency)

        return signal, eventList

    def getSignal(self, recordName) -> RecordSignal:
        pass

    def loadAnnotation(self, recordName):
        pass

    def getEventList(self, recordName, targetFrequency=1):
        pass

    def existAnnotation(self, recordId):
        """Check if an annotation exist for a given recordId.

        Returns:
            boolean: annotation exist
        """
        return False

    def updateFrequencyForEventList(self, eventList, targetFrequency):
        [e.updateFrequency(targetFrequency) for e in eventList]
        return eventList

    @staticmethod
    def get() -> "RecordLoader":
        packageName = RecordLoader.recordLoaders[RecordLoader.recordLoader.moduleName]
        return RecordLoader.recordLoader.get(packageName)

    def getRecordList(self):
        downloader = self.getDownloader()
        return downloader.getRecordList(self.filePath)

    def getMetaData(self, recordId):
        self.logError("getMetadata not implemented in used recordloader")
        return {}

    def getSignalTypeStrFromDict(self, signalName):
        if self.signalTypeDict == {}:
            self.signalTypeDict = dict(zip(self.targetSignals, self.targetSignalTypes))
        if signalName in self.signalTypeDict:
            signalTypeStr = self.signalTypeDict[signalName]
        else:
            self.logError("Signal '%s' had no type when initilizing the RecordLoader" % str(signalName))
            signalTypeStr = "unknown"
        return signalTypeStr

    def groupBy(self, groupName, recordIds, metadata=None):
        import pandas as pd

        if groupName is not None and metadata is None:
            raise Exception("groupBy is not implemented by this RecordLoader, can't group by '%s'" % groupName)
        if groupName is None:
            return {recordId: [recordId] for recordId in recordIds}
        
        # group by metadata list
        recordGroups = {}
        metadata = metadata.iloc if isinstance(metadata, pd.DataFrame) else metadata
        for data in metadata:
            recordGroups[data["recordId"]] = data[groupName] if groupName in data else ""
        
        groupedIds = {}
        for r in recordIds:
            group = recordGroups[r] if r in recordGroups else ""
            if group not in groupedIds:
                groupedIds[group] = []
            groupedIds[group].append(r)
        return groupedIds

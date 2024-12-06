import h5py
from pathlib import Path

from ..Signal import Signal
from ..RecordSignal import RecordSignal
import json

from ..RecordLoader import RecordLoader


class H5RecordLoader(RecordLoader):
    def __init__(
        self,
        filePath="",
        targetSignals=[],
        targetSignalTypes=[],
        optionalSignals=[],
        combineChannels=[],
    ) -> None:
        super().__init__(
            filePath=filePath,
            targetSignals=targetSignals,
            targetSignalTypes=targetSignalTypes,
            optionalSignals=optionalSignals,
            combineChannels=combineChannels,
        )
        self.h5 = None

    def getFilePath(self, recordName):
        return self.filePath + "/" + recordName + ".h5"

    def getSignal(self, recordName):
        path = self.getFilePath(recordName)
        self.h5 = h5py.File(path, "r")
        channelDescription = json.loads(self.h5.attrs["description"])
        descriptionMap = {}
        for desc in channelDescription:
            descriptionMap[desc["path"]] = desc

        psgSignal = RecordSignal()

        for name in self.targetSignals:
            desc = descriptionMap[name]
            signalArray = self.h5[name][:]
            signal = Signal(name, signalArray, frequency=desc["fs"])
            signal.typeStr = self.getSignalTypeStrFromDict(signal.name)
            psgSignal.addSignal(signal)

        return psgSignal

    def exist(self, recordName):
        return Path(self.getFilePath(recordName)).exists()

    def existAnnotation(self, recordName):
        return self.exist(recordName)

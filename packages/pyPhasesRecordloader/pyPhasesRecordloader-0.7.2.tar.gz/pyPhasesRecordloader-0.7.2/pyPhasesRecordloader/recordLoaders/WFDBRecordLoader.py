from pathlib import Path

import wfdb

from pyPhasesRecordloader.Event import Event
from pyPhasesRecordloader.RecordLoader import RecordLoader
from pyPhasesRecordloader.RecordSignal import RecordSignal
from pyPhasesRecordloader.Signal import Signal


class WFDBRecordLoader(RecordLoader):
    annotationExtension = "ann"

    def getFilePath(self, recordName):
        return self.filePath + "/" + recordName
    
    def getSignalHeaders(self, recordName):
        _, fields = wfdb.rdsamp(self.getFilePath(recordName), sampfrom=0, sampto=1)
        return [{"name": n, "type": self.getSignalTypeStrFromDict(n)} for n in fields["sig_name"]]
    
    def getMetaData(self, recordId):
        return {}

    def getSignal(self, recordName):
        signals, fields = wfdb.rdsamp(self.getFilePath(recordName))

        psgSignal = RecordSignal(recordId=recordName)

        for name in self.targetSignals:
            signalIndex = fields["sig_name"].index(name)
            signalArray = signals[:, signalIndex]
            signal = Signal(name, signalArray, frequency=fields["fs"])
            signal.typeStr = self.getSignalTypeStrFromDict(signal.name)
            psgSignal.addSignal(signal)

        return psgSignal

    def exist(self, recordName):
        return Path(self.getFilePath(recordName) + ".mat").exists()

    def existAnnotation(self, recordName):
        return Path(self.getFilePath(recordName) + "." + self.annotationExtension).exists()

    def getEventListFromWFDBAnnotations(self, wfdbannotations):
        events = []
        eventMap = {}
        annotationNames = wfdbannotations.aux_note
        for index, eventId in enumerate(annotationNames):

            if eventId[0] == "(":
                eventName = eventId[1:]
                event = Event(eventName, frequency=wfdbannotations.fs)
                if eventName in eventMap:
                    raise Exception("Nested Event %s in wfdb annotations" % eventName)
                eventMap[eventName] = event
                event.start = wfdbannotations.sample[index]
                events.append(event)
            elif eventId[-1:] == ")":
                eventName = eventId[:-1]
                if eventName not in eventMap:
                    raise Exception("Event closed before it was opened: " % eventName)
                event = eventMap[eventName]
                event.duration = wfdbannotations.sample[index] - event.start
                del eventMap[eventName]
            else:
                event = Event(eventId, frequency=wfdbannotations.fs)
                eventMap[eventId] = event
                event.start = wfdbannotations.sample[index]

                if "default" in eventMap:
                    lastEvent = eventMap["default"]
                    lastEvent.duration = event.start - lastEvent.start
                eventMap["default"] = event
                events.append(event)

        return events

    def getEventList(self, recordName, targetFrequency=1):
        annotations = wfdb.rdann(self.getFilePath(recordName), self.annotationExtension)
        eventArray = self.getEventListFromWFDBAnnotations(annotations)

        if targetFrequency != annotations.fs:
            eventArray = self.updateFrequencyForEventList(eventArray, targetFrequency)

        return eventArray

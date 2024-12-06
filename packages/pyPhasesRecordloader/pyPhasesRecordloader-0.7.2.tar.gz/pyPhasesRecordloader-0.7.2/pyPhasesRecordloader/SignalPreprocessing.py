from typing import List

import numpy as np

from pyPhases import classLogger
from pyPhasesRecordloader import ChannelsNotPresent, Event, RecordSignal, Signal


class PreprocessSteMissingException(Exception):
    pass


@classLogger
class SignalPreprocessing:
    def __init__(self, config) -> None:
        self.config = config
        self.stepsPerType = config["stepsPerType"]

    def step(self, stepname, signal: Signal, recordSignal: RecordSignal, **options):
        # check if manipulation step exist

        if hasattr(self, stepname):
            # call method
            return getattr(self, stepname)(signal, recordSignal, **options)
        else:
            raise PreprocessSteMissingException(f"Preprocessing {stepname} not found")

    def preprocessingSignal(self, psgSignal: RecordSignal):
        self.preprocessSignalByType(psgSignal, self.stepsPerType)

    def preprocessSignalByType(self, psgSignal: RecordSignal, stepsPerType):
        if stepsPerType is None:
            return
        
        for signal in psgSignal.signals:
            cName = signal.name
            if cName in psgSignal.signalNames:
                signal = psgSignal.getSignalByName(cName)
                signalType = signal.typeStr

                if signalType in stepsPerType:
                    stepNames = stepsPerType[signalType]

                    for processStep in stepNames:
                        options = {}
                        if isinstance(processStep, dict):
                            name = processStep["name"]
                            options = {key: value for key, value in processStep.items() if key != "name"}
                            processStep = name
                        self.step(processStep, signal, psgSignal, **options)
                elif signalType is not None:
                    self.logError(
                        f"Signaltype {signal.type} for signal {signal.name} has no preprocessing steps (defined in preprocessing.stepsPerType.[type])"
                    )

    def extendEvents(self, events: List[Event], extendEventsByName: dict):
        if extendEventsByName is not None:
            for event in events:
                if event.name in extendEventsByName:
                    addBefore, addAfter = extendEventsByName[event.name]
                    event.start -= addBefore
                    event.duration += addBefore + addAfter
        return events

    def resampleSimple(self, signal: Signal, recordSignal: RecordSignal, targetFrequency=None):
        targetFrequency = targetFrequency or recordSignal.targetFrequency
        factor = signal.frequency / targetFrequency
        if factor >= 1:
            signal.signal = signal.signal[:: int(factor)]
        else:
            signal.signal = np.repeat(signal.signal, int(1 / factor), axis=0)
        signal.frequency = targetFrequency

    def standardisation(self, signal: Signal, recordSignal: RecordSignal):
        center = np.mean(signal.signal)
        scale = np.std(signal.signal)
        if scale == 0:
            scale = 1
        signal.signal = (signal.signal - center) / scale

    def cut(self, signal: Signal, recordSignal: RecordSignal, minValue, maxValue):
        signal.signal[signal.signal > maxValue] = maxValue
        signal.signal[signal.signal < minValue] = minValue

    def normalize(self, signal: Signal, recordSignal: RecordSignal, minValue=0, maxValue=1):
        signalMin = min(signal.signal)
        signalMax = max(signal.signal)
        if minValue is None:
            minValue = signalMin

        if maxValue is None:
            maxValue = signalMax

        signalMinAbs = -1 * signalMin
        signal.signal = (signal.signal + signalMinAbs) / (signalMinAbs + signalMax)
        signal.signal *= maxValue - minValue
        signal.signal += minValue

    def normalizePercentage(self, signal: Signal, recordSignal: RecordSignal):
        self.cut(signal, recordSignal, 0, 100)
        self.normalize(signal, recordSignal, 0, 1)

    def resample(self, signal: Signal, recordSignal: RecordSignal, targetFrequency=None):
        from scipy.signal import resample
        targetFrequency = targetFrequency or recordSignal.targetFrequency

        signalLength = int(len(signal.signal) * targetFrequency / signal.frequency)
        signal.signal = resample(signal.signal, signalLength)
        signal.frequency = targetFrequency

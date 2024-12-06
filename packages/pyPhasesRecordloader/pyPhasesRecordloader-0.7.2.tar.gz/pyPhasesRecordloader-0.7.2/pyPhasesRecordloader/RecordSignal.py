from typing import List

import numpy as np

from pyPhases.util.Logger import classLogger
from .Signal import Signal


@classLogger
class RecordSignal:
    processType = np.float32
    finalType = np.float32
    labelType = np.int32

    def __init__(self, targetFrequency=None, recordId=None):
        self.recordId = recordId
        self.signals: List[Signal] = []
        self.labelSignals = []
        self.signalNames = []
        self.targetFrequency = targetFrequency
        self.shape = None

    def getSignalFrequency(self, y):
        yFrequency = self.targetFrequency / (self.getShape()[1] / y.shape[0])
        return yFrequency

    def getSignalLength(self):
        return self.getShape()[1]
    
    def __len__(self):
        return self.getSignalLength()

    @staticmethod
    def fromArray(array, targetFrequency=200, sourceFrequency=200, names=None, transpose=False):
        recordSignal = RecordSignal(targetFrequency=targetFrequency)
        if transpose:
            array = array.transpose()
        for i, signalArray in enumerate(array):
            name = names[i] if names is not None else "Signal%i" % i
            signal = Signal(name, signal=signalArray, frequency=sourceFrequency)
            recordSignal.addSignal(signal)

        return recordSignal
    
    def updateSignalsFromArray(self, array):
        for i, signalArray in enumerate(array):
            self.signals[i].signal = signalArray
        self.shape = None

    def addSignal(self, signal: Signal, signalLabel=None):
        signalLabel = signal.name if signalLabel is None else signalLabel
        self.signals.append(signal)
        self.signalNames.append(signalLabel)
        signal.signal = signal.signal.astype(self.processType)
        self.shape = None

    def addSignals(self, signals: "list[Signal]"):
        for s in signals:
            self.addSignal(s)

    def addLabelSignal(self, signal: Signal):
        self.labelType = signal.signal.dtype
        self.labelSignals.append(signal)

    def addLabelSignals(self, signals: "list[Signal]"):
        for s in signals:
            self.addLabelSignal(s)

    def getShape(self, forceRecalculate=False):
        if self.shape is None or forceRecalculate:
            count = len(self.signals)
            count += len(self.labelSignals)
            if count == 0:
                raise Exception("can't determine signal shape if no signal is present")
            firstSignal = self.signals[0]
            frequency = firstSignal.frequency
            length = len(firstSignal.signal)
            factor = frequency / self.targetFrequency
            if length % factor > 0:
                self.logWarning("Target frequency might not be unambiguously")

            length = int(length / factor)
            self.shape = (count, length)

        return self.shape

    def getChannelList(self, listOrSlice):
        return list(range(0, self.signals.shape[1]))[listOrSlice] if type(listOrSlice) == slice else listOrSlice

    def generateFlatline(self, name="FLATLINE"):
        if name in self.signalNames:
            return self.getSignalIndexByName(name)

        signal = Signal("FLATLINE", frequency=self.targetFrequency)
        signal.signal = np.full(self.getShape()[1], 0)
        self.addSignal(signal)
        return signal

    def getSignalIndexByName(self, name):
        if name not in self.signalNames:
            if name == "FLATLINE":
                self.generateFlatline()
            else:
                from .RecordLoader import ChannelsNotPresent
                raise ChannelsNotPresent([name])
        return self.signalNames.index(name)

    def getSignalByName(self, name) -> Signal:
        index = self.getSignalIndexByName(name)
        return self.signals[index]

    def getFirstSignalName(self, nameList) -> str:
        try:
            name = next(signalName for signalName in nameList if signalName in self.signalNames)
        except StopIteration:
            if "FLATLINE" in nameList:
                return "FLATLINE"
            from .RecordLoader import ChannelsNotPresent
            raise ChannelsNotPresent(nameList, msg="Non of the target signals (%s) is present in the record,: %s you can use FLATLINE as channel name to replace missing channels with a flat line" % (nameList, self.signalNames))
        return name

    def getFirstSignalByName(self, nameList) -> Signal:

        name = self.getFirstSignalName(nameList)
        if name == "FLATLINE":
            return self.generateFlatline()
        index = self.getSignalIndexByName(name)
        return self.signals[index]

    def createSignalArray(self, signals, transpose):
        if len(signals) > 1:
            try:
                a = np.concatenate([s.signal.reshape(1, -1) for s in signals], axis=0)
            except ValueError as e:
                # check if signals have different length
                mismatchedSignals = []
                for s in signals:
                    if len(s.signal) != len(signals[0].signal):
                        mismatchedSignals.append(s.name)

                raise Exception(
                    "Not all Signals have the same length, can't create a singla numpy array.\n"
                    + "Make sure all Signals in preprocessing.targetChannels are resampled to a even length.\n"
                    "Signals that have a different shape then the first one: %s\n" % mismatchedSignals + "Error: %s" % e
                )
        else:
            a = signals[0].signal.reshape(1, -1)

        if transpose:
            a = a.transpose(1, 0)

        return a

    def getSignalArray(self, targetChannels=None, transpose=True, fillEmpty=True):
        "get all psg Signals that are present in targetChannels concatenated into one array"

        if targetChannels is not None:
            cList = []

            # target channel can be a string representing the signal name, or an list with
            # channelnames, where the first one is picked
            for channelStringorArray in targetChannels:
                if isinstance(channelStringorArray, list):
                    try:
                        signal = self.getFirstSignalByName(channelStringorArray)
                    except StopIteration:
                        if fillEmpty:
                            signal = Signal("empty", np.full(self.getShape()[1], 0), self.targetFrequency)
                            self.logError(
                                "None of the given targetchannel (%s) is present in the current psg signal"
                                % str(channelStringorArray)
                            )
                        else:
                            raise Exception(
                                "None of the given targetchannel (%s) is present in the current psg signal"
                                % str(channelStringorArray)
                            )
                else:
                    signalName = channelStringorArray
                    signal = self.getSignalByName(signalName)

                cList.append(signal)
        else:
            cList = self.signals

        return self.createSignalArray(cList, transpose).astype(self.finalType)

    def getAnnotationArray(self, transpose=True):
        "get all annotation signals concatenated into one array"

        return self.createSignalArray(self.labelSignals, transpose).astype(self.labelType)

    def reduceSignals(self, keepSignalNames):
        newSignals = []
        newSignalNames = []
        for keep in keepSignalNames:
            signalName = keep if isinstance(keep, str) else self.getFirstSignalName(keep)
            signal = self.getSignalByName(signalName)
            newSignals.append(signal)
            newSignalNames.append(signal.name)
        self.signalNames = newSignalNames
        self.signals = newSignals
        self.shape = None

    def combine(self, channels, newName="Unknown", mean=True, derive=False):
        count = len(channels)
        mainIndex = self.getSignalIndexByName(channels[0])
        mainSignal = self.signals[mainIndex]
        sig = mainSignal.signal.copy()

        targetFrequency = mainSignal.frequency
        targetLength = len(sig)

        for name in channels:
            i = self.getSignalIndexByName(name)
            if i != mainIndex:
                signal = self.signals[i]
                sArray = signal.signal
                if signal.frequency != targetFrequency:
                    raise Exception(
                        "The Channel %s does not have the same frequency with %s ... unable to combine"
                        % (signal.name, mainSignal.name)
                    )

                if len(sArray) != targetLength:
                    raise Exception("can only combine channels with the same size/sample rate")

                if derive:
                    sig -= signal.signal
                else:
                    sig += signal.signal

        if mean:
            sig = sig / count

        self.addSignal(Signal(newName, sig, frequency=targetFrequency))

    def derive(self, channels, newName="Unknown", mean=True):
        self.combine(channels, newName, mean=False, derive=True)

    def signalOffset(self, startOffset, endOffset=None, offsetFrequency=1):
        startOffset /= offsetFrequency

        if endOffset is not None:
            endOffset /= offsetFrequency

        for s in self.signals + self.labelSignals:
            f = s.frequency
            start = int(startOffset * f)
            end = None if endOffset is None else int(endOffset * f)
            s.signal = s.signal[slice(start, end)]

        self.shape = None

    def signalCutBySignalBoolSignal(self, boolSignal):
        for s in self.signals + self.labelSignals:
            s.signal = s.signal[boolSignal]

    def __getitem__(self, signalNames) -> "RecordSignal":
        """ Returns a new RecordSignal object with the given signalNames.
        """
        signal = RecordSignal(targetFrequency=self.targetFrequency, recordId=self.recordId)
        if isinstance(signalNames, str):
            signalNames = [signalNames]
            
        for name in signalNames:
            signal.addSignal(self.getSignalByName(name))
            
        return signal
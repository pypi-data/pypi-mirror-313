from pathlib import Path

from ..RecordLoader import RecordLoader
from ..RecordSignal import RecordSignal
from ..Signal import Signal


class MatRecordLoader(RecordLoader):
    def __init__(self, filePath, targetSignals, targetSignalTypes) -> None:
        super().__init__(
            filePath=filePath,
            targetSignals=targetSignals,
            targetSignalTypes=targetSignalTypes,
        )
        self.WFDBRecordLoader = None
        self.samplingRate = 200
        self.extension = ".mat"

    def getFilePath(self, recordName):
        return self.filePath + "/" + recordName + self.extension

    def getSignal(self, recordName):
        from scipy.io import loadmat
        signals = loadmat(self.getFilePath(recordName))
        signals = signals["val"]

        psgSignal = RecordSignal()

        for name in self.targetSignals:
            signalIndex = self.signalMap.index(name)
            signalArray = signals[signalIndex, :]
            signal = Signal(name, signalArray, frequency=self.samplingRate)
            psgSignal.addSignal(signal)

        return psgSignal

    def exist(self, recordName):
        return Path(self.getFilePath(recordName)).exists()

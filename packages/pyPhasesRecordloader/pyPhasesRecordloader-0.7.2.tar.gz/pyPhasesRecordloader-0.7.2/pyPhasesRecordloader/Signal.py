from enum import Enum

import numpy as np
from pyPhases.util.Logger import classLogger


class SignalType(Enum):
    UNKNOWN = 0
    EEG = 1
    EOG = 2
    EMG = 3
    EFFORT = 4
    FLOW = 5
    MIC = 6
    SAO2 = 7
    BODY = 8
    RR = 9
    ECG = 10


signalTypeDict = {
    "sao2": SignalType.SAO2,
    # "hr": ,
    "eeg": SignalType.EEG,
    "eog": SignalType.EOG,
    "emg": SignalType.EMG,
    "ecg": SignalType.ECG,
    "body": SignalType.BODY,
    "effort": SignalType.EFFORT,
    "flow": SignalType.FLOW,
    # "light": ,
    # "oxstat": ,
    "mic": SignalType.MIC,
    # "cpap": ,
    "unknown": SignalType.UNKNOWN,
}

defaultChannelSettings = {
    SignalType.UNKNOWN: {
        "dimension": "",
        "physicalMin": 0,
        "physicalMax": 100,
        "digitalMin": 0,
        "digitalMax": 1023,
    },
    SignalType.EEG: {
        "dimension": "uV",
        "physicalMin": -300,
        "physicalMax": 300,
        "digitalMin": 0,
        "digitalMax": 1023,
    },
    SignalType.EOG: {
        "dimension": "uV",
        "physicalMin": -300,
        "physicalMax": 300,
        "digitalMin": 0,
        "digitalMax": 255,
    },
    SignalType.EMG: {
        "dimension": "uV",
        "physicalMin": -78,
        "physicalMax": 78,
        "digitalMin": 0,
        "digitalMax": 1023,
    },
    SignalType.EFFORT: {
        "dimension": "",
        "physicalMin": -100,
        "physicalMax": 100,
        "digitalMin": 0,
        "digitalMax": 4095,
    },
    SignalType.FLOW: {
        "dimension": "",
        "physicalMin": 0,
        "physicalMax": 4095,
        "digitalMin": 0,
        "digitalMax": 4095,
    },
    SignalType.MIC: {
        "dimension": "",
        "physicalMin": -100,
        "physicalMax": 100,
        "digitalMin": 0,
        "digitalMax": 255,
    },
    SignalType.SAO2: {
        "dimension": "%",
        "physicalMin": 0,
        "physicalMax": 100,
        "digitalMin": 0,
        "digitalMax": 1023,
    },
    SignalType.BODY: {
        "dimension": "",
        "physicalMin": 0,
        "physicalMax": 255,
        "digitalMin": 0,
        "digitalMax": 255,
    },
    SignalType.RR: {
        "dimension": "",
        "physicalMin": 0,
        "physicalMax": 200,
        "digitalMin": 0,
        "digitalMax": 200,
    },
    SignalType.ECG: {
        "dimension": "uV",
        "physicalMin": -300,
        "physicalMax": 300,
        "digitalMin": 0,
        "digitalMax": 1023,
    },
}


@classLogger
class Signal:
    def __init__(self, name, signal: np.ndarray, frequency: int, type=SignalType.UNKNOWN, typeStr="unknown") -> None:
        self.name = name
        self.signal = signal
        self.frequency = frequency
        self.type = type
        self.typeStr = typeStr
        self.isDigital = False

        self.dimension = None
        self.physicalMin = None
        self.physicalMax = None
        self.digitalMin = None
        self.digitalMax = None
        self.transducer = ""
        self.prefilter = ""
        self.sourceIndex = None
        self.processHistory = []
        self.quality = None

        self.loadDefaultSettings()

    def loadDefaultSettings(self):
        settings = defaultChannelSettings[self.type]
        for _, index in enumerate(settings):
            setattr(self, index, settings[index])

    def setSignalTypeFromTypeStr(self):
        if self.typeStr in signalTypeDict:
            self.type = signalTypeDict[self.typeStr]
        else:
            self.type = SignalType.UNKNOWN
            self.logWarning("Unkown type of signal '%s'" % self.typeStr)

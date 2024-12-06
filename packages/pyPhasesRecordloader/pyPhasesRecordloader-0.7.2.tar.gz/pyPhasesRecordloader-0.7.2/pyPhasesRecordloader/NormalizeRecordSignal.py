from pyPhases.util.Logger import classLogger
from pyPhasesRecordloader.RecordSignal import RecordSignal
from pyPhasesRecordloader.Signal import Signal


@classLogger
class NormalizeRecordSignal:
    def combine(self, signal: RecordSignal, combineChannels, targetSignals):
        from pyPhasesRecordloader.RecordLoader import ChannelsNotPresent

        for combineConfig in combineChannels:
            newChannelName = combineConfig["name"]
            channelType = combineConfig["type"]
            channels = combineConfig["channel"]
            if newChannelName in signal.signalNames and "overwrite" not in combineConfig:
                self.logError(f"Channel {newChannelName} already exists")
                continue

            if newChannelName in signal.signalNames and not combineConfig["overwrite"]:
                continue

            checkChannels = channels if isinstance(channels, list) else [channels]
            channelIsDefined = all(name in targetSignals for name in checkChannels)
            if not channelIsDefined:
                self.logWarning(f"Can't combine channel {newChannelName}, signal(s) {checkChannels} not in targetSignals")
                continue

            typeStr = combineConfig["combineType"]
            if typeStr == "copy":
                srcSignal = signal.getSignalByName(channels)
                srcArray = srcSignal.signal.copy()
                s = Signal(newChannelName, srcArray, srcSignal.frequency)
                signal.addSignal(s)
            elif typeStr == "derived":
                signal.derive(channels, newChannelName)
            elif typeStr == "mean":
                signal.combine(channels, newChannelName)
            elif typeStr == "select":
                found = False
                for name in channels:
                    if name in signal.signalNames:
                        index = signal.getSignalIndexByName(name)
                        signal.signals[index].name = newChannelName
                        signal.signalNames[index] = newChannelName
                        found = True
                        break
                if not found:
                    self.logError(f"Missing channel {newChannelName} for {signal.recordId}")
                    raise ChannelsNotPresent(channels, signal.recordId)
            elif typeStr == "selectByQuality":
                bestChannelIndex = -1
                bestQuality = -1
                for name in channels:
                    if name in signal.signalNames:
                        index = signal.getSignalIndexByName(name)
                        quality = signal.signals[index].quality
                        if quality is not None and quality > bestQuality:
                            bestQuality = quality
                            bestChannelIndex = index
                if bestChannelIndex >= 0:
                    signal.signals[bestChannelIndex].name = newChannelName
                    signal.signalNames[bestChannelIndex] = newChannelName
                else:
                    self.logError(
                        f"Missing channel {newChannelName} for {signal.recordId} or missing signal quality for channel selection"
                    )
                    raise ChannelsNotPresent(channels, signal.recordId)
            else:
                raise Exception(f"Combine type {typeStr} does not exist")

            newSignal = signal.getSignalByName(newChannelName)
            newSignal.typeStr = channelType
            newSignal.setSignalTypeFromTypeStr()

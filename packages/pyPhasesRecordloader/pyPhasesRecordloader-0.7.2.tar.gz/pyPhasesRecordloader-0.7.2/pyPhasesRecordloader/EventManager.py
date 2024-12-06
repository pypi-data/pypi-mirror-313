import math
from typing import List

import numpy as np
import pandas as pd

from pyPhases.util.Logger import classLogger

from .Event import Event


class EventNotListedException(Exception):
    pass


class EventWrongOrdering(Exception):
    pass


@classLogger
class EventManager:
    eventGroups: dict = None
    defaultIgnoreValue: str = "ignore"

    def __init__(self, eventGroups):
        self.eventGroups = eventGroups
        self.eventGroupMap = None

    def getEventsFromSignal(
        self, signal, values, potentiate=False, factor=1, order=True, owner=None, ignore=None
    ):  # , singleEvents=False
        signal = np.array(signal)  # force np array, to reduce unpredictable outcomes
        events = []
        valueCount = len(values)
        lastEvent = {i: None for i in range(valueCount)}

        for classIndex, eventName in enumerate(values):
            if ignore is not None and classIndex == ignore:
                continue

            if potentiate:
                checkSignal = signal & int(math.pow(2, classIndex)) > 0
            else:
                checkSignal = signal == classIndex

            eventPosition = np.where(checkSignal)[0]

            lastEvent = None
            lastIndex = -2
            for index in eventPosition:
                if index > lastIndex + 1:
                    time = index * factor
                    if lastEvent is not None:
                        lastEvent.duration = (lastIndex + 1) * factor - lastEvent.start
                        events.append(lastEvent)
                    lastEvent = Event(name=eventName, start=time, owner=owner)
                lastIndex = index
            if lastEvent is not None:
                lastEvent.duration = (lastIndex + 1) * factor - lastEvent.start
                events.append(lastEvent)

        if order:
            events.sort(key=lambda e: e.start)

        return events

    def getNumericEventsFromSignal(
        self, signal, eventName, potentiate=False, factor=1, order=True, owner=None
    ):  # , singleEvents=False
        signal = np.array(signal)  # force np array, to reduce unpredictable outcomes
        events = []
        values = np.unique(signal)
        values = values[~np.isnan(values)]
        valueCount = len(values)
        lastEvent = {i: None for i in range(valueCount)}

        for classIndex, numeric in enumerate(values):
            if potentiate:
                # checkSignal = signal & int(math.pow(2, classIndex)) > 0
                pass
            else:
                checkSignal = signal == numeric

            eventPosition = np.where(checkSignal)[0]

            lastEvent = None
            lastIndex = -2
            for index in eventPosition:
                if index > lastIndex + 1:
                    time = index * factor
                    if lastEvent is not None:
                        lastEvent.duration = (lastIndex + 1) * factor - lastEvent.start
                        events.append(lastEvent)
                    lastEvent = Event(name=eventName, start=time, owner=owner, amplitude=numeric)
                lastIndex = index
            if lastEvent is not None:
                lastEvent.duration = (lastIndex + 1) * factor - lastEvent.start
                events.append(lastEvent)

        if order:
            events.sort(key=lambda e: e.start)

        return events

    def getEventGroupMap(self):
        if self.eventGroupMap is None and self.eventGroups is not None:
            groupMap = {}
            for group in self.eventGroups.keys():
                eventNames = self.eventGroups[group]
                for eName in eventNames:
                    if eName in groupMap:
                        raise Exception("Event GroupMap is not distinct, the event %s is ambiguous" % eName)
                    groupMap[eName] = group
            self.eventGroupMap = groupMap

        return self.eventGroupMap

    def getDataframeFromEvents(self, events):
        groupMap = self.getEventGroupMap()
        eventDict = list(
            map(
                lambda e: (
                    e.name,
                    e.start,
                    e.duration,
                    e.start + e.duration,
                    e.amplitude,
                    e.manual,
                    groupMap[e.name] if groupMap is not None and e.name in groupMap else None,
                    e.data,
                ),
                events,
            )
        )
        columns = ["name", "start", "duration", "end", "amplitude", "manual", "group", "data"]
        return pd.DataFrame(eventDict, columns=columns)

    def getDFValuesFromGroup(
        self, df, fromDF, colMap, offsetStart=None, offsetEnd=None, fixedDuration=None, addClosingTags=False
    ):
        cols = {n: [] for n in colMap}

        if offsetStart is None:
            offsetStart = 0

        if offsetEnd is None:
            offsetEnd = 0

        for e in df.iloc:
            start = e.start + offsetStart
            if fixedDuration:
                end = e.start + fixedDuration + offsetEnd
            else:
                end = e.end + offsetEnd
            overlappingEvents = fromDF.query("start < %f and end > %f" % (end, start))

            for name in cols:
                eventString = ",".join([ev[colMap[name]] for ev in overlappingEvents.iloc])
                if len(overlappingEvents) > 0 and addClosingTags:
                    startOpen = "[" if overlappingEvents.iloc[0].start > e.start else "]"
                    endOpen = "[" if overlappingEvents.iloc[-1].end > e.end else "]"
                    eventString = startOpen + eventString + endOpen

                cols[name].append(eventString)

        return cols

    def appendDataframe(
        self, df, dfToAppend, colMap, offsetStart=None, offsetEnd=None, fixedDuration=None, addClosingTags=False
    ):
        cols = self.getDFValuesFromGroup(
            df,
            dfToAppend,
            colMap,
            offsetStart=offsetStart,
            offsetEnd=offsetEnd,
            fixedDuration=fixedDuration,
            addClosingTags=addClosingTags,
        )

        for name in cols:
            df.loc[:, name] = cols[name]

    def dfAppendGroups(
        self,
        df,
        sourceGroup,
        groupToAppend,
        newGroupName=None,
        offsetStart=None,
        offsetEnd=None,
        fixedDuration=None,
        addClosingTags=False,
        defaultValue="",
    ):
        newGroupName = groupToAppend if newGroupName is None else newGroupName
        colMap = {newGroupName: "name"}
        source = df.query("group == '%s'" % sourceGroup)

        cols = self.getDFValuesFromGroup(
            source,
            df.query("group == '%s'" % groupToAppend),
            colMap=colMap,
            offsetStart=offsetStart,
            offsetEnd=offsetEnd,
            fixedDuration=fixedDuration,
            addClosingTags=addClosingTags,
        )

        for name in cols:
            value = cols[name] if len(cols[name]) > 0 else defaultValue
            df.loc[source.index, name] = value

        return df.update(source)

    def getGroupEventsFromSignal(self, signal, eventGroup, potentiate=True, factor=1):  # , singleEvents=False
        values = self.eventGroups[eventGroup]

        return self.getEventsFromSignal(signal, values, potentiate=potentiate, factor=factor)

    def getEventSignalFromWfdbAnnotations(self, annotations, signalShape, defaultEventName="sleepStage"):
        annotationNames = annotations.aux_note
        annotationIndexes = annotations.sample
        defaultEventEpochLength = annotations.fs * 30 if annotations.fs is not None else 1
        return self.getEventSignalFromAnnotations(
            annotationIndexes, annotationNames, signalShape, defaultEventName, defaultEventEpochLength=defaultEventEpochLength
        )

    def findEventValue(self, eventValueName):
        for _, groupName in enumerate(self.eventGroups):
            group = self.eventGroups[groupName]
            if eventValueName in group:
                eventValue = 2 ** group.index(eventValueName)
                return groupName, eventValue
        raise EventNotListedException

    def getEventSignalFromAnnotationMap(
        self, annotations, signalShape, defaultEventName="sleepStage", exclusiveIndexing=True, forceGapBetweenEvents=False
    ):
        if len(annotations) == 0:
            annotationIndexes, annotationNames = [], []
        else:
            annotationIndexes, annotationNames = zip(*annotations)

        return self.getEventSignalFromAnnotations(
            annotationIndexes,
            annotationNames,
            signalShape,
            defaultEventName,
            exclusiveIndexing=exclusiveIndexing,
            forceGapBetweenEvents=forceGapBetweenEvents,
        )

    def getEventSignalFromEventDF(self, eventDF, targetFrequency=0, eventName="name"):
        return self.getWdfbCompatibleEventsFromList(eventDF.iloc, targetFrequency, eventName=eventName)

    def getWdfbCompatibleEventsFromList(self, events: List[Event], targetFrequency=0, eventName="name"):
        # transform the evnent list to wfdb compatible annotatio: [5, (event1], [6, event1)] or [[30, W], [60, R]]
        wdfbEvents = []
        for e in events:
            originalFrequency = 1
            factor = targetFrequency / originalFrequency
            start = int(e["start"] * factor)
            if np.isnan(e["duration"]):
                continue
            duration = int(e["duration"] * factor)
            end = start + duration
            name = e[eventName]

            if e.duration > 0:
                wdfbEvents.append([start, "(" + name])
                wdfbEvents.append([end - 1, name + ")"])
            else:
                wdfbEvents.append([start, name])

        return wdfbEvents

    def getWdfbCompatibleEventsFromEventList(
        self,
        events: List[Event],
        targetFrequency=0,
    ):
        # transform the evnent list to wfdb compatible annotatio: [5, (event1], [6, event1)] or [[30, W], [60, R]]
        wdfbEvents = []
        for e in events:
            originalFrequency = 1
            factor = targetFrequency / originalFrequency
            start = round(e.start * factor)
            if np.isnan(e.duration):
                continue
            duration = round(e.duration * factor)
            end = start + duration
            name = e.name

            if e.duration > 0:
                wdfbEvents.append([start, "(" + name])
                wdfbEvents.append([end - 1, name + ")"])
            else:
                wdfbEvents.append([start, name])

        return wdfbEvents

    def getEventSignalFromDF(self, events: List[Event], shape, targetFrequency, forceGapBetweenEvents=False, eventName="name"):
        wfdbEvents = self.getEventSignalFromEventDF(events, targetFrequency, eventName=eventName)
        return self.getEventSignalFromAnnotationMap(wfdbEvents, shape, forceGapBetweenEvents=forceGapBetweenEvents)

    def getEventSignalFromList(self, events: List[Event], shape, targetFrequency, forceGapBetweenEvents=False):
        wfdbEvents = self.getWdfbCompatibleEventsFromEventList(events, targetFrequency)
        return self.getEventSignalFromAnnotationMap(wfdbEvents, shape, forceGapBetweenEvents=forceGapBetweenEvents)

    def getEventSignalFromAnnotations(
        self,
        annotationIndexes,
        annotationNames,
        signalShape,
        defaultEventName="sleepStage",
        raiseEventNotListed=False,
        exclusiveIndexing=True,
        defaultEventEpochLength=1,
        forceGapBetweenEvents=False,
    ):
        # TODO: refactor, to make it more readable
        currentEventIndexes = {}
        lastDefaultGroupIndex = {defaultEventName: 0}
        lastdefaultGroupValue = {defaultEventName: 0}
        emptySignalValue = 0
        emptySignal = np.full(signalShape, emptySignalValue).astype(np.int32)
        eventSignals = {}

        def getSampleIndex(annotationIndex):
            return annotationIndexes[annotationIndex]

        for annotationIndex, event in enumerate(annotationNames):
            eventValueName = event
            start = True
            add = False
            eventValue = 1

            # eventMarker are events in the form of "(event" or "event)"
            isEventMarker = False
            eventName = None

            if event[0] == "(":
                eventValueName = event[1:]
                isEventMarker = True
            elif event[-1:] == ")":
                eventValueName = event[0:-1]
                start = False
                isEventMarker = True

            try:
                eventName, eventValue = self.findEventValue(eventValueName)
            except EventNotListedException:
                if raiseEventNotListed:
                    raise EventNotListedException()
                continue

            if eventName == self.defaultIgnoreValue:
                continue
            if eventName not in eventSignals:
                eventSignals[eventName] = np.copy(emptySignal)
                lastdefaultGroupValue[eventName] = 0
                lastDefaultGroupIndex[eventName] = 0
            if eventName not in currentEventIndexes:
                currentEventIndexes[eventName] = {}

            if start:
                if (
                    eventValueName in currentEventIndexes[eventName]
                    and currentEventIndexes[eventName][eventValueName][0] is not None
                ):
                    raise EventWrongOrdering("Event %s:%s startet twice" % (eventName, eventValueName))

                curValue = eventValue
                if not isEventMarker:
                    currentEventIndexes[eventName][eventValueName] = [
                        lastDefaultGroupIndex[eventName],
                        None,
                    ]
                    eventValue = lastdefaultGroupValue[eventName]
                    add = True
                else:
                    lastEvent = (
                        currentEventIndexes[eventName][eventValueName]
                        if eventValueName in currentEventIndexes[eventName]
                        else None
                    )
                    lastEnding = lastEvent[1] if lastEvent is not None else None
                    # store the current start of the event, and the end of the last event
                    currentEventIndexes[eventName][eventValueName] = [
                        getSampleIndex(annotationIndex),
                        lastEnding,
                    ]

                # update value and index for the default group
                if eventName == defaultEventName:
                    lastDefaultGroupIndex[eventName] = getSampleIndex(annotationIndex)
                    lastdefaultGroupValue[eventName] = curValue
            else:
                add = True

            if add:
                lastEventEnding = currentEventIndexes[eventName][eventValueName][1]
                # overwrite the last ending with the current position
                currentEventIndexes[eventName][eventValueName][1] = getSampleIndex(annotationIndex)

                eventStart, eventEnd = currentEventIndexes[eventName][eventValueName]
                if isEventMarker & exclusiveIndexing:
                    eventEnd += 1
                if isEventMarker and forceGapBetweenEvents:
                    if lastEventEnding == eventStart - 1:
                        # delete the last frame from the last event
                        eventSignals[eventName][lastEventEnding] = emptySignalValue

                if eventStart > eventEnd:
                    raise EventWrongOrdering(eventName, eventValue)

                if (eventName == defaultEventName) & ((eventEnd - eventStart) % defaultEventEpochLength > 0):
                    self.logWarning("%s epoch not with length %s" % (defaultEventName, defaultEventEpochLength))

                if any(eventSignals[eventName][slice(eventStart, eventEnd)] == eventValue) & (eventValue != emptySignalValue):
                    self.logWarning("the event %s:%i is overlapping itself " % (eventName, eventValue))
                    overlap = eventSignals[eventName][slice(eventStart, eventEnd)]
                    eventSignals[eventName][slice(eventStart, eventEnd)][overlap == eventValue] = 0

                eventSignals[eventName][slice(eventStart, eventEnd)] += eventValue
                # mark the current event as handled
                currentEventIndexes[eventName][eventValueName][0] = None

        if defaultEventName in eventSignals:  # & (lastDefaultGroupIndex[defaultEventName] != 0):
            finalIndex = len(eventSignals[defaultEventName])
            moduloFinalIndex = (finalIndex - lastDefaultGroupIndex[defaultEventName]) % defaultEventEpochLength
            if (defaultEventEpochLength > 1) & (moduloFinalIndex > 0):
                trueRest = (finalIndex - lastDefaultGroupIndex[defaultEventName]) % defaultEventEpochLength
                if (finalIndex - lastDefaultGroupIndex[defaultEventName]) > trueRest:
                    finalIndex = finalIndex - trueRest
                else:
                    finalIndex = lastDefaultGroupIndex[defaultEventName]
                    self.logWarning("last sleep epoch shorter than 30s, therefore skipped")
            lastValue = lastdefaultGroupValue[defaultEventName]
            eventSignals[defaultEventName][slice(lastDefaultGroupIndex[defaultEventName], finalIndex)] = lastValue

        return eventSignals

    def cutAndMergeEvents(self, df, cutEvents, field="name"):
        df.drop(cutEvents.index, inplace=True)
        return self.mergeEvents(df, field)

    def cutAndMergeEventsByQuery(self, df, cutQuery, field="name"):
        cutEvents = df.query(cutQuery)
        return self.cutAndMergeEvents(df, cutEvents, field)

    def mergeEvents(self, df, field="name"):
        lastEvent = None
        deleteIndexes = []
        for i, event in enumerate(df.iloc):
            keepEvent = True
            if lastEvent is not None:
                # last = (slice(lastEventIndex, ))
                lastSlice = slice(lastEventIndex, lastEventIndex + 1)

                if lastEvent["end"] != event["start"]:
                    df.loc[lastSlice, "duration"] = event["start"] - lastEvent["start"]
                    df.loc[lastSlice, "end"] = event["start"]
                    lastEvent = df.iloc[lastEventIndex]

                if event[field] == lastEvent[field]:
                    df.loc[lastSlice, "duration"] += event["duration"]
                    df.loc[lastSlice, "end"] = event["end"]
                    df.loc[i : i + 1, "duration"] = 0
                    deleteIndexes.append(i)
                    keepEvent = False

            if keepEvent:
                lastEventIndex = i
                lastEvent = event
        df.drop(df.query("duration == 0").index, inplace=True)
        return df

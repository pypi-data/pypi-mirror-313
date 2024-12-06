import pandas as pd

from ..RecordLoader import RecordLoader


class CSVMetaLoader(RecordLoader):
    def __init__(self, filePath, idColumn, relevantRows, getRowId=None) -> None:
        self.filePath = filePath
        self.df = pd.read_csv(filePath)
        self.idColumn = idColumn
        self.relevantRows = relevantRows
        if getRowId is None:
            getRowId = lambda r: r
        self.getRowId = getRowId

    def getMetaData(self, recordName):
        recordRow = self.df[self.df[self.idColumn] == self.getRowId(recordName)]
        if len(recordRow) == 0:
            return {}
        recordRow = recordRow.iloc[0]

        metaData = {}
        for nameId, pandasKey in self.relevantRows.items():
            if callable(pandasKey):
                metaData[nameId] = pandasKey(recordRow)
            else:
                metaData[nameId] = recordRow[pandasKey] if pandasKey in recordRow and not pd.isna(recordRow[pandasKey]) else None

        return metaData

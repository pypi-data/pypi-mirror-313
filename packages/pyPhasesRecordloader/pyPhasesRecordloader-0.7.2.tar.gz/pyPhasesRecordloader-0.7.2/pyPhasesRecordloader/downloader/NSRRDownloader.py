from pathlib import Path
from shutil import copy

from pyPhases.util import BatchProgress
from .Downloader import Downloader


class NSRRDownloaderBase(Downloader):
    def __init__(self, config) -> None:
        super().__init__(config)
        self.basePath = config["basePath"]
        self.extensions = config["extensions"]
        self.canReadRemote = config["canReadRemote"] if "canReadRemote" in config else True

    def getDownloadList(self):
        filelist = []
        for path in Path(self.basePath).rglob("*"):
            filelist.append(path.as_posix())

        if len(filelist) == 0:
            raise Exception("filelist is empty")
        filelist = self.filterList(filelist)

        return filelist

    def copyRecords(self, downloadelement):
        filePath, records = downloadelement
        for record in records:
            pathSplit = Path(record)
            self.copySingleRecord(pathSplit.stem, filePath)

    def downloadTo(self, filePath):

        self.preparePath(filePath)

        fileList = self.getDownloadList()

        downloadlist = []
        while len(fileList) > 0:
            recordId = fileList[0].split("/")[-1]
            records = list(filter(lambda r: r.find(recordId) != -1, fileList))
            downloadlist.append((filePath, records))
            for record in records:
                fileList.remove(record)

        bp = BatchProgress(downloadlist)
        bp.useMultiThreading = True
        bp.asynchronous = True
        bp.threadCount = 8
        bp.start(self.copyRecords)

    def copySingleRecord(self, recordId, filePath, force=False):

        for i in range(len(self.extensions)):
            src = Path(self.basePath, recordId + self.extensions[i])
            target = Path(filePath, recordId + self.extensions[i])
            if force or self.force:
                try:
                    target.unlink()
                except:
                    pass

            if target.exists():
                return

            copy(
                Path(src),
                Path(target),
            )


class NSRRDownloader(NSRRDownloaderBase):
    def __init__(self, config) -> None:
        super().__init__(config)
        self.basePathExtensionwise = config["basePathExtensionwise"]

    def copySingleRecord(self, recordId, filePath, force=False):

        for i in range(len(self.basePathExtensionwise)):
            src = Path(self.basePathExtensionwise[i], recordId + self.extensions[i])
            target = Path(filePath, recordId + self.extensions[i])
            if force or self.force:
                try:
                    target.unlink()
                except:
                    pass

            if target.exists():
                return

            copy(
                Path(src),
                Path(target),
            )


class NSRRDownloader2(NSRRDownloaderBase):
    def __init__(self, config) -> None:
        super().__init__(config)

    def copySingleRecord(self, recordId, filePath, force=False):

        for i in range(len(self.extensions)):
            src = Path(self.basePath, recordId + self.extensions[i])
            target = Path(filePath, recordId + self.extensions[i])
            if force or self.force:
                try:
                    target.unlink()
                except:
                    pass

            if target.exists():
                return

            if i == 1:  # special treatement for extension ".allscore.txt" in position 1 in extension list
                try:
                    copy(
                        Path(src),
                        Path(target),
                    )
                    break
                except:
                    pass
            else:
                copy(
                    Path(src),
                    Path(target),
                )

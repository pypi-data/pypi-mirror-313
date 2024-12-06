from pathlib import Path
from shutil import copytree

from pyPhases.util import BatchProgress
from .Downloader import Downloader


class FolderDownloader(Downloader):
    def __init__(self, config) -> None:
        super().__init__(config)
        self.basePath = config["basePath"]
        self.canReadRemote = config["canReadRemote"] if "canReadRemote" in config else False

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
            self.copySingleRecord(pathSplit.name, filePath, pathSplit.parent)

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
        src = Path(self.basePath, recordId)
        target = Path(filePath, recordId)
        if force or self.force:
            try:
                src.unlink()
            except:
                pass

        if target.exists():
            return

        copytree(
            Path(src),
            Path(target),
        )

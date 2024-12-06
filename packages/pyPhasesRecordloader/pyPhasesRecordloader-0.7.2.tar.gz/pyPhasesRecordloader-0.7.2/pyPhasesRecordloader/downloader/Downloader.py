import re
from abc import abstractmethod
from pathlib import Path


class NotFound(Exception):
    pass


class Downloader:
    downloaderMap = {}

    def __init__(self, config) -> None:
        self.force = "force" in config and config["force"]
        self.basePath = config["basePath"]
        self.extensions = config["extensions"] if "extensions" in config else None
        self.listFilter = config["listFilter"] if "listFilter" in config else None
        self.idPattern = config["idPattern"] if "idPattern" in config else "(.*)\..*?"
        self.listPattern = config["listPathPattern"] if "listPathPattern" in config else "(.*)"
        self.recordURI = config["recordURI"] if "recordURI" in config else "$1"
        self.canReadRemote = config["canReadRemote"] if "canReadRemote" in config else False
        self.options = {}

    @classmethod
    def loadFromConfig(cls, config):
        if config is None or "type" not in config:
            raise Exception(
                "A downloader is requested, and the type is not specified in the config file. Please specify the loader.myLoader.downloader.type in the config file"
            )

        type = config["type"]
        if type == "s3":
            from .S3Downloader import S3Downloader

            downloaderClass = S3Downloader
        elif type == "onlineRecordList":
            from .ListDownloader import ListDownloader

            downloaderClass = ListDownloader
        elif type == "allFromFolder":
            from .FolderDownloader import FolderDownloader

            downloaderClass = FolderDownloader
        elif type == "nsrr":
            from .NSRRDownloader import NSRRDownloader

            downloaderClass = NSRRDownloader
        elif type == "nsrr2":
            from .NSRRDownloader import NSRRDownloader2

            downloaderClass = NSRRDownloader2
        elif type == "html-directory":
            from .HTMLDownloader import HTMLDownloader
            downloaderClass = HTMLDownloader
        elif type in Downloader.downloaderMap:
            downloaderClass = Downloader.downloaderMap[type]
        else:
            raise Exception("Download type %s is not supported" % type)

        return downloaderClass(config)

    def filterExtensions(self, fileList, extensions):
        return [r for r in fileList if r.endswith(tuple(extensions))]

    def filterList(self, fileList):
        if self.extensions is not None:
            fileList = [r for r in fileList if r.endswith(tuple(self.extensions))]
        if self.listFilter is not None:
            listFilter = self.listFilter
            fileList = [r for r in fileList if r.find(listFilter) != -1]

        return fileList

    def getIdsFromFiles(self, fileList):
        p = re.compile(self.idPattern)
        recordList = []
        for filename in fileList:
            try:
                record = p.match(Path(filename).as_posix())[1]
                recordList.append(record)
            except TypeError:
                pass
        return recordList

    def getRecordList(self, filepath=None):
        filepath = self.basePath if filepath is None else filepath
        # try to get list from files in filepath
        recordList = []
        path = Path(filepath)
        if filepath[0:4] != 'http' and path.exists():
            for path in Path(filepath).rglob("*"):
                recordList.append(path.as_posix())

        # else download complete list
        if len(recordList) == 0:
            recordList = self.getDownloadList()

        if self.extensions is not None:
            recordList = self.filterExtensions(recordList, self.extensions[0])

        recordList = self.getIdsFromFiles(recordList)

        return recordList

    @abstractmethod
    def getDownloadList(self):
        """returns a list with all relevant files"""
        raise Exception("the getDownloadList is not yet implemented in the current Downloader")

    @abstractmethod
    def downloadTo(self, filePath):
        """download all relevant files to a specified filePath

        Args:
            filePath (str): path to download the file to
        """
        raise Exception("please use the static get method to get a specific downloader")

    @abstractmethod
    def copySingleRecord(self, recordId, filePath, force=False):
        raise Exception("the copySingleRecord is not yet implemented in the current Downloader")

    def preparePath(self, filePath):
        path = Path(filePath)
        path.mkdir(parents=True, exist_ok=True)

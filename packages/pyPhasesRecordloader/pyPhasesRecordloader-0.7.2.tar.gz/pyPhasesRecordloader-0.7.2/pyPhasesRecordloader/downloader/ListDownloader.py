import re

import requests
from pyPhases.util import BatchProgress

from pyPhasesRecordloader.downloader.Downloader import Downloader, NotFound


class ListDownloader(Downloader):
    def __init__(self, config) -> None:
        self.bucket = config["bucket"]
        self.list = config["list"]
        self.extensions = config["extensions"]
        self.extensionsOptional = config["extensionsOptional"]
        self.listFilter = config["listFilter"] if "listFilter" in config else None
        super().__init__(config)

    def getDownloadFileTuple(self, t):
        uri, filename, optional = t
        try:
            self.downloadFile(uri, filename, None)
        except NotFound as e:
            if not optional:
                raise e

    def getDownloadList(self):

        recordListUrl = self.list

        recordListContent = requests.get(recordListUrl, stream=False).content
        recordLines = recordListContent.decode("utf-8").split("\n")
        extensions = self.extensions
        optionalExtensions = self.extensionsOptional

        if self.listFilter is not None:
            p = re.compile(self.listFilter)
            recordLines = list(filter(lambda r: p.match(r) is not None, recordLines))

        downloadlist = []
        for line in recordLines:
            for extension in extensions + optionalExtensions:
                uri = line + extension
                downloadlist.append(uri)
        return downloadlist

    def downloadTo(self, filePath, patternString=None):

        mutlithread = "multithreading" not in self.options or self.options["multithreading"]

        recordListUrl = self.list
        basePath = self.basePath
        extensions = self.extensions
        optionalExtensions = self.extensionsOptional

        recordListContent = requests.get(recordListUrl, stream=False).content
        recordLines = recordListContent.decode("utf-8").split("\n")

        self.preparePath(filePath)

        if self.listFilter is not None:
            p = re.compile(self.listFilter)
            recordLines = list(filter(lambda r: p.match(r) is not None, recordLines))

        downloadlist = []
        for line in recordLines:
            recordId = line.split("/")[-1]
            for extension in extensions + optionalExtensions:

                optional = extension in optionalExtensions
                uri = basePath + "/" + line + extension
                filename = filePath + "/" + recordId + extension

                addTuple = patternString is None or re.search(re.compile(patternString), recordId) is not None

                if addTuple:
                    downloadlist.append((uri, filename, optional))

        bp = BatchProgress(downloadlist)
        bp.useMultiThreading = mutlithread
        bp.asynchronous = mutlithread
        bp.threadCount = 8
        bp.start(self.getDownloadFileTuple)

    def copySingleRecord(self, recordId, filePath, force=False):
        self.downloadTo(filePath, ".*?" + recordId + ".*?", mutlithread=False)

    def downloadFile(self, url, filename, tqdmIterator=None):
        if url[0:5] == "gs://":
            from google.cloud import storage

            bucketSplit = url[5:].split("/")
            bucket = bucketSplit[0]
            path = "/".join(bucketSplit[1:])
            client = storage.Client()
            bucket = client.get_bucket(bucket)
            blob = bucket.get_blob(path)
            blob.download_to_filename(filename)
        else:
            with open(filename, "ab") as f:
                headers = {}
                pos = f.tell()
                if pos:
                    headers["Range"] = f"bytes={pos}-"
                response = requests.get(url, headers=headers, stream=True)
                downloaded = pos
                chunkSize = 1024
                if response.status_code == 200:
                    for data in response.iter_content(chunk_size=chunkSize):
                        f.write(data)
                        if tqdmIterator is not None:
                            downloaded += chunkSize
                            tqdmIterator.set_postfix({"file": "{:.1f}MB".format(downloaded / 1024 / 1024)})
                elif response.status_code != 416:
                    # 416 - Requested Range Not Satisfiable
                    response.raise_for_status()

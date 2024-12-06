import boto3
from botocore import UNSIGNED
from botocore.client import Config
from tqdm import tqdm

from teleschlafmedizin.model.downloader.Downloader import Downloader


class S3Downloader(Downloader):
    def __init__(self, config) -> None:
        self.bucket = config["bucket"]
        super().__init__(config)

    def getDownloadList(self):

        client = boto3.client("s3", config=Config(signature_version=UNSIGNED))

        bucket_objects = client.list_objects(Bucket=self.bucket)["Contents"]

        return bucket_objects

    def downloadTo(self, filePath):

        client = boto3.client("s3", config=Config(signature_version=UNSIGNED))

        bucket_objects = self.getDownloadList()

        downloadList = tqdm(bucket_objects)
        downloadList.set_description("Download Raw data from S3 bucket")
        for bucket_object in downloadList:
            filename = bucket_object["Key"]
            fileSize = bucket_object["Size"]
            downloadedBytes = 0

            def update(bytes):
                nonlocal downloadedBytes
                downloadedBytes += bytes
                if fileSize > 0:
                    percentage = downloadedBytes / fileSize * 100
                    downloadList.set_postfix({"current file": "{:.1f}%".format(percentage)})

            client.download_file(
                Bucket=self.bucket,
                Key=filename,
                Filename=filePath + "/{}".format(filename),
                Callback=update,
            )

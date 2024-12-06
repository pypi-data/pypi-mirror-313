import os
import asyncio
import logging
from collections.abc import Callable
import aiofiles
from ..exceptions import FileError
from .UploadTo import UploadToBase
from ..interfaces.Boto3Client import Boto3Client


class UploadToS3(Boto3Client, UploadToBase):
    """
    uploadToS3.

    Upload a file (or collection of files) to a s3 Bucket.
    """

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.mdate = None
        self.local_name = None
        self.filename: str = ""
        self.whole_dir: bool = False
        self.preserve = True
        self.ContentType: str = "binary/octet-stream"
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """start Method."""
        await super(UploadToS3, self).start(**kwargs)
        if hasattr(self, "destination"):
            self.directory = self.destination["directory"]
            if not self.directory.endswith("/"):
                self.directory = self.source_dir + "/"
            self.directory = self.mask_replacement(self.destination["directory"])
        if hasattr(self, "source"):
            self.whole_dir = (
                self.source["whole_dir"] if "whole_dir" in self.source else False
            )
            if self.whole_dir is True:
                # if whole dir, is all files in source directory
                logging.debug(f"Uploading all files on directory {self.source_dir}")
                p = self.source_dir.glob("**/*")
                self._filenames = [x for x in p if x.is_file()]
            else:
                if "filename" in self.source:
                    p = self.source_dir.glob(self.filename)
                    self._filenames = [x for x in p if x.is_file()]
        try:
            if self.previous and self.input:
                self._filenames = self.input
            if hasattr(self, "file"):
                filenames = []
                for f in self._filenames:
                    p = self.source_dir.glob(f)
                    fp = [x for x in p if x.is_file()]
                    filenames = filenames + fp
                self._filenames = filenames
        except (NameError, KeyError):
            pass
        return self

    async def close(self):
        pass

    async def run(self):
        """Running Upload file to S3."""
        self._result = None
        try:
            use_credentials = self.credentials["use_credentials"]
            # del self.credentials['use_credentials']
        except KeyError:
            use_credentials = False
        async with self.get_client(
            use_credentials, credentials=self.credentials, service=self.service
        ) as s3_client:
            errors = {}
            files = {}
            for file in self._filenames:
                key = os.path.basename(file)
                filename = f"{self.directory}{key}"
                print("FILENAME ", filename)
                # TODO: making async with chunks (part data)
                async with aiofiles.open(file, mode="rb") as f:
                    content = await f.read()
                    response = await s3_client.put_object(
                        Bucket=self.bucket,
                        Key=filename,
                        Body=content,
                        ContentType=self.ContentType,
                    )
                    rsp = response["ResponseMetadata"]
                    status_code = int(rsp["HTTPStatusCode"])
                    if status_code == 200:
                        files[file] = filename
                    else:
                        errors[file] = FileError(f"S3: Upload Error: {rsp!s}")
            self._result = {"files": files, "errors": errors}
            self.add_metric("S3_UPLOADED", files)
            return self._result

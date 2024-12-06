import os
import asyncio
import re
from io import BytesIO
from typing import List
from collections.abc import Callable
import aiofiles
from botocore.exceptions import ClientError
from ..exceptions import FileError, ComponentError, FileNotFound
from .DownloadFrom import DownloadFromBase
from ..interfaces.Boto3Client import Boto3Client


class DownloadFromS3(Boto3Client, DownloadFromBase):
    """
    DownloadFromS3.

    **Overview**

        Download a file from an Amazon S3 bucket using the functionality from DownloadFrom.

    **Properties**

    .. table:: Properties
        :widths: auto

        +--------------------+----------+-----------+-----------------------------------------------------------------+
        | Name               | Required | Summary                                                                     |
        +--------------------+----------+-----------+-----------------------------------------------------------------+
        | credentials        |   Yes    | Credentials to establish connection with S3 service (username and password) |
        +--------------------+----------+-----------+-----------------------------------------------------------------+
        | bucket             |   Yes    | The name of the S3 bucket to download files from.                           |
        +--------------------+----------+-----------+-----------------------------------------------------------------+
        | source_dir         |   No     | The directory path within the S3 bucket to download files from.             |
        |                    |          | Defaults to the root directory (`/`).                                       |
        +--------------------+----------+-----------+-----------------------------------------------------------------+
        | source             |   No     | A dictionary specifying the filename to download.                           |
        |                    |          | If provided, takes precedence over `source_dir` and `_srcfiles`.            |
        +--------------------+----------+-----------+-----------------------------------------------------------------+
        | _srcfiles          |   No     | A list of filenames to download from the S3 bucket.                         |
        |                    |          | Used in conjunction with `source_dir`.                                      |
        +--------------------+----------+-----------+-----------------------------------------------------------------+
        | rename             |   No     | A new filename to use for the downloaded file.                              |
        +--------------------+----------+-----------+-----------------------------------------------------------------+
        | directory          |   Yes    | The local directory path to save the downloaded files.                      |
        +--------------------+----------+-----------+-----------------------------------------------------------------+
        | create_destination |   No     | A boolean flag indicating whether to create the destination directory       |
        |                    |          | if it doesn't exist. Defaults to `True`.                                    |
        +--------------------+----------+-----------+-----------------------------------------------------------------+

        save the file on the new destination.

    **Methods**

    * start()
    * close()
    * run()
    * s3_list(s3_client, suffix="")
    * save_attachment(self, filepath, content)
    * download_file(self, filename, obj)
    """

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.url: str = None
        self.folder = None
        self.rename: str = None
        self.context = None
        self.ContentType: str = "binary/octet-stream"
        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def s3_list(self, s3_client: Callable, suffix: str = "") -> List:
        if s3_client:
            kwargs = {
                "Bucket": self.bucket,
                "Delimiter": "/",
                "Prefix": self.source_dir,
            }
            prefix = self.source_dir
            files = []
            _patterns = []
            for file in self._srcfiles:
                _patterns.append(re.compile(f"^{self.source_dir}.{file}+$"))
            try:
                while True:
                    response = await s3_client.list_objects_v2(**kwargs)
                    if response["KeyCount"] == 0:
                        raise FileNotFound(
                            f"S3 Bucket Error: Content not found on {self.bucket}"
                        )
                    for obj in response["Contents"]:
                        key = obj["Key"]
                        if obj["Size"] == 0:
                            # is a directory
                            continue
                        try:
                            if hasattr(self, "source") and "filename" in self.source:
                                if self.source["filename"] == key:
                                    files.append(obj)
                        except (KeyError, AttributeError):
                            pass
                        if suffix is not None:
                            if key.startswith(prefix) and re.match(
                                prefix + suffix, key
                            ):
                                files.append(obj)
                        else:
                            try:
                                for pat in _patterns:
                                    mt = pat.match(key)
                                    if mt:
                                        files.append(obj)
                            except Exception as e:
                                self._logger.exception(e, stack_info=True)
                    try:
                        kwargs["ContinuationToken"] = response["NextContinuationToken"]
                    except KeyError:
                        break
            except ClientError as err:
                raise ComponentError(f"S3 Bucket Error: {err}") from err
        return files

    async def start(self, **kwargs):
        await super(DownloadFromS3, self).start(**kwargs)
        if self.source_dir and not self.source_dir.endswith("/"):
            self.source_dir = self.source_dir + "/"
        return True

    async def close(self):
        pass

    async def run(self):
        try:
            use_credentials = bool(self.credentials["use_credentials"])
        except KeyError:
            use_credentials = False
        try:
            if not self.directory.exists():
                if self.create_destination is True:
                    self.directory.mkdir(parents=True, exist_ok=True)
                else:
                    raise ComponentError(
                        f"S3: Cannot create destination directory: {self.directory}"
                    )
        except Exception as err:
            self._logger.error(f"S3: Error creating destination directory: {err}")
            raise ComponentError(
                f"S3: Error creating destination directory: {err}"
            ) from err
        async with self.get_client(
            use_credentials, credentials=self.credentials, service=self.service
        ) as s3_client:
            errors = {}
            files = {}
            if hasattr(self, "file"):
                # find src files using get_list:
                s3_files = await self.s3_list(s3_client)
                for obj in s3_files:
                    try:
                        file = obj["Key"]
                        try:
                            obj = await s3_client.get_object(
                                Bucket=self.bucket, Key=file
                            )
                        except Exception as e:
                            raise ComponentError(
                                f"S3: Error getting object from Bucket: {e}"
                            ) from e
                        result = await self.download_file(os.path.basename(file), obj)
                        if isinstance(result, BaseException):
                            errors[file] = result
                        else:
                            files[file] = result
                    except Exception as e:
                        raise ComponentError(f"{e!s}") from e
            else:
                for file in self._srcfiles:
                    if self.source_dir:
                        filename = f"{self.source_dir}{file}"
                    else:
                        filename = file
                    try:
                        self._logger.debug(f"S3: Downloading File {filename}")
                        obj = await s3_client.get_object(
                            Bucket=self.bucket, Key=filename
                        )
                    except Exception as e:
                        raise ComponentError(
                            f"S3: Error getting object from Bucket: {e}"
                        ) from e
                    result = await self.download_file(file, obj)
                    if isinstance(result, BaseException):
                        errors[file] = result
                    else:
                        files[file] = result
            # at end, create the result:
            self._result = {"files": files, "errors": errors}
            self.add_metric("S3_FILES", files)
            return self._result

    async def save_attachment(self, filepath, content):
        try:
            self._logger.info(f"S3: Saving attachment file: {filepath}")
            if filepath.exists() is True:
                if (
                    "replace" in self.destination
                    and self.destination["replace"] is True
                ):
                    # overwrite only if replace is True
                    async with aiofiles.open(filepath, mode="wb") as fp:
                        await fp.write(content)
                else:
                    self._logger.warning(
                        f"S3: File {filepath!s} was not saved, already exists."
                    )
            else:
                # saving file:
                async with aiofiles.open(filepath, mode="wb") as fp:
                    await fp.write(content)
        except Exception as err:
            raise FileError(f"File {filepath} was not saved: {err}") from err

    async def download_file(self, filename, obj):
        result = None
        ob_info = obj["ResponseMetadata"]["HTTPHeaders"]
        rsp = obj["ResponseMetadata"]
        status_code = int(rsp["HTTPStatusCode"])
        if status_code == 200:
            # file was found
            filepath = self.directory.joinpath(filename)
            if ob_info["content-type"] == self.ContentType:
                contenttype = ob_info["content-type"]
                data = None
                async with obj["Body"] as stream:
                    data = await stream.read()
                output = BytesIO()
                output.write(data)
                output.seek(0)
                result = {"type": contenttype, "data": output, "file": filepath}
                # then save it into directory
                await self.save_attachment(filepath, data)
            else:
                return FileNotFound(f'S3: Wrong File type: {ob_info["content-type"]!s}')
        else:
            return FileNotFound(f"S3: File {filename} was not found: {rsp!s}")
        return result

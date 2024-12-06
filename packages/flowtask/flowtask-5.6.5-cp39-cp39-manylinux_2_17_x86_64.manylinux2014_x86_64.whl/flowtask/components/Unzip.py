import os
import logging
import asyncio
from typing import List
from collections.abc import Callable
from pathlib import PosixPath, Path, PurePath
from zipfile import ZipFile, BadZipFile
from ..exceptions import FileError, ComponentError, FileNotFound
from .flow import FlowComponent
from ..interfaces.compress import CompressSupport


class Unzip(CompressSupport, FlowComponent):
    """
    Unzip

        Overview

            The Unzip class is a component for decompressing ZIP files in specified directories.
            It supports selecting specific files within the archive, applying directory masks, and
            optionally deleting the source ZIP file after extraction.

        .. table:: Properties
        :widths: auto

            +----------------+----------+-----------+---------------------------------------------------------------+
            | Name           | Required | Summary                                                                   |
            +----------------+----------+-----------+---------------------------------------------------------------+
            | filename       |   Yes    | The name of the ZIP file to decompress.                                   |
            +----------------+----------+-----------+---------------------------------------------------------------+
            | directory      |   Yes    | The target directory for decompression.                                   |
            +----------------+----------+-----------+---------------------------------------------------------------+
            | extract        |   No     | Dictionary specifying files to extract and/or target output directory.    |
            +----------------+----------+-----------+---------------------------------------------------------------+
            | delete_source  |   No     | Boolean indicating if the ZIP file should be deleted after extraction.    |
            +----------------+----------+-----------+---------------------------------------------------------------+
            | password       |   No     | Optional password for encrypted ZIP files.                                |
            +----------------+----------+-----------+---------------------------------------------------------------+

        Returns

            This component extracts the specified files from a ZIP archive into the target directory and
            returns a list of extracted file paths. Metrics such as the output directory and ZIP file name
            are tracked, and any errors related to file extraction or directory creation are logged for
            debugging purposes. If specified, the original ZIP file is deleted after extraction.
    """ #noqa

    _namelist = []
    _directory = ""

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self.filename: str = None
        self.directory: PurePath = None
        self._path: PurePath = None
        self._output: PurePath = None
        self._filenames: List = []
        self.delete_source: bool = False
        super(Unzip, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if isinstance(self.directory, str):
            self.directory = PosixPath(self.directory).resolve()
            self._path = PosixPath(self.directory, self.filename)
        if self.filename is not None:
            if hasattr(self, "masks"):
                self.filename = self.mask_replacement(self.filename)
            self._path = PosixPath(self.directory, self.filename)
        elif self.previous:
            if isinstance(self.input, PosixPath):
                self.filename = self.input
            elif isinstance(self.input, list):
                self.filename = PosixPath(self.input[0])
            elif isinstance(self.input, str):
                self.filename = PosixPath(self.input)
            else:
                filenames = list(self.input.keys())
                if filenames:
                    try:
                        self.filename = PosixPath(filenames[0])
                    except IndexError as err:
                        raise FileError("File is empty or doesnt exists") from err
            self._variables["__FILEPATH__"] = self.filename
            self._variables["__FILENAME__"] = os.path.basename(self.filename)
            self._path = self.filename
        else:
            raise FileError("Unzip: File is empty or doesn't exists")
        if hasattr(self, "extract"):
            for _, filename in enumerate(self.extract["filenames"]):
                filename = self.mask_replacement(filename)
                self._filenames.append(filename)
            if "directory" in self.extract:
                self._output = Path(self.extract["directory"]).resolve()
                # Create directory if not exists
                try:
                    self._output.mkdir(parents=True, exist_ok=True)
                except Exception as err:
                    logging.error(f"Error creating directory {self._output}: {err}")
                    raise ComponentError(
                        f"Error creating directory {self._output}: {err}"
                    ) from err
            else:
                # same directory:
                self._output = Path(self.directory)
        self.add_metric("OUTPUT_DIRECTORY", self._output)
        self.add_metric("ZIP_FILE", self.filename)
        return True

    async def close(self):
        pass

    async def run(self):
        # Check if File exists
        self._result = None
        if not self._path.exists() or not self._path.is_file():
            raise FileNotFound(
                f"Compressed File doesn't exists: {self._path}"
            )
        files = await self.uncompress_zip(
            source=self._path,
            destination=self._output,
            source_files=self._filenames,
            password=self.password if hasattr(self, "password") else None,
            remove_source=self.delete_source,
        )
        if self.delete_source is True:
            self._path.unlink(
                missing_ok=True
            )
        filenames = []
        for filename in files:
            f = self._output.joinpath(filename)
            filenames.append(f)
        self._result = filenames
        return self._result

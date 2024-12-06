from typing import List, Dict
from abc import abstractmethod
from collections.abc import Callable
import asyncio
import logging
import random
import ssl
from pathlib import Path, PosixPath
from functools import partial
import aiohttp
from aiohttp import web
from tqdm import tqdm
from ..exceptions import ComponentError, FileNotFound
from ..utils.encoders import DefaultEncoder, json_encoder
from .flow import FlowComponent
from ..interfaces.http import ua


class UploadToBase(FlowComponent):
    _credentials: Dict = {"username": str, "password": str}

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.accept: str = "text/plain"
        self.url: str = kwargs.get('url', None)
        self.overwrite: bool = True
        self.rename: bool = True
        self.create_destination: bool = kwargs.get('create_destination', False)
        # source:
        self.source_file: str = None
        self.source_dir: str = None
        # destination:
        self.filename: str = None
        self._filenames: List = []
        self._destination: List = []
        self._connection: Callable = None
        self.ssl: bool = False
        self.ssl_cafile: str = None
        self.ssl_certs: list = []
        super().__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        self._encoder = DefaultEncoder()
        self._valid_response_status: List = (200, 201, 202)
        # SSL Context:
        if self.ssl:
            # TODO: add CAFile and cert-chain
            self.ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS, cafile=self.ssl_cafile)
            self.ssl_ctx.options &= ~ssl.OP_NO_SSLv3
            self.ssl_ctx.verify_mode = ssl.CERT_NONE
            if self.ssl_certs:
                self.ssl_ctx.load_cert_chain(*self.ssl_certs)
        else:
            self.ssl_ctx = None

    def define_host(self):
        try:
            self.host = self.credentials["host"]
        except KeyError:
            self.host = self.host
        try:
            self.port = self.credentials["port"]
        except KeyError:
            self.port = self.port
        # getting from environment:
        self.host = self.get_env_value(self.host, default=self.host)
        self.port = self.get_env_value(str(self.port), default=self.port)
        if self.host:
            self._logger.debug(f"<{__name__}>: HOST: {self.host}, PORT: {self.port}")

    def build_headers(self):
        self.headers = {
            "Accept": self.accept,
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": random.choice(ua),
            **self.headers,
        }

    async def start(self, **kwargs):
        """Start.

        Processing variables and credentials.
        """
        if getattr(self, 'define_host', None) is not None:
            self.define_host()
        try:
            self.processing_credentials()
        except Exception as err:
            self._logger.error(err)
            raise
        if hasattr(self, "file"):
            filename = self.process_pattern("file")
            if hasattr(self, "masks"):
                filename = self.mask_replacement(filename)
            # path for file
            # get path of all files:
            self._logger.debug("Filename > {}".format(filename))
            self._filenames.append(filename)
        if hasattr(self, "source"):  # using the destination filosophy
            try:
                if hasattr(self, "masks"):
                    self.source_dir = self.mask_replacement(self.source["directory"])
                else:
                    self.source_dir = self.source["directory"]
            except KeyError:
                self.source_dir = "/"
            print(":: Source Dir: ", self.source_dir)
            self.source_dir = Path(self.source_dir)
            # filename:
            if "file" in self.source:
                self.source_file = self.process_pattern("file", parent=self.source)
            else:
                try:
                    self.source_file = self.mask_replacement(self.source["filename"])
                except KeyError:
                    self.source_file = None
        if hasattr(self, "destination"):
            self.directory = self.destination.get('directory')
            self.directory = self.mask_replacement(self.directory)
            if isinstance(self.directory, str):
                self.directory = Path(self.directory).resolve()
            # Create directory if not exists
            try:
                if self.create_destination is True:
                    self.directory.mkdir(parents=True, exist_ok=True)
            except OSError as err:
                raise ComponentError(
                    f"UploadTo: Error creating destination directory {self.directory}: {err}"
                ) from err
            except Exception as err:
                self._logger.error(
                    f"Error creating destination directory {self.directory}: {err}"
                )
                raise ComponentError(
                    f"Error creating destination directory {self.directory}: {err}"
                ) from err
            try:
                fname = self.destination.get('filename')
                if self.directory.exists():
                    self.filename = self.directory.joinpath(fname)
                else:
                    self.filename = fname
                self._logger.debug(
                    f"Raw Filename: {self.filename}\n"
                )
                if hasattr(self, "masks"):
                    self.filename = self.mask_replacement(self.filename)
                    self._destination.append(self.filename)
            except Exception:
                pass
        if self.url:
            self.build_headers()
        return True

    async def http_response(self, response: web.Response):
        """http_response.

        Return the request response of the HTTP Session

        Args:
            response (web.Response): the Response of the HTTP Session.

        Returns:
            Any: any processed data.
        """
        return response

    async def upload_session(
        self, url, method: str = "get", data: Dict = None, data_format: str = "json"
    ):
        """
        session.
            connect to an http source using aiohttp
        """
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        # TODO: Auth, Data, etc
        auth = {}
        params = {}
        _data = {"data": None}
        if self.credentials:
            if "username" in self.credentials:  # basic Authentication
                auth = aiohttp.BasicAuth(
                    self.credentials["username"], self.credentials["password"]
                )
                params = {"auth": auth}
            elif "token" in self.credentials:
                self.headers["Authorization"] = "{scheme} {token}".format(
                    scheme=self.credentials["scheme"], token=self.credentials["token"]
                )
        if data_format == "json":
            params["json_serialize"] = json_encoder
            _data["json"] = data
        else:
            _data["data"] = data
        async with aiohttp.ClientSession(**params) as session:
            meth = getattr(session, method)
            if self.ssl:
                ssl = {"ssl": self.ssl_ctx, "verify_ssl": True}
            else:
                ssl = {}
            fn = partial(
                meth,
                self.url,
                headers=self.headers,
                timeout=timeout,
                allow_redirects=True,
                **ssl,
                **_data,
            )
            try:
                async with fn() as response:
                    if response.status in self._valid_response_status:
                        return await self.http_response(response)
                    else:
                        raise ComponentError(
                            f"UploadTo: Error getting data from URL {response}"
                        )
            except aiohttp.HTTPError as err:
                raise ComponentError(
                    f"UploadTo: Error Making an SSL Connection to ({self.url}): {err}"
                ) from err
            except aiohttp.ClientSSLError as err:
                raise ComponentError(f"UploadTo: SSL Certificate Error: {err}") from err

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def run(self):
        pass

    def start_pbar(self, total: int = 1):
        return tqdm(total=total)

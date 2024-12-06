from typing import Optional, Union
import os
import asyncio
import random
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from io import BytesIO
from pathlib import Path
from urllib.parse import urlencode, urlparse
import urllib3
import aiofiles
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
import aiohttp
from aiohttp import BasicAuth
import httpx
from bs4 import BeautifulSoup as bs
from lxml import html, etree
from navconfig.logging import logging
from proxylists.proxies import (
    FreeProxy,
    Oxylabs
)
from ..utils import cPrint, SafeDict
from ..utils.json import JSONContent
from ..conf import HTTPCLIENT_MAX_SEMAPHORE, HTTPCLIENT_MAX_WORKERS
from .dataframes import PandasDataframe
from ..exceptions import ComponentError
from .credentials import CredentialsInterface


logging.getLogger("urllib3").setLevel(logging.WARNING)
urllib3.disable_warnings()
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


ua = [
    # Chrome - Desktop (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    # Chrome - Desktop (Mac)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",  # noqa
    # Safari - Desktop (Mac)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",  # noqa
    # Firefox - Desktop (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
    # Edge - Desktop (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46",  # noqa
    # Chrome - Mobile (Android)
    "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",  # noqa
    # Safari - Mobile (iOS)
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",  # noqa
    # Samsung Internet - Mobile (Android)
    "Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/21.0 Chrome/118.0.0.0 Mobile Safari/537.36",  # noqa
    # Firefox - Mobile (Android)
    "Mozilla/5.0 (Android 13; Mobile; rv:118.0) Gecko/118.0 Firefox/118.0",
    # Opera - Desktop (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0"  # noqa
]

mobile_ua = [
    "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",  # noqa
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',  # noqa
    'Mozilla/5.0 (Linux; Android 9; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.119 Mobile Safari/537.36',  # noqa
    'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.93 Mobile Safari/537.36',  # noqa
    'Mozilla/5.0 (Linux; Android 10; HUAWEI VOG-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36',  # noqa
    'Mozilla/5.0 (iPad; CPU OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1',  # noqa
]


class HTTPService(CredentialsInterface, PandasDataframe):
    """
    HTTPService.

    Overview

            Interface for making connections to HTTP services.
    """
    accept: str = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"  # noqa

    def __init__(self, *args, **kwargs):
        self.url: str = kwargs.get("url", None)
        self.accept: str = kwargs.get(
            "accept",
            self.accept
        )
        self.use_proxy: bool = kwargs.pop("use_proxy", False)
        self._free_proxy: bool = kwargs.pop('use_free_proxy', True)
        self._proxies: list = []
        self.rotate_ua: bool = kwargs.pop("rotate_ua", False)
        self.use_async: bool = bool(kwargs.pop("use_async", True))
        self.as_binary: bool = kwargs.pop('as_binary', False)
        self.download: bool = kwargs.pop('download', False)
        self.timeout: int = 30
        self.headers: dict = {}
        self.auth: dict = {}
        self.auth_type: str = None
        self.token_type: str = "Bearer"
        self._user, self._pwd = None, None
        self.method: str = kwargs.get("method", "get")
        self._default_parser: str = kwargs.pop('bs4_parser', 'html.parser')
        self.parameters = {}
        if self.rotate_ua is True:
            self._ua = random.choice(ua)
        else:
            self._ua: str = ua[0]
        self.headers = {
            "Accept": self.accept,
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self._ua,
            **self.headers,
        }
        self._encoder = JSONContent()
        # other arguments:
        self.arguments = kwargs
        # Executor:
        self._executor = ThreadPoolExecutor(
            max_workers=int(HTTPCLIENT_MAX_WORKERS)
        )
        self._semaphore = asyncio.Semaphore(
            int(HTTPCLIENT_MAX_SEMAPHORE)
        )
        super().__init__(*args, **kwargs)

    async def get_proxies(self):
        """
        Asynchronously retrieves a list of free proxies.
        TODO: SELECT or rotate the free/paid proxies.
        """
        if self._free_proxy is True:
            return await FreeProxy().get_list()
        else:
            return await Oxylabs(session_time=1).get_list()

    async def refresh_proxies(self):
        """
        Asynchronously refreshes the list of proxies if proxy usage is enabled.
        """
        if self.use_proxy is True:
            self._proxies = await self.get_proxies()

    def build_url(self, url, queryparams: str = "", args=None):
        """
        Constructs a full URL with optional query parameters and arguments.

        :param url: The base URL to be formatted.
        :param queryparams: Additional query parameters to be appended to the URL.
        :param args: Arguments to format within the URL.
        :return: The fully constructed URL.
        """
        url = str(url).format_map(SafeDict(**self._variables))
        if args:
            u = url.format(**args)
        else:
            u = url
        if queryparams:
            if "?" in u:
                full_url = u + "&" + queryparams
            else:
                full_url = u + "?" + queryparams
        else:
            full_url = u
        logging.debug(
            f"Resource URL: {full_url!s}"
        )
        return full_url

    def extract_host(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc

    async def session(
        self,
        url: str,
        method: str = "get",
        data: dict = None,
        cookies: dict = None,
        headers: dict = None,
        use_json: bool = False,
        follow_redirects: bool = False,
        use_proxy: bool = False,
        accept: str = None
    ):
        """
        Asynchronously sends an HTTP request using HTTPx.

        :param url: The URL to send the request to.
        :param method: The HTTP method to use (e.g., 'GET', 'POST').
        :param data: The data to send in the request body.
        :param use_json: Whether to send the data as JSON.
        :param cookies: A dictionary of cookies to send with the request.
        :param headers: A dictionary of headers to send with the request.
        :return: A tuple containing the result and any error information.
        """
        result = []
        error = {}
        auth = None
        proxies = None
        if accept is not None:
            self.headers["Accept"] = accept
        else:
            self.headers["Accept"] = self.accept
        if use_proxy is True:
            self._proxies = await self.get_proxies()
        if self._proxies:
            proxy = random.choice(self._proxies)
            if self._free_proxy is True:
                proxies = {
                    "http": proxy,
                    "https": proxy
                }
            else:
                proxies = {
                    "http://": httpx.AsyncHTTPTransport(
                        proxy=f"http://{proxy}"
                    ),
                    "https://": httpx.AsyncHTTPTransport(
                        proxy=f"http://{proxy}"
                    ),
                }
        if self.credentials:
            if "apikey" in self.auth:
                self.headers[
                    "Authorization"
                ] = f"{self.token_type} {self.auth['apikey']}"
            elif self.auth_type == "api_key":
                self.headers = {**self.headers, **self.credentials}
            elif self.auth_type == "key":
                url = self.build_url(
                    url, args=self.arguments, queryparams=urlencode(self.credentials)
                )
            elif self.auth_type in ["basic", "auth", "user"]:
                auth = (self.credentials["username"], self.credentials["password"])
        elif self._user and self.auth_type == "basic":
            auth = (self._user, self._pwd)
        cPrint(
            f"HTTP: Connecting to {url} using {method}",
            level="DEBUG"
        )
        if self.download is True:
            self.headers["Accept"] = "application/octet-stream"
            self.headers["Content-Type"] = "application/octet-stream"
            if self.use_streams is True:
                self.headers["Transfer-Encoding"] = "chunked"
        headers = self.headers
        if headers is not None and isinstance(headers, dict):
            headers = {**self.headers, **headers}
        timeout = httpx.Timeout(self.timeout)
        args = {"timeout": timeout, "headers": headers, "cookies": cookies}
        if auth is not None:
            args["auth"] = auth
        if proxies:
            if isinstance(proxies, dict):
                args['mounts'] = proxies
            else:
                args["proxies"] = proxies
        if self._debug is True:
            self.add_metric("HEADERS", headers)
        if proxies is not None:
            self.add_metric('Proxies', proxies)
        self.add_metric('URL', url)
        self.add_metric('METHOD', method)
        req_args = {
            "method": method.upper(),
            "url": url,
            "follow_redirects": follow_redirects,
            "json" if use_json else "data": data
        }
        # Process the response
        try:
            if hasattr(self, "_client"):
                # Use a client without context manager to keep the session alive
                # Remember to call `await self._client.aclose()` manually
                response = await self._client.request(**req_args)
            else:
                async with httpx.AsyncClient(**args) as client:
                    response = await client.request(**req_args)

            result, error = await self.process_response(response, url)

        except httpx.HTTPError as e:
            error = str(e)

        return (result, error)

    async def async_request(
        self,
        url,
        method: str = 'GET',
        data: dict = None,
        use_json: bool = False,
        use_proxy: bool = False,
        accept: Optional[str] = None
    ):
        """
        Asynchronously sends an HTTP request using aiohttp.

        :param url: The URL to send the request to.
        :param method: The HTTP method to use (e.g., 'GET', 'POST').
        :param data: The data to send in the request body.
        :param use_json: Whether to send the data as JSON.
        :param use_proxy: force proxy usage.
        :return: A tuple containing the result and any error information.
        """
        result = []
        error = {}
        auth = None
        proxy = None
        if use_proxy is True:
            self._proxies = await self.get_proxies()
        if self._proxies:
            proxy = random.choice(self._proxies)
            self.add_metric("Proxies", proxy)
        if self.credentials:
            if "apikey" in self.auth:
                self.headers[
                    "Authorization"
                ] = f"{self.token_type} {self.auth['apikey']}"
            elif self.auth_type == "api_key":
                self.headers = {**self.headers, **self.credentials}
            elif self.auth_type == "key":
                url = self.build_url(
                    url,
                    args=self.arguments,
                    queryparams=urlencode(self.credentials)
                )
            elif self.auth_type in ["basic", "auth", "user"]:
                auth = BasicAuth(
                    self.credentials["username"],
                    self.credentials["password"]
                )
        elif "apikey" in self.auth:
            self.headers["Authorization"] = f"{self.token_type} {self.auth['apikey']}"
        elif self.auth:
            token_type, token = list(self.auth.items())[0]
            self.headers["Authorization"] = f"{token_type} {token}"
        elif self._user and self.auth_type == "basic":
            auth = BasicAuth(self._user, self._pwd)
        cPrint(
            f"HTTP: Connecting to {url} using {method}",
            level="DEBUG"
        )
        if self._debug is True:
            self.add_metric("HEADERS", self.headers)
        self.add_metric("URL", url)
        self.add_metric("METHOD", method)
        if auth is not None:
            args = {"auth": auth}
        else:
            args = {}
        if accept is not None:
            self.headers["Accept"] = accept
        else:
            self.headers["Accept"] = self.accept
        if self.download is True:
            self.headers["Accept"] = "application/octet-stream"
            self.headers["Content-Type"] = "application/octet-stream"
            if hasattr(self, "use_streams"):
                self.headers["Transfer-Encoding"] = "chunked"
                args["stream"] = True
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession(
            headers=self.headers, timeout=timeout, auth=auth
        ) as session:
            try:
                if use_json is True:
                    async with session.request(
                        method.upper(), url, json=data, proxy=proxy, **args
                    ) as response:
                        result, error = await self.process_response(response, url)
                else:
                    async with session.request(
                        method.upper(), url, data=data, proxy=proxy, **args
                    ) as response:
                        # Process the response
                        result, error = await self.process_response(response, url)
            except aiohttp.ClientError as e:
                error = str(e)
        return (result, error)

    async def evaluate_error(
        self, response: Union[str, list], message: Union[str, list, dict]
    ) -> tuple:
        """evaluate_response.

        Check Response status and available payloads.
        Args:
            response (_type_): _description_
            url (str): _description_

        Returns:
            tuple: _description_
        """
        if isinstance(response, list):
            # a list of potential errors:
            for msg in response:
                if message in msg:
                    return True
        if isinstance(response, dict) and "errors" in response:
            errors = response["errors"]
            if isinstance(errors, list):
                for error in errors:
                    try:
                        if message in error:
                            return True
                    except TypeError:
                        if message == error:
                            return True
            else:
                if message == errors:
                    return True
        else:
            if message in response:
                return True
        return False

    async def process_response(self, response, url: str) -> tuple:
        """
        Processes the response from an HTTP request.

        :param response: The response object from aiohttp.
        :param url: The URL that was requested.
        :return: A tuple containing the processed result and any error information.
        """
        error = None
        result = None
        # Process the response
        status = self.response_status(response)

        if status >= 400:
            # Evaluate response body and headers.
            print(" == ERROR Headers == ")
            print(f"{response.headers}")
            content_type = response.headers.get("Content-Type", "").lower()
            if "application/json" in content_type:
                message = await self.response_json(response)
            elif "text/" in content_type:
                message = await self.response_text(response)
            elif "X-Error" in response.headers:
                message = response.headers["X-Error"]
            else:
                # Fallback to a unified read method for the raw body content
                message = await self.response_read(response)

            # Combine response headers and body for enriched logging
            error_context = {
                "status": status,
                "reason": await self.response_reason(response),
                "headers": response.headers,
                "body": message
            }

            # Log the detailed error context
            self._logger.error(f"Error: {error_context}")

            # Additional error handling or custom evaluation based on status
            if hasattr(self, 'no_errors'):
                for key, msg in self.no_errors.items():
                    if int(key) == status and await self.evaluate_error(message, msg):
                        return response, status

            # Raise an exception if error handling does not continue
            raise ConnectionError(f"HTTP Error {status}: {message!s}")
        else:
            if self.download is True:
                filename = os.path.basename(url)
                # Get the filename from the response headers, if available
                content_disposition = response.headers.get("content-disposition")
                if content_disposition:
                    _, params = content_disposition.split(";")
                    try:
                        key, value = params.strip().split("=")
                        if key == "filename":
                            filename = value.strip("'\"")
                    except ValueError:
                        pass
                if "{filename}" in str(self.filename):
                    self.filename = str(self.filename).format_map(
                        SafeDict(filename=filename)
                    )
                if "{" in str(self.filename):
                    self.filename = str(self.filename).format_map(
                        SafeDict(**self.arguments)
                    )
                if isinstance(self.filename, str):
                    self.filename = Path(self.filename)
                # Saving File in Directory:
                total_length = response.headers.get("Content-Length")
                self._logger.info(
                    f"HTTPClient: Saving File {self.filename}, size: {total_length}"
                )
                pathname = self.filename.parent.absolute()
                if not pathname.exists():
                    # Create a new directory
                    pathname.mkdir(parents=True, exist_ok=True)
                transfer = response.headers.get("transfer-encoding", None)
                if transfer is None:
                    chunk_size = int(total_length)
                else:
                    chunk_size = 8192
                # Asynchronous file writing
                if self.filename.exists() and self.filename.is_file():
                    overwrite = self.destination.get("overwrite", True)
                    if overwrite is False:
                        self._logger.warning(
                            f"HTTPClient: File Already exists: {self.filename}"
                        )
                        # Filename already exists
                        result = self.filename
                        return result, error
                    else:
                        self._logger.warning(
                            f"HTTPClient: Overwriting File: {self.filename}"
                        )
                        # Delete the file before downloading again.
                        try:
                            self.filename.unlink()
                        except Exception as e:
                            self._logger.warning(
                                f"HTTPClient: Error Deleting File: {self.filename}, {e}"
                            )
                if hasattr(self, "use_streams") and self.use_streams is True:
                    async with aiofiles.open(self.filename, "wb") as file:
                        async for chunk in response.content.iter_chunked(chunk_size):
                            await file.write(chunk)
                else:
                    with open(self.filename, "wb") as fp:
                        try:
                            fp.write(await self.response_read(response))
                        except Exception:
                            pass
                self._logger.debug(
                    f"Filename Saved Successfully: {self.filename}"
                )
                result = self.filename
            else:
                if self.accept == 'application/octet-stream':
                    data = await self.response_read(response)
                    buffer = BytesIO(data)
                    buffer.seek(0)
                    result = buffer
                elif self.accept in ('text/html'):
                    result = await self.response_read(response)
                    try:
                        # html parser for lxml
                        self._parser = html.fromstring(result)
                        # BeautifulSoup parser
                        self._bs = bs(response.text, self._default_parser)
                        result = self._bs
                    except Exception as e:
                        error = e
                elif self.accept in ('application/xhtml+xml', 'application/xml'):
                    result = await self.response_read(response)
                    try:
                        self._parser = etree.fromstring(result)
                    except etree.XMLSyntaxError:
                        self._parser = html.fromstring(result)
                    except Exception as e:
                        error = e
                elif self.accept == "application/json":
                    try:
                        result = await self.response_json(response)
                    except Exception as e:
                        logging.error(e)
                        # is not an json, try first with beautiful soup:
                        try:
                            self._bs = bs(
                                await self.response_text(response),
                                self._default_parser
                            )
                            result = self._bs
                        except Exception:
                            error = e
                elif self.as_binary is True:
                    result = await self.response_read(
                        response
                    )
                else:
                    result = await self.response_text(
                        response
                    )
        return result, error

    async def request(
        self,
        url: str,
        method: str = "GET",
        data: dict = None,
        use_proxy: bool = False,
        accept: Optional[str] = None
    ) -> tuple:
        """
        Sends an HTTP request using the requests library.

        :param url: The URL to send the request to.
        :param method: The HTTP method to use (e.g., 'GET', 'POST').
        :param data: The data to send in the request body.
        :return: A tuple containing the result and any error information.
        """
        result = []
        error = {}
        auth = None
        proxies = None
        if use_proxy is True:
            self._proxies = await self.get_proxies()
        if self._proxies:
            proxy = random.choice(self._proxies)
            proxies = {"http": proxy, "https": proxy, "ftp": proxy}
            self.add_metric("Proxies", proxies)
        if self.credentials:
            if "apikey" in self.auth:
                self.headers[
                    "Authorization"
                ] = f"{self.token_type} {self.auth['apikey']}"
            elif self.auth_type == "api_key":
                self.headers = {**self.headers, **self.credentials}
            elif self.auth_type == "key":
                url = self.build_url(
                    url, args=self.arguments, queryparams=urlencode(self.credentials)
                )
            elif self.auth_type == "basic":
                auth = HTTPBasicAuth(
                    self.credentials["username"], self.credentials["password"]
                )
            else:
                auth = HTTPBasicAuth(
                    self.credentials["username"], self.credentials["password"]
                )
        elif self._user and self.auth_type == "basic":
            auth = HTTPBasicAuth(self._user, self._pwd)
        cPrint(f"HTTP: Connecting to {url} using {method}", level="DEBUG")
        self.add_metric("URL", url)
        self.add_metric("METHOD", method)
        if auth is not None:
            args = {"auth": auth, "verify": False}
        else:
            args = {}
        if accept is not None:
            self.headers["Accept"] = accept
        else:
            self.headers["Accept"] = self.accept
        if self.download is True:
            self.headers["Accept"] = "application/octet-stream"
            self.headers["Content-Type"] = "application/octet-stream"
            if hasattr(self, "use_streams"):
                self.headers["Transfer-Encoding"] = "chunked"
                args["stream"] = True
        if self._debug is True:
            self.add_metric("HEADERS", self.headers)
        args["headers"] = self.headers
        args["timeout"] = self.timeout
        args["proxies"] = proxies
        if method == "get":
            my_request = partial(requests.get, **args)
        elif method == "post":
            my_request = partial(requests.post, data=data, **args)
        elif method == "put":
            my_request = partial(requests.put, data=data, **args)
        elif method == "delete":
            my_request = partial(requests.delete, data=data, **args)
        elif method == "patch":
            my_request = partial(requests.patch, data=data, *args)
        else:
            my_request = partial(requests.post, data=data, **args)
        try:
            # making request
            async with self._semaphore:
                loop = asyncio.get_running_loop()
                future = loop.run_in_executor(self._executor, my_request, url)
                result, error = await self.process_request(future, url)
            if error:
                if isinstance(error, BaseException):
                    raise error
                else:
                    raise ComponentError(f"{error!s}")
            return (result, error)
        except requests.exceptions.ReadTimeout as err:
            self._logger.warning(f"Timeout Error: {err!r}")
            # TODO: retrying
            raise ComponentError(f"Timeout: {err}") from err
        except Exception as err:
            self._logger.exception(str(err), stack_info=True)
            raise ComponentError(f"Error: {err}") from err

    async def process_request(self, future, url: str):
        """
        Processes the result of an asynchronous HTTP request.

        :param future: The future object representing the asynchronous operation.
        :param url: The URL that was requested.
        :return: A tuple containing the result and any error information.
        """
        # getting the result, based on the Accept logic
        error = None
        result = None
        loop = asyncio.get_running_loop()
        asyncio.set_event_loop(loop)
        done, _ = await asyncio.wait([future], return_when=asyncio.FIRST_COMPLETED)
        for f in done:
            response = f.result()
            # for response in await asyncio.gather(*future):
            # Check for HTTP errors
            try:
                response.raise_for_status()
            except HTTPError as http_err:
                # Handle HTTP errors here
                error = http_err
                # Log the error or perform other error handling
                self._logger.error(f"HTTP error occurred: {http_err}")
                # You can choose to continue, break, or return based on your logic
                continue
            try:
                if self.download is True:
                    # Filename:
                    filename = os.path.basename(url)
                    # Get the filename from the response headers, if available
                    content_disposition = response.headers.get("content-disposition")
                    if content_disposition:
                        _, params = content_disposition.split(";")
                        try:
                            key, value = params.strip().split("=")
                            if key == "filename":
                                filename = value.strip("'\"")
                        except ValueError:
                            pass
                    if "{filename}" in str(self.filename):
                        self.filename = str(self.filename).format_map(
                            SafeDict(filename=filename)
                        )
                    if "{" in str(self.filename):
                        self.filename = str(self.filename).format_map(
                            SafeDict(**self.arguments)
                        )
                    if isinstance(self.filename, str):
                        self.filename = Path(self.filename)
                    # Saving File in Directory:
                    total_length = response.headers.get("Content-Length")
                    self._logger.info(
                        f"HTTPClient: Saving File {self.filename}, size: {total_length}"
                    )
                    pathname = self.filename.parent.absolute()
                    if not pathname.exists():
                        # Create a new directory
                        pathname.mkdir(parents=True, exist_ok=True)
                    response.raise_for_status()
                    transfer = response.headers.get("transfer-encoding", None)
                    if transfer is None:
                        chunk_size = int(total_length)
                    else:
                        chunk_size = 8192
                    if self.filename.exists() and self.filename.is_file():
                        overwrite = self.destination.get("overwrite", True)
                        if overwrite is False:
                            self._logger.warning(
                                f"HTTPClient: File Already exists: {self.filename}"
                            )
                            # Filename already exists
                            result = self.filename
                            continue
                        else:
                            self._logger.warning(
                                f"HTTPClient: Overwriting File: {self.filename}"
                            )
                            # Delete the file before downloading again.
                            try:
                                self.filename.unlink()
                            except Exception as e:
                                self._logger.warning(
                                    f"HTTPClient: Error Deleting File: {self.filename}, {e}"
                                )
                    with open(self.filename, "wb") as fp:
                        try:
                            for chunk in response.iter_content(chunk_size=chunk_size):
                                fp.write(chunk)
                            fp.flush()
                        except Exception:
                            pass
                    self._logger.debug(f"Filename Saved Successfully: {self.filename}")
                    result = self.filename
                elif self.accept in ("text/html"):
                    result = response.content  # Get content of the response as bytes
                    try:
                        # html parser for lxml
                        self._parser = html.fromstring(result)
                        # BeautifulSoup parser
                        self._bs = bs(response.text, self._default_parser)
                        result = self._bs
                    except Exception as e:
                        error = e
                elif self.accept in ("application/xhtml+xml", "application/xml"):
                    result = response.content  # Get content of the response as bytes
                    try:
                        self._parser = etree.fromstring(result)
                    except Exception as e:
                        error = e
                elif self.accept == "application/json":
                    try:
                        result = response.json()
                    except Exception as e:
                        logging.error(e)
                        # is not an json, try first with beautiful soup:
                        try:
                            self._bs = bs(response.text, self._default_parser)
                            result = self._bs
                        except Exception:
                            error = e
                else:
                    result = response.text
            except requests.exceptions.ProxyError as err:
                raise ComponentError(f"Proxy Connection Error: {err!r}") from err
            except requests.ReadTimeout as err:
                return (result, err)
            except requests.exceptions.HTTPError as e:
                # Log the error or perform other error handling
                self._logger.error(f"HTTP error occurred: {error}")
                raise ComponentError(f"HTTP Error: {error!r}, ex: {e!s}") from e
            except Exception as e:
                logging.exception(e)
                return (result, e)
        # returning results
        return (result, error)

    @staticmethod
    async def response_read(response):
        if hasattr(response, 'aread'):
            return await response.aread()

        return await response.read()

    @staticmethod
    async def response_json(response):
        if asyncio.iscoroutinefunction(response.json):
            return await response.json()

        return response.json()

    @staticmethod
    def response_status(response):
        if hasattr(response, 'status_code'):
            return response.status_code

        return response.status

    @staticmethod
    async def response_text(response):
        if asyncio.iscoroutinefunction(response.text):
            return await response.text()

        return response.text

    @staticmethod
    async def response_reason(response):
        # Attempt to retrieve `reason`, `reason_phrase`, or fallback to an empty string
        reason = getattr(response, 'reason', getattr(response, 'reason_phrase', b''))

        return f"{reason!s}"

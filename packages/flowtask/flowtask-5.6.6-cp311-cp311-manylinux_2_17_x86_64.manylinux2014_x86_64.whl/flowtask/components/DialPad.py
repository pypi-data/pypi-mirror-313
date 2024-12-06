import asyncio
from collections.abc import Callable
from urllib.parse import urljoin
from .flow import FlowComponent
from ..interfaces.http import HTTPService
from ..exceptions import ComponentError


class DialPad(FlowComponent, HTTPService):
    """
        DialPad

        Overview

            The DialPad class is a component for interacting with the DialPad API. It extends the FlowComponent and HTTPService
            classes, providing methods for authentication, fetching statistics, and handling API responses.

        .. table:: Properties
        :widths: auto

            +------------------+----------+--------------------------------------------------------------------------------------------------+
            | Name             | Required | Description                                                                                      |
            +------------------+----------+--------------------------------------------------------------------------------------------------+
            | accept           |   No     | The accepted content type for API responses, defaults to "application/json".                     |
            +------------------+----------+--------------------------------------------------------------------------------------------------+
            | download         |   No     | The download flag indicating if a file download is required.                                     |
            +------------------+----------+--------------------------------------------------------------------------------------------------+
            | _credentials     |   Yes    | A dictionary containing the API key for authentication.                                          |
            +------------------+----------+--------------------------------------------------------------------------------------------------+
            | _base_url        |   Yes    | The base URL for the DialPad API.                                                                |
            +------------------+----------+--------------------------------------------------------------------------------------------------+
            | auth             |   Yes    | The authentication header for API requests.                                                      |
            +------------------+----------+--------------------------------------------------------------------------------------------------+
        Return

            The methods in this class manage the interaction with the DialPad API, including initialization, fetching statistics,
            processing results, and handling credentials.

    """ # noqa
    accept: str = "application/json"
    download = None
    _credentials: dict = {"APIKEY": str}

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        FlowComponent.__init__(self, loop=loop, job=job, stat=stat, **kwargs)
        HTTPService.__init__(self, **kwargs)

    async def start(self, **kwargs):
        self._base_url = "https://dialpad.com/api/v2/"

        self.processing_credentials()
        self.auth = {"apikey": self.credentials["APIKEY"]}

        return True

    async def dialpad_stats(self):
        # processing statistics asynchronously
        stats_url = urljoin(self._base_url, "stats/")
        processing_result, _ = await self.session(
            stats_url, "post", data=self.body_params, use_json=True
        )
        request_id = processing_result.get("request_id")

        get_result_url = urljoin(stats_url, request_id)
        response_result, _ = await self.session(get_result_url, use_json=True)
        file_url = response_result.get("download_url")

        self.download = False
        result, _ = await self.session(file_url)

        return result

    async def run(self):
        try:
            method = getattr(self, f"dialpad_{self.type}")
        except AttributeError as ex:
            raise ComponentError(f"{__name__}: Wrong 'type' on task definition") from ex

        result = await method()

        df_results = await self.from_csv(result)

        self._result = df_results
        return self._result

    async def close(self):
        pass

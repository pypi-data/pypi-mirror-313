import asyncio
from collections.abc import Callable
from urllib.parse import urljoin
import pandas as pd
from .flow import FlowComponent
from ..interfaces.http import HTTPService
from ..exceptions import ComponentError


class OdooInjector(HTTPService, FlowComponent):
    """
    OdooInjector

        Overview

            The OdooInjector class is a component for injecting data into an Odoo server using a provided API key.
            This component takes data from a Pandas DataFrame, formats it as payload, and sends it to an Odoo endpoint
            specified in the credentials, facilitating seamless integration with Odoo’s API.

        .. table:: Properties
        :widths: auto

            +----------------+----------+-----------+---------------------------------------------------------------+
            | Name           | Required | Summary                                                                |
            +----------------+----------+-----------+---------------------------------------------------------------+
            | credentials    |   Yes    | A dictionary containing connection details for the Odoo server:        |
            |                |          | "HOST", "PORT", "APIKEY", and "INJECTOR_URL".                          |
            +----------------+----------+-----------+---------------------------------------------------------------+
            | model          |   Yes    | The Odoo model into which data will be injected.                       |
            +----------------+----------+-----------+---------------------------------------------------------------+
            | headers        |   No     | Optional headers to include with the API request. Defaults to API key.  |
            +----------------+----------+-----------+---------------------------------------------------------------+
            | data           |   Yes    | The data to inject, formatted as a list of dictionaries from DataFrame. |
            +----------------+----------+-----------+---------------------------------------------------------------+

        Returns

            This component returns a Boolean indicating whether the data injection was successful.
            In case of errors, detailed logging is provided, and an exception is raised with the error message.
            Additionally, the component tracks successful API interactions and logs any unsuccessful payload deliveries
            for debugging and tracking.
    """ #noqa

    accept: str = "application/json"
    auth_type: str = "api_key"
    download = None
    _credentials: dict = {
        "HOST": str,
        "PORT": str,
        "APIKEY": str,
        "INJECTOR_URL": str,
    }

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        super().__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    async def start(self, **kwargs):
        if self.previous and isinstance(self.input, pd.DataFrame):
            self.data = self.input.to_dict(orient="records")

        self.processing_credentials()

        self.headers = {"api-key": self.credentials["APIKEY"]}

        self.url = self.get_url()

        return True

    async def run(self):
        payload = self.get_payload()
        result, error = await self.session(
            url=self.url, method="post", data=payload, use_json=True
        )

        if not result or (
            not error
            and 'error' not in result
            and "error" not in result.get("result")
            and result["result"].get("ids")
        ):
            self._logger.debug(result)
            return True

        error_msg = str(
            error or result.get('error') or result["result"].get("error") or result["result"]["messages"]
        )
        raise ComponentError(error_msg)

    async def close(self):
        return True

    def get_url(self):
        port = (
            f":{self.credentials['PORT']}" if self.credentials["PORT"] != "80" else ""
        )
        base_url = f"{self.credentials['HOST']}{port}"
        url = urljoin(base_url, self.credentials["INJECTOR_URL"])
        return url

    def get_payload(self):
        return {
            "model": self.model,
            "options": {
                # 'has_headers': True,
                "advanced": False,
                "keep_matches": False,
                "name_create_enabled_fields": getattr(self, "name_create_enabled_fields", {}),
                "import_set_empty_fields": [],
                "import_skip_records": [],
                "fallback_values": {},
                "skip": 0,
                "limit": 2000,
                # 'encoding': '',
                # 'separator': '',
                "quoting": '"',
                # 'sheet': 'Sheet1',
                "date_format": "",
                "datetime_format": "",
                "float_thousand_separator": ",",
                "float_decimal_separator": ".",
                "fields": [],
            },
            "data": self.data,
        }

from typing import Optional
import asyncio
from asyncdb import AsyncDB
from navconfig.logging import logging
from querysource.conf import asyncpg_url, default_dsn
from ..credentials import CredentialsInterface


class DBSupport(CredentialsInterface):
    """DBSupport.

        Interface for adding AsyncbDB-based Database Support to Components.
    """
    _service_name: str = 'Flowtask'
    _credentials = {
        "user": str,
        "password": str,
        "host": str,
        "port": int,
        "database": str,
    }

    def __init__(
        self,
        *args,
        **kwargs
    ):
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(
                'Flowtask.DBSupport'
            )
        super().__init__(*args, **kwargs)

    def event_loop(
        self, evt: Optional[asyncio.AbstractEventLoop] = None
    ) -> asyncio.AbstractEventLoop:
        if evt is not None:
            asyncio.set_event_loop(evt)
            return evt
        else:
            try:
                return asyncio.get_event_loop()
            except RuntimeError as exc:
                try:
                    evt = asyncio.new_event_loop()
                    asyncio.set_event_loop(evt)
                    return evt
                except RuntimeError as exc:
                    raise RuntimeError(
                        f"There is no Event Loop: {exc}"
                    ) from exc

    def get_connection(
        self,
        driver: str = "pg",
        dsn: Optional[str] = None,
        params: Optional[dict] = None,
        event_loop: Optional[asyncio.AbstractEventLoop] = None,
        **kwargs,
    ):
        # TODO: datasources and credentials
        if not kwargs and driver == "pg":
            kwargs = {
                "server_settings": {
                    "application_name": f"{self._service_name}.DB",
                    "client_min_messages": "notice",
                    "max_parallel_workers": "512",
                    "jit": "on",
                }
            }
        if not event_loop:
            event_loop = self.event_loop()
        args = {
            "loop": event_loop,
            **kwargs
        }
        if dsn is not None:
            args["dsn"] = dsn
        if params is not None:
            args["params"] = params
        return AsyncDB(
            driver, **args
        )

    def db_connection(
        self,
        driver: str = "pg",
        credentials: Optional[dict] = None,
        event_loop: Optional[asyncio.AbstractEventLoop] = None,
    ):
        if not credentials:
            credentials = {"dsn": default_dsn}
        else:
            credentials = {"params": credentials}
        kwargs = {}
        if driver == "pg":
            kwargs = {
                "server_settings": {
                    "application_name": f"{self._service_name}.DB",
                    "client_min_messages": "notice",
                    "max_parallel_workers": "512",
                    "jit": "on",
                }
            }
        if not event_loop:
            event_loop = self.event_loop()
        return AsyncDB(
            driver,
            loop=event_loop,
            **credentials,
            **kwargs
        )

    def pg_connection(
        self,
        dsn: Optional[str] = None,
        credentials: Optional[dict] = None,
        event_loop: Optional[asyncio.AbstractEventLoop] = None,
    ):
        if not credentials:
            if dsn is not None:
                credentials = {"dsn": dsn}
            else:
                credentials = {"dsn": asyncpg_url}
        else:
            credentials = {"params": credentials}
        kwargs: dict = {
            "min_size": 2,
            "server_settings": {
                "application_name": f"{self._service_name}.DB",
                "client_min_messages": "notice",
                "max_parallel_workers": "512",
                "jit": "on",
            },
        }
        if not event_loop:
            event_loop = self.event_loop()
        return AsyncDB(
            "pg",
            loop=event_loop, **credentials, **kwargs
        )

    def get_default_driver(self, driver: str):
        """get_default_driver.

        Getting a default connection based on driver's name.
        """
        driver_path = f"querysource.datasources.drivers.{driver}"
        drv = f"{driver}_default"
        try:
            driver_module = __import__(driver_path, fromlist=[driver])
            drv_obj = getattr(driver_module, drv)
            return drv_obj
        except ImportError as err:
            raise ImportError(
                f"Error importing driver: {err!s}"
            ) from err
        except AttributeError as err:
            raise AttributeError(
                f"Error getting driver: {err!s}"
            ) from err
        except Exception as err:
            raise Exception(
                f"Error getting default connection: {err!s}"
            ) from err

    def default_connection(self, driver: str):
        """default_connection.

        Default Connection to Database.
        """
        credentials = {}
        try:
            driver = self.get_default_driver(driver)
            credentials = driver.params()
            if driver.driver == 'pg' and credentials.get('username', None) is not None:
                credentials['user'] = credentials.pop('username')
        except ImportError as err:
            raise ImportError(
                f"Error importing Default driver: {err!s}"
            ) from err
        try:
            return self.get_connection(
                driver=driver.driver,
                params=credentials
            )
        except Exception as err:
            raise Exception(
                f"Error getting Default Connection: {err!s}"
            ) from err

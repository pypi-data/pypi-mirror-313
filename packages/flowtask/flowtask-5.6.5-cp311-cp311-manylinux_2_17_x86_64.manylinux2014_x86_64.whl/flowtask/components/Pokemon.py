import asyncio
from collections.abc import Callable
import math
from uuid import uuid4
from urllib.parse import urlencode, urljoin
from requests.models import PreparedRequest
import numpy as np
import pandas as pd
from .flow import FlowComponent
from ..interfaces.http import HTTPService
from ..exceptions import (
    ComponentError,
    DataError,
    DataNotFound
)


class Pokemon(HTTPService, FlowComponent):
    """
    Pokémon Component

    **Overview**

    This component interacts with the Pokémon API to retrieve data about machines or their on-hand inventory.
    It supports two main operations determined by the `type` parameter:

    - **"machines"**: Retrieves a list of machines.
    - **"inventory"**: Retrieves on-hand inventory data for specified machines.
    - **sites**: Retrieves the Pokemon sites
    - **locations**: Retrieves the Pokemon locations
    - **warehouses**: Retrieves the Pokemon warehouses


    The component handles authentication, constructs the necessary requests, processes the data,
    and returns a pandas DataFrame suitable for further analysis in your data pipeline.

    .. table:: Properties
       :widths: auto

    +----------------------------+----------+----------------------------------------------------------------------------------------------+
    |   Name                     | Required | Summary                                                                                      |
    +----------------------------+----------+----------------------------------------------------------------------------------------------+
    |   credentials              | Yes      | Dictionary containing API credentials: `"BASE_URL"`, `"CLIENT_ID"`, and `"CLIENT_SECRET"`.   |
    |                            |          | Credentials can be retrieved from environment variables.                                     |
    +----------------------------+----------+----------------------------------------------------------------------------------------------+
    |   type                     | Yes      | Type of operation to perform. Accepts `"machines"` to retrieve machine data or `"inventory"` |
    |                            |          | to retrieve machine inventory data.                                                          |
    +----------------------------+----------+----------------------------------------------------------------------------------------------+
    |   ids                      | No       | List of machine IDs to retrieve inventory for when `type` is `"inventory"`.                  |
    |                            |          | Overrides IDs from the previous step if provided.                                            |
    +----------------------------+----------+----------------------------------------------------------------------------------------------+
    |   data                     | No       | Data from the previous step, typically a pandas DataFrame containing machine                 |
    |                            |          | IDs in a column named `"machine_id"`. Used when `type` is `"inventory"`.                     |
    +----------------------------+----------+----------------------------------------------------------------------------------------------+

    **Returns**

    This component returns a pandas DataFrame containing the retrieved data from the Pokémon API.
    The structure of the DataFrame depends on the operation type:

    - **For `type = "machines"`**: The DataFrame contains information about machines, with columns corresponding
        to the machine attributes provided by the API.
    - **For `type = "inventory"`**: The DataFrame contains on-hand inventory details for each machine,
        including `machineId` and detailed slot information.
    """  # noqa
    accept: str = "application/json"
    download = None
    _credentials: dict = {
        "BASE_URL": str,
        "CLIENT_ID": str,
        "CLIENT_SECRET": str,
    }
    ids: list = []
    errors_df: pd.DataFrame = None

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.type: str = kwargs.get('type')
        self.machine_inventory: bool = kwargs.get('machine_inventory', False)
        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input

        self.processing_credentials()

        # Adding client_id and secret:
        self.headers["client_id"] = self.credentials["CLIENT_ID"]
        self.headers["client_secret"] = self.credentials["CLIENT_SECRET"]

        return True

    async def run(self):
        type_call = getattr(self, f"{self.type}", None)

        if not type_call:
            raise ComponentError(
                "incorrect or not provided type"
            )

        if not callable(type_call):
            raise ComponentError(
                f"Function {self.type} doesn't exist."
            )

        try:
            result = await type_call()
        except (ComponentError, DataError, DataNotFound) as e:
            self._logger.error(f"Error: {str(e)}")
            raise

        if not isinstance(result, pd.DataFrame):
            self._result = result
            return self._result

        errors_df = pd.DataFrame()

        if "errorCode" in result.columns:
            errors_df = result[result['errorCode'].notnull()]
            self._logger.error("ROWS with Errors Found. Check Log!")

        self.add_metric("NUMROWS", len(result.index))
        self.add_metric("NUMCOLS", len(result.columns))
        self.add_metric("ERRORROWS", len(errors_df.index))

        self._result = result

        if self._debug is True:
            self._print_data("Result Data", self._result)

            if not errors_df.empty:
                self._print_data("Error Data", errors_df)

        return self._result

    async def close(self):
        return True

    def _print_data(self, title: str, data_df: pd.DataFrame):
        """
        Prints the data and its corresponding column types for a given DataFrame.

        Parameters:
        title (str): The title to print before the data.
        data_df (pd.DataFrame): The DataFrame to print and inspect.
        """
        print(f"::: Printing {title} === ")
        print("Data: ", data_df)
        for column, t in data_df.dtypes.items():
            print(f"{column} -> {t} -> {data_df[column].iloc[0]}")

    def _create_url_arguments(self, method: str, path: str):
        """
        Creates the URL arguments for the given method and path.

        Parameters:
        method (str): The HTTP method for the request.
        path (str): The path for the request.

        Returns:
        dict: The URL arguments for the request.
        """
        self.headers["request-id"] = str(uuid4())
        url_args = {
            "method": method,
            "url": path,
            "use_proxy": False
        }
        return url_args

    async def _get_pokemon_results(self, args, payload):
        results, error = await self.session(**args, data=payload, use_json=True)

        if results and "machines" in results:
            df = await self.create_dataframe(results["machines"])
            df_exploded = df.explode("slots").reset_index(
                drop=True
            )  # Reset index to ensure uniqueness
            df = pd.concat(
                [df_exploded["machineId"], pd.json_normalize(df_exploded["slots"])],
                axis=1,
            )

            return df
        else:
            raise ComponentError(
                f"{__name__}: Error in Machines request: {error}"
            )

    def get_pokemon_url(self, resource, parameters: dict = None):
        url = urljoin(self.credentials["BASE_URL"], resource)
        if parameters:
            url += "?" + urlencode(parameters)
        return url

    def get_machines_inventory_payload(self, machines: list):
        return {"requestFilter": {"machineIds": machines}}

    @staticmethod
    def split_chunk_ids(items: pd.Series, chunk_size: str):
        """
        Splits a Series of IDs into chunks of a specified size.

        Parameters:
        items (pd.Series): A pandas Series containing the IDs to be split.
        chunk_size (int): The maximum number of IDs per chunk.

        Returns:
        list: A list of NumPy arrays, each containing a chunk of IDs.
            If the Series is empty or all IDs are NaN, returns an empty list or a list containing an empty array.
        """
        data = items.dropna().unique().astype(str)

        if data.size > 0:
            split_n = math.ceil(data.size / chunk_size)

            # Split into chunks of n items
            return np.array_split(data, split_n)  # Convert to NumPy array and split

        return [data]

    async def inventory(self):
        args = self._create_url_arguments(
            method="post",
            path=self.get_pokemon_url("machines/on-hand-inventory"),
        )
        # List of Machine IDs
        if self.data:
            self._logger.info(
                f'{__name__}: Using ids provided by previous step in the column "machine_id".'
            )
            self.data_ids = self.data["machine_id"]
        elif self.ids:
            self._logger.info(f"{__name__}: Using ids provided in Task arguments.")
            self.data_ids = pd.Series(self.ids)
        else:
            raise ComponentError(
                f'{__name__}: No machine "ids" provided to query to request Inventory'
            )

        ids_chunks = self.split_chunk_ids(
            items=self.data_ids,
            chunk_size=4,
        )

        df_items = pd.DataFrame()
        for ids_chunk in ids_chunks:
            payload = self.get_machines_inventory_payload(ids_chunk.tolist())
            items = await self._get_pokemon_results(args, payload)
            df_items = pd.concat([df_items, items], ignore_index=True)

        return df_items

    async def _get_pokemon_resource(self, resource: str = 'sites'):
        """Get a Pokemon Resource with optional Pagination (as sites, or Locations)


        Args:
        resource (str, optional): The resource to get (default'sites').

        Return:
        pd.DataFrame: The DataFrame containing the requested resource.

        """
        result = []
        offset = None
        off_args = None
        while True:
            if offset:
                off_args = {"offset": offset}
            args = self._create_url_arguments(
                method="get",
                path=self.get_pokemon_url(resource, off_args),
            )
            results, error = await self.session(**args)
            if error:
                raise DataError(
                    f"Error getting Pokemon {resource.capitalize()} {error}"
                )
            if r := results.get(resource, []):
                result.extend(r)
            else:
                break
            offset = results.get('offset', None)
            if offset is None:
                break
        if not result:
            raise DataNotFound(f"No Pokemon {resource.capitalize()} found")
        return await self.create_dataframe(result)

    async def sites(self):
        return await self._get_pokemon_resource('sites')

    async def locations(self):
        return await self._get_pokemon_resource('locations')

    async def warehouses(self):
        args = self._create_url_arguments(
            method="get",
            path=self.get_pokemon_url("warehouses/merch")
        )
        results, error = await self.session(**args)

        if result := results.get("merchWarehouses", None):
            return await self.create_dataframe(result)
        else:
            raise ComponentError(
                f"{__name__}: Error in Machines request: {error} {results}"
            )

    async def machines(self):
        args = self._create_url_arguments(
            method="get",
            path=self.get_pokemon_url("machines")
        )
        results, error = await self.session(**args)

        if result := results.get("machines", None):
            return await self.create_dataframe(result)
        else:
            raise ComponentError(
                f"{__name__}: Error in Machines request: {error} {results}"
            )

    async def health(self):
        args = self._create_url_arguments(
            method="get",
            path=self.get_pokemon_url("health-check")
        )
        result, error = await self.session(**args)

        if message := result.get("message", None):
            if message == "The ar-vending-prc-api is up and running":
                return result
            else:
                return result
        else:
            raise ComponentError(
                f"{__name__}: Error in Health request: {error}"
            )

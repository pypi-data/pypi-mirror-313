from typing import Dict
from navconfig.logging import logging
from querysource.exceptions import DataNotFound as QSNotFound
from ..exceptions import ComponentError, DataNotFound
from .QSBase import QSBase


class GoogleA4(QSBase):
    """
    GoogleA4

    Overview

        The GoogleA4 class is a component for interacting with Google Analytics 4 (GA4) to fetch and transform report data. 
        It extends the QSBase class and provides methods for retrieving reports and transforming the data into a specified format.

    .. table:: Properties
       :widths: auto

    +--------------+----------+-----------+----------------------------------------------------------+
    | Name         | Required | Summary                                                              |
    +--------------+----------+-----------+----------------------------------------------------------+
    | datalist     |   Yes    |  Method for reports                                                  |
    +--------------+----------+-----------+----------------------------------------------------------+
    | subtask      |   Yes    |  Identifiers of property and metrics                                 |
    +--------------+----------+-----------+----------------------------------------------------------+
    | type         |   Yes    | Defines the type of data handled by the component, set to "report".  |
    +--------------+----------+-----------+----------------------------------------------------------+
    | _driver      |   Yes    | Specifies the driver used by the component, set to "ga".             |
    +--------------+----------+-----------+----------------------------------------------------------+
    | _metrics     |   Yes    | A dictionary mapping GA4 metrics to their corresponding output names.|
    +--------------+----------+-----------+----------------------------------------------------------+
    | _qs          |   Yes    | Instance of the QSBase class used to interact with the data source.  |
    +--------------+----------+-----------+----------------------------------------------------------+

        Raises:
            DataNotFound: If no data is found.
            ComponentError: If any other error occurs during execution.

    Return

    The methods in this class return the requested report data from Google Analytics 4, formatted according to the specific requirements of the component.

    """


    type = "report"
    _driver = "ga"
    _metrics: Dict = {
        "sessions": "sessions",
        "totalUsers": "total_users",
        "newUsers": "new_users",
        "engagedSessions": "engaged_users",
        "sessionsPerUser": "per_user",
    }

    async def report(self):
        try:
            resultset = await self._qs.report()
            result = []
            # TODO: making a better data-transformation
            self.add_metric(
                "START_DATE", self._kwargs["start_date"]
            )
            self.add_metric("END_DATE", self._kwargs["end_date"])
            self.add_metric("COMPANY", self._kwargs["company_id"])
            self.add_metric("DIMENSION", self._kwargs["ga4_dimension"])
            for row in resultset:
                res = {}
                # res['property_id'] = self._kwargs['property_id']
                res["start_date"] = self._kwargs["start_date"]
                res["end_date"] = self._kwargs["end_date"]
                res["company_id"] = self._kwargs["company_id"]
                res["dimension"] = self._kwargs["dimensions"]
                if "ga4_dimension" in self._variables:
                    res["ga4_dimension"] = self._variables["ga4_dimension"]
                elif "ga4_dimension" in self._kwargs:
                    res["ga4_dimension"] = self._kwargs["ga4_dimension"]
                dimensions = {}
                for dimension in self._kwargs["dimensions"]:
                    dimensions[dimension] = row[dimension]
                res["dimensions"] = dimensions
                metrics = {}
                for metric in self._kwargs["metric"]:
                    metrics[metric] = row[metric]
                    try:
                        new_metric = self._metrics[metric]
                        res[new_metric] = row[metric]
                    except KeyError:
                        pass
                res["metric"] = metrics
                result.append(res)
            return result
        except QSNotFound as err:
            raise DataNotFound(f"GA4 Not Found: {err}") from err
        except Exception as err:
            logging.exception(err)
            raise ComponentError(f"Google Analytics 4 ERROR: {err!s}") from err

import asyncio
from collections.abc import Callable
import pandas as pd
import numpy as np
from ..exceptions import ComponentError
from .flow import FlowComponent


class tFilter(FlowComponent):
    """
    tFilter

        Overview

            The tFilter class is a component that applies specified filters to a Pandas DataFrame.
            It allows filtering rows based on multiple conditions and expressions, enabling targeted
            data extraction within a task flow.

        .. table:: Properties
        :widths: auto

            +--------------+----------+-----------+---------------------------------------------------------------+
            | Name         | Required | Summary                                                                |
            +--------------+----------+-----------+---------------------------------------------------------------+
            | operator     |   Yes    | Logical operator (e.g., `and`, `or`) used to combine filter conditions. |
            +--------------+----------+-----------+---------------------------------------------------------------+
            | conditions   |   Yes    | List of conditions with columns, values, and expressions for filtering. |
            |              |          | Format: `{ "column": <col_name>, "value": <val>, "expression": <expr> }`|
            +--------------+----------+-----------+---------------------------------------------------------------+

        Returns

            This component returns a filtered Pandas DataFrame based on the provided conditions. The component tracks metrics
            such as the initial and filtered row counts, and optionally limits the returned columns if specified.
            Additional debugging information can be outputted based on configuration.
    """  # noqa

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self.condition: str = ""
        super(tFilter, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        # Si lo que llega no es un DataFrame de Pandas se cancela la tarea
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError("Data Not Found", status=404)
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError("Incompatible Pandas Dataframe", status=404)
        return True

    async def close(self):
        pass

    async def run(self):
        self.add_metric("STARTED_ROWS", len(self.data.index))
        if hasattr(self, "filter"):
            try:
                if len(self.filter) > 1:
                    if not hasattr(self, "operator"):
                        raise ComponentError("Operator not found", status=404)
                    conditions = []
                    for cond in self.filter:
                        value = cond["value"]
                        column = cond["column"]
                        expression = cond.get('expression', '==')
                        if isinstance(value, str):
                            if expression == 'regex':
                                conditions.append(
                                    f"self.data['{column}'].str.match(r'{value}')"
                                )
                            else:
                                cond["value"] = "'{}'".format(value)
                                conditions.append(
                                    "(self.data['{column}'] {expression} {value})".format_map(
                                        cond
                                    )
                                )
                        if isinstance(value, list):
                            if expression == 'startswith':
                                # Use tuple directly with str.startswith
                                val = tuple(value)
                                condition = f"self.data['{column}'].str.startswith({val})"
                                conditions.append(f"({condition})")
                            elif expression == "regex":
                                # Regular expression match
                                conditions.append(
                                    f"self.data['{column}'].str.match(r'{value}')"
                                )
                            elif expression == "==":
                                conditions.append(
                                    "(self.data['{column}'].isin({value}))".format_map(
                                        cond
                                    )
                                )
                            elif expression == "!=":
                                # not:
                                conditions.append(
                                    "(~self.data['{column}'].isin({value}))".format_map(
                                        cond
                                    )
                                )
                        # self.condition = f'{self.condition} {self.operator} ' if self.condition else ''
                    # apply:
                    self.condition = f" {self.operator} ".join(conditions)
                    print("CONDITION >> ", self.condition)
                    self.data = self.data.loc[
                        eval(self.condition)
                    ]  # pylint: disable=W0123
                else:
                    cond = self.filter[0]
                    column = cond["column"]
                    value = cond["value"]
                    expression = cond.get('expression', '==')
                    if isinstance(value, list):
                        if expression == 'startswith':
                            # Use tuple directly with str.startswith
                            val = tuple(value)
                            self.condition = f"self.data['{column}'].str.startswith({val})"
                            self.data = self.data.loc[eval(self.condition)]
                        elif expression == 'regex':
                            self.condition = f"self.data['{column}'].str.contains(r'{value}')"
                            self.data = self.data.loc[eval(self.condition)]
                        elif expression == '!=':
                            self.condition = f"~self.data['{column}'].isin({value})"
                            self.data = self.data.loc[eval(self.condition)]
                        else:
                            self.data = self.data.loc[self.data[column].isin(value)]
                    else:
                        self.condition = (
                            "(self.data.{column} {expression} {value})".format_map(cond)
                        )
                        self.data = self.data.loc[
                            eval(self.condition)
                        ]  # pylint: disable=W0123
            except Exception as err:
                raise ComponentError(f"Generic Error on Data: error: {err}") from err
            print("Filtered: ", self.data)
            self.add_metric("FILTERED_ROWS", len(self.data.index))
        if hasattr(self, "columns"):
            # returning only a subset of data
            self.data = self.data[self.columns]
        if self._debug is True:
            print("::: Printing Column Information === ")
            for column, t in self.data.dtypes.items():
                print(column, "->", t, "->", self.data[column].iloc[0])
        self.add_metric("FILTERED_COLS", len(self.data.columns))
        self._result = self.data
        return self._result

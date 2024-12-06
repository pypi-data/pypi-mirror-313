from typing import Any
import builtins
import traceback
import querysource.utils.functions as qsfunctions
from ....utils import cPrint, check_empty
from . import functions as alertfunc
from . import colfunctions as colfunc
from ..abstract import AbstractEvent
# from ..interfaces import Notification
from ....interfaces.notification import Notification


class Alert(Notification, AbstractEvent):
    def __init__(self, *args, **kwargs):
        # adding checks:
        self.system_checks: list = kwargs.pop("system_checks", [])
        self.result_checks: list = kwargs.pop("result_checks", [])
        self.column_checks: list = kwargs.pop("column_checks", [])
        super().__init__(*args, **kwargs)

    async def __call__(self, *args, **kwargs):
        task = kwargs.pop("task", None)
        program = task.getProgram()
        task_name = f"{program}.{task.taskname}"
        try:
            stats = task.stats.to_json()
        except AttributeError:
            stats = None

        df = task.resultset()

        errors = []

        if self.system_checks:
            rst = await self.process_checks(self.system_checks, stats, task_name)
            errors += rst

        if self.result_checks:
            if check_empty(df):
                return None
            data = {"num_rows": len(df), "num_columns": df.shape[1]}
            rst = await self.process_checks(self.result_checks, data, task_name)
            errors += rst

        if self.column_checks:
            # Get the summary statistics of the DataFrame
            desc = df.describe()
            err = []
            for check in self.column_checks:
                fname, colname, fn, params = self.get_pandas_function(check)
                # Check if the column exists in the DataFrame
                if colname not in df.columns:
                    self._logger.warning(f"Column {colname} not found in DataFrame.")
                    continue
                # execute the function:
                self._logger.debug(f"Exec {fname} with args {params}")
                actual_value, result = fn(df, desc, colname, **params)
                if result is False:
                    # threshold was reached
                    self._logger.error(
                        f"{task_name}: Threshold for {fname} was reached with: {actual_value} on {colname}"
                    )
                    err.append(
                        {"function": fname, "column": colname, "value": actual_value}
                    )

        if errors:
            # TODO: send a notification about threshold violation.
            await self.notify(task_name, errors)

    def get_pandas_function(self, payload: dict):
        fname = list(payload.keys())[0]
        func = None
        try:
            params = payload[fname]
        except KeyError:
            params = {}
        # Extract the column name from the parameters
        col_name = params.pop("column")
        try:
            func = getattr(colfunc, fname)
        except AttributeError:
            self._logger.warning(f"Function {fname} does not exist on Alert System")
        return fname, col_name, func, params

    def get_function(self, payload: dict):
        fname = list(payload.keys())[0]
        try:
            params = payload[fname]
        except KeyError:
            params = {}
        try:
            func = getattr(alertfunc, fname)
        except AttributeError:
            try:
                func = getattr(qsfunctions, fname)
            except AttributeError:
                try:
                    func = globals()[fname]
                except AttributeError:
                    try:
                        func = getattr(builtins, fname)
                    except AttributeError:
                        func = None
        if not func:
            self._logger.warning(f"Function {fname} doesn't exist on Flowtask.")
            return None
        return fname, func, params

    def exec_function(self, fname, func, data, **kwargs):
        self._logger.debug(f"Exec {fname} with args {kwargs}")
        try:
            return func(data, **kwargs)
        except (TypeError, ValueError) as err:
            self._logger.exception(str(err), exc_info=True, stack_info=True)
            traceback.print_exc()
            return None

    async def process_checks(self, checks, data, task_name):
        errors = []
        for check in checks:
            fname, fn, params = self.get_function(check)
            colname, value, result = self.exec_function(fname, fn, data, **params)
            if result is False:
                # threshold was reached
                self._logger.error(
                    f"{task_name}: Threshold for {fname} was reached with: {value} on {colname}"
                )
                errors.append({"function": fname, "column": colname, "value": value})
        return errors

    async def notify(self, task_name: str, errors: list):
        pass
        # cPrint(
        #     f"{task_name}: {fname} reached for {colname} with value: {value}",
        #     level='CRITICAL'
        # )
        # Getting a Notify component based on Alert configuration:

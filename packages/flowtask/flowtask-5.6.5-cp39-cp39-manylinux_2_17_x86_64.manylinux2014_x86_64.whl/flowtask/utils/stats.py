"""TaskMonitor.

Collect and saves stats for execution of tasks.
"""
import os
import sys
from typing import Any, Union
import asyncio
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import time
from statistics import mean
from contextlib import suppress
from psutil import virtual_memory, cpu_percent, Process


executor = ThreadPoolExecutor(max_workers=1)


class StepMonitor:
    def __init__(self, name, parent=None) -> None:
        self.name = name
        self.executed_at: datetime = datetime.now()
        self.stats: dict = {}
        self.traceback: str = ""
        self._parent: Any = parent

    def add_metric(self, key, value) -> None:
        self.stats[key] = value

    def stacktrace(self, trace: str) -> None:
        self.traceback = trace

    def parent(self):
        return self._parent

    def __str__(self) -> str:
        trace = ""
        if self.traceback:
            trace = f"StackTrace: <{self.traceback!s}>\n"
        stat = (
            f"{self.name}:\n"
            f"Executed At: {self.executed_at}:\n"
            f"<{self.stats!r}>\n"
            f"{trace!s}\n"
        )
        return stat


class TaskMonitor:
    def __init__(
        self, name: str, program: str, task_id: str, userid: Union[int, str] = None
    ) -> None:
        self.task_name = name
        self.task_id = task_id
        self._started: bool = False
        self.traceback = None
        self.stats: dict = {}
        self.user: Union[int, str] = None
        self.steps: list[StepMonitor] = []
        self.executed_at: datetime = datetime.now()
        self.start_time: float = 0
        self.finish_time: float = 0
        self.duration: float = 0
        self._sampling_task: asyncio.Task
        self.program: str = program
        # CPU and RAM stats:
        self.baseline_cpu: float = 0
        self.baseline_ram: float = 0
        self._cpu_usage_data: list = []
        self._ram_usage_data: list = []
        self._memory_info: list = []
        # returned values of Stats
        self.max_cpu_used: float = 0
        self.avg_cpu_used: float = 0
        self.max_ram_used: float = 0
        self.avg_ram_used: float = 0
        self.memory_usage: float = 0
        # self.cpu_percent = partial(cpu_percent, interval=0)
        ## Memory usage:
        self._pid = os.getpid()
        self._process = Process(self._pid)
        self._memory_before = self._process.memory_info().rss
        ## TODO: passing User information:
        if sys.stdin and sys.stdin.isatty():
            self.exec_type = "console"
            try:
                self.user = os.environ.get("USER")
            except Exception:
                self.user = os.environ.get("USERNAME")
        else:
            # was dispatched from code
            try:
                if "qw" in sys.argv[0]:
                    self.exec_type = "worker"
                else:
                    self.exec_type = "task"
            except IndexError:
                self.exec_type = "code"
                self.user = os.getlogin()
        if not self.user:
            self.user = userid
        print(f"Execution Mode: {self.exec_type} by User: {self.user}")

    def __str__(self) -> str:
        steps = "\n".join([f"{step!s}" for step in self.steps])
        if steps:
            steps = f"Steps: \n{steps!s}\n"
        stat = (
            f"Task: {self.task_name}\n"
            f"ID: {self.task_id}\n"
            f"< {self.stats!r} >\n"
            f"{steps!s}"
        )
        return stat

    def to_json(self) -> dict:
        steps = {}
        for step in self.steps:
            steps[step.name] = {"executed_at": step.executed_at, **step.stats}
        stat = {
            "Task": self.task_name,
            "program": self.program,
            "task_name": f"{self.program}.{self.task_name}",
            "ID": self.task_id,
            **self.stats,
            "steps": {**steps},
        }
        return stat

    def add_step(self, step: StepMonitor) -> None:
        self.steps.append(step)

    def start_timing(self):
        self.start_time = time.time()

    def end_timing(self):
        self.finish_time = time.time()
        self.duration = self.finish_time - self.start_time

    def stacktrace(self, trace: str) -> None:
        self.traceback = trace

    def is_started(self) -> bool:
        return self._started

    async def cpu_percent(self, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(executor, cpu_percent)
        # return cpu_percent(*args, **kwargs)

    def _get_virtual_memory(self):
        return virtual_memory().percent

    async def get_virtual_memory(self):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(executor, self._get_virtual_memory)

    def _get_memory_info(self):
        return Process().memory_info().rss / 1048576

    async def get_memory_info(self):
        loop = asyncio.get_running_loop()
        memory_info = await loop.run_in_executor(executor, self._get_memory_info)
        return memory_info

    async def _get_current_state(self, interval: float = 0.3):
        """_get_current_state.
            Get the Current state of System, will be collected async every tick.
        Args:
            interval (float, optional): interval of collecting information. Defaults to 0.2.
        Raises:
            err: _description_
        """
        while True:
            try:
                if not self._started:  # Stop if _started is False.
                    break
                memory = await self.get_memory_info()
                cpu = await self.cpu_percent()
                ram = await self.get_virtual_memory()
                self._cpu_usage_data.append(cpu)
                self._ram_usage_data.append(ram)
                self._memory_info.append(memory)

                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                continue
            except Exception as err:
                logging.exception(f"Can't, Collect CPU/RAM metrics due to error: {err}")
                continue

    async def start(self, interval: float = 0.3):
        try:
            # check if not started:
            if not self._started:
                self._started = True
                self.start_timing()
                # Start task to call func periodically:
                self._sampling_task = asyncio.ensure_future(
                    self._get_current_state(interval)
                )
            # is started
        except Exception as err:
            logging.exception(f"Task Monitor Failed to Start, error: {err}")

    def _calculate_stats(self):
        if self._cpu_usage_data:
            self.max_cpu_used = max(self._cpu_usage_data)
            self.avg_cpu_used = mean(self._cpu_usage_data)
            self.max_ram_used = max(self._ram_usage_data)
            self.avg_ram_used = mean(self._ram_usage_data)
            self.memory_usage = mean(self._memory_info)

    async def stop(self) -> dict:
        try:
            # Check is sampling is happening
            if self._started:
                # Stopping Monitor.
                self._started = False
                # Stop task and await it stopped:
                self._sampling_task.cancel()
                try:
                    with suppress(asyncio.CancelledError):
                        await self._sampling_task
                except asyncio.CancelledError:
                    pass  # Task cancellation is expected, so just ignore the error.
                except Exception as err:
                    logging.exception(
                        f"Task Monitor failed to stop the sampling task: {err}"
                    )
                # Stop the clock, making calculations
                self.end_timing()
                self._calculate_stats()
                memory_after = 0
                rss_in_bytes = 0
                try:
                    memory_after = await asyncio.to_thread(
                        lambda: self._process.memory_info().rss
                    )
                    rss_in_bytes = memory_after - self._memory_before
                except Exception as err:
                    logging.exception(f"Unable to get Memory Info: {err}")
                self.stats.update(
                    {
                        "executed_at": f"{self.executed_at:%Y-%m-%d %H:%M}",
                        "duration": f"{self.duration:.5f}",
                        "pid": self._pid,
                        "max_cpu": round(float(self.max_cpu_used), 2),
                        "avg_cpu": round(float(self.avg_cpu_used), 2),
                        "max_ram": round(float(self.max_ram_used), 2),
                        "avg_ram": round(float(self.avg_ram_used), 2),
                        "memory_usage": self.memory_usage,
                        "thread_memory": round(rss_in_bytes / (1024 * 1024), 4),
                        "exec_type": self.exec_type,
                        "user": self.user,
                    }
                )
                return self.stats
            else:
                return {}
        except Exception as err:
            logging.exception(f"Task Monitor Failed to Stop, due to: {err}")
            raise

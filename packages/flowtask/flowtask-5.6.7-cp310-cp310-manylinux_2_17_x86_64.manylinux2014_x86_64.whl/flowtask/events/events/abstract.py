from abc import ABC, abstractmethod
import asyncio
from navconfig import config
from navconfig.logging import logging
from ...utils import cPrint
from ...interfaces import (
    LogSupport,
    MaskSupport,
    LocaleSupport
)


class AbstractEvent(MaskSupport, LogSupport, LocaleSupport, ABC):
    """Abstract Event Class.

    This class is the base class for all events in FlowTask.
    """
    def __init__(self, *args, **kwargs):
        self.disable_notification: bool = kwargs.pop(
            "disable_notification",
            False
        )
        super(AbstractEvent, self).__init__(*args, **kwargs)
        self._environment = config
        self._name_ = kwargs.get("name", self.__class__.__name__)
        self._logger = logging.getLogger(
            f"FlowTask.Event.{self._name_}"
        )
        # program
        self._program = kwargs.pop("program", "navigator")
        self._new_evt: bool = False
        try:
            self._loop = asyncio.get_event_loop()
        except RuntimeError:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._new_evt: bool = True
        if not self._loop:
            raise RuntimeError(
                "Event must be called from an Asyncio Event Loop"
            )
        self._task = kwargs.pop("task", None)
        self._args = args
        self._kwargs = kwargs
        # variables to be passed between actions and events
        self._variables: dict = {}
        # set the attributes of Action:
        for arg, val in kwargs.items():
            try:
                setattr(self, arg, val)
            except Exception as err:
                self._logger.warning(
                    f"Event: Wrong Attribute: {arg}={val}"
                )
                self._logger.error(err)

    async def close(self):
        if self._new_evt is True:
            try:
                self._loop.close()
            except RuntimeError:
                pass

    @abstractmethod
    async def __call__(self):
        """Called when event is dispatched."""

    def __repr__(self) -> str:
        return f"Event.{self.__class__.__name__}()"

    def name(self):
        return self._name_

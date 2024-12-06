from collections.abc import Callable
import asyncio
from ...interfaces.zammad import zammad
from ..BaseAction import BaseAction


class Zammad(BaseAction, zammad):
    """zammad.

    Generic Interface for managing Zammad instances.
    """

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ) -> None:
        """Init Method."""
        BaseAction.__init__(self, loop=loop, job=job, stat=stat, **kwargs)
        zammad.__init__(self, **kwargs)

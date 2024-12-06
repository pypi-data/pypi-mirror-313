from ..utils import cPrint, SafeDict
from .flow import FlowComponent


class Dummy(FlowComponent):
    async def start(self, **kwargs):
        """
        start.

            Initialize (if needed) a task
        """
        return True

    async def run(self):
        """
        run.

        Close (if needed) a task
        """
        try:
            self.message = self.message.format_map(SafeDict(**self._mask))
            cPrint(f"Message IS: {self.message}")
            self.add_metric("message", self.message)
        except Exception:
            self.save_traceback()
            raise
        return True

    async def close(self):
        """
        close.

        Close (if needed) a task
        """

    def save_stats(self):
        """
        Extension to save stats for this component
        """

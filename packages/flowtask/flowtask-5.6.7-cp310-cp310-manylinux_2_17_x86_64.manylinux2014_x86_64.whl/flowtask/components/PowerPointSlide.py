from pathlib import Path
from flowtask.interfaces.powerpoint import PowerPointClient
from .flow import FlowComponent
from ..exceptions import DataNotFound


class PowerPointSlide(FlowComponent, PowerPointClient):

    async def start(self, **kwargs):
        if self.previous and self.input:
            self.data = self.input

        if not self.data:
            raise DataNotFound("No Data Provided to create slides from.")

    async def run(self):
        result_file_path = self.create_presentation_from_template(
            template_path=Path(self.template_path),
            slide_contents=self.data,
            file_path=Path(self.output_file_path),
            default_master_index=getattr(self, "default_master_index", 0),
            default_layout_index=getattr(self, "default_layout_index", 1),
        )
        self._result = result_file_path
        self.add_metric("Slides Result Path", f"{self._result!s}")
        # Please return the number of slides if you need a metric.
        # self.add_metric("# of Slides created", len(prs.slides))
        return self._result

    async def close(self):
        pass

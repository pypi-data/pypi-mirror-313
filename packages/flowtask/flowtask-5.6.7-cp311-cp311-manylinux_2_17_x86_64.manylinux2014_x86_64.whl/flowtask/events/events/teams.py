from notify.models import TeamsCard, TeamsChannel
from notify.providers.teams import Teams
from notify.conf import MS_TEAMS_DEFAULT_TEAMS_ID, MS_TEAMS_DEFAULT_CHANNEL_ID
from ...utils.json import json_encoder
from ...interfaces.env import EnvSupport
from .abstract import AbstractEvent


class TeamsMessage(AbstractEvent, EnvSupport):
    async def __call__(self, *args, **kwargs):
        team_id = kwargs.pop("team_id", MS_TEAMS_DEFAULT_TEAMS_ID)
        channel = kwargs.pop("channel", MS_TEAMS_DEFAULT_CHANNEL_ID)
        channel_name = kwargs.pop("channel_name", "General")
        tm = Teams(
            as_user=True,
            team_id=team_id,
        )
        self.channel = self.get_env_value(
            channel, default=MS_TEAMS_DEFAULT_CHANNEL_ID
        )
        channel = TeamsChannel(
            name=channel_name,
            team_id=team_id,
            channel_id=self.channel,
        )
        status = kwargs.pop("status", "done")
        task = kwargs.pop("task", None)
        program = task.getProgram()
        task_name = f"{program}.{task.taskname}"
        task_id = task.task_id
        message = kwargs.pop("message", f"Task Completed {task_name}, {task_id}")
        try:
            stat = task.stats  # getting the stat object:
            stats = stat.to_json()
        except AttributeError:
            stats = []
        if status == "done":
            icon = "✅"
        elif status in ("error", "failed", "exception", "task error"):
            icon = "🛑"
        elif status in (
            "warning",
            "file_not_found",
            "not_found",
            "data_not_found",
            "done_warning",
        ):
            icon = "⚠️"
        elif status in ("empty_file"):
            icon = "📄"
        else:
            icon = "✅"
        txt = f"{icon} {message}"
        if self.type == "card":
            msg = TeamsCard(
                text=txt,
                summary=f"Task Summary: {task_name}",
                title=f"Task {task_name} uid:{task_id}",
            )
            if hasattr(self, "with_stats"):
                # iterate over task stats:
                for stat, value in stats["steps"].items():
                    section = msg.addSection(activityTitle=stat, text=stat)
                    section.addFacts(
                        facts=[{"name": stat, "value": json_encoder(value)}]
                    )
            if hasattr(self, 'with_codereview'):
                # Add Code Review
                section = msg.addSection(activityTitle="Code Review", text="Code Review")
                section.addFacts(
                    facts=[{"name": "Code Review", "value": json_encoder(stats['Review'])}]
                )
        async with tm as conn:
            result = await conn.send(recipient=channel, message=msg)
            return result

from collections.abc import Callable
import asyncio
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
import pandas as pd
from msgraph.generated.models.chat_message import (
    ChatMessage
)
from msgraph.generated.models.chat import Chat
from .flow import FlowComponent
from ..interfaces.AzureGraph import AzureGraph
from ..exceptions import ComponentError, DataNotFound, ConfigError


class MSTeamsMessages(AzureGraph, FlowComponent):
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.channel_id: str = kwargs.pop('channel_id', None)
        self.team_id: str = kwargs.pop('team_id', None)
        self.chat_id: str = kwargs.pop('chat_id', None)
        self.chat_name: str = kwargs.pop('chat_name', None)
        self.program_name: str = kwargs.get('program_name', None)
        self._weeks: int = kwargs.get('weeks', 1)
        self.start_time: str = kwargs.pop('start_time', None)
        self.end_time: str = kwargs.pop('end_time', None)
        self.as_dataframe: bool = kwargs.get('as_dataframe', False)
        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )
        if self.program_name is None:
            self.program_name = self._program

    async def start(self, **kwargs):
        await super().start(**kwargs)
        self.processing_credentials()
        if not self.team_id:
            raise ConfigError(
                "Must Provide a *team_id* Attribute."
            )
        # Processing Channel and Team:
        self.team_id = self.mask_replacement(self.team_id)
        self.channel_id = self.mask_replacement(self.channel_id)
        self.chat_id = self.mask_replacement(self.chat_id)
        # Processing the start time and end time:
        if self.start_time:
            self.start_time = self.mask_replacement(self.start_time)
            if isinstance(self.start_time, str):
                # convert to datetime with Z
                self.start_time = datetime.strptime(
                    self.start_time, "%Y-%m-%dT%H:%M:%S.%fZ"
                )
        else:
            # One Week Ago.
            self.start_time = (datetime.utcnow() - timedelta(weeks=self._weeks)).isoformat() + 'Z'
        if self.end_time:
            self.end_time = self.mask_replacement(self.end_time)
            if isinstance(self.end_time, str):
                # convert to datetime with Z
                self.end_time = datetime.strptime(
                    self.end_time, "%Y-%m-%dT%H:%M:%S.%fZ"
                )
        else:
            self.end_time = datetime.utcnow().isoformat() + 'Z'  # Current time
        return True

    def _process_messages(self, messages: list) -> list:
        msgs = []
        default_datetime = datetime(1970, 1, 1, tzinfo=timezone.utc)
        for message in messages:
            if isinstance(message, ChatMessage):
                # extracting info from message:
                user = {}
                if message.from_:
                    usr = message.from_.user
                    user = {
                        "sender_id": usr.id,
                        "sender_name": usr.display_name
                    }
                content = str(message.body.content)
                soup = BeautifulSoup(content, 'html.parser')
                stripped_content = soup.get_text()
                msg = {
                    "message_id": message.id,
                    **user,
                    "chat_id": message.chat_id,
                    "created_date": message.created_date_time,
                    "policy_violation": message.policy_violation,
                    "content": content,
                    "text": stripped_content,
                }
                msgs.append(msg)
            elif isinstance(message, Chat):
                print('Chat > ', message, message.id)
                # get the additional data from Chat:
                data = message.additional_data
                chat_id = message.additional_data.get('chatId')
                # extracting user from message Chat
                user = {}
                if data.get('from'):
                    usr = data.get('from')['user']
                    user = {
                        "sender_id": str(usr.get('id', None)),
                        "sender_name": usr.get('displayName', None)
                    }
                content = None
                if message.additional_data and message.additional_data.get('body') and message.additional_data['body'].get('content'):
                    content = str(message.additional_data['body'].get('content', None))
                if content:
                    soup = BeautifulSoup(content, 'html.parser')
                    stripped_content = soup.get_text()
                else:
                    stripped_content = ''
                created_time = default_datetime
                if message.additional_data and message.additional_data.get('createdDateTime'):
                    created_time = message.additional_data['createdDateTime']
                msg = {
                    "message_id": message.id,
                    **user,
                    "chat_id": chat_id,
                    "created_date": created_time,
                    "policy_violation": '',
                    "content": content,
                    "text": stripped_content,
                }
                msgs.append(msg)
            elif isinstance(message, dict):
                chat_id = message.get('id', None)
                sender_name = message.get('from', {}).get('user', {}).get('displayName', 'Unknown')
                user = {
                    "sender_id": message.get('from', {}).get('user', {}).get('id', 'Unknown'),
                    "sender_name": sender_name
                }
                content = str(message.get('body', {}).get('content', ''))
                created_time = message.get('createdDateTime', default_datetime)
                print(f"[{created_time}] {sender_name}: {content}")
                content = str(message.body.content)
                soup = BeautifulSoup(content, 'html.parser')
                stripped_content = soup.get_text()
                msg = {
                    "message_id": message.get('id', None),
                    **user,
                    "chat_id": chat_id,
                    "sender_name": sender_name,
                    "content": content,
                    "text": stripped_content,
                    "created_date": created_time if created_time else default_datetime,
                    "policy_violation": '',
                }
                msgs.append(msg)
            else:
                self._logger.error(
                    f'Unable to parse Message: {message}: {type(message)}'
                )
                continue
        return msgs

    async def run(self):
        async with self.open() as client:
            try:
                if self.chat_name is not None:
                    # Find chat id by name:
                    chat = await client.find_chat_by_name(self.chat_name)
                    messages = await client.get_chat_messages(
                        chat_id=chat.id,
                        start_time=self.start_time,
                        end_time=self.end_time
                    )
                elif self.chat_id is not None:
                    # Using the chat Id for extracting chat messages:
                    messages = await client.get_chat_messages(
                        chat_id=self.chat_id,
                        start_time=self.start_time,
                        end_time=self.end_time
                    )
                elif self.channel_id is not None:
                    messages = await client.get_msteams_channel_messages(
                        team_id=self.team_id,
                        channel_id=self.channel_id,
                        start_time=self.start_time,
                        end_time=self.end_time
                    )
                    if not messages:
                        raise DataNotFound(
                            f"Found no messages on MS Team {self.team_id}:{self.channel_id}"
                        )
                # Processing the messages:
                msgs = self._process_messages(messages)
                df = pd.DataFrame(msgs)
                if self.as_dataframe is True:
                    # Adding program, channel name to dataframe:
                    df['program'] = self.program_name
                    if self.chat_name:
                        df['chat_name'] = self.chat_name
                    if self.channel_id:
                        df['channel_id'] = self.channel_id
                    # Convert to Created Date
                    df['created_date'] = df['created_date'].replace(pd.NaT, None)
                    # return only the dataframe:
                    self._result = df
                    return self._result
                self._result = {
                    "data": df,
                    "messages": msgs,
                    "raw_messages": messages
                }
                self.add_metric('NUM_MESSAGES', len(messages))
                return self._result
            except Exception as exc:
                self._logger.error(
                    f"Error getting Teams Channel Messages: {exc}"
                )
                raise ComponentError(
                    f"Error getting Teams Channel Messages: {exc}"
                )

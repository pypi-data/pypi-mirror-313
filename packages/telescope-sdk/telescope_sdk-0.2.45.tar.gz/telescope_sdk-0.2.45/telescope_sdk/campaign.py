from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field

from telescope_sdk.common import UserFacingDataType


class ICPAssistantChatMessageType(str, Enum):
    MESSAGE = "MESSAGE"
    ERROR = "ERROR"


class ICPAssistantChatMessageSender(str, Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"


class ICPAssistantChatMessage(BaseModel):
    type: ICPAssistantChatMessageType
    sender: ICPAssistantChatMessageSender
    text: str
    sent_at: str


class OutreachStatus(str, Enum):
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    ERROR = 'DISABLED'


class Campaign(UserFacingDataType):
    name: str
    outreach_status: OutreachStatus
    sequence_id: Optional[str] = Field(default=None)
    active_icp_id: Optional[str] = Field(default=None)
    outreach_enabled: Optional[bool] = Field(default=None)
    icp_assistant_chat_history: Optional[List[ICPAssistantChatMessage]] = Field(default=None)
    icp_assistant_chat_enabled: bool = Field(default=False)

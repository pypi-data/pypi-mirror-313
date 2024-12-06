from enum import Enum
from typing import Optional

from pydantic import Field

from telescope_sdk.common import UserFacingDataType


class ProspectInteractionEventType(str, Enum):
    PROSPECT_REPLIED_POSITIVE = 'PROSPECT_REPLIED_POSITIVE'
    PROSPECT_REPLIED_NEGATIVE = 'PROSPECT_REPLIED_NEGATIVE'
    PROSPECT_REPLIED_UNKNOWN_SENTIMENT = 'PROSPECT_REPLIED_UNKNOWN_SENTIMENT'
    PROSPECT_BOUNCE_NOTIFICATION = 'PROSPECT_BOUNCE_NOTIFICATION'
    PROSPECT_OOO_NOTIFICATION = 'PROSPECT_OOO_NOTIFICATION'


class ProspectInteractionEvent(UserFacingDataType):
    campaign_id: str
    prospect_id: str
    type: ProspectInteractionEventType
    thread_id: Optional[str] = Field(default=None)
    sent_at: Optional[str] = Field(default=None)
    subject: Optional[str] = Field(default=None)
    text_reply: Optional[str] = Field(default=None)
    is_auto_reply: Optional[bool] = Field(default=None)

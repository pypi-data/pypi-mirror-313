from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field

from telescope_sdk.common import UserFacingDataType


class SequenceStepType(str, Enum):
    EMAIL = 'EMAIL'


class SequenceStep(BaseModel):
    id: str
    type: SequenceStepType
    seconds_from_previous_step: int
    subject: str
    body: str
    signature: Optional[str] = Field(default=None)


class Sequence(UserFacingDataType):
    steps: List[SequenceStep]

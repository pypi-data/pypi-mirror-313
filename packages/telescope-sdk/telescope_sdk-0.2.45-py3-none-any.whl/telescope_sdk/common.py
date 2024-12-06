from enum import Enum
from typing import Optional, Dict
from pydantic import BaseModel, Field, ConfigDict

from telescope_sdk.utils import convert_country_name_to_iso_code


class Source(str, Enum):
    PDL = "PDL"
    REVENUEBASE = "REVENUEBASE"
    USER_UPLOAD = "USER_UPLOAD"
    MIXRANK = "MIXRANK"
    UNKNOWN = "UNKNOWN"


class TelescopeBaseType(BaseModel):
    """
    Base class for all top-level Telescope entities.
    """
    id: str
    created_at: str
    updated_at: str

    model_config = ConfigDict(use_enum_values=True)

    def to_dynamodb_format(self) -> Dict[str, any]:
        return self.model_dump(exclude_none=True)


class IngestedDataType(TelescopeBaseType):
    """
    Base data type for entities which are ingested from external sources (e.g. PDL, RevenueBase, etc.)
    """
    source: Source
    version: Optional[int] = None


class UserFacingDataType(TelescopeBaseType):
    """
    Base data type for entities which are created by or for users and which have a defined owner.
    """
    owner_id: str


class Location(BaseModel):
    line_1: Optional[str] = Field(default=None)
    line_2: Optional[str] = Field(default=None)
    postal_code: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    county: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)

    @classmethod
    def from_pdl(cls, pdl_input: Dict[str, any]) -> Optional['Location']:
        country = pdl_input.get('country')
        return cls(
            line_1=pdl_input.get('street_address'),
            line_2=pdl_input.get('address_line_2'),
            country=convert_country_name_to_iso_code(country) if country else None,
            state=pdl_input.get('region'),
            postal_code=pdl_input.get('postal_code'),
            city=pdl_input.get('locality')
        )

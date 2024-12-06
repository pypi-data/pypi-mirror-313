from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class FilterableLocationType(str, Enum):
    COUNTRY_GROUP = "COUNTRY_GROUP"
    GROUP = "GROUP"
    COUNTRY = "COUNTRY"
    CITY = "CITY"
    ADMIN_DIVISION_1 = "ADMIN_DIVISION_1"
    ADMIN_DIVISION_2 = "ADMIN_DIVISION_2"


class FilterableLocation(BaseModel):
    id: str
    name: str
    type: FilterableLocationType
    standard_location_ids: List[str]
    admin_division_1: Optional[str] = None
    admin_division_2: Optional[str] = None
    country: Optional[str] = None
    population: Optional[int] = None

from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from telescope_sdk.common import TelescopeBaseType
from telescope_sdk.locations import FilterableLocation
from telescope_sdk.company import CompanySizeRange, FoundedYearRange, RevenueRange


class ExampleCompany(BaseModel):
    id: str
    name: str


class TypedCompanyTagType(str, Enum):
    INDUSTRY_TAGS = "industry_tags"
    TARGET_CUSTOMER_INDUSTRY_TAGS = "target_customer_industry_tags"
    TECHNOLOGY_TAGS = "technology_tags"
    COMPANY_TYPE_TAGS = "company_type_tags"
    PRODUCT_SERVICES_TAGS = "products_services_tags"
    BUSINESS_MODEL = "business_model"
    STAGE = "stage"
    OTHER = "other"
    BUSINESS_NEED = "business_need"


class TypedCompanyTag(BaseModel):
    keyword: str = Field(description="The keyword, e.g. `b2b`, `saas`, `startup`, `rna-sequencing`")
    type: TypedCompanyTagType = Field(
        description=f"Type of the keyword. Allowed values: [{', '.join([f'{e.value}' for e in TypedCompanyTagType])}]. "
        "Can only be one of those allowed types."
    )


class SpecialCriterionSupportStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    PARTLY_SUPPORTED = "PARTLY_SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"


class SpecialCriterionTargetEntity(str, Enum):
    PERSON = "PERSON"
    COMPANY = "COMPANY"


class SpecialCriterionMappedDataPoint(BaseModel):
    data_point: str
    arguments_json: Optional[str] = Field(default=None)


class SpecialCriterion(BaseModel):
    enabled: Optional[bool] = Field(default=True)
    original_user_input: Optional[str] = Field(default=None)
    text: str
    target_entity: SpecialCriterionTargetEntity
    support_status: SpecialCriterionSupportStatus
    unsupported_reason: Optional[str] = Field(default=None)
    mapped_data_points: List[SpecialCriterionMappedDataPoint] = Field(default_factory=list)
    min_matching_score: Optional[float] = Field(default=0.0)
    accept_unknown: Optional[bool] = Field(default=True)


class ExtractedCompanyProfile(BaseModel):
    company_type_description: str
    structured_keywords: List[TypedCompanyTag]


class IdealCustomerProfile(TelescopeBaseType):
    name: Optional[str] = Field(default=None)
    campaign_id: str
    example_companies: List[ExampleCompany]
    fictive_example_company_descriptions: List[str] = Field(default_factory=list)
    full_company_descriptive_info: Optional[str] = Field(default=None)
    summary_company_descriptive_info: Optional[str] = Field(default=None)
    clean_company_descriptive_info: Optional[str] = Field(default=None)
    full_contact_descriptive_info: Optional[str] = Field(default=None)
    summary_contact_descriptive_info: Optional[str] = Field(default=None)
    job_titles: List[str] = Field(default_factory=[])
    excluded_job_titles: Optional[List[str]] = Field(default=None)
    keywords: Optional[List[str]] = Field(default=None)
    company_search_typed_keywords: Optional[List[TypedCompanyTag]] = Field(default=None)
    extracted_company_profiles: Optional[List[ExtractedCompanyProfile]] = Field(default=None)
    negative_keywords: Optional[List[str]] = Field(default=None)
    hq_location_filters: Optional[List[FilterableLocation]] = Field(default=None)
    hq_location_excludes: Optional[List[FilterableLocation]] = Field(default=None)
    employee_location_filters: Optional[List[FilterableLocation]] = Field(default=None)
    employee_location_excludes: Optional[List[FilterableLocation]] = Field(default=None)
    industries: Optional[List[str]] = Field(default=None)
    company_size_range: Optional[CompanySizeRange] = Field(default=None)
    company_types: Optional[List[str]] = Field(default=None)
    founded_year_range: Optional[FoundedYearRange] = Field(default=None)
    company_types_description: List[str] = Field(default_factory=list)
    special_criteria: List[SpecialCriterion] = Field(default_factory=list)
    company_revenue_range: Optional[RevenueRange] = Field(default=None)
    require_email: Optional[bool] = Field(default=None)
    only_show_verified_emails: Optional[bool] = Field(default=None)
    hide_companies_in_another_campaign: Optional[bool] = Field(default=None)
    hide_leads_in_another_campaign: Optional[bool] = Field(default=None)
    deleted_at: Optional[str] = Field(default=None)
    min_company_matching_score: Optional[float] = Field(default=None)

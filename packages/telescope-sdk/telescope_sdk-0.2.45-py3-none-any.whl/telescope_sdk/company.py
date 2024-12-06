from typing import Optional, Dict, List
from pydantic import BaseModel, Field

from telescope_sdk.common import IngestedDataType, Location, Source
from telescope_sdk.company_types import CompanyType, PDLCompanyType
from telescope_sdk.utils import convert_pdl_company_type_to_company_type, get_current_datetime_aws_format


class Tag(BaseModel):
    tag_classification: str
    tag: str


class CompanyEnrichment(BaseModel):
    company_summary: Optional[str] = Field(default=None)
    tags: Optional[List[Tag]] = Field(default=None)


class CompanySizeRange(BaseModel):
    lower: Optional[int] = Field(default=None)
    upper: Optional[int] = Field(default=None)


class RevenueRange(BaseModel):
    lower: Optional[int] = Field(default=None)
    upper: Optional[int] = Field(default=None)


class FoundedYearRange(BaseModel):
    lower: Optional[int] = Field(default=None)
    upper: Optional[int] = Field(default=None)


class SocialNetworkLinks(BaseModel):
    LinkedIn: Optional[List[str]] = Field(default=None)
    Facebook: Optional[List[str]] = Field(default=None)
    Instagram: Optional[List[str]] = Field(default=None)
    Twitter: Optional[List[str]] = Field(default=None)
    X: Optional[List[str]] = Field(default=None)
    Youtube: Optional[List[str]] = Field(default=None)


class PageSummary(BaseModel):
    url: Optional[str] = Field(default=None)
    summary: Optional[str] = Field(default=None)


class CrunchbaseFunding(BaseModel):
    crunchbase_company_name: Optional[str] = Field(default=None)
    crunchbase_company_url: Optional[str] = Field(default=None)
    funding_round_count: Optional[int] = Field(default=None)
    funding_url: Optional[str] = Field(default=None)
    investor_count: Optional[int] = Field(default=None)
    investor_names: Optional[List[str]] = Field(default=None)
    organization_investors_urls: Optional[List[str]] = Field(default=None)
    people_investors_urls: Optional[List[str]] = Field(default=None)
    round_amount_: Optional[int] = Field(default=None)
    round_currency: Optional[str] = Field(default=None)
    round_date: Optional[str] = Field(default=None)
    round_name: Optional[str] = Field(default=None)


class Company(IngestedDataType):
    name: str
    linkedin_internal_id: str
    linkedin_url: str
    pdl_id: Optional[str] = Field(default=None)  # deprecated
    universal_name_id: Optional[str] = Field(default=None)  # deprecated
    tagline: Optional[str] = Field(default=None)  # might be translated # deprecated
    original_tagline: Optional[str] = Field(default=None)  # deprecated
    description: Optional[str] = Field(default=None)  # might be translated
    original_description: Optional[str] = Field(default=None)
    company_description_language_iso_code: Optional[str] = Field(default=None)
    domain_name: Optional[str] = Field(default=None)
    website: Optional[str] = Field(default=None)
    landing_page_content: Optional[str] = Field(default=None)  # deprecated
    logo_url: Optional[str] = Field(default=None)
    industry: Optional[str] = Field(default=None)
    categories: Optional[List[str]] = Field(default=None)  # deprecated
    specialties: Optional[List[str]] = Field(default=None)  # deprecated
    company_type: Optional[str] = Field(default=None)
    company_size_range: Optional[CompanySizeRange] = Field(default=None)
    est_revenue_range: Optional[str] = Field(default=None)
    est_revenue_range_number: Optional[RevenueRange] = Field(default=None)
    est_revenue_source: Optional[str] = Field(default=None)
    company_size_on_linkedin: Optional[int] = Field(default=None)
    founded_year: Optional[int] = Field(default=None)
    hq: Optional[Location] = Field(default=None)
    hq_standard_location_ids: Optional[List[str]] = Field(default=None)
    locations: Optional[List[Location]] = Field(default=None)
    locations_standard_locations_ids: Optional[List[List[str]]] = Field(default=None)
    last_enriched_at: Optional[str] = Field(default=None)
    enrichment: Optional[CompanyEnrichment] = Field(default=None)
    # new (mixrank v3)
    linkedin_follower_count: Optional[int] = Field(default=None)
    stock_exchange_code: Optional[str] = Field(default=None)
    ticker: Optional[str] = Field(default=None)
    is_valid_company_website: Optional[bool] = Field(default=None)
    is_website_link_valid: Optional[bool] = Field(default=None)
    matching_landing_page_summary: Optional[bool] = Field(default=None)
    company_landing_page_summary: Optional[str] = Field(default=None)
    company_summary: Optional[str] = Field(default=None)
    crunchbase_funding: Optional[list[CrunchbaseFunding]] = Field(default=None)
    social_network_links: Optional[SocialNetworkLinks] = Field(default=None)
    business_model: Optional[list[str]] = Field(default=None)
    products_services_tags: Optional[list[str]] = Field(default=None)
    technology_tags: Optional[list[str]] = Field(default=None)
    industry_tags: Optional[list[str]] = Field(default=None)
    target_customer_industry_tags: Optional[list[str]] = Field(default=None)
    company_type_tags: Optional[list[str]] = Field(default=None)
    stage_tags: Optional[list[str]] = Field(default=None)
    is_software_as_a_service: Optional[bool] = Field(default=None)
    pricing_pages_summaries: Optional[list[PageSummary]] = Field(default=None)
    pricing_summary: Optional[str] = Field(default=None)
    product_services_pages_summaries: Optional[list[PageSummary]] = Field(default=None)
    product_services_summary: Optional[str] = Field(default=None)

    @classmethod
    def from_pdl(cls, pdl_input: Dict[str, any]) -> Optional['Company']:
        name = pdl_input.get('name')
        linkedin_internal_id = pdl_input.get('linkedin_id')
        if not name or not linkedin_internal_id:
            return None

        pdl_domain_name = pdl_input.get('website')
        pdl_company_type = pdl_input.get('type')
        pdl_company_size = pdl_input.get('size')
        pdl_company_size_range_split = pdl_company_size.split('-') if pdl_company_size else None
        pdl_location = pdl_input.get('location')

        return cls(
            id=linkedin_internal_id,
            source=Source.PDL,
            version=0,
            created_at=get_current_datetime_aws_format(),
            updated_at=get_current_datetime_aws_format(),
            name=name.capitalize(),
            linkedin_internal_id=linkedin_internal_id,
            pdl_id=pdl_input.get('id'),
            universal_name_id=pdl_input.get('id'),
            tagline=pdl_input.get('headline'),
            description=pdl_input.get('summary'),
            domain_name=pdl_domain_name,
            website=f'https://{pdl_domain_name}' if pdl_domain_name else None,
            linkedin_url=pdl_input.get('linkedin_url') or f'https://www.linkedin.com/company/{linkedin_internal_id}',
            industry=pdl_input.get('industry'),  # should this be canonical?
            categories=pdl_input.get('tags'),
            company_type=CompanyType(convert_pdl_company_type_to_company_type(PDLCompanyType[pdl_company_type]))
            if pdl_company_type else None,
            company_size_range=CompanySizeRange(
                lower=int(pdl_company_size_range_split[0]),
                upper=int(pdl_company_size_range_split[1])
            ) if pdl_company_size_range_split and len(pdl_company_size_range_split) == 2 else None,
            est_revenue_range=pdl_input.get('inferred_revenue'),
            company_size_on_linkedin=pdl_input.get('employee_count'),
            founded_year=pdl_input.get('founded'),
            hq=Location.from_pdl(pdl_location) if pdl_location else None,
            locations=[Location.from_pdl(pdl_location)] if pdl_location else None,
            last_enriched_at=get_current_datetime_aws_format(),
            telescope_icp=None,
            uprank=None,
            downrank=None
        )

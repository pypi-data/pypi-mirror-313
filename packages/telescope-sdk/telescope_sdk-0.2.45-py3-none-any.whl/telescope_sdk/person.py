from decimal import Decimal
from typing import Optional, Dict, List, Union
from hashlib import md5
from enum import Enum

from pydantic import BaseModel, Field

from telescope_sdk.common import IngestedDataType, Location, Source
from telescope_sdk.utils import (
    convert_country_name_to_iso_code,
    convert_date_string_to_datetime_string,
    get_current_datetime_aws_format,
    normalize_url
)


class CanonicalJobTitle(BaseModel):
    title: str
    confidence: Decimal


class ExperienceCompany(BaseModel):
    name: Optional[str] = Field(default=None)
    linkedin_internal_id: Optional[str] = Field(default=None)
    linkedin_url: Optional[str] = Field(default=None)
    location: Optional[Location] = Field(default=None)
    website: Optional[str] = Field(default=None)

    @classmethod
    def from_pdl(cls, pdl_input: Dict[str, any]) -> Optional['ExperienceCompany']:
        location = pdl_input.get('location')
        return cls(
            name=pdl_input.get('name'),
            linkedin_internal_id=pdl_input.get('linkedin_id'),
            linkedin_url=pdl_input.get('linkedin_url'),
            website=pdl_input.get('website'),
            location=Location.from_pdl(location) if location else None
        )


class Experience(BaseModel):
    company: Optional[ExperienceCompany] = Field(default=None)
    start_datetime: Optional[str] = Field(default=None)
    end_datetime: Optional[str] = Field(default=None)
    is_primary: Optional[bool] = Field(default=None)
    job_title: Optional[str] = Field(default=None)
    job_title_levels: Optional[List[str]] = Field(default=None)

    @classmethod
    def from_pdl(cls, pdl_input: Dict[str, any]) -> Optional['Experience']:
        title = pdl_input.get('title', {}) or {}
        company = pdl_input.get('company')
        start_date = pdl_input.get('start_date')
        end_date = pdl_input.get('end_date')
        return cls(
            company=ExperienceCompany.from_pdl(company) if company else None,
            start_datetime=convert_date_string_to_datetime_string(start_date) if start_date else None,
            end_datetime=convert_date_string_to_datetime_string(end_date) if end_date else None,
            is_primary=pdl_input.get('is_primary'),
            job_title=title.get('name'),
            job_title_levels=title.get('levels')
        )


class Degree(BaseModel):
    levels: Optional[List[str]] = Field(default=None)
    majors: Optional[List[str]] = Field(default=None)


class Education(BaseModel):
    degree: Optional[Union[Degree, str]] = Field(default=None)
    institution_logo_url: Optional[str] = Field(default=None)
    institution_name: Optional[str] = Field(default=None)
    institution_linkedin_url: Optional[str] = Field(default=None)
    start_datetime: Optional[str] = Field(default=None)
    end_datetime: Optional[str] = Field(default=None)

    @classmethod
    def from_pdl(cls, pdl_input: Dict[str, any]) -> Optional['Education']:
        school = pdl_input.get('school', {}) or {}
        start_date = pdl_input.get('start_date')
        end_date = pdl_input.get('end_date')
        return cls(
            degree=Degree(
                levels=pdl_input.get('degrees'),
                majors=pdl_input.get('majors')
            ),
            institution_logo_url=None,
            institution_name=school.get('name'),
            institution_linkedin_url=school.get('linkedin_url'),
            start_datetime=convert_date_string_to_datetime_string(start_date) if start_date else None,
            end_datetime=convert_date_string_to_datetime_string(end_date) if end_date else None
        )


class Language(BaseModel):
    name: Optional[str] = Field(default=None)
    proficiency: Optional[int] = Field(default=None)


class EmailStatus(str, Enum):
    valid = 'valid'
    invalid = 'invalid'
    disposable = 'disposable'
    catchall = 'catchall'
    unknown = 'unknown'


class Person(IngestedDataType):
    first_name: str
    last_name: str
    middle_name: Optional[str] = Field(default=None)
    pdl_id: Optional[str] = Field(default=None)
    headline: Optional[str] = Field(default=None)
    about: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    personal_emails: Optional[List[str]] = Field(default=None)
    phone_numbers: Optional[List[str]] = Field(default=None)
    linkedin_url: Optional[str] = Field(default=None)
    linkedin_internal_id: Optional[str] = Field(default=None)
    industry: Optional[str] = Field(default=None)
    company_id: Optional[str] = Field(default=None)
    job_title: Optional[str] = Field(default=None)
    job_title_seniority_tags: Optional[List[str]] = Field(default=None)
    job_title_department_tags: Optional[List[str]] = Field(default=None)
    job_role_description: Optional[str] = Field(default=None)
    job_start_date: Optional[str] = Field(default=None)
    job_last_updated: Optional[str] = Field(default=None)
    interests: Optional[List[str]] = Field(default=None)
    skills: Optional[List[str]] = Field(default=None)
    experience: Optional[List[Experience]] = Field(default=None)
    education: Optional[List[Education]] = Field(default=None)
    languages: Optional[List[Language]] = Field(default=None)
    location: Optional[Location] = Field(default=None)
    standard_location_ids: Optional[List[str]] = Field(default=None)
    tags: Optional[List[str]] = Field(default=None)
    uploaded_by_user_id: Optional[str] = Field(default=None)
    last_enriched_at: Optional[str] = Field(default=None)
    email_last_checked_at: Optional[str] = Field(default=None)
    email_status: Optional[EmailStatus] = Field(default=None)
    email_quality_score: Optional[float] = Field(default=None)
    connection_count: Optional[int] = Field(default=None)
    follower_count: Optional[int] = Field(default=None)
    profile_pic: Optional[str] = Field(default=None)

    @classmethod
    def from_pdl(cls, pdl_input: Dict[str, any]) -> Optional['Person']:
        first_name = pdl_input.get('first_name')
        last_name = pdl_input.get('last_name')
        pdl_id = pdl_input.get('id')
        if not first_name or not last_name or not pdl_id:
            return None

        first_name = first_name.capitalize()
        last_name = last_name.capitalize()

        country = pdl_input.get('location_country')
        job_start_date = pdl_input.get('job_start_date')
        job_last_updated = pdl_input.get('job_last_updated')
        linkedin_url = normalize_url(pdl_input.get('linkedin_url'))

        return cls(
            id=md5(linkedin_url.encode()).hexdigest(),
            source=Source.PDL,
            version=0,
            created_at=get_current_datetime_aws_format(),
            updated_at=get_current_datetime_aws_format(),
            first_name=first_name,
            last_name=last_name,
            middle_name=pdl_input.get('middle_name'),
            pdl_id=pdl_id,
            headline=None,
            about=pdl_input.get('summary'),
            email=pdl_input.get('work_email'),
            personal_emails=pdl_input.get('personal_emails'),
            phone_numbers=pdl_input.get('phone_numbers'),
            linkedin_url=linkedin_url,
            linkedin_internal_id=pdl_input.get('linkedin_id'),
            industry=pdl_input.get('industry'),
            company_id=pdl_input.get('job_company_linkedin_id'),
            job_title=pdl_input.get('job_title'),
            canonical_job_titles=None,
            job_title_levels=pdl_input.get('job_title_levels'),
            job_role_description=pdl_input.get('job_summary'),
            job_start_date=convert_date_string_to_datetime_string(job_start_date) if job_start_date else None,
            company_name=pdl_input.get('job_company_name'),
            company_linkedin_url=pdl_input.get('job_company_linkedin_url'),
            company_industry=pdl_input.get('job_company_industry'),
            company_year_founded=pdl_input.get('job_company_founded'),
            job_last_updated=convert_date_string_to_datetime_string(job_last_updated) if job_last_updated else None,
            interests=pdl_input.get('interests'),
            skills=pdl_input.get('skills'),
            experience=[Experience.from_pdl(experience) for experience in pdl_input.get('experience', [])],
            education=[Education.from_pdl(education) for education in pdl_input.get('education', [])],
            languages=[Language.model_validate(language) for language in pdl_input.get('languages', [])],
            location=Location(
                line_1=pdl_input.get('location_street_address'),
                line_2=pdl_input.get('location_address_line_2'),
                country=convert_country_name_to_iso_code(country) if country else None,
                state=pdl_input.get('location_region'),
                postal_code=pdl_input.get('location_postal_code'),
                city=pdl_input.get('location_locality')
            ),
            tags=pdl_input.get('tags'),
            uploaded_by_user_id=None,
            last_enriched_at=get_current_datetime_aws_format(),
            telescope_icp=None,
            uprank=None,
            downrank=None
        )

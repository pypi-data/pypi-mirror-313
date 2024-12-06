import logging
from datetime import datetime
from typing import Optional

from pycountry import countries

from telescope_sdk.company_types import CompanyType, PDLCompanyType, company_to_pdl_company_map

logger = logging.getLogger(__name__)


def convert_datetime_to_aws_format(datetime_obj: datetime) -> str:
    """
    Converts a UTC datetime object to AWS format (YYYY-MM-DDTHH:MM:SS.SSSZ)
    :param datetime_obj: Input datetime object
    :return: AWS Formatted datetime string.
    """
    return f'{datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4]}Z'


def get_current_datetime_aws_format() -> str:
    """
    Returns the current UTC datetime in AWS format (YYYY-MM-DDTHH:MM:SS.SSSZ)
    :return: AWS Formatted datetime string.
    """
    return convert_datetime_to_aws_format(datetime.utcnow())


def convert_country_name_to_iso_code(country_name: str) -> Optional[str]:
    """
    Converts a country name string to a 2-letter ISO 3166 Alpha-2 country code. Returns None if the country name is
    not recognized
    :param country_name: input country name. E.g. United States
    :return: 2-letter country code. E.g. US
    """
    # special handling for UK
    if country_name == 'UK':
        return 'GB'

    try:
        possible_country_matches = countries.search_fuzzy(country_name)
        if len(possible_country_matches) > 0:
            return possible_country_matches[0].alpha_2
    except LookupError:
        return None


def convert_country_iso_code_to_name(country_code: str) -> Optional[str]:
    """
    Converts a 2-letter ISO 3166 Alpha-2 country code to country name. Returns None if the country code is not
    recognized
    :param country_code: 2-letter country code. E.g. US
    :return: country name. E.g. United States
    """
    try:
        optional_country_match = countries.get(alpha_2=country_code)
        if optional_country_match is not None:
            return optional_country_match.name
    except LookupError:
        return None


def convert_date_string_to_datetime_string(date_string: str) -> Optional[str]:
    """
    Converts a date string to a datetime string in AWS Format (YYYY-MM-DDTHH:MM:SS.SSSZ). Date string can be in the
    format YYYY-MM-DD, YYYY-MM, or YYYY.
    :param date_string: E.g. 2021-01-01, 2021-01, or 2021
    :return: AWS Formatted datetime string. E.g. 2021-01-01T00:00:00.000Z
    """
    length = len(date_string)
    try:
        if length == 10:
            return convert_datetime_to_aws_format(datetime.strptime(date_string, "%Y-%m-%d"))
        if length == 7:
            return convert_datetime_to_aws_format(datetime.strptime(date_string, "%Y-%m"))
        if length == 4:
            return convert_datetime_to_aws_format(datetime.strptime(date_string, "%Y"))
        logger.warning(f'Invalid date string format: {date_string}')
    except ValueError as e:
        logger.warning(f'Unable to convert date string {date_string} to datetime string. Error: {e}')
        return None


def convert_company_type_to_pdl_company_type(key: CompanyType) -> Optional[PDLCompanyType]:
    """
    Converts a Company Type key to PDLs Company Type format.
    :return: PDL Company Type.
    """
    return company_to_pdl_company_map.get(key, None)


def convert_pdl_company_type_to_company_type(key: PDLCompanyType) -> Optional[CompanyType]:
    """
    Converts a PDL Company Type key to Company Type format. Only returns the first occurrence.
    :return: Company Type.
    """
    return next((k for k, v in company_to_pdl_company_map.items() if v == key), None)


def normalize_url(url: str) -> str:
    """
    PDL provides url in the form of linkedin.com/company/company-name
    Normalize url string to add https://www. string to match url from Revenuebase
    """

    if url:
        url = url.replace(" ", "").strip("/")
        if not url.startswith("https://www."):
            url = ("https://www." + url)
        else:
            return url
    else:
        return ""
    return url

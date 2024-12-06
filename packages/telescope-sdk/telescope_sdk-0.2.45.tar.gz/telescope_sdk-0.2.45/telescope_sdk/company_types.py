from enum import Enum


class CompanyType(str, Enum):
    PRIVATELY_HELD = "PRIVATELY_HELD"
    SOLE_PROPRIETORSHIP = "SOLE_PROPRIETORSHIP"
    PUBLIC_COMPANY = "PUBLIC_COMPANY"
    GOVERNMENT_AGENCY = "GOVERNMENT_AGENCY"
    PARTNERSHIP = "PARTNERSHIP"
    SELF_EMPLOYED = "SELF-EMPLOYED"
    SELFEMPLOYED = "SELFEMPLOYED"
    NONPROFIT = "NONPROFIT"
    EDUCATIONAL_INSTITUTION = "EDUCATIONAL_INSTITUTION"


class PDLCompanyType(str, Enum):
    educational = "educational"
    government = "government"
    nonprofit = "nonprofit"
    private = "private"
    public = "public"


company_to_pdl_company_map = {
    CompanyType.PRIVATELY_HELD: PDLCompanyType.private,
    CompanyType.SOLE_PROPRIETORSHIP: PDLCompanyType.private,
    CompanyType.PUBLIC_COMPANY: PDLCompanyType.public,
    CompanyType.GOVERNMENT_AGENCY: PDLCompanyType.government,
    CompanyType.PARTNERSHIP: PDLCompanyType.private,
    CompanyType.SELF_EMPLOYED: PDLCompanyType.private,
    CompanyType.NONPROFIT: PDLCompanyType.nonprofit,
    CompanyType.EDUCATIONAL_INSTITUTION: PDLCompanyType.educational
}

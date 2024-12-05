from dataclasses import dataclass, field
from datetime import datetime

from inoopa_utils.typesense_helpers import datetime_to_unix_timestamp


@dataclass(slots=True)
class NaceCodeTypesense:
    country: str
    level: int
    code: str
    section_label: str
    section_code: str
    label_en: str
    label_en_extended: str
    label_en_embedding: list[float] | None = None
    label_en_extended_embedding: list[float] | None = None
    label_fr: str | None = None
    label_fr_extended: str | None = None
    label_fr_extended_embedding: list[float] | None = None
    label_fr_embedding: list[float] | None = None
    label_nl: str | None = None
    label_nl_extended: str | None = None
    label_nl_extended_embedding: list[float] | None = None
    label_nl_embedding: list[float] | None = None


@dataclass
class EntityName:
    name: str | None = None
    name_fr: str | None = None
    name_nl: str | None = None
    name_de: str | None = None
    website: str | None = None


@dataclass(init=False)
class CompanyNameTypesense(EntityName):
    _id: str
    establishments: list[EntityName] | None = None

    # We have to manually define the __init__ method here because of the way dataclasses work with inheritance
    def __init__(self, _id: str, establishments: list[EntityName] | None = None, **kwargs):
        super().__init__(**kwargs)
        self._id = _id
        self.establishments = establishments


@dataclass(slots=True)
class WebsiteTypesense:
    companies_id: list[str] | None = None
    # In typesense we can't search for a null value, we set has_companies_id to True/False to be able to search for it
    # See: https://typesense.org/docs/guide/tips-for-searching-common-types-of-data.html#searching-for-null-or-empty-values
    has_companies_id: bool = True
    # Typesense doesn't support datetime objects. So we convert it to unix timestamp.
    # See: https://typesense.org/docs/26.0/api/collections.html#notes-on-indexing-common-types-of-data
    last_crawling: int = field(default_factory=lambda: datetime_to_unix_timestamp(datetime.now()))
    mongo_best_website_url: str | None = None
    home_page_url: str | None = None
    home_page_status_code: int | None = None
    home_page_text: str | None = None
    home_page_embedding: list[float] | None = None
    about_page_url: str | None = None
    about_page_status_code: int | None = None
    about_page_text: str | None = None
    about_page_embedding: list[float] | None = None
    contact_page_url: str | None = None
    contact_page_status_code: int | None = None
    contact_page_text: str | None = None
    contact_page_embedding: list[float] | None = None


@dataclass(slots=True)
class WebsiteTypesenseV2:
    """New implementation of the website Typesense collection."""

    companies_id: list[str]
    # Typesense doesn't support datetime objects. So we convert it to unix timestamp.
    # See: https://typesense.org/docs/26.0/api/collections.html#notes-on-indexing-common-types-of-data
    mongo_best_website_url: str
    domain: str
    last_crawling: int = field(default_factory=lambda: datetime_to_unix_timestamp(datetime.now()))
    page_about_url: str | None = None
    page_about_text: str | None = None
    page_about_embedding: str | None = None
    page_contact_url: str | None = None
    page_contact_text: str | None = None
    page_contact_embedding: str | None = None

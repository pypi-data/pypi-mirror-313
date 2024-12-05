from datetime import datetime
from dataclasses import dataclass


@dataclass(slots=True)
class CO2DataLegacy:
    """
    Dataclass to store the co2 data from our legacy SQL database table (co2_emissions).

    Each object represents a single company.
    These data are not updated anymore. We stopped development on this project.
    This is kept for reference purpose only.
    """
    # Company ID (same _id as in company collection with leading zeros BE:012345667)
    _id: str
    # Company ID (id in the old format (VAT without leading zeros) BE:12345667)
    legacy_entity_id: str
    date: datetime
    # ISO code of the country (BE, FR, NL)
    country: str
    first_best_nace_4: str | None = None
    first_best_nace_score: float | None = None
    first_best_nace_count: int | None = None
    second_best_nace_4: str | None = None
    second_best_nace_score: float | None = None
    third_best_nace_4: str | None = None
    third_best_nace_score: float | None = None
    first_declared_nace_4: str | None = None
    first_declared_nace_count: int | None = None
    estimated_staff: int | None = None
    employee_category: int | None = None
    staff_type: str | None = None
    average_ratio_scope1_first_best_nace: float | int | None = None
    average_ratio_scope1_second_best_nace: float | int | None = None
    average_ratio_scope1_third_best_nace: float | int | None = None
    average_ratio_scope1_declared_nace: float | int | None = None
    scope1_weight: float | int | None = None
    IC_80_firstnace_scope1: float | int | None = None
    scope1_declared: float | int | None = None
    average_ratio_scope2_first_best_nace: float | int | None = None
    average_ratio_scope2_second_best_nace: float | int | None = None
    average_ratio_scope2_third_best_nace: float | int | None = None
    average_ratio_scope2_declared_nace: float | int | None = None
    scope2_weight: float | int | None = None
    IC_80_firstnace_scope2: float | int | None = None
    scope2_declared: float | int | None = None
    last_updated: datetime | None = None

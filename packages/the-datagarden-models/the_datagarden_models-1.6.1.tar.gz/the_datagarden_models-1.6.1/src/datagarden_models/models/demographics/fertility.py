from typing import Optional

from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel


class FertilityV1Legends:
    TOTAL_BIRTHS = "Total number of births in the population."
    BIRTHS_BY_AGE = "Number of births categorized by age of the mother."
    AVERAGE_AGE_MOTHER = "Average age of mothers at childbirth."
    MEDIAN_AGE_MOTHER = "Median age of mothers at childbirth."
    FERTILITY_RATE = "Overall fertility rate per woman."
    FERTILITY_RATE_BY_AGE = "Fertility rates categorized by age of the mother."
    BIRTH_RATE = "Crude birth rate in number of births per 1000 people."


L = FertilityV1Legends


class Fertility(DataGardenSubModel):
    total_births: Optional[float] = Field(default=None, description=L.TOTAL_BIRTHS)
    births_by_age: dict = Field(default_factory=dict, description=L.BIRTHS_BY_AGE)
    average_age_mother: Optional[float] = Field(default=None, description=L.AVERAGE_AGE_MOTHER)
    median_age_mother: Optional[float] = Field(default=None, description=L.MEDIAN_AGE_MOTHER)
    fertility_rate: Optional[float] = Field(default=None, description=L.FERTILITY_RATE)
    fertility_rate_by_age: dict = Field(default_factory=dict, description=L.FERTILITY_RATE_BY_AGE)
    birth_rate: Optional[float] = Field(default=None, description=L.BIRTH_RATE)


class FertilityV1Keys:
    TOTAL_BIRTHS = "total_births"
    BIRTHS_BY_AGE = "births_by_age"
    AVERAGE_AGE_MOTHER = "average_age_mother"
    MEDIAN_AGE_MOTHER = "median_age_mother"
    FERTILITY_RATE = "fertility_rate"
    FERTILITY_RATE_BY_AGE = "fertility_rate_by_age"
    BIRTH_RATE = "birth_rate"

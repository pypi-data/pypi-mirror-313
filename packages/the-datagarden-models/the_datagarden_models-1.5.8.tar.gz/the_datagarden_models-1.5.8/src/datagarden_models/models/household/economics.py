from typing import Optional

from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel
from datagarden_models.models.base.standard_models import (
    EconomicsValue,
    ValueAndPercentage,
)


###########################################
########## Start Model defenition #########
###########################################
class HouseholdIncomeLegends:
    AVERAGE_INCOME = "Average household income."
    PERCENTAGE_HIGH_INCOME = "Percentage of households with high income."
    PERCENTAGE_LOW_INCOME = "Percentage of households with low income."


HI = HouseholdIncomeLegends


class HouseholdIncome(DataGardenSubModel):
    average_income: Optional[EconomicsValue] = Field(default=None, description=HI.AVERAGE_INCOME)
    percentage_high_income: Optional[float] = Field(default=None, description=HI.PERCENTAGE_HIGH_INCOME)
    percentage_low_income: Optional[float] = Field(default=None, description=HI.PERCENTAGE_LOW_INCOME)


class HouseholdIncomeKeys:
    AVERAGE_INCOME = "average_income"
    PERCENTAGE_HIGH_INCOME = "percentage_high_income"
    PERCENTAGE_LOW_INCOME = "percentage_low_income"


###########################################
########## Start Model defenition #########
###########################################
class EconomicsLegends:
    HOUSEHOLD_INCOME = "Average household income."
    SOCIAL_WELFARE_BENEFIT = "Population count with social welfare benefit other then pension."


EL = EconomicsLegends


class Economics(DataGardenSubModel):
    household_income: Optional[HouseholdIncome] = Field(default=None, description=EL.HOUSEHOLD_INCOME)
    social_welfare_benefit: Optional[ValueAndPercentage] = Field(
        default=None, description=EL.SOCIAL_WELFARE_BENEFIT
    )


class EconomicsKeys(HouseholdIncomeKeys):
    HOUSEHOLD_INCOME = "household_income"
    SOCIAL_WELFARE_BENEFIT = "social_welfare_benefit"

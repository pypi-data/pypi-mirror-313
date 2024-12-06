from typing import Optional

from pydantic import Field

from .models import DataGardenSubModel

###########################################
########## Start Model defenition #########
###########################################


class EconomicBaseKeys:
    VALUE = "value"
    UNIT = "unit"
    CURRENCY = "currency"


class EconomicBaseLegends:
    VALUE = "value in units of given currency,"
    UNIT = "units of measure."
    CURRENCY = "currency of measure."


L = EconomicBaseLegends


class EconomicsValue(DataGardenSubModel):
    value: Optional[float] = Field(default=None, description=L.VALUE)
    unit: int = Field(default=1, description=L.UNIT)
    currency: str = Field(default="EUR", description=L.CURRENCY)

    class Meta:
        exclude_fields_in_has_values_check: list[str] = ["unit", "currency"]


###########################################
########## Start Model defenition #########
###########################################
class ValueAndPercentageKeys:
    VALUE = "value"
    PERCENTAGE = "percentage"
    UNIT = "unit"
    COUNT = "count"


class CountValueAndPercentageLegends:
    VALUE = "value in units of given currency,"
    PERCENTAGE = "percentage of total."
    UNIT = "units of measure."
    COUNT = "count of items in single units."


VP = CountValueAndPercentageLegends


class ValueAndPercentage(DataGardenSubModel):
    value: Optional[float] = Field(default=None, description=VP.VALUE)
    percentage: Optional[float] = Field(default=None, description=VP.PERCENTAGE)
    unit: int = Field(default=1, description=VP.UNIT)
    count: Optional[float] = Field(default=None, description=VP.COUNT)

    class Meta:
        exclude_fields_in_has_values_check: list[str] = ["unit"]

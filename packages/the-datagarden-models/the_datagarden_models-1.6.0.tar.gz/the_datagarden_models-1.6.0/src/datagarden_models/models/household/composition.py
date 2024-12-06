from typing import Optional

from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel


###########################################
########## Start Model defenition #########
###########################################
class CompositionLegends:
    BY_TYPE = "Count of households composition types by type."
    AVERAGE_HOUSEHOLD_SIZE = "Average household size in number of people."


CL = CompositionLegends


class Composition(DataGardenSubModel):
    by_type: dict[str, float] = Field(default_factory=dict, description=CL.BY_TYPE)
    average_household_size: Optional[float] = Field(default=None, description=CL.AVERAGE_HOUSEHOLD_SIZE)


class CompositionKeys:
    BY_TYPE = "by_type"
    AVERAGE_HOUSEHOLD_SIZE = "average_household_size"

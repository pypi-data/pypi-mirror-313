from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel

from .base_demographics import AgeGender


class LifeExpectancyV1Keys:
    LIFE_EXPECTANCY_AT_BIRTH = "life_expectancy_at_birth"
    REMAINING_LIFE_EXPECTANCY = "remaining_life_expectancy"


class LifeExpectancyV1Legends:
    LIFE_EXPECTANCY_AT_BIRTH = (
        "Life expectancy per age or age group at birth. " "In years expected to live when born"
    )
    REMAINING_LIFE_EXPECTANCY = (
        "Life expectancy per age or age group at current age. " "In years expected to live as of current age"
    )


L = LifeExpectancyV1Legends


class LifeExpectancy(DataGardenSubModel):
    life_expectancy_at_birth: AgeGender = Field(
        default_factory=AgeGender, description=L.LIFE_EXPECTANCY_AT_BIRTH
    )

    remaining_life_expectancy: AgeGender = Field(
        default_factory=AgeGender, description=L.REMAINING_LIFE_EXPECTANCY
    )

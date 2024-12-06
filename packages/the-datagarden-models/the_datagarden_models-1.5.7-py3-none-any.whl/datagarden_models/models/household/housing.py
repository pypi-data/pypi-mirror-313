from typing import Optional

from pydantic import Field

from datagarden_models.models.base import (
    DataGardenSubModel,
    EconomicBaseKeys,
    EconomicsValue,
    ValueAndPercentage,
    ValueAndPercentageKeys,
)


########## Start Model defenition #########
###########################################
class DwellingTypeKeys:
    DETACHED = "detached"
    SEMI_DETACHED = "semi_detached"
    ROW_HOUSE = "row_house"
    APARTMENT = "apartment"
    BOAT_HOUSE = "boat_house"
    MOBILE_HOME = "mobile_home"


class DwellingTypeLegends:
    DETACHED = "Detached house."
    SEMI_DETACHED = "Semi-detached house."
    ROW_HOUSE = "Row or town house."
    APARTMENT = "Apartment or flat."
    BOAT_HOUSE = "Boat house."
    MOBILE_HOME = "Mobile home."


DT = DwellingTypeLegends


class DwellingType(DataGardenSubModel):
    detached: Optional[ValueAndPercentage] = Field(default=None, description=DT.DETACHED)
    semi_detached: Optional[ValueAndPercentage] = Field(default=None, description=DT.SEMI_DETACHED)
    row_house: Optional[ValueAndPercentage] = Field(default=None, description=DT.ROW_HOUSE)
    apartment: Optional[ValueAndPercentage] = Field(default=None, description=DT.APARTMENT)
    boat_house: Optional[ValueAndPercentage] = Field(default=None, description=DT.BOAT_HOUSE)
    mobile_home: Optional[ValueAndPercentage] = Field(default=None, description=DT.MOBILE_HOME)


###########################################
########## Start Model defenition #########
###########################################
class TenureKeys:
    OWNED = "owned"
    RENTED = "rented"
    INHABITED = "inhabited"
    SOCIAL_HOUSING = "social_housing"


class TenureLegends:
    OWNED = "Houses owned."
    RENTED = "Houses rented."
    INHABITED = "Houses inhabited."
    SOCIAL_HOUSING = "Social housing."


T = TenureLegends


class Tenure(DataGardenSubModel):
    owned: Optional[ValueAndPercentage] = Field(default=None, description=T.OWNED)
    rented: Optional[ValueAndPercentage] = Field(default=None, description=T.RENTED)
    inhabited: Optional[ValueAndPercentage] = Field(default=None, description=T.INHABITED)
    social_housing: Optional[ValueAndPercentage] = Field(default=None, description=T.SOCIAL_HOUSING)


###########################################
########## Start Model defenition #########
###########################################
class DwellingKeys:
    TENURE = "tenure"


class DwellingLegends:
    TENURE = "Ownership status of the house."
    TYPE = "Type of housing by type in percentage or value."


D = DwellingLegends


class Dwelling(DataGardenSubModel):
    type: DwellingType = Field(default_factory=DwellingType, description=D.TYPE)
    tenure: Tenure = Field(default_factory=Tenure, description=D.TENURE)


###########################################
########## Start Model defenition #########
###########################################
class HousingCharacteristicsKeys:
    NUMBER_OF_ROOMS = "number_of_rooms"
    CONSTRUCTION_PERIOD = "construction_period"


class HousingCharacteristicsLegends:
    NUMBER_OF_ROOMS = "Number of rooms."
    CONSTRUCTION_PERIOD = "Construction period."


HC = HousingCharacteristicsLegends


class HousingCharacteristics(DataGardenSubModel):
    number_of_rooms: Optional[int] = Field(default=None, description=HC.NUMBER_OF_ROOMS)
    construction_period: Optional[dict[str, ValueAndPercentage]] = Field(
        default=None, description=HC.CONSTRUCTION_PERIOD
    )


###########################################
########## Start Model defenition #########
###########################################
class HousingLegends:
    DWELLING = "Housing categorization."
    CHARACTERISTICS = "Housing characteristics."
    AVG_REAL_ESTATE_VALUE = "Average value of real estate in the regpion."
    HOUSEHOLDS_PER_KM2 = "Number of households per square kilometer."
    NR_OF_HOUSEHOLDS = "Number of households."


L = HousingLegends


class Housing(DataGardenSubModel):
    dwelling: Dwelling = Field(default_factory=Dwelling, description=L.DWELLING)
    characteristics: HousingCharacteristics = Field(
        default_factory=HousingCharacteristics, description=L.CHARACTERISTICS
    )
    avg_real_estate_value: Optional[EconomicsValue] = Field(default=None, description=L.AVG_REAL_ESTATE_VALUE)
    nr_of_households: Optional[int] = Field(default=None, description=L.NR_OF_HOUSEHOLDS)
    households_per_km2: Optional[float] = Field(default=None, description=L.HOUSEHOLDS_PER_KM2)


class HousingKeys(
    EconomicBaseKeys,
    DwellingTypeKeys,
    ValueAndPercentageKeys,
    TenureKeys,
    DwellingKeys,
    HousingCharacteristicsKeys,
):
    DWELLING = "dwelling"
    CHARACTERISTICS = "characteristics"
    TENURE = "tenure"
    AVG_REAL_ESTATE_VALUE = "avg_real_estate_value"
    NR_OF_HOUSEHOLDS = "nr_of_households"
    HOUSEHOLDS_PER_KM2 = "households_per_km2"

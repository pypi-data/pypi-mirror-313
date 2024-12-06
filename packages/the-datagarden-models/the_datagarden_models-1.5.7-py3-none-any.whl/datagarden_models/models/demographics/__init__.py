from pydantic import Field

from ..base import DataGardenModel, DataGardenModelKeys, DataGardenModelLegends
from .base_demographics import DemographicsBaseKeys
from .education import Education, EducationV1Keys
from .fertility import Fertility, FertilityV1Keys
from .life_expectancy import LifeExpectancy, LifeExpectancyV1Keys
from .mortality import Mortality, MortalityV1Keys
from .population import Population, PopulationV1Keys


class DemographicsV1Keys(
    DataGardenModelKeys,
    PopulationV1Keys,
    FertilityV1Keys,
    LifeExpectancyV1Keys,
    MortalityV1Keys,
    DemographicsBaseKeys,
    EducationV1Keys,
):
    POPULATION = "population"
    MORTALITY = "mortality"
    FERTILITY = "fertility"
    LIFE_EXPECTANCY = "life_expectancy"
    EDUCATION = "education"
    DATAGARDEN_MODEL_NAME = "Demographics"


class DemographicsV1Legends(DataGardenModelLegends):
    MODEL_LEGEND = "Demographic models for a region. "
    POPULATION = "Population indicators for the region. "
    MORTALITY = "Mortality indicators for the region. "
    FERTILITY = "Fertility indicators for the region. "
    LIFE_EXPECTANCY = "Life expectancy indicators for the region. "
    EDUCATION = "Education level indicators for the region. "


L = DemographicsV1Legends


class DemographicsV1(DataGardenModel):
    datagarden_model_version: str = Field("v1.0", frozen=True, description=L.DATAGARDEN_MODEL_VERSION)
    population: Population = Field(default_factory=Population, description=L.POPULATION)
    life_expectancy: LifeExpectancy = Field(default_factory=LifeExpectancy, description=L.LIFE_EXPECTANCY)
    mortality: Mortality = Field(default_factory=Mortality, description=L.MORTALITY)
    fertility: Fertility = Field(default_factory=Fertility, description=L.FERTILITY)
    education: Education = Field(default_factory=Education, description=L.EDUCATION)

from pydantic import Field

from datagarden_models.models.base import DataGardenModel
from datagarden_models.models.base.legend import DataGardenModelLegends

from .composition import Composition, CompositionKeys
from .economics import Economics, EconomicsKeys
from .housing import Housing, HousingKeys


###########################################
########## Start Model defenition #########
###########################################
class HouseholdV1Keys(CompositionKeys, HousingKeys, EconomicsKeys):
    DATAGARDEN_MODEL_NAME = "Household"
    COMPOSITION = "composition"
    HOUSING = "housing"
    ECONOMICS = "economics"


class HouseholdV1Legends(DataGardenModelLegends):
    MODEL_LEGEND: str = "Data on household type and composition for a region. "
    COMPOSITION = "Data on composition of households for a region. "
    HOUSING = "Data on housing for a region. "
    ECONOMICS = "Data on household economics for a region. "


L = HouseholdV1Legends


class HouseholdV1(DataGardenModel):
    composition: Composition = Field(default_factory=Composition, description=L.COMPOSITION)
    housing: Housing = Field(default_factory=Housing, description=L.HOUSING)
    economics: Economics = Field(default_factory=Economics, description=L.ECONOMICS)

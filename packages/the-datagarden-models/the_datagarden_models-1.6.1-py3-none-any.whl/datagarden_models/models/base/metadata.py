from pydantic import BaseModel, Field


class MetadataModelKeys:
    DATA_IS_PROJECTION = "data_is_projection"


class MetadataModelLegends:
    DATA_IS_PROJECTION = "data is identified by the source as a projection."
    # DATA_IS_DERIVED = \
    # "data is derived by the datagarden from different sources and possibly machine learning models"


MML = MetadataModelLegends


class MetadataModel(BaseModel):
    data_is_projection: bool = Field(default=False, description=MML.DATA_IS_PROJECTION)
    # data_is_derived: bool = Field(default=False, description=DataGardenModelLegends.DATA_IS_DERIVED)

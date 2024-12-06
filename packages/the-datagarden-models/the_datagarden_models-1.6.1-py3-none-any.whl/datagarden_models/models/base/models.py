from typing import Optional

from pydantic import BaseModel, Field, model_validator

from .legend import DataGardenModelLegends, Legend
from .metadata import MetadataModel, MetadataModelKeys


class DataGardenSubModel(BaseModel):
    class Meta:
        exclude_fields_in_has_values_check: list[str] = []

    def has_values(self, data: BaseModel | None = None) -> bool:
        # Recursively check if any field has a non-default or non-empty value
        data = data or self
        for field, value in data:
            if field == "datagarden_model_version":
                continue
            if field in self.Meta.exclude_fields_in_has_values_check:
                continue

            if isinstance(value, DataGardenSubModel):
                if self.has_values(value):
                    return True
            elif value or value == 0 or value is False:  # This will check for truthy values (non-empty)
                return True
        return False

    @classmethod
    def legends(cls) -> Legend:
        return Legend(model=cls)

    @property
    def is_empty(self) -> bool:
        return not self.has_values()

    def __bool__(self) -> bool:
        return not self.is_empty


class DataGardenModelKeys(MetadataModelKeys):
    DATAGARDEN_MODEL_VERSION = "datagarden_model_version"
    LOCAL_REGIONAL_DATA = "local_regional_data"
    METADATA = "metadata"


class DataGardenModel(DataGardenSubModel):
    datagarden_model_version: str = Field(
        "v1.0",
        frozen=True,
        description=DataGardenModelLegends.DATAGARDEN_MODEL_VERSION,
    )
    local_regional_data: Optional[dict] = Field(
        default=None, description=DataGardenModelLegends.LOCAL_REGIONAL_DATA
    )
    metadata: MetadataModel = Field(default=MetadataModel(), description=DataGardenModelLegends.METADATA)

    @model_validator(mode="before")
    def check_datagarden_model_version(cls, values):
        if (
            "datagarden_model_version" in values
            and values["datagarden_model_version"] != cls.model_fields["datagarden_model_version"].default
        ):
            raise ValueError("The field 'datagarden_model_version' is immutable.")
        return values

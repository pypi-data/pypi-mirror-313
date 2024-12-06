from typing import Optional

from pydantic import Field

from datagarden_models import AVAILABLE_MODELS
from datagarden_models.models.base import DataGardenSubModel


def test_legends_are_available_for_all_models():
    for model in AVAILABLE_MODELS:
        print(model)
        legend = model.legends()

        assert legend is not None


def test_legends_pipe_in_annotation():
    class TestModel(DataGardenSubModel):
        field_name: int | None = Field(default=None, description="test")

    legend = TestModel.legends()

    assert legend.field_name is not None
    assert legend.field_name.type_class_name == "int"


def test_legends_optional_in_annotation():
    class TestModel(DataGardenSubModel):
        field_name: Optional[int] = Field(default=None, description="test")

    legend = TestModel.legends()

    assert legend.field_name is not None
    assert legend.field_name.type_class_name == "int"


def test_legends_for_type_dict():
    class TestModel(DataGardenSubModel):
        field_name: dict = Field(default_factory=dict, description="test")

    legend = TestModel.legends()

    assert legend.field_name is not None
    assert legend.field_name.type_class_name == "dict"

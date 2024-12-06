"""


Objects for discovery of available dataclasses
- AVAILABLE_MODELS: List with all Datagarden models
- AVAILABLE_MODEL_NAMES: List with all data models names (as str)
- DatagardenModels: Class with all Datagarden models as class constant
        >>> DatagardenModels.DEMOGRAPHICS  # returns latest version of the Demographic
                                             Pydantic data class

- DatagardenModelKeys: Class with all key classes for the Datagarden model classes.
        >>> keys = DatagardenModelKeys.DEMOGRAPHICS  # returns latest version of the
                                                       Demographic key class
        >>> keys.POPULATION  # returns the model key for the POPUPLATION field.


"""

from .models import DatagardenModelKeys, DatagardenModels
from .models.base import DataGardenModel


def get_values_from_class(cls: type):
    for key, value in vars(cls).items():
        if not key.startswith("__"):
            yield value


AVAILABLE_MODEL_NAMES: list[str] = [
    klass.DATAGARDEN_MODEL_NAME for klass in get_values_from_class(DatagardenModelKeys)
]

AVAILABLE_MODELS: list[type[DataGardenModel]] = list(get_values_from_class(DatagardenModels))


__all__ = [
    "DatagardenModels",
    "DatagardenModelKeys",
    "AVAILABLE_MODELS",
    "AVAILABLE_MODEL_NAMES",
]

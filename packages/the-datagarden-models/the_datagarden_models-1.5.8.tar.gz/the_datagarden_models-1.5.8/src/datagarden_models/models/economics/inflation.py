from typing import Optional

from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel


class PriceIndexFixedKeys:
    INDEX = "index"
    REFERENCE_YEAR = "reference_year"


class PriceIndexFixedLegends:
    INDEX = "Price index (reference year = 100)."
    REFERENCE_YEAR = "Reference year for the price index."


PI = PriceIndexFixedLegends


class PriceIndexFixed(DataGardenSubModel):
    index: Optional[float] = Field(default=None, description=PI.INDEX)
    reference_year: Optional[str] = Field(default=None, description=PI.REFERENCE_YEAR)


class InflationV1Legends:
    INFLATION_YOY = "Inflation versus previous year in percent."
    PRICE_INDEX = "Price index vs fixed year."


L = InflationV1Legends


class Inflation(DataGardenSubModel):
    inflation_yoy: Optional[float] = Field(default=None, description=L.INFLATION_YOY)
    price_index: PriceIndexFixed = Field(default_factory=PriceIndexFixed, description=L.PRICE_INDEX)


class InflationV1Keys(PriceIndexFixedKeys):
    INFLATION_YOY = "inflation_yoy"
    PRICE_INDEX = "price_index"

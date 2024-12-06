from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel
from datagarden_models.models.economics.base_economics import EconomicsValue


class PublicSpendingByCofogCategoryKeys:
    CURRENCY = "currency"
    VALUE = "value"
    SHARE_OF_GDP = "share_of_gdp"


class PublicSpendingByCofogCategoryLegends:
    CURRENCY = "Currency of the public spending value."
    VALUE_BY_COFOG_CATEGORY = "Public spending by cofog category."
    SHARE_OF_GDP_BY_COFOG_CATEGORY = "Share of GDP by cofog category."


PSBCC = PublicSpendingByCofogCategoryLegends


class PublicSpendingByCofogCategory(DataGardenSubModel):
    currency: str = Field(default="EUR", description=PSBCC.CURRENCY)
    value: dict[str, float] = Field(default_factory=dict, description=PSBCC.VALUE_BY_COFOG_CATEGORY)
    share_of_gdp: dict[str, float] = Field(
        default_factory=dict, description=PSBCC.SHARE_OF_GDP_BY_COFOG_CATEGORY
    )


class PublicSpendingLegends:
    BY_COFOG_CATEGORY = "Public spending by cofog category."
    TOTAL = "Total public spending."


PS = PublicSpendingLegends


class PublicSpendingV1(DataGardenSubModel):
    by_cofog_category: PublicSpendingByCofogCategory = Field(
        default_factory=PublicSpendingByCofogCategory,
        description=PS.BY_COFOG_CATEGORY,
    )
    total: EconomicsValue = Field(default_factory=EconomicsValue, description=PS.TOTAL)


class PublicSpendingV1Keys(PublicSpendingByCofogCategoryKeys):
    BY_COFOG_CATEGORY = "by_cofog_category"
    TOTAL = "total"

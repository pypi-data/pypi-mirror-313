from typing import Annotated, Optional

from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel
from datagarden_models.models.base.standard_models import EconomicsValue


########## Start Model defenition #########
class CurrentAccountBalanceLegends:
    BALANCE = "Current account balance."
    PERCENTAGE_OF_GDP = "Current accounts as a percentage of GDP."


CA = CurrentAccountBalanceLegends


class CurrentAccountBalance(DataGardenSubModel):
    balance: Optional[EconomicsValue] = Field(default=None, description=CA.BALANCE)
    percentage_of_gdp: Optional[float] = Field(default=None, description=CA.PERCENTAGE_OF_GDP)


########## Start Model defenition #########
class TradeBalanceTypeKeys:
    BALANCE = "balance"
    PERCENTAGE_OF_IMPORTS = "percentage_of_imports"
    PERCENTAGE_OF_GDP = "percentage_of_gdp"
    NORMALIZED_TRADE_BALANCE = "normalized_trade_balance"


class TradeBalanceTypeLegends:
    BALANCE = "Trade balance."
    PERCENTAGE_OF_IMPORTS = "Trade balance as a percentage of imports."
    PERCENTAGE_OF_GDP = "Trade balance as a percentage of GDP."
    NORMALIZED_TRADE_BALANCE = "Normalized trade balance (-1 to 1, 0 means a fully balanced trade)."


PI = TradeBalanceTypeLegends


class TradeBalanceType(DataGardenSubModel):
    balance: Optional[EconomicsValue] = Field(default=None, description=PI.BALANCE)
    percentage_of_imports: Optional[float] = Field(default=None, description=PI.PERCENTAGE_OF_IMPORTS)
    percentage_of_gdp: Optional[float] = Field(default=None, description=PI.PERCENTAGE_OF_GDP)
    normalized_trade_balance: Optional[Annotated[float, Field(ge=-1, le=1)]] = Field(
        default=None, description=PI.NORMALIZED_TRADE_BALANCE
    )


########## Start Model defenition #########
class TradeBalanceKeys:
    SERVICES = "services"
    GOODS = "goods"
    GOODS_AND_SERVICES = "goods_and_services"
    CURRENT_ACCOUNT_BALANCE = "current_account_balance"


class TradeBalanceLegends:
    SERVICES = "Trade balance information for services."
    GOODS = "Trade balance information for goods."
    GOODS_AND_SERVICES = "Trade balance information for services and goods."
    CURRENT_ACCOUNT_BALANCE = "Current account balance information."


L_TB = TradeBalanceLegends


class TradeBalance(DataGardenSubModel):
    services: TradeBalanceType = Field(default_factory=TradeBalanceType, description=L_TB.SERVICES)
    goods: TradeBalanceType = Field(default_factory=TradeBalanceType, description=L_TB.GOODS)
    goods_and_services: TradeBalanceType = Field(
        default_factory=TradeBalanceType, description=L_TB.GOODS_AND_SERVICES
    )
    current_account_balance: CurrentAccountBalance = Field(
        default_factory=CurrentAccountBalance, description=L_TB.CURRENT_ACCOUNT_BALANCE
    )


########## Start Model defenition #########
class ImportExportKeys:
    SERVICES = "services"
    GOODS = "goods"
    GOODS_AND_SERVICES = "goods_and_services"


class ImportExportLegends:
    SERVICES = "Value for services trade."
    GOODS = "Value for goods trade."
    GOODS_AND_SERVICES = "Value for services and goods trade."


L_IMP_EXP = ImportExportLegends


class Import(DataGardenSubModel):
    goods: Optional[float] = Field(default=None, description=L_IMP_EXP.GOODS)
    services: Optional[float] = Field(default=None, description=L_IMP_EXP.SERVICES)
    goods_and_services: Optional[float] = Field(default=None, description=L_IMP_EXP.GOODS_AND_SERVICES)


class Export(Import): ...


########## Start Model defenition #########
class TradeV1Legends:
    IMPORTS = "Imports information."
    EXPORTS = "Exports information."
    TRADE_BALANCE = "Trade balance information."


L_TRADE_V1 = TradeV1Legends


class TradeV1(DataGardenSubModel):
    trade_balance: TradeBalance = Field(default_factory=TradeBalance, description=L_TRADE_V1.TRADE_BALANCE)
    imports: Import = Field(default_factory=Import, description=L_TRADE_V1.IMPORTS)
    exports: Export = Field(default_factory=Export, description=L_TRADE_V1.EXPORTS)


class TradeV1Keys(TradeBalanceTypeKeys, TradeBalanceKeys, ImportExportKeys):
    IMPORTS = "imports"
    EXPORTS = "exports"
    TRADE_BALANCE = "trade_balance"

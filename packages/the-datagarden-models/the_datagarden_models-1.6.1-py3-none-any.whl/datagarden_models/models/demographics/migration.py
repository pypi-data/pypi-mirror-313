from typing import Optional

from pydantic import Field

from ..base import DataGardenSubModel


###########################################
########## Start Model defenition #########
###########################################
class MigrationV1Legends:
    NET_MIGRANTION = "Net number of migrants. In number of individuals."
    NET_MIGRATION_RATE = "Migration rate. In number of migrants per 1.000 persons."


L = MigrationV1Legends


class Migration(DataGardenSubModel):
    net_migrantion: Optional[float] = Field(default=None, description=L.NET_MIGRANTION)
    net_migration_rate: Optional[float] = Field(default=None, description=L.NET_MIGRATION_RATE)


class MigrationV1Keys:
    NET_MIGRANTION = "net_migrantion"
    NET_MIGRATION_RATE = "net_migration_rate"

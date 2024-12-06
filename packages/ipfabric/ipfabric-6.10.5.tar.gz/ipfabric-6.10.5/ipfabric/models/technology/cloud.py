import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Cloud(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def virtual_machines(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/virtual-machines", sn=self.sn)

    @computed_field
    @property
    def virtual_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/virtual-machines-interfaces", sn=self.sn)

import logging
from typing import Any, Optional, List

from pydantic import BaseModel, Field, field_validator, model_validator

from ipfabric.tools import raise_for_status, validate_ip_network_str

logger = logging.getLogger("ipfabric")


class Networks(BaseModel):
    exclude: Optional[List[str]] = Field(default_factory=list)
    include: Optional[List[str]] = Field(default_factory=list)

    @field_validator("exclude", "include")
    @classmethod
    def _verify_valid_networks(cls, v: List[str]) -> List[str]:
        return [validate_ip_network_str(_) for _ in v]

    @model_validator(mode="after")
    def _verify_include_not_empty(self):
        if not self.include:
            raise ValueError("Discovery Settings Network Include list cannot be empty.")
        return self


class Discovery(BaseModel):
    client: Any = Field(exclude=True)
    _networks: Optional[Networks] = None

    def model_post_init(self, __context: Any) -> None:
        self._networks = self._get_networks()

    @property
    def networks(self):
        return self._networks

    def _get_networks(self):
        res = raise_for_status(self.client.get("settings"))
        return Networks(**res.json()["networks"])

    def update_discovery_networks(self, subnets: list, include: bool = False):
        payload = dict()
        payload["networks"] = dict()
        if include:
            payload["networks"]["include"] = subnets
            payload["networks"]["exclude"] = self.networks.exclude
        else:
            payload["networks"]["exclude"] = subnets
            payload["networks"]["include"] = self.networks.include
        res = raise_for_status(self.client.patch("settings", json=payload))
        return Networks(**res.json()["networks"])

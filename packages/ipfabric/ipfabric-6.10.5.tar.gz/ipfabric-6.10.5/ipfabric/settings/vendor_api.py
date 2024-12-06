import logging
from typing import Any, ClassVar, Union

from pydantic import ValidationError, Field
from pydantic.dataclasses import dataclass

from ipfabric.exceptions import deprecated_args_decorator
from ipfabric.settings.vendor_api_models import (
    AWS,
    Azure,
    CheckPointApiKey,
    CheckPointUserAuth,
    CiscoAPIC,
    CiscoFMC,
    CiscoFMCToken,
    ForcePoint,
    GCP,
    JuniperMist,
    Merakiv1,
    Prisma,
    RuckusVirtualSmartZone,
    SilverPeak,
    Versa,
    Viptela,
    NSXT,
)
from ipfabric.tools import raise_for_status

API_MODELS = (
    AWS,
    Azure,
    CheckPointApiKey,
    CheckPointUserAuth,
    CiscoAPIC,
    CiscoFMC,
    CiscoFMCToken,
    ForcePoint,
    GCP,
    JuniperMist,
    Merakiv1,
    Prisma,
    RuckusVirtualSmartZone,
    SilverPeak,
    Versa,
    Viptela,
    NSXT,
)

TYPE_TO_MODEL = {c.model_fields["type"].default: c for c in API_MODELS}

CONNECTION_PARAMS = [
    "rejectUnauthorized",
    "respectSystemProxyConfiguration",
    "maxConcurrentRequests",
    "maxCapacity",
    "refillRate",
    "refillRateIntervalMs",
]

logger = logging.getLogger("ipfabric")


@deprecated_args_decorator(version="7.0", no_args=False, kwargs_only=True)
@dataclass
class VendorAPI:
    client: Any = Field(exclude=True)
    _api_url: ClassVar[str] = "settings/vendor-api"

    def get_vendor_apis(self) -> list:
        """
        Get all vendor apis and sets them in the Authentication.apis
        :return: self.credentials
        """
        return raise_for_status(self.client.get(self._api_url)).json()

    def add_vendor_api(self, api: Union[API_MODELS]) -> dict:
        params = api.model_dump()
        return raise_for_status(self.client.post(self._api_url, json=params)).json()

    @staticmethod
    def _return_api_id(api_id: Union[dict, str, int]) -> str:
        if isinstance(api_id, dict):
            api_id = api_id["id"]
        elif isinstance(api_id, int):
            api_id = str(api_id)
        return api_id

    def delete_vendor_api(self, api_id: Union[dict, str, int]):
        api_id = self._return_api_id(api_id)
        return raise_for_status(self.client.delete(self._api_url + "/" + api_id)).status_code

    def _enable_api(self, api_id: Union[dict, str, int], enable: bool = True) -> int:
        api_id = self._return_api_id(api_id)
        return raise_for_status(self.client.patch(self._api_url + "/" + api_id, json={"isEnabled": enable})).status_code

    def enable_vendor_api(self, api_id: Union[dict, str, int]) -> int:
        return self._enable_api(api_id)

    def disable_vendor_api(self, api_id: Union[dict, str, int]) -> int:
        return self._enable_api(api_id, False)

    @staticmethod
    def _validate_update(params):
        if params["type"] == "checkpoint-mgmt-api":
            try:
                CheckPointApiKey.model_validate(params)
            except ValidationError:
                try:
                    CheckPointUserAuth.model_validate(params)
                except ValidationError:
                    raise SyntaxError(
                        "Error validating updated data for Checkpoint API "
                        "please provide either apiKey or username and password."
                    )
        else:
            try:
                TYPE_TO_MODEL[params["type"]].model_validate(params)
            except ValidationError:
                raise SyntaxError("Error validating updated data for Vendor API please see missing required arguments.")
        return params

    def update_vendor_api(
        self, current: dict, update: Union[Union[API_MODELS], dict], restore_conn_defaults: bool = False
    ) -> dict:
        current.pop("details", None)
        api_id = current.pop("id")

        if isinstance(update, API_MODELS):
            update = vars(update)

        params = {**current, **update}
        if restore_conn_defaults:
            default = {
                k: v for k, v in vars(TYPE_TO_MODEL[params["type"]].model_construct()).items() if k in CONNECTION_PARAMS
            }
            params.update(default)

        self._validate_update(params)

        return raise_for_status(self.client.put(self._api_url + "/" + str(api_id), json=params)).json()

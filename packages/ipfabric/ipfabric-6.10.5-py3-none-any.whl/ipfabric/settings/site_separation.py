import logging
from copy import deepcopy
from typing import Any, Optional
from warnings import warn

from pydantic import Field
from pydantic.dataclasses import dataclass

from ipfabric.exceptions import deprecated_args_decorator
from ipfabric.tools import raise_for_status

logger = logging.getLogger("ipfabric")


@deprecated_args_decorator(version="7.0", no_args=False, kwargs_only=True)
@dataclass
class SiteSeparation:
    client: Optional[Any] = Field(None, exclude=True)
    ipf: Optional[Any] = None

    def __post_init__(self):
        if not self.ipf and not self.client:
            raise SyntaxError("No IPF Client passed.")
        elif self.ipf and not self.client:
            msg = "Argument `ipf` is being changed to `client` in `7.0` please update your scripts."
            warn(msg, DeprecationWarning, stacklevel=2)
            logger.warning(msg)
            self.client = self.ipf

    def get_separation_rules(self):
        return self.client.get("settings/site-separation").json()

    def _post_rule(self, data):
        return raise_for_status(self.client.post("settings/site-separation/test-regex", json=data)).json()

    @staticmethod
    def _create_rule(transformation, regex):
        transformation = transformation.lower()
        if transformation not in ["uppercase", "lowercase", "none"]:
            raise SyntaxError('Transformation type is not in ["uppercase", "lowercase", "none"].')
        return {"regex": regex, "transformation": transformation}

    def get_rule_matches(self, rule):
        rule = deepcopy(rule)
        [rule.pop(key, None) for key in ["id", "note", "siteName"]]
        return self._post_rule(rule)

    def get_hostname_matches(self, regex, transformation):
        rule = self._create_rule(transformation, regex)
        rule["type"] = "regexHostname"
        return self._post_rule(rule)

    def get_snmp_matches(self, regex, transformation):
        rule = self._create_rule(transformation, regex)
        rule["type"] = "regexSnmpLocation"
        return self._post_rule(rule)

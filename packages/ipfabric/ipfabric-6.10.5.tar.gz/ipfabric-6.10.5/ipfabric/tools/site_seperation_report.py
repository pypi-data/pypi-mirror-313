import logging
from copy import deepcopy
from typing import Optional

from pydantic.dataclasses import dataclass

from ipfabric.settings.attributes import Attributes
from ipfabric.settings.site_separation import SiteSeparation

logger = logging.getLogger("ipfabric")


@dataclass
class Matches:
    hostname: str
    sn: str
    old_site_name: str
    rule_type: str
    new_site_name: Optional[str] = None
    rule_number: Optional[int] = None
    rule_note: Optional[str] = None
    regex: Optional[str] = None
    transformation: Optional[str] = None


def check_attributes(ipf, devices):
    matches = list()
    attributes = {a["sn"]: a for a in Attributes(ipf).all(filters={"name": ["eq", "siteName"]})}
    for sn, dev in deepcopy(devices).items():
        if sn in attributes:
            matches.append(
                Matches(
                    hostname=dev["hostname"],
                    sn=sn,
                    old_site_name=attributes[sn]["value"],
                    rule_type="attributes",
                    rule_number=-1,
                )
            )
            devices.pop(sn)
    return matches


def _create_device_match(match, data, rule, devices, idx):
    site = match["siteName"] if data["matchingGroupApplied"] else rule["siteName"]
    transformation = rule["transformation"] if rule["transformation"] != "none" else None
    return Matches(
        hostname=match["hostname"],
        old_site_name=devices[match["sn"]]["siteName"],
        sn=match["sn"],
        new_site_name=site,
        rule_type=rule["type"],
        rule_number=idx,
        rule_note=rule["note"],
        regex=rule["regex"],
        transformation=transformation,
    )


def map_devices_to_rules(ipf, snapshot_id: str = "$last"):
    ss = SiteSeparation(ipf)
    devices = {
        d["sn"]: d for d in ipf.inventory.devices.all(columns=["hostname", "sn", "siteName"], snapshot_id=snapshot_id)
    }
    rules = ss.get_separation_rules()

    matches = check_attributes(ipf, devices) if rules["manualEnabled"] else list()

    for idx, rule in enumerate(rules["rules"]):
        data = ss.get_rule_matches(rule)
        for match in data["matched"]:
            if match["sn"] in devices:
                matches.append(_create_device_match(match, data, rule, devices, idx))
                devices.pop(match["sn"], None)

    for sn, dev in devices.items():
        matches.append(
            Matches(hostname=dev["hostname"], sn=sn, old_site_name=dev["siteName"], rule_type="noMatchingRule")
        )
    return [vars(m) for m in matches]

from __future__ import annotations

import os
from typing import List, Optional, Union, Dict

from pydantic import BaseModel

PYDANTIC_EXTRAS = os.getenv("IPFABRIC_PYDANTIC_EXTRAS", "allow")


class BaseSecurity(BaseModel, extra=PYDANTIC_EXTRAS):
    name: Optional[str] = None
    type: Optional[str] = None
    original: Optional[str] = None


class DefaultAction(BaseSecurity, BaseModel, extra=PYDANTIC_EXTRAS):
    chainName: Optional[str] = None


class Reference(BaseSecurity, BaseModel, extra=PYDANTIC_EXTRAS):
    dictionary: str
    key: str


class ReferenceValue(BaseModel, extra=PYDANTIC_EXTRAS):
    reference: Reference


class ValueItem(BaseSecurity, BaseModel, extra=PYDANTIC_EXTRAS):
    min: Union[int, str]
    max: Union[int, str]
    version: Optional[int] = None


class ValueOriginalType(BaseSecurity, BaseModel, extra=PYDANTIC_EXTRAS):
    category: Optional[str] = None
    value: List[Union[ValueItem, ValueOriginalType, ReferenceValue]]


class ValueItemIpPort(BaseSecurity, BaseModel, extra=PYDANTIC_EXTRAS):
    toIp: ValueOriginalType
    toPort: Optional[ValueOriginalType] = None


class HeaderField(BaseModel, extra=PYDANTIC_EXTRAS):
    header: Optional[str] = None
    field: Optional[str] = None


class NexthopIp(BaseModel):
    ip: str
    ipLong: int


class NexthopInt(BaseModel):
    int: str


class PathLookupOption(BaseSecurity, HeaderField, BaseModel, extra=PYDANTIC_EXTRAS):
    matchedValue: Optional[Union[ValueOriginalType, ReferenceValue]] = None
    isDynamic: Optional[bool] = None
    value: Optional[Union[str, ValueOriginalType, List[ValueItemIpPort], ReferenceValue]] = None
    nexthopList: Optional[List[Union[NexthopIp, NexthopInt]]] = None


class LogOptions(BaseModel, extra=PYDANTIC_EXTRAS):
    logStart: bool
    logEnd: bool


class DiscoveryOptions(BaseModel, extra=PYDANTIC_EXTRAS):
    logOptions: LogOptions


class Action(BaseSecurity, BaseModel, extra=PYDANTIC_EXTRAS):
    pathLookupOptions: Optional[Union[List[PathLookupOption], List[ValueItemIpPort], str]] = None
    chainName: Optional[str] = None
    discoveryOptions: Optional[DiscoveryOptions] = None


class MaskResult(BaseModel, extra=PYDANTIC_EXTRAS):
    mask: int
    result: int


class Right(BaseSecurity, BaseModel, extra=PYDANTIC_EXTRAS):
    value: Optional[Union[str, int, MaskResult, List[Union[str, int, ValueItem]]]] = None
    reference: Optional[Reference] = None


class LeftRight(BaseSecurity, BaseModel, extra=PYDANTIC_EXTRAS):
    left: Optional[HeaderField] = None
    operator: Optional[str] = None
    right: Optional[Right] = None
    category: Optional[str] = None
    reference: Optional[Reference] = None
    description: Optional[str] = None


class Group(LeftRight, BaseModel, extra=PYDANTIC_EXTRAS):
    group: str
    name: Optional[str] = None
    items: Optional[List[Union[LeftRight, Group]]] = None
    item: Optional[Union[LeftRight, Group]] = None


class Chain(BaseModel, extra=PYDANTIC_EXTRAS):
    chainName: str
    chainType: str
    checkType: str


class Test(LeftRight, BaseModel, extra=PYDANTIC_EXTRAS):
    group: Optional[str] = None
    items: Optional[List[Union[LeftRight, Group, Chain]]] = None


class Category(BaseModel, extra=PYDANTIC_EXTRAS):
    category: str
    operator: str
    original: str


class Rule(BaseSecurity, BaseModel, extra=PYDANTIC_EXTRAS):
    action: Action
    active: bool
    natEvaluationType: Optional[str] = None
    test: Union[Test, Chain, Category]
    uid: Optional[str] = None
    description: Optional[str] = None
    sequenceNumber: Optional[int] = None


class RuleChain(BaseSecurity, BaseModel, extra=PYDANTIC_EXTRAS):
    defaultAction: DefaultAction
    rules: List[Rule]
    hideInUi: Optional[bool] = False


class SetField(BaseSecurity, BaseModel, extra=PYDANTIC_EXTRAS):
    category: Optional[str] = None
    description: Optional[str] = None
    value: List[ValueItem]


class StringArray(BaseSecurity, BaseModel, extra=PYDANTIC_EXTRAS):
    value: List[str]


class String(BaseSecurity, BaseModel, extra=PYDANTIC_EXTRAS):
    value: str


class NamedValues(BaseModel, extra=PYDANTIC_EXTRAS):
    numberSet: Optional[Dict[str, SetField]] = None
    numberSetGroup: Optional[Dict[str, Union[SetField, ValueOriginalType]]] = None
    stringSet: Optional[Dict[str, SetField]] = None
    stringArray: Optional[Dict[str, StringArray]] = None
    string: Optional[Dict[str, String]] = None


class Machine(BaseModel, extra=PYDANTIC_EXTRAS):
    entryChainName: str
    ruleChains: Dict[str, RuleChain]
    namedTests: Optional[Dict[str, Union[LeftRight, Group]]] = None
    namedValues: Optional[NamedValues] = None


class Security(BaseModel, extra=PYDANTIC_EXTRAS):
    machineAcl: Optional[Machine] = None
    machineNat44: Optional[Machine] = None
    machinePbr: Optional[Machine] = None
    machineZones: Optional[Machine] = None
    zones: Optional[Dict[str, List[str]]] = None


class SecurityModel(BaseModel, extra=PYDANTIC_EXTRAS):
    hostname: str
    security: Security

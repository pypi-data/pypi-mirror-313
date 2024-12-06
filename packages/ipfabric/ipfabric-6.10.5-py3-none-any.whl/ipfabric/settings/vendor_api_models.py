import json
from typing import List, Union, Literal

from pydantic import field_validator, BaseModel, Field, AnyHttpUrl
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated

from ipfabric.tools import valid_slug

AWS_REGIONS = [
    "af-south-1",
    "ap-east-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-south-1",
    "ap-south-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-southeast-3",
    "ap-southeast-4",
    "ca-central-1",
    "eu-central-1",
    "eu-central-2",
    "eu-north-1",
    "eu-south-1",
    "eu-south-2",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "il-central-1",
    "me-central-1",
    "me-south-1",
    "sa-east-1",
    "us-east-1",
    "us-east-2",
    "us-gov-east-1",
    "us-gov-west-1",
    "us-west-1",
    "us-west-2",
]

URL = Annotated[AnyHttpUrl, AfterValidator(lambda x: str(x))]


class DefaultRateLimiterSettings(BaseModel):
    maxConcurrentRequests: int = 100000
    maxCapacity: int = 300
    refillRate: int = 10
    refillRateIntervalMs: int = 1000


class VendorAPI(BaseModel):
    """
    base Vendor API config
    """

    slug: str
    comment: str = ""
    isEnabled: bool = True

    @field_validator("slug")
    @classmethod
    def check_slug(cls, slug):
        return valid_slug(slug)


class SystemProxy(BaseModel):
    """
    support for Proxy Servers when utilizing Vendor APIs
    """

    respectSystemProxyConfiguration: bool = True


class RejectUnauthorized(SystemProxy, BaseModel):
    """
    support for credentials when utilizing Vendor APIs
    """

    rejectUnauthorized: bool = True


class UserAuthBaseUrl(BaseModel):
    """
    support for authentication when utilizing Vendor APIs
    """

    username: str
    password: str
    baseUrl: URL


class AssumeRole(BaseModel):
    role: str


class AWS(VendorAPI, SystemProxy, DefaultRateLimiterSettings, BaseModel):
    """
    AWS vendor api support
    """

    apiKey: str
    apiSecret: str
    regions: list
    assumeRoles: List[Union[str, dict, AssumeRole]] = Field(default_factory=list)
    type: Literal["aws-ec2"] = "aws-ec2"
    maxCapacity: int = 50

    @field_validator("regions")
    @classmethod
    def check_region(cls, regions):
        for r in regions:
            if r.lower() not in AWS_REGIONS:
                raise ValueError(f"{r} is not a valid AWS Region")
        return [r.lower() for r in regions]

    @field_validator("assumeRoles")
    @classmethod
    def check_roles(cls, roles):
        validated_roles = list()
        for role in roles:
            if isinstance(role, str):
                validated_roles.append(AssumeRole(role=role))
            elif isinstance(role, dict):
                if "role" in role:
                    validated_roles.append(AssumeRole(**role))
                else:
                    raise SyntaxError(f'Role {role} not in \'{{"role": "<arn:aws:iam::*****:role/*****>"}}\' format.')
            elif isinstance(role, AssumeRole):
                validated_roles.append(role)
        return validated_roles


class Azure(VendorAPI, SystemProxy, DefaultRateLimiterSettings, BaseModel):
    """
    Azure vendor api support
    """

    clientId: str
    clientSecret: str
    subscriptionId: str
    tenantId: str
    type: Literal["azure"] = "azure"
    maxConcurrentRequests: int = 1000


class CheckPointBase(VendorAPI, RejectUnauthorized, DefaultRateLimiterSettings, BaseModel):
    baseUrl: URL
    domains: List[str] = Field(default_factory=list)
    type: Literal["checkpoint-mgmt-api"] = "checkpoint-mgmt-api"
    maxConcurrentRequests: int = 1000


class CheckPointApiKey(CheckPointBase):
    """
    Checkpoint vendor api support
    """

    apiKey: str


class CheckPointUserAuth(CheckPointBase, UserAuthBaseUrl, BaseModel):
    """
    checkpoint authentication vendor api support
    """

    ...


class CiscoAPIC(VendorAPI, RejectUnauthorized, UserAuthBaseUrl, DefaultRateLimiterSettings, BaseModel):
    """
    Cisco APIC vendor api support
    """

    type: Literal["ciscoapic"] = "ciscoapic"
    maxConcurrentRequests: int = 10


class CiscoFMCBase(VendorAPI, RejectUnauthorized, DefaultRateLimiterSettings, BaseModel):
    type: Literal["ciscofmc"] = "ciscofmc"
    maxConcurrentRequests: int = 9
    maxCapacity: int = 110
    refillRate: int = 110
    refillRateIntervalMs: int = 60000


class CiscoFMC(CiscoFMCBase, UserAuthBaseUrl, BaseModel):
    """
    Cisco FMC User Auth Vendor API Support
    """

    ...


class CiscoFMCToken(CiscoFMCBase):
    """
    Cisco FMC Token Auth Vendor API Support
    """

    apiToken: str


class ForcePoint(VendorAPI, RejectUnauthorized, DefaultRateLimiterSettings, BaseModel):
    """
    ForcePoint vendor api support
    """

    authenticationKey: str
    baseUrl: URL
    type: Literal["forcepoint"] = "forcepoint"
    maxConcurrentRequests: int = 10


class GCPCredentials(BaseModel):
    """
    GCP Credentials
    """

    auth_provider_x509_cert_url: str
    auth_uri: str
    client_email: str
    client_id: str
    client_x509_cert_url: str
    private_key: str
    private_key_id: str
    project_id: str
    token_uri: str
    type: str
    universe_domain: str


class GCP(VendorAPI, RejectUnauthorized, BaseModel):
    """
    GCP vendor api support

    Args:
        credentialsJson: JSON File, Dictionary, or String of GCP Credentials
    """

    credentialsJson: Union[GCPCredentials, dict, str]
    type: Literal["gcp"] = "gcp"

    @field_validator("credentialsJson")
    @classmethod
    def validate_credentials(cls, credentials):
        if isinstance(credentials, dict):
            return GCPCredentials(**credentials)
        elif isinstance(credentials, str):
            try:
                with open(credentials, "r") as f:
                    return GCPCredentials(**json.load(f))
            except FileNotFoundError:
                try:
                    return GCPCredentials(**json.loads(credentials))
                except json.JSONDecodeError:
                    raise ValueError("credentialsJson must be a valid JSON file, JSON string or Python dictionary.")
        else:
            return credentials


class JuniperMist(VendorAPI, RejectUnauthorized, DefaultRateLimiterSettings, BaseModel):
    """
    Juniper Mist vendor api support
    """

    apiToken: str
    apiVer: Literal["v1"] = "v1"
    type: Literal["juniper-mist"] = "juniper-mist"
    baseUrl: URL = "https://api.mist.com"
    maxConcurrentRequests: int = 250


class Merakiv1(VendorAPI, RejectUnauthorized, DefaultRateLimiterSettings, BaseModel):
    """
    Meraki v1 vendor api support
    """

    apiKey: str
    baseUrl: URL
    organizations: List[str] = Field(default_factory=list)
    apiVer: Literal["v1"] = "v1"
    type: Literal["meraki-v0"] = "meraki-v0"
    maxCapacity: int = 10


class Prisma(VendorAPI, RejectUnauthorized, DefaultRateLimiterSettings, BaseModel):
    """
    Prisma vendor api support
    """

    username: str
    password: str
    tsgid: str
    type: Literal["prisma"] = "prisma"
    maxConcurrentRequests: int = 4


class RuckusVirtualSmartZone(VendorAPI, RejectUnauthorized, UserAuthBaseUrl, DefaultRateLimiterSettings, BaseModel):
    """
    Ruckus Virtual SmartZone vendor api support
    """

    apiVer: Literal["v9_1"] = "v9_1"
    type: Literal["ruckus-vsz"] = "ruckus-vsz"
    maxConcurrentRequests: int = 10


class SilverPeak(VendorAPI, RejectUnauthorized, UserAuthBaseUrl, DefaultRateLimiterSettings, BaseModel):
    """
    SilverPeak vendor api support
    """

    loginType: str = "Local"
    type: Literal["silverpeak"] = "silverpeak"
    maxConcurrentRequests: int = 5

    @field_validator("loginType")
    @classmethod
    def check_login(cls, login_type):
        if login_type not in ["Local", "RADIUS", "TACACS+"]:
            raise ValueError(f"{login_type} is not a valid login type must be in ['Local', 'RADIUS', 'TACACS+']")
        return login_type


class Versa(VendorAPI, RejectUnauthorized, UserAuthBaseUrl, DefaultRateLimiterSettings, BaseModel):
    """
    Versa vendor api support
    """

    paginationLimit: int = 1000
    type: Literal["versa"] = "versa"
    combinedDiscovery: bool = True
    maxConcurrentRequests: int = 10
    maxCapacity: int = 100
    refillRate: int = 2


class Viptela(VendorAPI, RejectUnauthorized, UserAuthBaseUrl, DefaultRateLimiterSettings, BaseModel):
    """
    Viptela vendor api support
    """

    type: Literal["viptela"] = "viptela"
    combinedDiscovery: bool = True
    maxConcurrentRequests: int = 25


class NSXT(VendorAPI, RejectUnauthorized, UserAuthBaseUrl, BaseModel):
    """
    NSXT vendor api support
    """

    type: Literal["nsxT"] = "nsxT"
    maxConcurrentRequests: int = 40
    maxCapacity: int = 100
    refillRate: int = 50

# IP Fabric 

IPFabric is a Python module for connecting to and communicating against an IP Fabric instance.

***For full documentation please see [IP Fabric Documentation Portal](https://docs.ipfabric.io/main/integrations/python/).***

## IP Fabric

[IP Fabric](https://ipfabric.io) is a vendor-neutral network assurance platform that automates the 
holistic discovery, verification, visualization, and documentation of 
large-scale enterprise networks, reducing the associated costs and required 
resources whilst improving security and efficiency.

It supports your engineering and operations teams, underpinning migration and 
transformation projects. IP Fabric will revolutionize how you approach network 
visibility and assurance, security assurance, automation, multi-cloud 
networking, and trouble resolution.

**Integrations or scripts should not be installed directly on the IP Fabric VM unless directly communicated from the
IP Fabric Support or Solution Architect teams.  Any action on the Command-Line Interface (CLI) using the root, osadmin,
or autoboss account may cause irreversible, detrimental changes to the product and can render the system unusable.**

## Bugs

A bug has been identified when ~2,000 requests are being made to the API.  The underlining issue seems to be with the
implementation of `http2`. The workaround is to set `http2=False` in the `IPFClient` class.  Example error:

`httpx.RemoteProtocolError: <ConnectionTerminated error_code:ErrorCodes.NO_ERROR, last_stream_id:1999, additional_data:None>`

## Upcoming Deprecation Notices

**In `ipfabric>=v7.1.x` Python 3.8 will be removed as a supported version as it is now 
[End of Life](https://devguide.python.org/versions/) as of 2024-10-07.**

In `ipfabric>=v7.0.0` the following will be changed/deprecated:

- All classes including `IPFClient()` will switch to keyword only arguments to support Pydantic BaseModel.
  - `IPFClient('https//url')` -> `IPFClient(base_url='https//url')`
- `IPFClient().intent.intent_by_name()` will be removed and is replaced by `IPFClient().intent.intents_by_name()`
- The following endpoints were moved and the old methods will be removed:
  - `Technology.LoadBalancing.virtual_servers_f5_partitions` -> `Technology.LoadBalancing.partitions`
  - `Technology.Sdwan.sites` -> `Technology.Sdwan.versa_sites`
  - `Technology.Sdwan.links` -> `Technology.Sdwan.versa_links`

## Versioning

Semantic Versioning: `Major.Minor.Patch`

Starting with IP Fabric version 5.0.x the `ipfabric` SDK is recommended to match your IP Fabric major and minor version.  
We will try to keep some backwards compatability (SDK version `6.9.x` should work with IP Fabric API `6.8`) however new 
features may break some functionality.  By ensuring that your `ipfabric` SDK's match your IP Fabric major and minor  
version will ensure compatibility and will continue to work.

The Patch version of the SDK is used for bug fixes and new features that are compatible with the major and minor version.

## Defaulted to Streaming Data

See [Notices](NOTICES.md) for full information.

* GET URL is limited to 4096 characters.
  * Complex queries and filters could go over this limit; however in testing it was very difficult to reach this.
* CSV Export
  * Only supported with a streaming GET request and return a bytes string of data in the Python SDK.
  * It will also convert times to human-readable format.
  * **`reports` (returning Intent Check data) is not supported with CSV export, however is required when filtering based on Intents (colors).**

```python
from ipfabric import IPFClient
ipf = IPFClient(streaming=True)

dev = ipf.inventory.devices.all()
print(type(dev))  # list 

dev_csv = ipf.fetch_all('tables/inventory/devices', export='csv')
print(type(dev_csv))  # bytes 

# Timezone can be changed for CSV export; see `ipfabric.tools.shared.TIMEZONES`
dev_csv_tz = ipf.inventory.devices.all(export='csv', csv_tz='UTC')

# If specifying to return reports and CSV request will drop reports input and use GET
dev_csv_reports = ipf.fetch_all('tables/inventory/devices', reports=True, export='csv')
"""CSV export does not return reports, parameter has been excluded."""
print(type(dev_csv_reports))  # bytes

# If URL exceeds 4096 characters the following exception will be raised:
# raise InvalidURL(f"URL exceeds max character limit of 4096: length={len(url)}.")
```

## Installation

```
pip install ipfabric
```

To use `export='df'` on some methods please install `pandas` with `ipfabric`

```
pip install ipfabric[pd]
```

## Introduction

Please take a look at [API Programmability - Part 1: The Basics](https://ipfabric.io/blog/api-programmability-part-1/)
for instructions on creating an API token.

Most of the methods and features can be located in [Examples](examples) to show how to use this package. 
Another great introduction to this package can be found at [API Programmability - Part 2: Python](https://ipfabric.io/blog/api-programmability-python/)

## Authentication

### Username/Password

Supply in client:
```python
from ipfabric import IPFClient
ipf = IPFClient('https://demo3.ipfabric.io/', auth=('user', 'pass'))
```

### Token

```python
from ipfabric import IPFClient
ipf = IPFClient('https://demo3.ipfabric.io/', auth='token')
```

### Environment 

The easiest way to use this package is with a `.env` file.  You can copy the sample and edit it with your environment variables. 

```commandline
cp sample.env .env
```

This contains the following variables which can also be set as environment variables instead of a .env file.
```
IPF_URL="https://demo3.ipfabric.io"
IPF_TOKEN=TOKEN
IPF_VERIFY=true
```

Or if using Username/Password:
```
IPF_URL="https://demo3.ipfabric.io"
IPF_USERNAME=USER
IPF_PASSWORD=PASS
```

## Development

### Poetry Installation

IPFabric uses [Poetry](https://pypi.org/project/poetry/) to make setting up a virtual environment with all dependencies
installed quick and easy.

Install poetry globally:
```
pip install poetry
```

To install a virtual environment run the following command in the root of this directory.

```
poetry install
```

To run examples, install extras:
```
poetry install ipfabric -E examples
```

### Test and Build

```
poetry run pytest
poetry build
```

Prior to pushing changes run:
```
poetry run black ipfabric
poetry update
```

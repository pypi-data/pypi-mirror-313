# NAble Data Extraction API wrapper/Library

This is a Python wrapper/library for the NAble Data Extraction API.  The NAble API returns data in xml format, this tool will convert those to lists and dictionaries for ease of use.

The official API documentation from NAble can be found [here](https://documentation.n-able.com/remote-management/userguide/Content/api_calls.htm). I have tried to keep my naming scheme similar to theirs.

NOTE:  
- This is still in extremely early stages of development, function names may change! 
- Most functions have docstrings, but proper documentation has not yet been created.

## Table Of Contents
*I don't know how to make this yet, so it's Coming Soon*


## Installation

```
pip install NAbleAPI
```

## Getting Started

To use the NAble API, you will need to know your region and have an API key.

1. Download the package (this entire github) and extract it.
2. Get an API key. Follow [these instructions](https://documentation.n-able.com/remote-management/userguide/Content/api_key.htm) to get your API key.
3. Find your region (see below)


### Regions

To find your region, check [this page](https://documentation.n-able.com/remote-management/userguide/Content/determine_url.htm) or view table below. 

Notes: 
- Not all regions have been tested, if your region is marked 'untested' on the table below, please let me know whether it works.
- If your dashboard URL starts with `www2`, assume it is just `www` for the region.
- If there is another abbreviation or country code you would like added, let me know!

| Dashboard URL | Region | Status |
| --- | --- | --- |
| www.am.remote.management | americas, ams | Untested |
| wwwasia.system-monitor.com | asia | Untested |
| www.system-monitor.com | australia, au, aus | Untested |
| wwweurope1.systemmonitor.eu.com | europe, eu | Untested |
| wwwfrance.systemmonitor.eu.com | france, fr | Untested |
| wwwfrance1.systemmonitor.eu.com | france1, fr1 | Untested |
| wwwgermany1.systemmonitor.eu.com | germany, de, deu | Untested |
| wwwireland.systemmonitor.eu.com | ireland, ie, irl | Untested |
| wwwpoland1.systemmonitor.eu.com | poland, pl,pol | Untested |
| www.systemmonitor.co.uk | united kingdom, uk, gb, gbr | **Verified** |
| www.systemmonitor.us | united states, us, usa | Untested |

### Using the package


#### Create a new .py file in the root directory and import the NAble package
```
from NAbleAPI import NAble
```

#### Authenticate with your API key
```
na = NAble('[YOUR REGION]','[YOUR API KEY]')
```

Example

```
na = NAble('uk','f821213a8d3q43843dj39824')
```

(Not a real API key, don't try to use it)


#### Make your first request
Gee it sure would be helpful is there was documentation for the available commands.  Unfortunately, there isn't right now.

Get all your clients

```
myNAbleClients = na.clients()
```


#### Storing your key
It's probably best not to store your API key in your script. Instead, you can create a .env file and use that.

1. Create a new file called `.env` in the root directory
2. Put your API key in it (do not put it in quotes, type exactly as shown below)
```
NABLE_KEY = f821213a8d3q43843dj39824
```
3. Get the key from file
``` 
from NAbleAPI import NAble # Import the NAble package
import os # Import OS package (built into Python, I'm like 99% sure)

NABLE_KEY = os.getenv("NABLE_KEY")

na = NAble('uk',NABLE_KEY)
```

## API Endpoints
The endpoints are grouped by category on NAble's website, so I have done the same below.
I found the names on NAbles site to be a bit long, so I have shortened them a bit. The `Function Name` is what you will use in Python.
I'm doing my best to get them all added!



### Clients, SItes, and Devices 
Official NAble documentation page [here](https://documentation.n-able.com/remote-management/userguide/Content/devices.htm)
| Service | Status | Function Name | Description |
| --- | --- | --- | --- |
| list_clients | Working | clients() | List all clients |
| list_sites | Working | sites() | List sites for a client |
| list_servers | Working | servers() | list servers at a site |
| list_workstations | Working | workstations() | list workstations at a site |
| list_agentless_assets | Working | agentlessAssets() | List agentless assets at a site |
| list_devices_at_client | Working | clientDevices() | List all workstations or servers for a client |
| list_device_monitoring_details | Working | deviceDetails() | Get details for a single device | 
| add_client | Planned | addClient() | Add a client |
| add_site | Planned | addSite() | Add a site | 
| get_site_installation_package() | Partially Working | siteInstallPackage | Create/Get a site installation package (returns rawbytes right now) |

### Checks and results
Official NAble documentation page [here](https://documentation.n-able.com/remote-management/userguide/Content/checks_and_results.htm)
| Service | Status | Function Name | Description |
| --- | --- | --- | --- |
| list_checks | Working | checks() |  List all checks for a device |
| list_failing_checks | Working | failingChecks() | List all failing checks |
| list_check_config | Working | checkConfig() | Get a single checks configuration |
| get_formatted_check_output | Working | formattedCheckOutput() | Get first line of check result |
| list_outages | Working | checks() | List all outages for a device |
| list_performance_history | Untested | performanceHistory() |  Get performance history of a device |
| list_drive_space_history | Working | driveSpaceHistory() |  Get Device Storage History |
| list_exchange_storage_history | Untested | exchangeStorageHistory() | Get Exchange Storage History |
| clear_check | Untested | clearCheck() |  Clear a check |
| add_check_note | Working | addNote() |  Add note to a check |
| list_templates | Untested | templates() |  List all server/workstation monitoring templates |

### Anti-Virus Update Check Information
Official NAble documentation page [here](https://documentation.n-able.com/remote-management/userguide/Content/api_av_info.htm)
| Service | Status | Function Name | Description |
| --- | --- | --- | --- |
| list_supported_av_products | Working | supportedAVs() | Lists supported AVs |
| list_av_definitions | Working | AVDefinitions() | Get definitions for specific AV Product |
| get_av_definition_release_date | Working | AVDefinitionsReleaseDate() | Get release date of specific AV version |
| list_av_history | Working | AVHistory() | List last 60s of AV status (I got 90 though...) |

### List Backup Check History
Official NAble documentation page [here](https://documentation.n-able.com/remote-management/userguide/Content/list_backup_history.htmm)
PLANNED

### Asset Tracking Information
Official NAble documentation page [here](https://documentation.n-able.com/remote-management/userguide/Content/asset_tracking_information.htm)
PLANNED

### Settings
Official NAble documentation page [here](https://documentation.n-able.com/remote-management/userguide/Content/settings.htm)
PLANNED

### Patch Management
Official NAble documentation page [here](https://documentation.n-able.com/remote-management/userguide/Content/patch_management.htm)
PLANNED

### Managed Anti-Virus
Official NAble documentation page [here](https://documentation.n-able.com/remote-management/userguide/Content/managed_antivirus2.htm)
PLANNED

### Backup & Recovery
Official NAble documentation page [here](https://documentation.n-able.com/remote-management/userguide/Content/api_mob_over.htm)
PLANNED

### Run Task Now
Official NAble documentation page [here](https://documentation.n-able.com/remote-management/userguide/Content/run_task_now.htm)
PLANNED

### List Active Directory Users
Official NAble documentation page [here](https://documentation.n-able.com/remote-management/userguide/Content/list_active_directory_users.htm)
PLANNED


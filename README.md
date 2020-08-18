# GVE_DevNet_Meraki_Device_Editor
script that reads from an Excel file and changes the network, name, location and tags for a set of Meraki devices 





## Contacts
* Jorge Banegas

## Solution Components
* Meraki python SDK
* Excel python SDK (xlrd library)

## Installation/Configuration
- To the install the dependencies, use pip

```
pip install -r requirements.txt
```

- After installing the dependendencies, make sure to generate an Excel file with the appropriate info. Reference the provided file for the format. 

- In the config file, include your Meraki API key, latitude/longitude of the devices (1 location for all), and the organization ID of interest (https://developer.cisco.com/meraki/api/#!get-organizations)

```python
# API key from the Meraki dashboard
MERAKI_DASHBOARD_API_KEY = ''

```

- Last, run the script and enter the file name as an input. Example below

```
python3 main.py filename.xlsx
```

# Screenshots

- Meraki Device configuration before executing script

![/IMAGES/0image.png](/IMAGES/before_script.png)

- Script execution

![/IMAGES/0image.png](/IMAGES/execution.png)

- Meraki Device configuration after executing script

![/IMAGES/0image.png](/IMAGES/after_script.png)



### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.

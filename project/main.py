""" Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import meraki
import xlrd
import credentials
import logging
import sys

# function to return the networkid based of the name
def return_network_id(name):
    global networks

    for network in networks:
        if network["name"] == name:
            return network["id"]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("meraki_script.log"),
        logging.StreamHandler()
    ]
)

log_str = '*'*15 + ' New Script Run ' + '*'*15
logging.info('')
logging.info('*' * len(log_str))
logging.info(log_str)
logging.info('*' * len(log_str))
logging.info('')

# get the file name
try:
    excel_file = sys.argv[1]
except IndexError:
    logging.error('Excel Filename missing from CLI arguments!!')
    logging.error(
        'Syntax should be "python.exe .update_meraki_ap_names.py '
        'excel_file_in_same_directory.csv"')
    quit(1)

dashboard = meraki.DashboardAPI(api_key=credentials.meraki_api_key, print_console=False,output_log=False)

my_orgs = dashboard.organizations.getOrganizations()

for org in my_orgs:
    print("Org name: ", org["name"],"Org ID: ", org["id"])

input_org_id = input("Enter Organization ID: ")

networks = dashboard.organizations.getOrganizationNetworks(organizationId=input_org_id)



# read the workbook, we'll just use the first sheet only
wb = xlrd.open_workbook(excel_file)
sheet = wb.sheet_by_index(0)

# find the column numbers for the serial, network, and tags

for i in range(sheet.ncols):
    if sheet.cell_value(0, i).lower() == 'serial':
        sn_col = i
    elif sheet.cell_value(0, i).lower() == 'network':
        network_col = i
    elif sheet.cell_value(0, i).lower() == 'tags':
        tags_col = i
    elif sheet.cell_value(0, i).lower() == 'name':
        names_col = i
    elif sheet.cell_value(0, i).lower() == 'lat':
        lat_col = i
    elif sheet.cell_value(0, i).lower() == 'long':
        long_col = i

# add all the entries to a list of dictionaries to reference later
ap_list = []

for i in range(1, sheet.nrows):
    ap = {}

    ap["serial"] = sheet.cell_value(i, sn_col)
    ap["network"] = sheet.cell_value(i, network_col)
    ap["tags"] = sheet.cell_value(i, tags_col)
    ap["name"] = sheet.cell_value(i, names_col)
    ap["lat"] = sheet.cell_value(i, lat_col)
    ap["lng"] = sheet.cell_value(i, long_col)

    ap_list.append(ap)

for row in ap_list:
    # update the device's tags
    tags = row["tags"].split(",")
    print(row)
    dashboard.devices.updateDevice(serial=row["serial"],tags=tags,name=row["name"],lat=row["lat"],lng=row["lng"])


    network_id = return_network_id(row["network"])
    try:
        dashboard.networks.claimNetworkDevices(networkId=network_id,serials=[row["serial"]])
    except:
        # if claiming fails, remove device from existing network and try again 
        device = dashboard.devices.getDevice(serial=row["serial"])
        dashboard.networks.removeNetworkDevices(networkId=device["networkId"],serial=row["serial"])
        dashboard.networks.claimNetworkDevices(networkId=network_id,serials=[row["serial"]])

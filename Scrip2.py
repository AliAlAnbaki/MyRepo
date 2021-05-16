#! /usr/bin/env python
"""
script showing how to create network configurations by combining data from CSV files with Jinja templates.
Expected output 
----------------------
!
interface Ethernet1/15
  description Link to esxi-01 port nic 0 for Host1
  switchport
  switchport mode trunk
  no shutdown
  

!
interface Ethernet1/16
  description Link to esxi-01 port nic 1 for Host2
  switchport
  switchport mode trunk
  no shutdown
  

!
interface Ethernet1/17
  description Link to esxi-01 port nic 2 for Host3
  switchport
  switchport mode trunk
  no shutdown
  

!
interface Ethernet1/18
  description Link to esxi-01 port nic 3 for Host4
  switchport
  switchport mode trunk
  no shutdown
  

!
interface Ethernet1/19
  description Link to db-01 port nic 0 for Database Server1
  switchport
  switchport mode access
  switchport access vlan 100
  spanning-tree port type edge
  no shutdown
  

!
interface Ethernet1/20
  description Link to db-01 port nic 1 for Database Server2
  switchport
  switchport mode access
  switchport access vlan 100
  spanning-tree port type edge
  no shutdown
  

!
interface Ethernet1/21
  description Link to dev-db-01 port nic 0 for Database Server1
  switchport
  switchport mode access
  switchport access vlan 101
  spanning-tree port type edge
  no shutdown
  

!
interface Ethernet1/22
  description Link to dev-db-01 port nic 1 for Database Server2
  switchport
  switchport mode access
  switchport access vlan 101
  spanning-tree port type edge
  no shutdown
  

!
interface Ethernet1/23
  description Link to admin-01 port nic 0 for Admin Server1
  switchport
  switchport mode access
  switchport access vlan 102
  spanning-tree port type edge
  no shutdown
  

!
interface Ethernet1/24
  description Link to admin-01 port nic 2 for Admin Server2
  switchport
  switchport mode access
  switchport access vlan 102
  spanning-tree port type edge
  no shutdown
  

!
interface Ethernet1/25
  description Link to server-01 port nic 0 for App Server1
  switchport
  switchport mode access
  switchport access vlan 103
  spanning-tree port type edge
  no shutdown
  

!
interface Ethernet1/26
  description Link to server-01 port nic 1 for App Server2
  switchport
  switchport mode access
  switchport access vlan 103
  spanning-tree port type edge
  no shutdown
  

"""

import csv
from jinja2 import Template
from netmiko import ConnectHandler

source_file = "ports.csv"
interface_template_file = "config_template.j2"

# Sandbox Nexus 9000 switch to send configuration or you can use any switch has connectvity
device = {
             "address": "sbx-nxos-mgmt.cisco.com",#hostname or ip addrees of switch
             "device_type": "cisco_nxos",
             "ssh_port": 8181,
             "username": "admin",
             "password": "Admin_1234!"
            }


#  place holder for full configuration
interface_configs2 = ""

# Open the J2 file  and create a J2 Object
with open(interface_template_file) as f:
    interface_template = Template(f.read(), keep_trailing_newline=True)

# Open up the CSV file containing the data
with open(source_file) as f:
# Use DictReader to access data from CSV
    reader = csv.DictReader(f)
# For each row in the CSV, generate an interface configuration using the jinja template
    for row in reader:
        interface_config = interface_template.render(
            interface = row["Interface"],
            vlan = row["VLAN"],
            server = row["Server"],
            link = row["Link"],
            purpose = row["Purpose"]
        )

 # Append this interface configuration to the full configuration
        interface_configs2 += interface_config

## Save the final configuraiton to a file
with open("interface_configs2.txt", "w") as f:
    f.write(interface_configs2)

# Use Netmiko to connect to the device and send the configuration
with ConnectHandler(ip = device["address"],
                    port = device["ssh_port"],
                    username = device["username"],
                    password = device["password"],
                    device_type = device["device_type"]) as ch:

    config_set = interface_configs2.split("\n")
    output = ch.send_config_set(config_set)
    print(output)

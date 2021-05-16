 #! /usr/bin/env python
"""
Script to create network config by using CSV files with Jinja templates.
Expected OUtput
------------------------
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
# importing modules
import csv
from jinja2 import Template


# Assign var to CSV file and J2 file
source_file = "ports.csv"
interface_template_file = "config_template.j2"

# place holder for full configuration
interface_configs = ""

# Open the J2 file  and create a J2 Object
with open(interface_template_file) as f:
    interface_template = Template(f.read(), keep_trailing_newline= True)

# Open the CSV file
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
# Append interface configuration to the full configuration
        interface_configs += interface_config

# Save the final configuraiton to interface_configs
with open("interface_configs.txt", "w") as f:
    f.write(interface_configs)

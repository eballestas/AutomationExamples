# Automation CheatSheet eballest
------------------------------------------------------------------------------------------------------------------------
## Python Libraries
from  jin
from netmiko import ConnectHandler
import csv
from jinja2 import Template

### get time
from datetime import datetime
now = datetime.now()
year = now.year 
month = now.month
day = now.day

## General File parsing

### Open a csv file
source_file = 'switch-ports.csv'
with open(source_file) as f:
    reader = csv.DictReader(f)

### Open a Jinja2 Template
interface_template = 'switchport-interface-template.j2'
with open(interface_template) as f:
    interface_template = Template(f.read(), keep_trailing_newline=True)

### open to a file
with open('file_name') as f:
    f.read(output)

### Write to a file
with open('file_name', 'w') as f:
    f.write(output)

------------------------------------------------------------------------------------------------------------------------

## Netmiko
### Type of devices:

    - "cisco_asa": CiscoAsaSSH,
    - "cisco_ftd": CiscoFtdSSH,
    - "cisco_ios": CiscoIosSSH,
    - "cisco_nxos": CiscoNxosSSH,
    - "cisco_s300": CiscoS300SSH,
    - "cisco_tp": CiscoTpTcCeSSH,
    - "cisco_wlc": CiscoWlcSSH,
    - "cisco_xe": CiscoIosSSH,
    - "cisco_xr": CiscoXrSSH,

------------------------------------------------------------------------------------------------------------------------
## Connect to a device using netmiko

### Simple Connection
from netmiko import Netmiko

connection = Netmiko(host = "10.122.188.197", port="22" , username="admin" , password="cisco!123", device_type= "cisco_ios")

output= connection.send_command("show version")
print(output)
connection.disconnect()

------------------------------------------------------------------------------------------------------------------------
### Connection using a Dictionary

from netmiko import ConnectHandler

cisco_device = {
    'device_type': 'cisco_ios',
    'host': '10.122.188.197',
    'username': 'admin',
    'password': 'cisco!123',    #Can be replaced with getpass.getpass(), from getpass import getpass
    'port': '22',               #optional default 22
    'secret': 'cisco!123',      #optional default ''
    'verbose': True             #optional default False
}

connection = ConnectHandler(**cisco_device)
output = connection.send_command('show int | in input rate|output rate|is up')
connection.disconnect()

------------------------------------------------------------------------------------------------------------------------
### connect to a device using a file as a ip source

with open('routerIP.txt') as f:
    router_list = f.read().splitlines()
 
for routers in router_list:
    print ('Connecting to device" ' + routers)
    ios_device = {
    'device_type': 'cisco_ios',
    'host': 'routers',
    'username': 'admin',
    'password': 'password'
    }

connection = ConnectHandler(**ios_device)  
output=net_connect.send_config_set(commands_list)
print(output)

------------------------------------------------------------------------------------------------------------------------

## find prompt

### Run priviledge commands
hostname =  connection.find_prompt()
if '>' in hostname:
connection.enable()
output = connection.send_command('show run')
print(output)

### change to config mode
connection.config_mode()
connection.send_command('user eballest password cisco')
connection.exit_config_mode()


### send commands on config mode using a list 
connection.enable()
connection.config_mode()

commands = ['interface lo0','ip add 1.1.1.1 255.255.255.255','exit','do wr']
connection.send_config_set(commands)
print(commands)
print(connection.find_prompt())

### send commands and receive them on FSM
output = connection.send_command('show ip int br | ex una', use_textfsm=True)
list1 = [(interface.get('intf', 'NA'),interface.get('status', 'NA')) for interface in output]

## Jinja 2 Templates


! Generated Configuration
interface {{ interface }}
  description Link to {{ server }} port {{ link }} for {{ purpose }}
  switchport
  {% if vlan == "trunk" -%}
  switchport mode trunk
  {% else -%}
  switchport mode access
  switchport access vlan {{ vlan }}
  spanning-tree port type edge
  {% endif -%}
  no shutdown

### Jinja2 templating + python(netmiko) + CSV

import csv
from jinja2.environment import Template
from netmiko import ConnectHandler


source_file = 'switch-ports.csv'
interface_template = 'switchport-interface-template.j2'

interface_configs = ''


with open(interface_template) as f:
    interface_template = Template(f.read(), keep_trailing_newline=True)
    
with open(source_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        interface_config = interface_template.render(
        interface = row["Interface"],
        vlan = row["VLAN"],
        server = row["Server"],
        link = row["Link"],
        purpose = row["Purpose"],
        hostname = row["Switch"]
        )
        interface_configs += interface_config
    print(interface_configs)
        
<!-- with open('interface_configuration.txt', 'w') as f:
    f.write(interface_configs)
     -->
<!-- 
<Connection handler block> -->

    config_set = interface_configs.split("\n")
    output = connection.send_config_set(config_set)
    print(output)


import sys


def pytail(arguments):
    with open(arguments[0]) as f:
        if len(arguments) > 1:
            lines = f.readlines()[-int(arguments[1]):]
        else:
            lines = f.readlines()[-10:]
    for line in lines:
        print(line)
    
pytail(sys.argv[1:])
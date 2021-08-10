import csv
from jinja2 import Template
from netmiko import ConnectHandler

"""
Script that creates interface configuration for a cisco device based on a CSV file 'switch-ports.csv'    
"""

interfaceConfigurations = ''

### Open a Jinja2 Template
interface_template = 'interfaceConfiguration.j2'
with open(interface_template) as f:
    interface_template = Template(f.read(), keep_trailing_newline=True)

### Open a csv file and render the jinja2 template
source_file = 'switch-ports.csv'
with open(source_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        interfaceConfig = interface_template.render(
            interface = row['Interface'],
            server = row['Server'],
            link = row['Link'],
            purpose = row['Purpose'],
            vlan = row['VLAN']
        )
        interfaceConfigurations += interfaceConfig # appending the configuration to a str variable
        
### Write to a file
with open('interfaceConfigurations', 'w') as f: # sending the configuration to a text file for later review
    f.write(interfaceConfigurations)

## Conections values for one switch, if required to connect to multiple devices, create a list of dict lista = [dict1,dict2,dict3]
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

config_set = interfaceConfigurations.split("\n")
output = connection.send_config_set(config_set)
connection.disconnect()
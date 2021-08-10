from typing import OrderedDict
from netmiko import ConnectHandler
from tabulate import tabulate

cisco_device = {
    'device_type': 'cisco_ios',
    'host': '10.122.188.197',
    'username': 'admin',
    'password': 'cisco!123',
    'port': '22',               #optional default 22
    'secret': 'cisco!123',      #optional default ''
    'verbose': True             #optional default False
}

connection = ConnectHandler(**cisco_device)
output = connection.send_command('show interface ', use_textfsm=True )    # filtering information to a list, as textfsm collects unnecesary info
output = sorted(output, key = lambda i: i['input_packets'], reverse=True) # key = lambda i: i['input_packets'] can be replaced with itemgetter
print( tabulate(output, headers='keys', tablefmt="pipe"),)                # print a table with tabulate
    
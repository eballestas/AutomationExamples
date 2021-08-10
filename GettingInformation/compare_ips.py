import operator
from netmiko import ConnectHandler
from getpass import getpass
"""
Using netmiko to get information from a device + getpass
show ip interface brief on a Cisco Switch
"""

cisco_device = {
    'device_type': 'cisco_ios',
    'host': '10.122.188.197',
    'username': 'admin',
    'password': getpass(),      #getpass implementation ** getpass requests the info without echoing back **
    'port': '22',               #optional default 22
    'secret': 'cisco!123',      #optional default ''
    'verbose': True             #optional default False
}

connection = ConnectHandler(**cisco_device)
output = connection.send_command('show ip int br | ex una', use_textfsm=True) # FSM implementation 

lista = [(row.get('intf','NA'),row.get('ipaddr','NA')) for row in output] # filtering information to a list, as textfsm collects unnecesary info

sortedList = sorted(lista, key=operator.itemgetter(1), reverse=True) # the  key=operator.itemgetter(1) can be replaced with a lambda func
print(f'Highest interface is {sortedList[0][0]} with ip address {sortedList[0][1]}')
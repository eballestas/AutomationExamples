
from netmiko import ConnectHandler
import pprint

"""
Script to  collect information from a switch using textfsm with netmiko
'show interface switchport' is the command send to the switch
"""

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
connection.enable()
output = connection.send_command('show interface switchport', use_textfsm = True) 

print('\n')
print("{:<15} {:<8} {:<13}".format('Int:', 'Vlan:', 'Mode:')) # can be replaced with tabulate
print('-----------------------------------------------')      # Printing with formating
for row in output:
        print("{:<15} {:8} {:<13}".format(row['interface'], row['access_vlan'],row['admin_mode']))

connection.disconnect()


from netmiko import ConnectHandler
from off_switch_functions import Get_Switch_List
import time

#Grabs a config given a text file
def grabconfigtxt(txt_file_name):
    
    print("Username: ")
    username = input()
    print("Password: ")
    password = input()

    switch_list = Get_Switch_List(f"{txt_file_name}.txt")

    '''
    Example of switch input for netmiko:

    switch_details = {
        'device_type' : 'cisco_ios',
        'host' : '10.120.250.99', #Subject to current switch in list
        'username' : username,
        'password' : password,
        'port' : 22,
    }
    '''

    for switch in switch_list:
        switch_details = {
        'device_type' : 'cisco_ios',
        'host' : switch,
        'username' : username,
        'password' : password,
        'port' : 22,
        }
        
        net_connect = ConnectHandler(**switch_details)
        
        #print(f"\n For {switch_details['host']}")
        switch_hostname = (net_connect.send_command('show conf | include hostname').split()[1])
        conf_output = net_connect.send_command('show conf')
        #print(conf_output)
        
        print(f"Working on: {switch_hostname}\n")
        switch_txt = open(f"{switch_hostname}.txt", "w")
        switch_txt.write(conf_output)
        switch_txt.close()
        print(f"Completed: {switch_hostname}\n")
        
        time.sleep(1) #As to not attempt to make every connection in half a second...
        print("---------------------\n Finished")
        
#Grabs a config given an ip address
def grabconfigip(switch_ip):
        
    print("Username: ")
    username = input()
    print("Password: ")
    password = input()

    '''
    Example of switch input for netmiko:

    switch_details = {
        'device_type' : 'cisco_ios',
        'host' : '10.120.250.99', #Subject to current switch in list
        'username' : username,
        'password' : password,
        'port' : 22,
    }
    '''
    switch_details = {
    'device_type' : 'cisco_ios',
    'host' : switch_ip,
    'username' : username,
    'password' : password,
    'port' : 22,
    }
    
    net_connect = ConnectHandler(**switch_details)
        
    #print(f"\n For {switch_details['host']}")
    switch_hostname = (net_connect.send_command('show conf | include hostname').split()[1])
    conf_output = net_connect.send_command('show conf')
    #print(conf_output)
        
    print(f"Working on: {switch_hostname}\n")
    switch_txt = open(f"{switch_hostname}.txt", "w")
    switch_txt.write(conf_output)
    switch_txt.close()
    print(f"Completed: {switch_hostname}\n")
        
    print("---------------------\n Finished")
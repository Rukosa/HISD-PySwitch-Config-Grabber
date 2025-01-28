from netmiko import ConnectHandler
import ipaddress   
import time

#Returns the connection details of a switch given the IP.
def switch_connect(switch_ip):
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
    
    return switch_details


#Grabs a config given a text file
def grabconfigtxt(txt_file_name):
    switch_list = Get_Switch_List(f"{txt_file_name}.txt")

    for switch_ip in switch_list:
        if not check_ip(switch_ip):
            print(f"IP {switch_ip} is invalid... Skipping...")
            continue
        
        net_connect = ConnectHandler(**switch_connect(switch_ip))
        
        switch_hostname = (net_connect.send_command('show conf | include hostname').split()[1])
        conf_output = net_connect.send_command('show conf')
        #print(conf_output)
        
        #File write
        print(f"Working on: {switch_hostname}\n")
        switch_txt = open(f"{switch_hostname}.txt", "w")
        switch_txt.write(conf_output)
        switch_txt.close()
        print(f"Completed: {switch_hostname}\n")
        
        time.sleep(1) #As to not attempt to make every connection in half a second...
        print("---------------------\n Finished")
        
#Grabs a config given an ip address
def grabconfigip(switch_ip):
    net_connect = ConnectHandler(**switch_connect(switch_ip))
        
    switch_hostname = (net_connect.send_command('show conf | include hostname').split()[1])
    conf_output = net_connect.send_command('show conf')
    #print(conf_output)
    
    #File write   
    print(f"Working on: {switch_hostname}\n")
    switch_txt = open(f"{switch_hostname}.txt", "w")
    switch_txt.write(conf_output)
    switch_txt.close()
    print(f"Completed: {switch_hostname}\n")
        
    print("---------------------\n Finished")
    
    
#dumps config given the ip address
def dumpconfig(switch_ip, txt_file_name):
    net_connect = ConnectHandler(**switch_connect(switch_ip))
    switch_hostname = (net_connect.send_command('show conf | include hostname').split()[1])

    print(f"Dumping config on: {switch_hostname}\n")
    net_connect.send_config_from_file(txt_file_name)
    net_connect.send_command("wr mem")
    print(f"Config successfully dumped on: {switch_hostname}\n")


#Makes a list of ip addresses from a text file
def Get_Switch_List(txt_file):
    switch_txt = open(txt_file, "r")
    switches = ""
    
    for line in switch_txt:
        switches = switches + line
    switch_txt.close()

    switch_list = switches.splitlines()
    return switch_list
    #print(switch_list)
    
#Checks if ip address is valid
def check_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        print("Invalid IP address")
        return False
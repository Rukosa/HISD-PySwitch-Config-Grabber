from netmiko import ConnectHandler
import ipaddress   
import time
import getpass

#Returns the connection details of a switch given the IP.
def switch_connect(switch_ip, username="", password=""):
    if username == "" and password == "":
        username = input("Username: ")
        try:
            password = getpass.getpass()
        except Exception as err:
            print("--------------------------")
            print(err)
            print("--------------------------")
            
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
    
    if switch_ip == 'serial':
        port = input("Serial line: ")
        switch_details = {
            'device_type' : 'cisco_ios_serial',
            'port' : port,
            'username' : username,
            'password' : password,
            'serial_settings' : {
                'baudrate' : 9600,
                'timeout' : 15,
                },
        }
    else:
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
    username = input("Username: ")
    try:
        password = getpass.getpass()
    except Exception as err:
        print("--------------------------")
        print(err)
        print("--------------------------")

    for switch_ip in switch_list:
        if not check_ip(switch_ip):
            print(f"IP {switch_ip} is invalid... Skipping...")
            continue
        try:
            net_connect = ConnectHandler(**switch_connect(switch_ip, username, password))
            
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
        except Exception as err:
            print("--------------------------")
            print(switch_ip)
            print(err)
            print("--------------------------")

        
#Grabs a config given an ip address
def grabconfigip(switch_ip):
    try:
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
    except Exception as err:
        print("--------------------------")
        print(err)
        print("--------------------------")
    
    
    
#dumps config given the ip address
def dumpconfig(switch_ip, txt_file_name):
    try:
        net_connect = ConnectHandler(**switch_connect(switch_ip))
        switch_hostname = (net_connect.send_command('show conf | include hostname').split()[1])

        print(f"Dumping config on: {switch_hostname}\n")
        net_connect.send_config_from_file(txt_file_name + ".txt")
        net_connect.send_command("wr mem")
        print(f"Config successfully dumped on: {switch_hostname}\n")
    except Exception as err:
        print("--------------------------")
        print(err)
        print("--------------------------")


#Changes an interface on a switch
def change_interface(switch_ip, config_dict):
    try:
        net_connect = ConnectHandler(**switch_connect(switch_ip))
        switch_hostname = (net_connect.send_command('show conf | include hostname').split()[1])
        #Splits up some of the interfaces into an easier output/input
        interface_array = (net_connect.send_command('show conf | include interface GigabitEthernet').splitlines())
        filtered_array = [item for item in interface_array if "GigabitEthernet0/0" not in item.split()]
        for index, interface in enumerate(filtered_array):
            index = index + 1
            print(str(index) + ". " + interface)
        selected_interface = filtered_array[int(input("Select a port number: ")) - 1]
        #Splits up the vlans into an easier output/input
        vlan_array = []
        for index, vlan_key in enumerate(config_dict.keys()):
            index = index + 1
            print(str(index) + ". " + vlan_key)
            vlan_array.append(vlan_key)
        vlan_input = config_dict[vlan_array[int(input("Select a vlan: ")) - 1]]
        vlan_input.insert(0, selected_interface)
        
        #Defaults the interface then sets it given the settings. *Default is deciding not to default interfaces right now but doesnt fail..
        net_connect.send_config_set("default" + selected_interface)
        send_vlan = (net_connect.send_config_set(vlan_input))
        net_connect.send_command("wr mem")
        print(send_vlan)
        
        repeat_change = input("Change another (y/n): ")
        if repeat_change == "y":
            change_interface(switch_ip, config_dict)
            return
        return
        

    except Exception as err:
        print("--------------------------")
        #print(err)
        print("--------------------------")


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
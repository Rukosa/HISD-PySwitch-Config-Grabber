#A menu of options that the user can execute if only one of these is needed
from off_switch_functions import *

option_txt = '''
1. Grab configs
2. Dump configs
3. Edit vlans
4. Find MAC Address
'''

option_list = {
"1":(grab_configs_opt), #Grab configs
"2":(dump_config_opt), #Dump configs
"3":(edit_vlans_opt), #Edit vlans
"4":(find_mac_opt) #Find mac
}

while(True):
    print("\n--------------------------")
    print(option_txt)
    choice = input("#")
    if choice in list(option_list.keys()):
        option_list[choice]()
    else:
        print("Invalid input")     
    3
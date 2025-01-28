#A menu of options that the user can execute if only one of these is needed
from off_switch_functions import *

option_txt = '''
1. Grab configs
2. Dump configs
'''

option_list = {
"1":(grab_configs_opt), #Grab configs
"2":(dump_config_opt) #Dump configs
}

while(True):
    print("\n--------------------------")
    print(option_txt)
    choice = input("#")
    if choice in list(option_list.keys()):
        option_list[choice]()
    else:
        print("Invalid input")     
    
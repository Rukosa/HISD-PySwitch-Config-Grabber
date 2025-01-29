#Menu options to get details and fill in what is needed for the switch
#logic is a bit complex..
from on_switch_functions import *
import os


#Menu options    
def grab_configs_opt(choice=0):
    if choice == 0:
        print('''
1. Grab one config (Network)
2. Grab many configs (Network)
3. Grab one config (Serial) 
        ''')
        choice = input("#")
    #one
    if choice == '1':
        switch_ip = input("IP of switch: ")
        if not check_ip(switch_ip):
            print("IP is invalid...")
            grab_configs_opt(choice)
            return
        grabconfigip(switch_ip)
    #many 
    elif choice == '2':
        switch_txt = input("Name of text file [no file extension!]: ")
        if check_txt_exists(switch_txt):
            grabconfigtxt(switch_txt)
        else:
            grab_configs_opt(choice)
            return
    elif choice == '3':
        grabconfigip('serial')
    else:
        print("Invalid input...")
        grab_configs_opt()

#Built to have reset points. Reset to a certain point by filling in a value with 0 or restart with a blank function call
def dump_config_opt(switch_ip=0, dump_txt=0, serial_or_network=0):
    #Serial/Network logic
    if serial_or_network == 0:
        print('''
    1. Serial
    2. Network
            ''')
        serial_or_network = input('#')
    if serial_or_network == '1':
        switch_ip = 'serial'
    elif not (serial_or_network == '2') and not (serial_or_network == '1'):
        print("Invalid input")
        dump_config_opt()
        return
    #Switch IP and Text logic. Switch IP assumes network was chosen
    if switch_ip == 0:
        switch_ip = input("IP of switch: ")
        if not check_ip(switch_ip):
            print("IP is invalid...")
            dump_config_opt(0, 0, serial_or_network)
            return
    if dump_txt == 0:
        dump_txt = input("Name of config txt file [no file extension!]: ")
        if not check_txt_exists(dump_txt):
            dump_config_opt(switch_ip, 0, serial_or_network)
            return
    
    confirm_input = input(f"Are you sure you want to dump to {switch_ip} with {dump_txt}.txt? (y/n): ")
    if confirm_input == 'y':
        dumpconfig(switch_ip, dump_txt)
    elif confirm_input == 'n':
        dump_config_opt()
    else:
        print("Invalid input")
        dump_config_opt(switch_ip, dump_txt, serial_or_network)
        
def check_txt_exists(txt_file):
    if os.path.exists(txt_file + ".txt"):
        return True
    print(f"{txt_file}.txt does not exist...")
    return False
from on_switch_functions import *
import os

#Menu options    
def grab_configs_opt(choice=0):
    if choice == 0:
        print('''
1. Grab one config
2. Grab many configs
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
    else:
        print("Invalid input...")
        grab_configs_opt()
    
def dump_config_opt(switch_ip=0, dump_txt=0):
    if switch_ip == 0:
        switch_ip = input("IP of switch: ")
        if not check_ip(switch_ip):
            print("IP is invalid...")
            dump_config_opt()
            return
    if dump_txt == 0:
        dump_txt = input("Name of config txt file [no file extension!]: ")
        if not check_txt_exists(dump_txt):
            dump_config_opt(switch_ip)
            return
    
    confirm_input = input(f"Are you sure you want to dump to {switch_ip} with {dump_txt}.txt? (y/n): ")
    if confirm_input == 'y':
        dumpconfig(switch_ip, dump_txt)
    elif confirm_input == 'n':
        dump_config_opt()
    else:
        print("Invalid input")
        dump_config_opt(switch_ip, dump_txt)
        
def check_txt_exists(txt_file):
    if os.path.exists(txt_file + ".txt"):
        return True
    print(f"{txt_file}.txt does not exist...")
    return False
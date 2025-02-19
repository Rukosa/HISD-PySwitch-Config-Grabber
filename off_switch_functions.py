#Menu options to get details and fill in what is needed for the switch
#logic is a bit complex..
from on_switch_functions import *
import os
import re
import ast


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
        


#Changes vlans on switch. Most inputs are validated so it is unlikely the user will run into issues after choosing a model.
def edit_vlans_opt(switch_ip=0, serial_or_network=0, config_set=False, current_config=None, model_selected=""):
    #auto connection here??
    #Manual selection vvvvv------
    model_selection_dict = {}
    if not config_set:
        switch_models = open("vlans.txt", "r")
        vlan_text = ""

        #Loads up the vlan text file and parses variables from them
        for line in switch_models:
            vlan_text = vlan_text + line
        switch_models.close()
        vlan_configs, vlan_vars = parse_dict_with_variables(vlan_text)
        current_config = (vlan_configs, vlan_vars)
        
        #Displays the model list and loads them up into a dictionary to get their keys later. Then asks to set variables for said model
        #Else config_set=True will assume these steps have already been done and uses the tuple argument
        print("\n-----Select a model from the list-----")
        for index, switch in enumerate(list(vlan_vars.keys())):
            index = index + 1
            print(str(index) + ". " + switch)
            model_selection_dict.update({str(index): switch})
        
        model_selected = input("Select a model: ")
        selected_config = set_variables_for_selected_model(vlan_configs, vlan_vars, model_selection_dict[model_selected])
        config_set = True
    else:
        selected_config = vlan_configs = current_config[0]
        vlan_vars = current_config[1]
        for index, switch in enumerate(list(vlan_vars.keys())):
            index = index + 1
            model_selection_dict.update({str(index): switch})
    
    #Serial or network logic + ip logic
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
        edit_vlans_opt(0, 0, config_set, current_config, model_selected)
        return
    if switch_ip == 0:
        switch_ip = input("IP of switch: ")
        if not check_ip(switch_ip):
            print("IP is invalid...")
            edit_vlans_opt(0, serial_or_network, config_set, current_config, model_selected)
            return
    change_interface(switch_ip, selected_config[model_selection_dict[model_selected]])
    
def find_mac_opt(mac=None):
    if mac == None:
        mac_address_input = input("12 Digit Mac Address: ")
        mac = mac_address_input
        if len(mac_address_input) != 12:
            find_mac_opt()
    switch_txt = input("Name of text file of possible switches [no file extension!]: ")
    if check_txt_exists(switch_txt):
        find_mac(convert_mac(mac), switch_txt)
    else:
        find_mac_opt(mac)
        return

#Next 2 functions are courtesy of some *heavily* modified chatgpt code! It made some good comments so I'm leaving them :)
#Parses an input structered like a dictionary and extracts variables wrapped in *asterisk*
def parse_dict_with_variables(config_text):
    try:
        config_dict = ast.literal_eval(config_text)  # Convert text to dictionary
    except (SyntaxError, ValueError) as e:
        print(f"Error parsing input: {e}")
        return None, None  # Return None if parsing fails

    vlan_variables = {}  # Store extracted variables

    # Iterate through models and VLANs
    for model, vlans in config_dict.items():
        vlan_variables[model] = {}
        for vlan_name, settings in vlans.items():
            for i, line in enumerate(settings):
                # Find any text inside *asterisks*
                matches = re.findall(r"\*(.*?)\*", line)
                for var_name in matches:
                    vlan_variables[model][var_name] = None  # Initialize variable
                    config_dict[model][vlan_name][i] = line.replace(f"*{var_name}*", var_name)  # Keep placeholder

    return config_dict, vlan_variables  # Return updated config and extracted variables

#Modifies the config dictionary given the selected switch model
def set_variables_for_selected_model(config_dict, vlan_variables, selected_model):
    """
    Set variables for the selected model by prompting for input and updating the config.

    :param config_dict: The parsed configuration dictionary
    :param vlan_variables: The dictionary of extracted variable names
    :param selected_model: The model selected by the user for which to set the variables
    :return: Updated config_dict with variables set for the selected model
    """
    if selected_model not in vlan_variables:
        print(f"Model {selected_model} not found!")
        return config_dict  # Return the config without any changes if model is not found

    # Loop through the variables for the selected model
    for var_name in vlan_variables[selected_model]:
        # Prompt the user for input to set the variable
        user_input = input(f"Enter a value for variable '{var_name}' in model '{selected_model}': ")

        # Replace the variable in the config dictionary
        for vlan_name, settings in config_dict[selected_model].items():
            for i, line in enumerate(settings):
                if var_name in line:
                    config_dict[selected_model][vlan_name][i] = line.replace(var_name, user_input)

    return config_dict  # Return the updated config with variables set for the selected model (easier to return the whole thing and select later!)

#Finds if a text file exists
def check_txt_exists(txt_file):
    if os.path.exists(txt_file + ".txt"):
        return True
    print(f"{txt_file}.txt does not exist...")
    return False

def convert_mac(s):
    return s[:4] + '.' + s[4:8] + '.' + s[8:]
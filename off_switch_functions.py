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
        
def check_txt_exists(txt_file):
    if os.path.exists(txt_file + ".txt"):
        return True
    print(f"{txt_file}.txt does not exist...")
    return False




def parse_dict_with_variables(config_text):
    """
    Parses a structured dictionary-like text input, extracting all variables 
    that are wrapped in asterisks (*ANYTHING*).
    """
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

    return config_dict  # Return the updated config with variables set for the selected model

    
    

vlan_text = config_text = """
#This functions as if it were evaluating it as a nested dictionary in Python! Assuming it is written as such it will work.
#Ensure you have a comma after the model brackets!
{

"1234": {
"INTERNET ACCESS": [
"switchport access vlan *INTERNET_ACCESS*",
"mls qos trust cos",
"auto qos voip cisco-phone",
"spanning-tree portfast",
"spanning-tree guard root",
"service-policy input AutoQoS-Police-CiscoPhone"
],
"WIRELESS AP": [
"switchport access vlan *WIRELESS_AP*",
"more wireless settings",
"some other setting"
]
}, 

"5678": {
"INTERNET ACCESS": [
"switchport access vlan *INTERNET_ACCESS*",
"mls qos trust cos",
"auto qos voip cisco-phone",
"spanning-tree portfast",
"spanning-tree guard root",
"service-policy input AutoQoS-Police-CiscoPhone"
],
"WIRELESS AP": [
"switchport access vlan *WIRELESS_AP*",
"more wireless settings",
"some other setting"
]
},


}
"""

test_vlan, vlan_vars = parse_dict_with_variables(vlan_text)
from pprint import pprint
pprint(vlan_vars)
updated_config = set_variables_for_selected_model(test_vlan, vlan_vars, '5678')
pprint(updated_config)




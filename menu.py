#A menu of options that the user can execute if only one of these is needed
from on_switch_functions import grabconfigtxt

option_list = '''
1. Grab configs
2. Dump a config
'''

def grab_configs():
    print('''
          1. Grab one config
          2. Grab campus configs
          3. Grab ALL configs 
          ''')
    choice = input("#")
    
    
    #fill in inputs
    
def dump_config():
    print("Name of config txt file: ")
    #Create function to dump config line by line

#print("Please choose an option below: " + option_list)
txt_file = input("Text file to grab ip(s) from [no file extension!]: ")
grabconfigtxt(txt_file)
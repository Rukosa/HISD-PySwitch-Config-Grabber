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
    

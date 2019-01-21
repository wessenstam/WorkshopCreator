# Import the needed modules
import requests
import json
import html
from tkinter import *
import subprocess

def Repo_Pull(http_url):

    # Get the full html urls and the name for the workshops repos
    r=requests.get(http_url)

    #Assign the output to the my_dict Dictionairy
    my_dict = json.loads(r.text)

    # Define to emtpy lists
    list_html_url=[]
    list_name_url=[]

    # Assign all the two variables to the list so we can use the list later on
    for key in my_dict:
        first_key = key['html_url']
        first_value= key['name']
        list_html_url.append(first_key)
        list_name_url.append(first_value)

    # Combine the two lists to a new Dictionairy
    return dict(zip(list_name_url,list_html_url))
    

def Create_UI(dict):

    # Set some variables
    master = Tk()
    count=0
    var=StringVar()
    module_list=[]

    # Get the selected parts of the workshop and put them in a list
    def var_states(key):
        module_list.append(key)
        #print("Selected: " + key)
        #print("Length of the Module_list= "+str(len(module_list)))

    # Clone the selected modules from github
    def selected_modules():
        print("The following items have been selected:")
        count = 1
        for value in module_list:
            print('Cloning ' + value + ' from ' + right_dict[value] + ' (' + str(count) + ' of '  + str(len(module_list)) + ')')
            cmd_to_run='git clone ' + right_dict[value]
            var_out=subprocess.Popen([cmd_to_run], shell=True, stderr=subprocess.PIPE)

            # Counter +1
            count +=1


    # Create the GUI
    Label(master, text="Your selection:").grid(row=0, sticky=W)
    
    
    # For all Repos found, create a checkbox. As soon as the checkbox is ticked, send info to a list
    for value_field in right_dict:
        var = value_field
        Checkbutton(master, text=value_field, variable=value_field, command=lambda key=value_field: var_states(key)).grid(row=count+1, sticky=W)
        count += 1

    # If the Quit button is selected, kill the app
    # If the Show button is clicked, show the list that has been selected
    Button(master, text='Show', command=selected_modules).grid(row=count+1, sticky=W, pady=4)
    Button(master, text='Quit', command=master.quit).grid(row=count+1, sticky=E, pady=4)
    
    mainloop()

#Define the URL for pulling the Repos
url='http://api.github.com/users/nutanixworkshops/repos'

# Call the function to pull the list of the repos
right_dict=Repo_Pull(url)
#print(right_dict)

Create_UI(right_dict)
# Import the needed modules
import requests
import json
import html
from tkinter import *
from tkinter import messagebox
import subprocess
import os


# Function for pulling the repos form the URL
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
    
# Function for the UI and related stuff
def Create_UI(dict):

    # Set some variables
    master = Tk()
    count=0
    var=StringVar()
    module_list=[]

    #Function for throwng errors
    def throw_error(message):
        messagebox.showerror('Error has occured','The receiving error has been: ' + str(message) + '\nThe program will now stop')
        exit()

    # Get the selected parts of the workshop and put them in a list
    def var_states(key):
        module_list.append(key)
        #print("Selected: " + key)
        #print("Length of the Module_list= "+str(len(module_list)))

    # Clone or Pull the selected modules from github
    def selected_modules():
        count = 1
        for value in module_list:
            # Checking to see if the directory already exists. If so run pull not clone
            if os.path.exists('./'+value):
                # DEBUG print('Chaning to pull and not clone')
                cmd_to_run='cd ./' + value + ' && git pull && cd ..'
                var_out=subprocess.Popen([cmd_to_run], shell=True, stderr=subprocess.PIPE)

                # If any issues, show an error message and kill the program
                if var_out.returncode is not None:
                    throw_error(var_out.communicate())

            else:
                #DEBUG print('Cloning ' + value + ' from ' + right_dict[value] + ' (' + str(count) + ' of '  + str(len(module_list)) + ')')
                cmd_to_run='git clone ' + right_dict[value]
                var_out=subprocess.Popen([cmd_to_run], shell=True, stderr=subprocess.PIPE)

                # If any issues, show an error message and kill the program
                if var_out.returncode is not None: 
                    throw_error(var_out.communicate())

            # Counter +1
            count +=1


    # Create the GUI
    Label(master, text="Make your selection:").grid(row=0, sticky=W)
    
    # For all Repos found, create a checkbox. As soon as the checkbox is ticked, send info to a list
    for value_field in right_dict:
        var = value_field
        Checkbutton(master, text=value_field, variable=value_field, command=lambda key=value_field: var_states(key)).grid(row=count+1, sticky=W)
        count += 1

    # If the Quit button is selected, kill the app
    # If the Create button is clicked, create the list that has been selected
    Button(master, text='Create', command=selected_modules).grid(row=count+1, sticky=W, pady=4)
    Button(master, text='Quit', command=master.quit).grid(row=count+1, sticky=E, pady=4)
    
    mainloop()

#Define the URL for pulling the Repos
url='http://api.github.com/users/nutanixworkshops/repos'

# Call the function to pull the list of the repos
right_dict=Repo_Pull(url)

# Call the create the UI components
Create_UI(right_dict)
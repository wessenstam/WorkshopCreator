# Import the needed modules
import requests
import json
import html
from tkinter import *
from tkinter import messagebox
import subprocess
import os
import sys
import fileinput
import time

# Check Python 3 is being used!!!
if sys.version_info[0] < 3:
    raise Exception("Sorry to say, but this script must be used on Python 3")       

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
def Create_UI(my_values,action):

    # Set some variables
    master = Tk()
    count=0
    var=StringVar()
    global module_list
    module_list=[]

    #Function for throwing errors
    def throw_error(message):
        master.withdraw()
        messagebox.showerror('Error has occured','The receiving error has been: ' + str(message) + '\nThe program will now stop')
        exit()

    def all_ok():
        master.withdraw()

        # Create the message text
        msg_txt='Cloned module(s):\n'
        for module in module_list:
            msg_txt=msg_txt + module + '\n'

        # Show all ok messagebox with the selected modules and stop the program
        messagebox.showinfo('All has been cloned',msg_txt)

        # Close the UI 
        master.quit()
    
    # Get the order of the fields and put them in an ordering list
    def change_modules():
        print('values from the changes: ' + var_txt.get())

    # Get the selected parts of the workshop and put them in a list
    def var_states(key):
        module_list.append(key)
        #print("Selected: " + key)
        #print("Length of the Module_list= "+str(len(module_list)))

    # Clone or Pull the selected modules from github
    def selected_modules():
        # Set some parameters
        count = 1

        # For all selected modules pull or clone the github repo
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
        
        # Notify the user that all have been cloned
        all_ok()

    # If the action is start, create the GUI accordingly
    if action =='start':

        # Create the GUI
        Label(master, text="Make your selection:").grid(row=0, sticky=W)
        
        # For all Repos found, create a checkbox. As soon as the checkbox is ticked, send info to a list
        for value_field in my_values:
            var = value_field
            Checkbutton(master, text=value_field, variable=value_field, command=lambda key=value_field: var_states(key)).grid(row=count+1, sticky=W)
            count += 1

        # If the Quit button is selected, kill the app
        # If the Create button is clicked, create the list that has been selected
        Button(master, text='Create', command=selected_modules).grid(row=count+1, sticky=W, pady=4)
        Button(master, text='Quit', command=master.quit).grid(row=count+1, sticky=E, pady=4)
        
        # Start the GUI
        master.mainloop()
        
    else:
        # Create the GUI
        Label(master, text="Change order if needed\n(use 0-" + str(len(my_values))+ ') to change the order').grid(row=0, sticky=W)
        
        # For all selected Repos, create a window that allows to change the order
        for value_field in my_values:
            Label(master, text=str(count) +'. ' + value_field).grid(row=count+1, column=0, sticky=W)
            Entry(master).grid(row=count+1, column=1, sticky=E)
            count += 1

        # If the Quit button is selected, kill the app
        # If the Create button is clicked, create the list that has been selected
        Button(master, text='Change', command=change_modules).grid(row=count+1, sticky=W, pady=4)
        Button(master, text='Quit', command=master.quit).grid(row=count+1, sticky=E, pady=4)
        
        # Start the GUI
        master.mainloop()
        

# Function to run command line commands
def command_to_run(cmd):
    var_out=subprocess.Popen([cmd], shell=True, stderr=subprocess.PIPE)
    # Check on errors
    if not str(var_out.communicate):
        print('error has occured: ' + str(var_out.communicate()))
    #    exit()
    

# Clean up Any left overs before beginning
cmd_to_run='rm -Rf WorkDir' # Create the command
command_to_run(cmd_to_run) # Run via function


#Define the URL for pulling the Repos
url='http://api.github.com/users/nutanixworkshops/repos'

# Call the function to pull the list of the repos
right_dict=Repo_Pull(url)

# Call the create the UI components and the action is start
Create_UI(right_dict,'start')

# Create the needed directory structure and copy all cloned repos in WorkDir
cmd_part = 'mkdir -p WorkDir && mv '
for module in module_list:
    cmd_to_run = cmd_part + module + ' WorkDir/'
    command_to_run(cmd_to_run)

# Put the index_templ.rst in the WorkDir
cmd_to_run='cp index_templ.rst WorkDir/index.rst'
command_to_run(cmd_to_run)

# Change the copies index.rst file to hold the repos just cloned
filename='WorkDir/index.rst'
replacement_text=''

time.sleep(2)

with fileinput.FileInput(filename, inplace=True) as file:
    for line in file:
        # Searching for the first to be replaced line
        if 'holding 1' in line:
            for module in module_list:
                replacement_text=replacement_text + module + ', '
            # Strip last two characters from replacement_text
            replacement_text=replacement_text[:-2]
            print(line.replace('holding 1', replacement_text), end='')
            # Reset variabale
            replacement_text=''
        elif ':hidden:' in line:
            replacement_text=':hidden:\n\n'
            for module in module_list:
                replacement_text=replacement_text + module + '/index\n'
            print(line.replace(':hidden:', replacement_text), end='')
            # Reset variabale
            replacement_text=''
        else: # Save line anyways!!
            print(line, end='')




########################################################## TO DO ################################################ 
# Call the create the UI components and the action is show to make changes to the order of the list
# Still need to create. Use https://www.python-course.eu/tkinter_entry_widgets.php as example
# Create_UI(module_list,'show')
########################################################## TO DO ################################################ 
# -------------------------------------- #
# Programador: Genís Martínez   		 #
# Programador: David Tomas               #
# -------------------------------------- #

import xmlrpc.client
import os

# ---------------------------- Connex Establishment ----------------------------- #

s = xmlrpc.client.ServerProxy('http://localhost:8005')  # We create the server proxy

TASKS_ID = []   # We create the list of tasks

#---------------------------------- SWITCH OPTIONS ------------------------------ #
def choose_task():
    print ("******************************************")
    print ("*                                        *")
    print ("*               Submit task              *")
    print ("*                                        *")
    print ("******************************************\n")

    function_name = input("Function to be executes: ")
    function_args = input("Arguments of the function: ")
    print("Submitting task...")
    job_id = s.submit_task(function_name, function_args)
    print("Task submitted with id: " + str(job_id))
    if job_id != -1:
        TASKS_ID.append(job_id)

def read_result():
    print ("******************************************")
    print ("*                                        *")
    print ("*               Read result              *")
    print ("*                                        *")
    print ("******************************************\n")

    print("Created tasks by ID:")
    for tsk in TASKS_ID:
        print(tsk)  # Print the list of tasks

    selected = input("Select the task to know the result: ")
    ret_val = s.read_result(selected)   # We read the result of the task with id = selected
    if ret_val == -1:   # If the task has not finished yet, we print an error message
        print("\nThe result of the task with id ",selected," is:\n",ret_val)    # We print the result
    else:
        print("\nError: No job founf with id ",selected,". It is possible that the job has not finished yet.\n")    # We print the result


def add_server():
    print ("******************************************")
    print ("*                                        *")
    print ("*               Add Server               *")
    print ("*                                        *")
    print ("******************************************\n")
    print(s.add_server())   # We add a new server

def rem_server():
    print ("******************************************")
    print ("*                                        *")
    print ("*             Remove Server              *")
    print ("*                                        *")
    print ("******************************************\n")

    print ("Active server IDs:")
    print(s.list_server())  # We print the list of active servers
    print("\nWrite the IDs of the target workers (separated by space):")
    target = input()    # We read the target server

    print(s.remove_server(target))    # We remove the target server

def print_servers():
    print ("******************************************")
    print ("*                                        *")
    print ("*              List Server               *")
    print ("*                                        *")
    print ("******************************************\n")
    print(s.list_server())  # We print the list of active servers

def invalid_option():
    print ("******************************************")
    print ("*                                        *")
    print ("*            Invalid Option              *")
    print ("*                                        *")
    print ("******************************************\n")
    print("Please, select a valid option.\n")

# ------------------------------ SWITCH OPTIONS ----------------------------- #
switch_options = {      # We create a dictionary with the options
    '1': choose_task,
    '2': add_server,
    '3': print_servers(),
    '4': rem_server,
    '5': read_result
}

# ------------------------------------ CLEAR -------------------------------- #
def wipe_screen():
    os.system('clear')

# ------------------------------------ MAIN -----------------------------------#

def show_menu():
    print("******************************************")
    print("*                                        *")
    print("*                WELCOME                 *")
    print("*                                        *")
    print("******************************************")
    print("*                                        *")
    print("* Which action do you want to perform?   *")
    print("*  0 - Exit.                             *")
    print("*  1 - Submit a task.                    *")
    print("*  2 - Add server.                       *")
    print("*  3 - List servers.                     *")
    print("*  4 - Remove server.                    *")
    print("*  5 - Read task result.                 *")
    print("*                                        *")
    print("******************************************")


    choice = -1
    while (choice != 0):
        show_menu()    # We show the menu
        choice = input('Your choice: ')   # We ask the user for a choice
        wipe_screen()   # We clear the screen

        switch_options.get(choice, invalid_option)()    # We execute the function associated to the choice
        input('\nPress any key to continue...')
        wipe_screen()   # We clear the screen

    print("Shutting down client...")

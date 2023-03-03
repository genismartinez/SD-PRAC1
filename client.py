# -------------------------------------- #
# Programador: Genís Martínez   		 #
# Programador: David Tomas               #
# -------------------------------------- #

import xmlrpc.client
import os

# ---------------------------- Connex Establishment ----------------------------- #

s = xmlrpc.client.ServerProxy('http://localhost:8005')

TASKS_ID = []

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
        print(tsk)

    selected = input("Select the task to know the result: ")
    ret_val = s.read_result(selected)
    if ret_val == -1:
        print("\nThe result of the task with id ",selected," is:\n",ret_val)
    else:
        print("\nError: No job founf with id ",selected,". It is possible that the job has not finished yet.\n")


def add_server():
    print ("******************************************")
    print ("*                                        *")
    print ("*               Add Worker               *")
    print ("*                                        *")
    print ("******************************************\n")
    print(s.add_server())

def rem_server():
    print ("******************************************")
    print ("*                                        *")
    print ("*             Remove Worker              *")
    print ("*                                        *")
    print ("******************************************\n")

    print ("Active worker IDs:")
    print(s.list_server())
    print("\nWrite the IDs of the target workers (separated by space):")
    target = input()

    print(s.remove_server(target))    #Falta argument.

def print_servers():
    print ("******************************************")
    print ("*                                        *")
    print ("*              List Worker               *")
    print ("*                                        *")
    print ("******************************************\n")
    print(s.list_server())

def invalid_option():
    print ("******************************************")
    print ("*                                        *")
    print ("*            Invalid Option              *")
    print ("*                                        *")
    print ("******************************************\n")
    print("Please, select a valid option.\n")

switch_options = {
    '1': choose_task,
    '2': add_server,
    '3': print_servers(),
    '4': rem_server,
    '5': read_result
}

def wipe_screen():
    os.system('clear')

# ---------------------------------------- MAIN -----------------------------------#

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
        show_menu()
        choice = input('Your choice: ')
        wipe_screen()

        switch_options.get(choice, invalid_option)()
        input('\nPress any key to continue...')
        wipe_screen()

    print("Shutting down client...")

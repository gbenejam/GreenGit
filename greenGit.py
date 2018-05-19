'''
This script pushes just the first unpushed commit to origin.
It can also be configured to make the pushes automatically at a given time.

README

To use this software you need python version 3.5 at least installed in your computer.
There are two ways to execute this:
1. With a normal script execution.
2. With crontab so that it executes automatically.

To execute it just once go to the folder of the project you want to push (the one
with the .git folder) and run:
python3 greenGit.py project-base-folder [number-of-commits [crontab-expression]]

To execute it automatically each period of time you need to add it to crontab.
With this method you can forget about pushing to GitHub and the script will push
each day just the number of commits passed by parameter to the script (by default 1),
so that the commit map appears completely green.

To add the execution of the script to the crontab you need to call this script with
the parameters that you would pass to create the cron scheduling. This is:
    python3 greenGit.py project-folder number-of-commits min hour day-of-month month day-of-week

The parameters are received in order, so all the previous parameters are mandatory
in case you want to set a specific one. The parameters not set for the crontab-expression
will be considered as if they were '*'.

'''

# Imports

import subprocess
import sys
import os


# Classes to set and use the different command line options

class CommandLineParameters():
    '''
    Class to create objects that represent the command line options. Each command line parameter
    is listed in the object as a separate parameter and the __str__ method returns the command
    entered to the command line.
    '''
    cron_expression = '(crontab -l 2>/dev/null; echo "{0} {1} {2} {3} {4} {5} {6}") | crontab -'

    def __init__(self, parameter_list):
        '''
        Initializes the object with the parameters passed as argument.
        parameter_list is the list of parameters received through the command line execution.
        Those optional parameters that are not specified in the list will be initialized with a
        default value if needed.
        '''
        # path of the script
        self.project_path = __get_parameter__(1, parameter_list)
        
        # number of commits to be done
        self.commits_number = __get_parameter__(2, parameter_list)
        
        # get cron parameters
        self.minute = __get_parameter__(3, parameter_list)
        self.hour = __get_parameter__(4, parameter_list)
        self.month_day = __get_parameter__(5, parameter_list)
        self.month = __get_parameter__(6, parameter_list)
        self.week_day = __get_parameter__(7, parameter_list)

        # boolean to know if cron expression needs to be executed or not
        self.execute_cron = parameter_list > 3

    def __str__(self):
        '''
        String representation of the command executed.
        '''
        return f'python3 {self.project_path} {self.commits_number} {self.minute} {self.hour} '\
            + f'{self.month_day} {self.month} {self.week_day}'

    @staticmethod
    def __get_parameter__(parameter_number, parameter_list):
        '''
        Private static method.
        Given a list (parameter_list), returns the object at position 'parameter_number'. 
        It makes sure that if the index is out of bounds the object returned will be properly
        default initialized.

        commits_number is default initialized to 1.
        Not specified cron parameters (minute, hour, ...) are initialized to '*'.
        '''
        if parameter_number >= len(parameter_list):
            # there is no parameter set and we need to initialize it
            if parameter_number == 1:
                return '.'
            elif parameter_number == 2:
                return 1
            else:
                return '*'

        return parameter_list[parameter_number]

    def get_cron_expression():
        return CommandLineParameters.cron_expression.format(
            self.minute, self.hour, self.month_day, self.month, self.week_day,
            self.project_path, self.commits_number)


class CommandExecutor():
    '''
    This class encapsulates the execution of all the available commands for this script.
    It provides a list with the commands that are possible to execute. 
    '''
    CONST_COMMANDS = {
        'cd' : __go_to_folder__
        'cron': __get_cron_command_list__
    }

    ERROR_CODES = {
        -2: 'Command does not exist'
        -1: 'Unknown error'
    }

    def __init__(self):
        '''
        Nothing to do here. This class is just a wrapper for some methods.
        '''
        pass

    def execute(self, command, command_generator):
        '''
        This method gets the command to execute and runs it.
        command specifies the function to be used (found in CONST_COMMANDS) to get the
        expression that needs to be executed.
        command_generator is an optional object that can be passed and may be used by
        the function to generate the command to be run.
        '''
        try:
            command_list = CONST_COMMANDS[command](command_generator)
        except KeyError:
            # Print the error and return negative number meaning failure of execution
            print('CommandExecutor - Unrecognized command')
            return -2
        except Exception as error:
            print('Exception: ' + repr(error)) 
            return -1

        # If we arrive here it means that command_list is initialized
        result = subprocess.run(command_list, shell=True)
        # To be able to read the output add stdout=subprocess.PIPE to the run call.
        # To read the result output execute: result.stdout.decode('utf-8')
        return result.returncode

    @staticmethod
    def __get_cron_command_list__(command_generator):
        '''
        This is the function used to generate the cron expression to be run to schedule
        the the execution of this script.
        command_generator is an object of type CommandLineParameters, which can return a
        valid cron expression.
        '''
        try:
            return command_generator.get_cron_expression()
        except:
            raise Exception('CommandExecutor - Could not get cron expression')


# Functions to check if the push is needed

def has_git_subfolder():
    '''
    Checks if the path where the script is being executed contains also a .git subfolder.
    @return true if there is the .git subfolder and false otherwise.
    '''
    pass

def number_of_commits_today():
    '''
    Checks the number of commits that has been done today.
    @return the number of commits done today.
    '''
    pass

def is_push_needed():
    '''
    Checks if the number of commits for today hasn't still been done and if the folder
    where the script is being executed has a .git subfolder in it.
    @return true if there is a .git subfolder and the number of commits done today is
    less than number-of-commits, and false otherwise.
    '''
    pass


# Functions to execute git commands

def get_current_branch():
    '''
    This function returns the name of the current branch of the repository.
    '''
    pass

def get_commit_to_push():
    '''
    Function that, checking the number_of_commits needed, picks a commit SHA from the
    results of the corresponding git log command.
    '''
    pass

def push_commits():
    '''
    Function that executes the pushing of number_of_commits (if available) to the remote
    repository.
    '''
    pass


# Main method

def execute_script():
    '''
    This is the main method of the script.
    This method checks if a push is needed and if there are commits available to push.
    Then it takes care of getting all the information needed from git commands and of
    pushing to the remote repository the specified number of commits.
    '''

    # get command line options and create CommandLineParameters object
    script_options = CommandLineParameters(sys.argv)
    command_executer = CommandExecutor()

    if script_options.execute_cron:
        command_executer.execute('cron', script_options)

    # if there are commits and we still haven't commit all script_options.commits_number
    # and if we are in a directory with .git folder, then push the commits
    if is_push_needed(command_executer, script_options.commits_number):
        push_commits(command_executer, script_options.commits_number)


# Script start

if __name__ == '__main__':
    execute_script()


# NOTES

# check if the folder has a .git subfolder
# check if the number of commits published today equals to the number of commits passed as parameter
# To do this check the log of the remote repository and check the date for today

# if both previous conditions are true then execute the next commands
# get the unpushed commits in chronological order: git log @{u}..HEAD --format=oneline --reverse
# check if there are commits available to be pushed
# get the branch and SHA of commit that has to be pushed
# push the first unpushed commit once we have its SHA: git push <remotename> <commit SHA>:<remotebranchname>


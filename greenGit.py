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
python3 greenGit.py [number-of-commits [crontab-expression]]

To execute it automatically each period of time you need to add it to crontab.
With this method you can forget about pushing to GitHub and the script will push
each day just the number of commits passed by parameter to the script (by default 1),
so that the commit map appears completely green.

To add the execution of the script to the crontab you need to call this script with
the parameters that you would pass to create the cron scheduling. This is:
    python3 greenGit.py number-of-commits min hour day-of-month month day-of-week

The parameters are received in order, so all the previous parameters are mandatory
in case you want to set a specific one. The parameters not set for the crontab-expression
will be considered as if they were '*'.

'''

# Imports

import subprocess
import sys
import os


# Global variables

number_of_commits = 1
cron_expression = None


# Functions to set and use the different command line options

def get_command_line_options():
    '''
    Gets the number of commits variable (defaults to 1).
    If available also gets the crontab expression to be able to create a cron job to run
    periodically this script. If there is no variables for the cron expression then there is
    no cron job scheduled.
    Sets the respective global variables number_of_commits and cron_expression with the values
    read from the command line.
    '''
    global number_of_commits, cron_expression
    
    # Get the number_of_commits parameter if exists
    if len(sys.argv) > 1:
        number_of_commits = sys.argv[1];
        
    # Get the cron_expression object
    cron_expression = CronExpression(sys.argv[2:])

def set_cron_job():
    '''
    Create cron schedule task from the cron_exrpession global object.
    '''
    pass

class CronExpression():
    '''
    Class to create objects that represent a crontab expression. Each different parameter of a
    crontab expression is listed in the object as a separate parameter and the __str__ method
    returns the resulting crontab expression.
    '''

    def __init__(self, parameter_list):
        '''
        Initializes a CronExpression object with the parameters passed as argument.
        parameter_list is a list of parameters in the same order as expected for the crontab
        command. Those parameters that are not specified in the list will be considered as '*'.
        '''
        # number of commits to be done
        self.commits_number = __get_parameter__(1, parameter_list)
        # get cron parameters
        self.minute = __get_parameter__(2, parameter_list)
        self.hour = __get_parameter__(3, parameter_list)
        self.month_day = __get_parameter__(4, parameter_list)
        self.month = __get_parameter__(5, parameter_list)
        self.week_day = __get_parameter__(6, parameter_list)
        # path of the script
        self.script_path = os.path.realpath(__file__)

    def __str__(self):
        return f'{self.minute} {self.hour} {self.month_day} {self.month} {self.week_day} '\
            + f'python3 {self.script_path}'

    @staticmethod
    def __get_parameter__(parameter_number, parameter_list):
        '''
        Private static method.
        Given a list (parameter_list), returns the object at position 'parameter_number'. 
        It makes sure that if the index is out of bounds it won't give any error and will
        return '*'.
        '''
        if parameter_number >= len(parameter_list):
            return '*'

        return parameter_list[parameter_number]


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

def push_commit():
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

    get_command_line_options()
    print(number_of_commits)
    if cron_expression == None:
        print('No cron expression was assigned to cron_expression global variable')


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


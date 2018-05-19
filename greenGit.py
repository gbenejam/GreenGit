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

import sys
import os

# Custom package imports

import commandExecutor
import commandLineInterpreter


# Global const variables

CONST_COMMANDS = {
    'git-is-repo': 'git rev-parse --is-inside-work-tree'
    'git-remote-today-log': 'git log origin/{} --format=oneline --since=00:00'
    'git-branch-name': 'git rev-parse --abbrev-ref HEAD'
    'git-unpushed-commits': 'git log @{u}..HEAD --format=oneline --reverse'
    'git-push': 'git push origin {sha}:origin/{branch}'
}

    
# Functions to check if the push is needed

def is_git_repo(command_executer):
    '''
    Checks if the cwd of the command_executer object is inside a git repository.
    @return true if it is a git repository and false otherwise.
    '''
    result = command_executer.execute(CONST_COMMANDS['git-is-repo'])
    result = result.lower()
    return result == 'true'

def number_of_lines(output_text):
    '''
    Count the number of lines in the string passed as parameter.
    @return number of lines in output_text
    '''
    return len(output_text.split('\n'))

def is_push_needed(command_executer, commits_num, branch):
    '''
    Checks if the number of commits for today hasn't still been done.
    PRECONDITION: the command_executer.cwd is a directory with a git repository.
    branch is the name of the current branch in the project.
    @return true if the number of commits done today is less than commits_num and 
    false otherwise.
    '''
    # get the number of commits pushed today
    commits_pushed_command = CONST_COMMANDS['git-remote-today-log'].format(branch)
    commits_pushed_today = command_executer.execute(commits_pushed_command, number_of_lines)
    # compare the commits pushed today to the number of commits needed
    return commits_pushed_today > commits_num


# Functions to execute git commands

def get_commit_to_push(command_executer, commits_num):
    '''
    Function that, checking the number_of_commits needed, picks a commit SHA from the
    results of the corresponding git log command.
    '''
    result = command_executer.execute(CONST_COMMANDS['get-unpushed-commits'])
    commits = result.split('\n')
    
    if commits_num < len(commits):
        chosen_commit = commits[commits_num]
    else:
        chosen_commit = commits[-1]

    try:
        # get the sha of the commit
        sha = chosen_commit[0:chosen_commit.index(' ')]
    except ValueError:
        print('Error trying to get the SHA of the commit to be pushed')
        raise Exception('Abort program')

    return sha

def push_commits(command_executer, commits_num, branch_name):
    '''
    Function that executes the pushing of number_of_commits (if available) to the remote
    repository.
    '''
    commit_sha = get_commit_to_push(command_executer, commits_num)
    command = CONST_COMMANDS['git-push'].format(sha=commit_sha, branch=branch_name)
    command_executer.execute(command)


# Main method

def execute_script():
    '''
    This is the main method of the script.
    This method checks if a push is needed and if there are commits available to push.
    Then it takes care of getting all the information needed from git commands and of
    pushing to the remote repository the specified number of commits.
    '''

    # get command line options and create CommandLineInterpreter object
    script_options = CommandLineInterpreter(sys.argv)
    # initialize CommandExecuter with the project directory as cwd
    command_executer = CommandExecuter(script_options.project_path)

    if script_options.execute_cron:
        command_executer.execute(script_options.get_cron_expression)

    if is_git_repo(command_executer):
        # get the current branch of the project
        branch = command_executer.execute(CONST_COMMANDS['git-branch-name'])
    
        if is_push_needed(command_executer, script_options.commits_number):
            push_commits(command_executer, script_options.commits_number, branch)


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

'''
Old way of checking git repository... not entirely accurate.

    full_path = project_path + '/' if project_path[-1] != '/' else ''
    full_path += '.git'
    return os.path.isdir(full_path)
'''


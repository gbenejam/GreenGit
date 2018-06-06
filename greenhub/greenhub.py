#!/usr/bin/env python3

'''
This script pushes just the first unpushed commit to origin.
It can also be configured to make the pushes automatically at a given time.
'''


# Imports

import sys

# Custom package imports
if __name__ == '__main__':
    from commandExecuter import CommandExecuter
    from commandLineInterpreter import CommandLineInterpreter
else:
    from .commandExecuter import CommandExecuter
    from .commandLineInterpreter import CommandLineInterpreter


# Global const variables

CONST_COMMANDS = {
    # git commands
    'git-is-repo': 'git rev-parse --is-inside-work-tree',
    'git-origin-head-sha': 'git log origin/{} -1 --format=oneline',
    'git-remote-today-log': 'git log origin/{} --format=oneline --since=00:00',
    'git-branch-name': 'git rev-parse --abbrev-ref HEAD',
    'git-unpushed-commits': 'git log @{u}..HEAD --format=oneline --reverse',
    'git-push': 'git push origin {sha}:{branch}',
    'git-change-dates': 'git filter-branch --env-filter ',
    'git-stash': 'git stash -u',
    'git-stash-pop': 'git stash pop',
    'git-folder-path': 'git rev-parse --absolute-git-dir',
    # general bash commands
    'get-date': 'date -R',
    'remove-refs-original-folder': 'rm -rf {path}/refs/original',
    'get-greenhub-path': 'which greenhub'
}

BASH_ENV_FILTER = '\'export GIT_AUTHOR_DATE="{date}"\n' \
    + 'export GIT_COMMITTER_DATE="{date}"\' -f -- {origin_head}..HEAD'

    
# Functions to check if the push is needed

def is_git_repo(command_executer):
    '''
    Checks if the cwd of the command_executer object is inside a git repository.
    @return true if it is a git repository and false otherwise.
    '''
    result = command_executer.execute(CONST_COMMANDS['git-is-repo'])
    result = result.lower()
    return result == 'true'

def get_number_of_lines(output_text):
    '''
    Count the number of lines in the string passed as parameter.
    @return number of lines in output_text
    '''
    lines_list = output_text.split('\n')
    # remove empty elements
    lines_list = [line for line in lines_list if line]
    return len(lines_list)

def get_sha(text_line):
    '''
    Given a git log formatted line (--format=oneline), return the commit SHA from it.
    @return commit SHA of text_line
    '''
    try:
        # get the sha of the commit
        sha = text_line[0:text_line.index(' ')]
    except ValueError:
        print('Error trying to get the SHA of:')
        print(text_line)
        raise Exception('Abort program')

    return sha

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
    commits_pushed_today = command_executer.execute(commits_pushed_command, get_number_of_lines)
    # compare the commits pushed today to the number of commits needed
    return commits_pushed_today < commits_num


# Functions to execute git commands

def get_origin_head_sha(command_executer, branch):
    formatted_command = CONST_COMMANDS['git-origin-head-sha'].format(branch)
    return command_executer.execute(formatted_command, get_sha)

def get_commit_to_push(command_executer, commits_num):
    '''
    Function that, checking the number_of_commits needed, picks a commit SHA from the
    results of the corresponding git log command.
    '''
    result = command_executer.execute(CONST_COMMANDS['git-unpushed-commits'])
    commits = result.split('\n')
    
    if commits_num < len(commits):
        chosen_commit = commits[commits_num - 1]
    else:
        return None

    return get_sha(chosen_commit)

def push_commits(command_executer, commits_num, branch_name):
    '''
    Function that executes the pushing of number_of_commits (if available) to the remote
    repository.
    '''
    commit_sha = get_commit_to_push(command_executer, commits_num)
    
    if commit_sha is not None:
        command = CONST_COMMANDS['git-push'].format(sha=commit_sha, branch=branch_name)
        command_executer.execute(command)


def change_commit_dates(command_executer, branch, current_date, git_folder_path):
    '''
    This function gets all the unpushed commits and changes their date to the actual one.
    This is needed so that GitHub paints the green commit in today's day (it paints the
    box based on commit's date instead of push date).
    '''
    origin_head_sha = get_origin_head_sha(command_executer, branch)
    
    change_date_command = CONST_COMMANDS['git-change-dates'] + BASH_ENV_FILTER
    change_date_command = change_date_command.format(date=current_date, \
        origin_head=origin_head_sha)

    # first the .git/refs/original folder needs to be deleted to run the filter-branch
    remove_folder_command = CONST_COMMANDS['remove-refs-original-folder'].format(
        path=git_folder_path)
    command_executer.execute(remove_folder_command)

    # the command can not be executed if there are unstaged changes, so first stash them
    command_executer.execute(CONST_COMMANDS['git-stash'])
    # then run the command to change the date of unpushed commits
    # the command needs to be run from the top level of the working tree
    command_executer.execute(change_date_command, None, git_folder_path[0:-4])
    # and finally, pop the recently saved stash to leave the working directory as it was
    command_executer.execute(CONST_COMMANDS['git-stash-pop'])


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
    if script_options.exit:
        return
    
    # initialize CommandExecuter with the project directory as cwd
    command_executer = CommandExecuter(script_options.get_project_path(),
                                       script_options.is_verbose())

    git_folder_path = command_executer.execute(CONST_COMMANDS['git-folder-path'])
    current_time = command_executer.execute(CONST_COMMANDS['get-date'])
    
    if script_options.execute_cron:
        print('WARNING:')
        print('To use cron feature you need to leave the computer on.')
        print('You also need to have the SSH feature enabled to access the remote repository.')

        # the path will end with /.git but we want the parent folder, so up to -4 index
        absolute_path = git_folder_path[0:-4]
        greenhub_path = command_executer.execute(CONST_COMMANDS['get-greenhub-path'])
        command_executer.execute(script_options.get_cron_expression(
            absolute_path, greenhub_path))
        return
    
    if is_git_repo(command_executer):
        # get the current branch of the project
        branch = command_executer.execute(CONST_COMMANDS['git-branch-name'])

        if is_push_needed(command_executer, script_options.get_commits_number(), branch):
            '''
            GitHub paints the colors in the calendar of commits based on the date of the
            commit, so we need to change the date of the commits that are going to be
            pushed (and the rest that come after) to today.
            Each push will do this, so every commit goes into a different box in the
            calendar.
            '''
            change_commit_dates(command_executer, branch, current_time, git_folder_path)
            push_commits(command_executer, script_options.get_commits_number(), branch)


# Script start

if __name__ == '__main__':
    execute_script()


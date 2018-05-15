'''
This script pushes just the first unpushed commit to origin.
All rights reserved.

README

To use this software you need python version 3.5 at least installed in your computer.
There are two ways to execute this:
1. With a normal script execution.
2. With crontab so that it executes automatically.

To execute it just once go to the folder of the project you want to push (the one
with the .git folder) and run:
python3 greenGit.py [number-of-commits]

To execute it automatically each period of time you need to add it to crontab.
With this method you can forget about pushing to GitHub and the script will push
each day just the number of commits passed by parameter to the script (by default 1),
so that the commit map appears completely green.

To add the execution of the script to the crontab you need to follow the next steps
(on a MacOS):

'''

# Imports

import subprocess


# Global variables and methods

def hasGitSubfolder():
    '''
    Checks if the path where the script is being executed contains also a .git subfolder.
    @return true if there is the .git subfolder and false otherwise.
    '''
    pass

def numberOfCommitsToday():
    '''
    Checks the number of commits that has been done today.
    @return the number of commits done today.
    '''

def isPushNeeded():
    '''
    Checks if the number of commits for today hasn't still been done and if the folder
    where the script is being executed has a .git subfolder in it.
    @return true if there is a .git subfolder and the number of commits done today is
    less than number-of-commits, and false otherwise.
    '''
    pass

def executePush():
    pass


# Script start


# check if the folder has a .git subfolder
# check if the number of commits published today equals to the number of commits passed as parameter
# To do this check the log of the remote repository and check the date for today

# if both previous conditions are true then execute the next commands
# get the unpushed commits in chronological order: git log @{u}..HEAD --format=oneline --reverse
# check if there are commits available to be pushed
# get the branch and SHA of commit that has to be pushed
# push the first unpushed commit once we have its SHA: git push <remotename> <commit SHA>:<remotebranchname>

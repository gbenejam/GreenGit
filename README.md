# GreenHub
Useful tool for managing your commits and when they are pushed.
It's purpose is to change the date of your commits so that each day you have at least one commit and to push only a part of those commits each day.
With this (and some work on your part...) you will get GitHub's (or GitLab) activity map fully painted!


## Instructions

To use this software you need python version 3.6 at least installed in your computer.
There are two ways to execute this:
1. Normal script execution.
2. With crontab so that it executes automatically.

To execute it just once go to the folder of the project you want to push (the one
with the .git folder) and run:

`python3 greenGit.py [number-of-commits [crontab-expression]]`

You can also install the module so that it is accessible from any location in your computer. To do it download the project folder and execute the following command in it:

`python3 -m pip install .`

### Automatic execution

To execute it automatically each period of time you need to add it to crontab.
With this method you can forget about pushing to GitHub and the script will push
each day just the number of commits passed by parameter to the script (by default 1),
so that the commit map appears completely green.

To use the automatic execution you will need to leave your computer on and to have the SSH feature enabled to access the remote repository (or else the script will prompt for your password and it won't be automatic anymore...).

To generate the SSH keys and be able to use the crontab feature follow steps in:
https://help.github.com/articles/connecting-to-github-with-ssh/

### Script options

greenhub [options]

Separate the options with spaces. Do not group them.

#### -c cron expression

The parameters are received in order, so all the previous parameters are mandatory
in case you want to set a specific one. The parameters not set for the crontab-expression
will be considered as if they were '*'.

If you need to pass '*' as an argument to cron, you have to put it between quotes.

#### -v

Verbose. Prints all the commands the script is running and their output to the standard output.

#### -h

Help. Prints this usage in the command line.

#### -n commits_number

The number of commits to be pushed each day. Default is 1 commit per day.

#### -p path

The path of the project to be managed. If not specified it will be the current directory from where the command is being executed.

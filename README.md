# GreenHub
Useful tool for MacOS that uses the Commit of the Day approach to help you keep your Github green


## Instructions

To use this software you need python version 3.5 at least installed in your computer.
There are two ways to execute this:
1. With a normal script execution.
2. With crontab so that it executes automatically.

To execute it just once go to the folder of the project you want to push (the one
with the .git folder) and run:

`python3 greenGit.py [number-of-commits [crontab-expression]]`

To execute it automatically each period of time you need to add it to crontab.
With this method you can forget about pushing to GitHub and the script will push
each day just the number of commits passed by parameter to the script (by default 1),
so that the commit map appears completely green.

To add the execution of the script to the crontab you need to call this script with
the parameters that you would pass to create the cron scheduling. This is:

`python3 greenGit.py number-of-commits min hour day-of-month month day-of-week`

The parameters are received in order, so all the previous parameters are mandatory
in case you want to set a specific one. The parameters not set for the crontab-expression
will be considered as if they were '*'.

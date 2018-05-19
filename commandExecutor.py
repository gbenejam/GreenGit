'''
This script contains the wrapper object to allow greenGit.py to execute terminal commands.
'''

# Imports

import subprocess


class CommandExecuter():
    '''
    This class encapsulates the execution of commands and running callbacks when they finish
    executing.
    '''

    def __init__(self, cwd=None):
        '''
        Nothing to do here. This class is just a wrapper for some methods.
        '''
        self.cwd = cwd

    def execute(self, command, callback=None):
        '''
        This method gets the command to execute and runs it.
        @return the returncode of the command or the result of the callback if provided.
        '''
        command = __shell_injection_prevention__(command)
        result = subprocess.run(command, shell=True, cwd=self.cwd, stdout=subprocess.PIPE)

        # Decode the result so that it is readable
        output = result.stdout.decode('utf-8')

        if type(callback) == 'function':
            return callback(output)
        else:
            return output

    @staticmethod
    def __shell_injection_prevention__(command):
        '''
        This method prevents shell injection by scaping the quotes characters.
        Use single quotes, and put single quotes into double quotes.
        The string $'b is then quoted as '$'"'"'b'.
        '''
        return "'" + s.replace("'", "'\"'\"'") + "'"



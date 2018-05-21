'''
This script contains the wrapper object to allow greenGit.py to execute terminal commands.
'''

# Imports

import subprocess


def __shell_injection_prevention__(command):
    '''
    This method prevents shell injection by scaping the quotes characters.
    Use single quotes, and put single quotes into double quotes.
    The string $'b is then quoted as $'"'"'b.
    '''
    return command.replace("'", "'\"'\"'")

    
class CommandExecuter():
    '''
    This class encapsulates the execution of commands and running callbacks when they finish
    executing.
    '''

    def __init__(self, cwd, verbose=False):
        '''
        Nothing to do here. This class is just a wrapper for some methods.
        '''
        self.cwd = cwd
        self.verbose = verbose

    def log(self, text):
        '''
        This method logs the running command and the output if the object is set to be
        verbose.
        '''
        if self.verbose:
            print(text)
            
    def execute(self, command, callback=None):
        '''
        This method gets the command to execute and runs it.
        @return the returncode of the command or the result of the callback if provided.
        '''
        command = __shell_injection_prevention__(command)
        self.log(command)
        
        result = subprocess.run(command, shell=True, cwd=self.cwd, stdout=subprocess.PIPE)

        # Decode the result so that it is readable
        output = result.stdout.decode('utf-8')
        # Trim last end of line
        output = output.rstrip()
        self.log(output)
        
        if type(callback) == 'function':
            return callback(output)
        else:
            return output
        


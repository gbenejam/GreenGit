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
            
    def execute(self, command, callback=None, directory=None):
        '''
        This method gets the command to execute and runs it.
        @return the returncode of the command or the result of the callback if provided.
        '''
        self.log(command)

        working_dir = directory if directory is not None else self.cwd
        result = subprocess.run(command, shell=True, cwd=working_dir, stdout=subprocess.PIPE)

        # Decode the result so that it is readable
        output = result.stdout.decode('utf-8')
        # Trim last end of line
        output = output.rstrip()
        self.log('  ' + output)

        if type(callback).__name__ == 'function':
            self.log('Executing callback function: {}'.format(callback.__name__))
            return callback(output)
        else:
            return output
        


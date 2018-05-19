'''
This script contains the wrapper object to allow greenGit.py to execute terminal commands.
'''


class ExecutionException(Exception):
    '''
    Custom exception class to raise command line issues that may make the execution order
    impossible to be run.
    '''
    pass


class CommandExecuter():
    '''
    This class encapsulates the execution of all the available commands for this script.
    It provides a list with the commands that are possible to execute. 
    '''
    CONST_COMMANDS = {
        'cd' : __go_to_folder__
        'cron': __get_cron_command__
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
            command_to_execute = CONST_COMMANDS[command](command_generator)
        except KeyError:
            # Print the error and return negative number meaning failure of execution
            print('CommandExecuter - Unrecognized command')
            return -2
        except ExecutionException as error:
            print('ExecutionException: ' + repr(error)) 
            return -1

        # If we arrive here it means that command_to_execute is initialized
        command_to_execute = __shell_injection_prevention__(command_to_execute)
        result = subprocess.run(command_to_execute, shell=True)
        # To be able to read the output add stdout=subprocess.PIPE to the run call.
        # To read the result output execute: result.stdout.decode('utf-8')
        return result.returncode

    @staticmethod
    def __shell_injection_prevention__(command):
        '''
        This method prevents shell injection by scaping the quotes characters.
        Use single quotes, and put single quotes into double quotes.
        The string $'b is then quoted as '$'"'"'b'.
        '''
        return "'" + s.replace("'", "'\"'\"'") + "'"

    @staticmethod
    def __go_to_folder__(command_generator):
        '''
        This method generates the command to go to the project folder to be able to run
        all the other commands from there.
        command_generator is the CommandLineParameters object which contains the path of
        the project that needs to get commits pushed.
        '''
        return 'cd ' + command_generator.project_path
    
    @staticmethod
    def __get_cron_command__(command_generator):
        '''
        This is the function used to generate the cron expression to be run to schedule
        the the execution of this script.
        command_generator is an object of type CommandLineParameters, which can return a
        valid cron expression.
        '''
        try:
            return command_generator.get_cron_expression()
        except:
            raise ExecutionException('CommandExecuter - Could not get cron expression')


# command executer object ready to be used by scripts that import this one
command_executer = CommandExecuter()


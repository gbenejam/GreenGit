'''
This script contains the command line interpreter class to be able to read command line options
passed to the greenGit.py script.
'''


green_git_usage_str = ''


def __get_parameter__(parameter_number, parameter_list):
    '''
    Given a list (parameter_list), returns the object at position 'parameter_number'. 
    It makes sure that if the index is out of bounds the object returned will be properly
    default initialized.

    commits_number is default initialized to 1.
    Not specified cron parameters (minute, hour, ...) are initialized to '*'.
    '''
    if parameter_number >= len(parameter_list):
        # there is no parameter set and we need to initialize it
        if parameter_number == 1:
            return '.'
        elif parameter_number == 2:
            return 1
        else:
            return '*'

    return parameter_list[parameter_number]



class CommandLineInterpreter():
    '''
    Class to create objects that represent the command line options. Each command line parameter
    is listed in the object as a separate parameter and the __str__ method returns the command
    entered to the command line.
    '''
    cron_expression = '(crontab -l 2>/dev/null; echo "{0} {1} {2} {3} {4} {5} {6}") | crontab -'

    def __init__(self, parameter_list):
        '''
        Initializes the object with the parameters passed as argument.
        parameter_list is the list of parameters received through the command line execution.
        Those optional parameters that are not specified in the list will be initialized with a
        default value if needed.
        '''
        # path of the script
        self.project_path = __get_parameter__(1, parameter_list)
        
        # number of commits to be done
        self.commits_number = __get_parameter__(2, parameter_list)
        
        # get cron parameters
        self.minute = __get_parameter__(3, parameter_list)
        self.hour = __get_parameter__(4, parameter_list)
        self.month_day = __get_parameter__(5, parameter_list)
        self.month = __get_parameter__(6, parameter_list)
        self.week_day = __get_parameter__(7, parameter_list)

        # boolean to know if cron expression needs to be executed or not
        self.execute_cron = len(parameter_list) > 3

    def __str__(self):
        '''
        String representation of the command executed.
        '''
        return f'python3 {self.project_path} {self.commits_number} {self.minute} {self.hour} '\
            + f'{self.month_day} {self.month} {self.week_day}'

    def get_cron_expression(self):
        return CommandLineInterpreter.cron_expression.format(
            self.minute, self.hour, self.month_day, self.month, self.week_day,
            self.project_path, self.commits_number)



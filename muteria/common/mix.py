""" This Module implement some utility mathods used throughout the project.
        - The function `confirm_execution` is usefule to request user
            confirmation before proceeding the execution of a task that 
            is considered important to verify user certainty in proceeding.
            An example is the deletion of the data directory...
        - The class `ErrorHandler` define function that are called to 
            terminate the execution gracefully and informativelly 
            upon error. 
"""

from __future__ import print_function

import sys
import shutil
import logging
import inspect

def confirm_execution(question):
    """
    Ask user to enter Y or N (case-insensitive).

    :return: True if the answer is Y.
    :rtype: bool
    """
    reading_func = input
    if sys.version_info.major < 3:
        reading_func = eval('raw_input')
    answer = ""
    while answer not in ["y", "n"]:
        answer = reading_func("%s %s" % (question, "[Y/N] ")).lower()
    return answer == "y"
#~ def confirm_execution()

class ErrorHandler(object):
    repos_dir_manager = None
    # Make sure that there is no infinite recursive call to error_exit
    # if the function `RepositoryManager.revert_repository` make a call
    # to `error_exit`
    error_exit_revert_repo_called = False
    
    def __init__(self):
        pass

    @classmethod
    def set_corresponding_repos_manager(cls, repos_dir_manager):
        cls.assert_true (cls.repos_dir_manager is not None, \
                            err_string="the repo dir manager is already set", \
                            call_location=__file__)
        cls.repos_dir_manager = repos_dir_manager
    #~ def set_corresponding_repos_manager()

    @classmethod
    def error_exit(cls, err_string=None, call_location=None, error_code=1, \
                                                            ask_revert=True):
        if call_location is not None:
            logging.error("# Error happened in location {}".format(\
                                                            call_location))
        logging.error("#Error happened in function %s" % inspect.stack()[1][3])
        if err_string:
            logging.error(err_string)
        if ask_revert and not cls.error_exit_revert_repo_called:
            if confirm_execution("Do you want to revert repository files?"):
                logging.info("@ post error: Reverting repository files")
                cls.error_exit_revert_repo_called = True
                cls.repos_dir_manager.revert_repository(as_initial=False)
        else:
            logging.info("@ post error: Manually revert the repository files")
        print("# Exiting with code %d" % error_code)
        exit(error_code)
    #~ def error_exit()

    @classmethod
    def assert_true(cls, condition, err_string=None, \
                                call_location=None, ask_revert=True):
        '''
        Call this function with the parameter *__file__*
        as location_called_from
        '''
        if not condition:
            cls.error_exit(err_string=err_string, \
                            call_location=call_location, ask_revert=ask_revert)
    #~ def error_exit_file()
#~ class ErrorHandler

class GlobalConstants(object):
    UNCERTAIN_TEST_VERDICT = None

    PASS_TEST_VERDICT = False
    
    FAIL_TEST_VERDICT = True
    
    MUTANT_ALIVE_VERDICT = False
    
    MUTANT_KILLED_VERDICT = True
#~ class GlobalConstants
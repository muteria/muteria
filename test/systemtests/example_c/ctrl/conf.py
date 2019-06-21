import os
import subprocess

from muteria.configmanager.configurations import SessionMode
from muteria.configmanager.configurations import TestcaseToolsConfig
from muteria.configmanager.configurations import CriteriaToolsConfig
from muteria.drivers.testgeneration import TestToolType
from muteria.drivers.criteria import CriteriaToolType
from muteria.drivers.criteria import TestCriteria

from muteria.common.mix import GlobalConstants

this_dir = os.path.dirname(os.path.abspath(__file__))

devtestlist = ['test_lib.sh']
def dev_test_runner(test_name, repo_root_dir, exe_path_map, env_vars):
    # TODO: use exe_path_map

    if test_name == 'test_lib.sh':
        #TODO fix it
        cwd = os.getcwd()
        os.chdir(repo_root_dir)

        try:
            args_list = [test_name]
            p = subprocess.Popen(['bash']+args_list, \
                                             #close_fds=True, \
                                            stderr=subprocess.PIPE,\
                                            stdout=subprocess.PIPE)
            #stdout, stderr = p.communicate()
            #stdout = stdout.decode('UTF-8').splitlines()
            #stderr = stderr.decode('UTF-8').splitlines()
            retcode = p.wait()
        except:
            # ERROR
            return GlobalConstants.TEST_EXECUTION_ERROR
        
        # Parse the result
        hasfail = False
        hasfail |= (retcode != 0)

        os.chdir(cwd)
        return GlobalConstants.FAIL_TEST_VERDICT if hasfail else \
                                            GlobalConstants.PASS_TEST_VERDICT
    # ERROR
    return GlobalConstants.TEST_EXECUTION_ERROR
#~ def dev_test_runner()

def build_func(repo_root_dir, exe_rel_paths, compiler, flags_list, clean, reconfigure):
    cwd = os.getcwd()
    os.chdir(repo_root_dir)
    try:
        tmp_env = os.environ.copy()
        if compiler is not None:
            tmp_env["CC"] = compiler
        if flags_list is not None:
            tmp_env["CFLAGS"] = " ".join(flags_list)
        
        def print_err(sub_p, msg):
            stdout, stderr = sub_p.communicate()
            stdout = stdout.decode('UTF-8').splitlines()
            stderr = stderr.decode('UTF-8').splitlines()
            print(stdout)
            print(stderr)
        #~ def print_err()

        if reconfigure:
            args_list = ['clean']
            p = subprocess.Popen(['make']+args_list, env=tmp_env, \
                                                    stderr=subprocess.PIPE,\
                                                    stdout=subprocess.PIPE)
            retcode = p.wait()
            if retcode != 0:
                print_err(p, "reconfigure failed")
                os.chdir(cwd)
                return GlobalConstants.COMMAND_FAILURE 
        if clean:
            args_list = ['clean']
            p = subprocess.Popen(['make']+args_list, env=tmp_env, \
                                                    stderr=subprocess.PIPE,\
                                                    stdout=subprocess.PIPE)
            retcode = p.wait()
            if retcode != 0:
                print_err(p, "clean failed")
                os.chdir(cwd)
                return GlobalConstants.COMMAND_FAILURE 
        
        p = subprocess.Popen(['make'], env=tmp_env, stderr=subprocess.PIPE,\
                                                    stdout=subprocess.PIPE)
        retcode = p.wait()
        if retcode != 0:
            print_err(p, "clean failed")
            os.chdir(cwd)
            return GlobalConstants.COMMAND_FAILURE 
    except:
        os.chdir(cwd)
        return GlobalConstants.COMMAND_FAILURE

    os.chdir(cwd)
    return GlobalConstants.COMMAND_SUCCESS
#~ def build_func()

### 

PROGRAMMING_LANGUAGE='C'
REPOSITORY_ROOT_DIR=os.path.join(os.path.dirname(this_dir), 'repo')
OUTPUT_ROOT_DIR=os.path.join(os.path.dirname(this_dir), 'ctrl', "output")
RUN_MODE=SessionMode.EXECUTE_MODE

TARGET_SOURCE_INTERMEDIATE_CODE_MAP = {'lib/lib.c':'lib/lib.o', 'main.c':'main.o'}
REPO_EXECUTABLE_RELATIVE_PATHS = ['main']
CODE_BUILDER_FUNCTION = build_func

CUSTOM_DEV_TEST_RUNNER_FUNCTION = dev_test_runner
DEVELOPER_TESTS_LIST = devtestlist

TESTCASE_TOOLS_CONFIGS = [
        TestcaseToolsConfig(tooltype=TestToolType.USE_ONLY_CODE, toolname='custom_devtests', config_id=0),
]

ENABLED_CRITERIA = [
        TestCriteria.STATEMENT_COVERAGE, 
        TestCriteria.BRANCH_COVERAGE,
        TestCriteria.FUNCTION_COVERAGE,
]

gnucov = CriteriaToolsConfig(tooltype=CriteriaToolType.USE_ONLY_CODE, toolname='gcov', config_id=0)
CRITERIA_TOOLS_CONFIGS_BY_CRITERIA = {crit: [gnucov] for crit in ENABLED_CRITERIA} 
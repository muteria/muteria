import os
import subprocess

from muteria.configmanager.configurations import SessionMode
from muteria.configmanager.configurations import TestcaseToolsConfig
from muteria.configmanager.configurations import CriteriaToolsConfig
from muteria.configmanager.configurations import ToolUserCustom
from muteria.drivers.testgeneration import TestToolType
from muteria.drivers.criteria import CriteriaToolType
from muteria.drivers.criteria import TestCriteria
from muteria.drivers import DriversUtils

from muteria.repositoryandcode.build_utils.c import make_build_func

from muteria.common.mix import GlobalConstants

from muteria.drivers.testgeneration.testcase_formats.bash import \
                                                            bash_test_runner

this_dir = os.path.dirname(os.path.abspath(__file__))

devtestlist = ['test_lib.sh']
def dev_test_runner(test_name, *args, **kwargs):
    # TODO: use exe_path_map

    if test_name == 'test_lib.sh':
        return bash_test_runner(test_name, *args, **kwargs)

    # ERROR
    return GlobalConstants.TEST_EXECUTION_ERROR
#~ def dev_test_runner()

def build_func(*args, **kwargs):
    return make_build_func(*args, **kwargs)
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

# custom devtest
dev_test = TestcaseToolsConfig(tooltype=TestToolType.USE_ONLY_CODE, toolname='custom_devtests', config_id=0)
dev_test.set_one_test_execution_timeout(2)

# klee tests
klee_test = TestcaseToolsConfig(tooltype=TestToolType.USE_ONLY_CODE, toolname='klee', \
                        tool_user_custom=ToolUserCustom(POST_TARGET_CMD_ORDERED_FLAGS_LIST=[('-sym-args', '2', '2', '2')]))
klee_test.set_one_test_execution_timeout(2)

# test tool list
TESTCASE_TOOLS_CONFIGS = [
        dev_test, #klee_test,
]

ENABLED_CRITERIA = [
        TestCriteria.STATEMENT_COVERAGE, 
        TestCriteria.BRANCH_COVERAGE,
        TestCriteria.FUNCTION_COVERAGE,
        TestCriteria.WEAK_MUTATION,
        TestCriteria.MUTANT_COVERAGE,
        TestCriteria.STRONG_MUTATION,
]

gnucov = CriteriaToolsConfig(tooltype=CriteriaToolType.USE_ONLY_CODE, toolname='gcov', config_id=0)
mart = CriteriaToolsConfig(tooltype=CriteriaToolType.USE_ONLY_CODE, toolname='mart', config_id=0)
CRITERIA_TOOLS_CONFIGS_BY_CRITERIA = {}
CRITERIA_TOOLS_CONFIGS_BY_CRITERIA[TestCriteria.STATEMENT_COVERAGE] = [gnucov] 
CRITERIA_TOOLS_CONFIGS_BY_CRITERIA[TestCriteria.BRANCH_COVERAGE] = [gnucov]
CRITERIA_TOOLS_CONFIGS_BY_CRITERIA[TestCriteria.FUNCTION_COVERAGE] = [gnucov] 
CRITERIA_TOOLS_CONFIGS_BY_CRITERIA[TestCriteria.WEAK_MUTATION] = [mart] 
CRITERIA_TOOLS_CONFIGS_BY_CRITERIA[TestCriteria.MUTANT_COVERAGE] = [mart] 
CRITERIA_TOOLS_CONFIGS_BY_CRITERIA[TestCriteria.STRONG_MUTATION] = [mart] 

LOG_DEBUG = True
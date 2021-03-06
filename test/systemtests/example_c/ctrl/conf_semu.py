
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _conf import *
sys.path.pop(0)

import muteria.drivers.testgeneration.tools_by_languages.c.semu.semu \
                                                                as semu_module

# semu tests
semu_test = TestcaseToolsConfig(tooltype=TestToolType.USE_CODE_AND_TESTS, toolname='semu', \
                        tool_user_custom=ToolUserCustom(
                            PRE_TARGET_CMD_ORDERED_FLAGS_LIST=[
                                #('-semu-disable-statediff-in-testgen',),
                                #('-semu-continue-mindist-out-heuristic',),
                                #('-semu-use-basicblock-for-distance',),
                                ('-semu-forkprocessfor-segv-externalcalls',),
                                #('-semu-testsgen-only-for-critical-diffs',),
                                #('-semu-consider-outenv-for-diffs',),

                                ('-semu-mutant-max-fork', '0'),
                                ('-semu-checknum-before-testgen-for-discarded', '2'),
                                ('-semu-mutant-state-continue-proba', '0.25'),
                                ('-semu-precondition-length', '0'), # start from top
                                #('-semu-max-total-tests-gen', '1000')
                                ('-semu-max-tests-gen-per-mutant', '5'),
                            ], 
                            POST_TARGET_CMD_ORDERED_FLAGS_LIST=[('-sym-args', '2', '2', '2')]
                            )
                        )
semu_test.set_one_test_execution_timeout(2)
semu_test.set_test_gen_maxtime(60)

# test tool list
TESTCASE_TOOLS_CONFIGS = [
        dev_test, semu_test,
]

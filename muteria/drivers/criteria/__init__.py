
from __future__ import print_function

import muteria.common.mix as common_mix

class CriteriaToolType(common_mix.EnumAutoName):
    USE_ONLY_CODE = "StaticCriteriaTool"
    #USE_CODE_AND_TESTS = "DynamicCriteriaTool"

    def get_tool_type_classname(self):
        return self.get_field_value()
    #~ def get_tool_type_classname():
#~ class CriteriaToolType

class TestCriteria(common_mix.EnumAutoName):
    STATEMENT_COVERAGE = "statement_coverage"
    BRANCH_COVERAGE = "branch_coverage"
    FUNCTION_COVERAGE = "function_coverage"

    MUTANT_COVERAGE = "mutant_coverage"
    WEAK_MUTATION = "weak_mutation"
    STRONG_MUTATION = "strong_mutation"
#~ class TestCriteria
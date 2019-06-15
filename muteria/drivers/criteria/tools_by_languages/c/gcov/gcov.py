
from __future__ import print_function

import os
import sys
import re
import shutil
import shlex
import logging
import subprocess

import muteria.common.mix as common_mix
import muteria.common.fs as common_fs

from muteria.repositoryandcode.codes_convert_support import CodeFormats
from muteria.repositoryandcode.callback_object import DefaultCallbackObject

from muteria.drivers.criteria.base_testcriteriatool import BaseCriteriaTool
from muteria.drivers.criteria import TestCriteria
from muteria.drivers import DriversUtils

ERROR_HANDLER = common_mix.ErrorHandler

class CriteriaToolGCov(BaseCriteriaTool):
    def __init__(self, *args, **kwargs):
        BaseCriteriaTool.__init__(self, *args, **kwargs)
        self.instrumentation_details = os.path.join(\
                    self.instrumented_code_storage_dir, '.instru.meta.json')
        self.gcov_files_list_filename = "gcov_files.json"
        self.gc_files_dir = os.path.join(\
                                        self.criteria_working_dir, "gcno_gcda")
        self.instrument_callback_obj = self.InstrumentCallbackObject()
        self.instrument_callback_obj.set_post_callback_args(self.gc_files_dir)
        # clean any possible gcda file
        for file_ in self._get_gcda_list():
            os.remove(file_)
        for file_ in self._get_gcov_list():
            os.remove(file_)
    #~ def __init__()

    def _get_gcov_list(self):
        gcov_files = []
        for root, dirs, files in os.walk(self.gc_files_dir):
            for file_ in files:
                if file_.endswith('.gcov'):
                    gcov_files.append(os.path.join(root, file_))
        return gcov_files
    #~ def _get_gcov_list()

    def _get_gcda_list(self):
        gcda_files = []
        for root, dirs, files in os.walk(self.gc_files_dir):
            for file_ in files:
                if file_.endswith('.gcda'):
                    gcda_files.append(os.path.join(root, file_))
        return gcda_files
    #~ def _get_gcda_list()

    class InstrumentCallbackObject(DefaultCallbackObject):
        def after_command(self):
            gc_files_dir = self.post_callback_args
            for _, obj in list(self.source_files_to_objects.items()):
                rel_raw_filename, _ = os.path.splitext(obj)
                gcno_file = rel_raw_filename + '.gcno' 
                relloc = os.path.join(gc_files_dir, os.path.dirname(obj))
                if not os.path.isdir(relloc):
                    os.makedirs(relloc)
                shutil.copy2(os.path.join(self.repository_rootdir, gcno_file),\
                                    os.path.join(gc_files_dir, gcno_file))
            return DefaultCallbackObject.after_command(self)
        #~ def after_command()
    #~ class InstrumentCallbackObject

    @classmethod
    def installed(cls, custom_binary_dir=None):
        """ Check that the tool is installed
            :return: bool reprenting whether the tool is installed or not 
                    (executable accessible on the path)
                    - True: the tool is installed and works
                    - False: the tool is not installed or do not work
        """
        for prog in ('gcc', 'gcov'):
            if not DriversUtils.check_tool(prog=prog, args_list=['--version'],\
                                                    expected_exit_codes=[0]):
                return False
        return True
    #~ def installed()

    @classmethod
    def _get_meta_instrumentation_criteria(cls):
        """ Criteria where all elements are instrumented in same file
            :return: list of citeria
        """
        return [
                TestCriteria.STATEMENT_COVERAGE,
                TestCriteria.BRANCH_COVERAGE,
                TestCriteria.FUNCTION_COVERAGE,
               ]
    #~ def _get_meta_instrumentation_criteria()

    @classmethod
    def _get_separated_instrumentation_criteria(cls):
        """ Criteria where all elements are instrumented in different files
            :return: list of citeria
        """
        return []
    #~ def _get_separated_instrumentation_criteria()

    def get_instrumented_executable_paths(self, enabled_criteria):
        crit_to_exes_map = {}
        obj = common_fs.loadJSON(self.instrumentation_details)
        exes = [p for _, p in list(obj.items())]
        for criterion in enabled_criteria:
            crit_to_exes_map[criterion] = exes
        return crit_to_exes_map
    #~ def get_instrumented_executable_paths()

    def _get_criterion_element_executable_path(self, criterion, element_id):
        ERROR_HANDLER.error_exit("not applicable for gcov", __file__)
    #~ def _get_criterion_element_executable_path

    def _get_criterion_element_environment_vars(self, criterion, element_id):
        '''
            return: python dictionary with environment variable as key
                     and their values as value (all strings)
        '''
        ERROR_HANDLER.error_exit("not applicable for gcov", __file__)
    #~ def _get_criterion_element_environment_vars()

    def _get_criteria_environment_vars(self, result_dir_tmp, enabled_criteria):
        '''
        return: python dictionary with environment variable as key
                     and their values as value (all strings)
        '''
        ERROR_HANDLER.error_exit("not applicable for gcov", __file__)
    #~ def _get_criteria_environment_vars()

    def _collect_temporary_coverage_data(self, criteria_name_list, \
                                            test_execution_verdict, \
                                            used_environment_vars, \
                                                    result_dir_tmp):
        ''' get gcov files from gcda files into result_dir_tmp
        '''
        prog = 'gcov'

        cov2flags = {
                    TestCriteria.STATEMENT_COVERAGE: [],
                    TestCriteria.BRANCH_COVERAGE: ['-b', '-c'],
                    TestCriteria.FUNCTION_COVERAGE: ['-f'],
                }

        args_list = []
        for criterion in criteria_name_list:
            args_list += cov2flags[criterion]

        gcda_files = self._get_gcda_list()

        raw_filename_list = [os.path.splitext(f) for f in gcda_files]
        args_list += raw_filename_list
        
        if len(gcda_files) > 0:
            # collect gcda (gcno)
            p = subprocess.Popen([prog]+args_list, close_fds=True, \
                                            stderr=subprocess.DEVNULL,\
                                            stdout=subprocess.DEVNULL)
            retcode = p.wait()
            if retcode != 0:
                ERROR_HANDLER.error_exit("Program {} {}.".format(prog,\
                        'error collecting coverage is problematic'), __file__)
            
            # delete gcda
            for gcda_f in gcda_files:
                os.remove(gcda_f)
            
            common_fs.dumpJSON(self._get_gcov_list(), \
                                os.path.join(result_dir_tmp,\
                                                self.gcov_files_list_filename))
    #~ def _collect_temporary_coverage_data()

    def _extract_coverage_data_of_a_test(self, enabled_criteria, \
                                    test_execution_verdict, result_dir_tmp):
        ''' read json files and extract data
            return: the dict of criteria with covering count
        '''
        gcov_list = common_fs.loadJSON(os.path.join(result_dir_tmp,\
                                                self.gcov_files_list_filename))
        
        res = {c: {} for c in enabled_criteria}

        func_cov = None
        branch_cov = None
        statement_cov = {}
        if TestCriteria.FUNCTION_COVERAGE in enabled_criteria:
            func_cov = res[TestCriteria.FUNCTION_COVERAGE]
        if TestCriteria.BRANCH_COVERAGE in enabled_criteria:
            branch_cov = res[TestCriteria.BRANCH_COVERAGE]
        if TestCriteria.STATEMENT_COVERAGE in enabled_criteria:
            statement_cov = res[TestCriteria.STATEMENT_COVERAGE]

        for gcov_file in gcov_list:
            with open(gcov_file) as fp:
                last_line = None
                src_file = None
                for raw_line in fp:
                    line = raw_line.strip()
                    col_split = [v.strip() for v in line.split(':')]

                    if len(col_split) > 2 and col_split[1] == '0':
                        # preamble
                        if col_split[2] == "Source":
                            src_file = col_split[3]
                    elif line.startswith("function "):
                        # match function
                        parts = line.split()
                        ident = DriversUtils.make_meta_element(parts[1], \
                                                                    src_file)
                        func_cov[ident] = int(parts[3])
                    elif line.startswith("branch "):
                        # match branch
                        parts = line.split()
                        ident = DriversUtils.make_meta_element(parts[1], \
                                                                    last_line)
                        branch_cov[ident] = int(parts[3])

                    elif len(col_split) > 2 and \
                                            re.match(r"^\d+$", col_split[1]):
                        # match line
                        if col_split[0] == '-':
                            continue
                        last_line = DriversUtils.make_meta_element(\
                                                        col_split[1], src_file)
                        if col_split[0] in ('#####', '====='):
                            exec_count = 0
                        else:
                            exec_count = \
                                    int(re.findall(r'^\d+', col_split[0])[0])
                        statement_cov[last_line] = exec_count

        # delete gcov files
        for gcov_f in self._get_gcov_list():
            os.remove(gcov_f)

        return res
    #~ def _extract_coverage_data_of_a_test()

    def _do_instrument_code (self, outputdir, exe_path_map, \
                                        code_builds_factory, \
                                        enabled_criteria, parallel_count=1):
        # Setup
        if os.path.isdir(self.instrumented_code_storage_dir):
            shutil.rmtree(self.instrumented_code_storage_dir)
        os.mkdir(self.instrumented_code_storage_dir)
        if os.path.isdir(self.gc_files_dir):
            shutil.rmtree(self.gc_files_dir)
        os.mkdir(self.gc_files_dir)

        prog = 'gcc'

        flags = ['--coverage', '-fprofile-dir', self.gc_files_dir, '-O0']
        additionals = ["-fkeep-inline-functions", "-fkeep-static-functions"]
        
        flags += additionals
        
        rel_path_map = {}
        exes, _ = code_builds_factory.repository_manager.get_relative_exe_map()
        for exe in exes:
            filename = os.path.basename(exe)
            rel_path_map[exe] = os.path.join(\
                                self.instrumented_code_storage_dir, filename)
        ret = code_builds_factory.transform_src_into_dest(\
                        src_fmt=CodeFormats.C_SOURCE,\
                        dest_fmt=CodeFormats.NATIVE_CODE,\
                        src_dest_files_paths_map=rel_path_map,\
                        compiler=prog, flags=flags, clean_tmp=True, \
                        reconfigure=True, \
                        callback_object=self.instrument_callback_obj)
        # write down the rel_path_map
        ERROR_HANDLER.assert_true(not os.path.isfile(\
                self.instrumentation_details), "must not exist here", __file__)
        common_fs.dumpJSON(rel_path_map, self.instrumentation_details)

        if not ret:
            ERROR_HANDLER.error_exit("Program {} {}.".format(prog,\
                                        'but problematic'), __file__)
    #~ def _do_instrument_code()
#~ class CriteriaToolGCov
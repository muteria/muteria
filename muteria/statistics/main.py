
from __future__ import print_function

import os
import shutil
from jinja2 import Template
import webbrowser

import muteria.common.mix as common_mix
import muteria.common.matrices as common_matrices

import muteria.statistics.algorithms as stats_algo

import muteria.controller.explorer as fd_structure

ERROR_HANDLER = common_mix.ErrorHandler

class StatsComputer(object):
    @staticmethod
    def merge_lmatrix_into_right(lmatrix_file, rmatrix_file):
        lmatrix = common_matrices.ExecutionMatrix(filename=lmatrix_file)
        if not os.path.isfile(rmatrix_file):
            shutil.copy2(lmatrix_file, rmatrix_file)
        else:
            rmatrix = common_matrices.ExecutionMatrix(filename=rmatrix_file)
            rmatrix.update_with_other_matrix(lmatrix)
            rmatrix.serialize()

    @staticmethod
    def compute_stats(config, explorer):
        # get the matrix of each test criterion
        coverages = {}
        for c in config.ENABLED_CRITERIA.get_val():
            if explorer.file_exists(fd_structure.CRITERIA_MATRIX[c]):
                mat_file = explorer.get_existing_file_pathname(\
                                            fd_structure.CRITERIA_MATRIX[c])
                mat = common_matrices.ExecutionMatrix(filename=mat_file)
                row2collist = mat.query_active_columns_of_rows()
                cov = len([k for k,v in row2collist.items() if len(v) > 0])
                tot = len(row2collist)
                coverages[c.get_str()] = '{:.2f}'.format(cov * 100.0 / tot)
        
        template_file = os.path.join(os.path.dirname(\
                            os.path.abspath(__file__)), 'summary_report.html')
        report_file = explorer.get_file_pathname(\
                                            fd_structure.STATS_MAIN_FILE_HTML)
        rendered = Template(open(template_file).read()).render( \
                                                    {'coverages':coverages})
        with open(report_file, 'w') as f:
            f.write(rendered)
        print(coverages)
        webbrowser.open('file://' + report_file,new=2)
#~ class DataHandling
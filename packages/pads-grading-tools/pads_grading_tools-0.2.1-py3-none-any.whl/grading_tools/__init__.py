from grading_tools.common.commands import CliProgram
from grading_tools.common.defaults import MinimalConfig
from grading_tools.upload_export_gen import *
from grading_tools.table_gen import *
from grading_tools.diagram_gen import *
from grading_tools.merging import *


def mk_cli_program(default_config: MinimalConfig | None = None) -> CliProgram:
    return CliProgram('grading-toolbox', GenExcelTable, GenDiagram, GenGroupUpload, GenGradeUpload, Merging,
                      default_config=default_config)


if __name__ == '__main__':
    mk_cli_program().parse_and_run()

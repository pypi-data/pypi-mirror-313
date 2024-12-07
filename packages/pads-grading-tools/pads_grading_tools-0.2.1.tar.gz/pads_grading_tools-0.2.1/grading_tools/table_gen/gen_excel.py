from typing import Any

from grading_tools.common.commands import CommandModule
from grading_tools.table_gen.grading_table_commons import COLUMN_NAME_LEVEL_START
from .gen_assignment_groups_table import register_gen_group_info, gen_group_info_table
from .gen_grading_table import register_gen_grading_table, gen_grading_table


class GenExcelTable(CommandModule):
    module_name = 'gen-excel'
    commands = [('grading', register_gen_grading_table, gen_grading_table),
                ('groups-info', register_gen_group_info, gen_group_info_table)]

    @property
    def additional_config(self) -> dict[str, Any]:
        nd = self.default_config['naming_dictionary']
        return {
            'DEFAULT_GRADING_FILE_NAME': 'grading.xlsx',
            'DEFAULT_INDEX_COLUMNS': list(nd.IDENTITY_COLS) + [nd.MATR_COL],
            'AUX_SHEET_NAME': 'Aux',
            'DEFAULT_SHEET_NAME': nd.GRADING_SHEET_NAME,
            'DEFAULT_TABLE_NAME': nd.GRADING_TABLE_NAME,
            'FALLBACK_SCORE': '',
            'CHECKBOX_SYMBOL': 'x',
            'placeholder_row_count': 10,
            'upper_label_level': COLUMN_NAME_LEVEL_START,
        } | {
            'DEFAULT_GROUP_FORMATS': ['Group A1 {:03}', 'Group A2 {:03}'],
            'DEFAULT_GROUPS_FILE_NAME': 'moodle-groups-info.xlsx',
            'DEFAULT_GROUPING_NAMES': ['Assignment Part 1', 'Assignment Part 2'],
        }


if __name__ == '__main__':
    GenExcelTable().as_program('gen').parse_and_run()

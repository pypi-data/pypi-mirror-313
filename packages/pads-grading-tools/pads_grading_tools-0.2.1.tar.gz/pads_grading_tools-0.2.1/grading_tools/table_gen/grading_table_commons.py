from __future__ import annotations

from typing import Sequence, Iterable

import pandas as pd

from grading_tools.common.gradable_spec import GradableNode, GradableSpec
from grading_tools.common.utils import read_generic_table

COLUMN_NAME_LEVEL_START = 1
GK_INFO_TABLE_NAME = 'GKInfo'


def equalize(p: tuple, pad_to: int, trim_front: int = 0):
    if trim_front > 0:
        p = p[trim_front:]
    return p + (p[-1],) * max(pad_to - len(p), 0)


def mk_name(path: Sequence[str], start_depth: int = 1) -> str:
    return '-'.join(path[start_depth:])


def mk_node_name(n: GradableNode, start_depth: int = COLUMN_NAME_LEVEL_START) -> str:
    return mk_name(tuple(n.label for n in n.ancestry), start_depth)


def mk_sum_formula_over_ranges(ranges: list[list[GradableNode]],
                               output_table: str,
                               max_points: float | None = None,
                               with_equals: bool = True,
                               upper_label_level: int = COLUMN_NAME_LEVEL_START, **config) -> tuple[str, bool]:
    formula = ''
    for i, local_range in enumerate(ranges):
        s, e = local_range[0], local_range[-1]
        if i > 0:
            formula += '+'
        formula += f'SUM([@[{mk_node_name(s, upper_label_level)}]:[{mk_node_name(e, upper_label_level)}]])'
    if max_points:
        formula = f'MIN({max_points},{formula})'
    if with_equals:
        formula = '=' + formula
    return formula, False


def mk_mandatory_col_disjunction(nodes: Iterable[GradableNode], upper_label_level: int = COLUMN_NAME_LEVEL_START,
                                 **config) -> str | None:
    s = ', '.join((f'[@[{mk_node_name(n, upper_label_level)}]]="{config["CHECKBOX_SYMBOL"]}"' for n in nodes if
                   n.get_info('mandatory')))
    return f'OR({s})' if s else None


def mk_mandatory_col_condition(nodes: Iterable[Iterable[GradableNode]], **config) -> str | None:
    s = ', '.join((dis for rng in nodes if (dis := mk_mandatory_col_disjunction(rng, **config))))
    return f'AND({s})' if s else None


def mk_marked_formula_over_ranges(ranges: list[list[GradableNode]],
                                  output_table: str,
                                  max_points: float | None = None,
                                  with_equals: bool = True,
                                  upper_label_level: int = COLUMN_NAME_LEVEL_START, **config) -> tuple[str, bool]:
    formula = ''
    mandatory_col_groups = []
    for i, local_range in enumerate(ranges):
        s, e = local_range[0], local_range[-1]
        start_col = mk_node_name(s, upper_label_level)
        end_col = mk_node_name(e, upper_label_level)
        # cancelled due to excel non-cooperation
        # this formula works if it is intered via the interface..
        # local_formula = f'SUMPRODUCT(IF([@[{start_col}]:[{end_col}]]="{config["CHECKBOX_SYMBOL"]}", 1, 0), INDEX({GK_INFO_TABLE_NAME}[[{start_col}]:[{end_col}]], 1,))'
        cns = (mk_node_name(n, upper_label_level) for n in local_range)
        ifs = (f'IF([@[{c}]]="{config["CHECKBOX_SYMBOL"]}", INDEX({GK_INFO_TABLE_NAME}[[{c}]], 1), 0)' for c in cns)
        local_formula = f'SUM({", ".join(ifs)})'
        # local_formula = f'SUM(IF([@[{start_col}]:[{end_col}]]="{config["CHECKBOX_SYMBOL"]}", 1, 0) * INDEX({GK_INFO_TABLE_NAME}[[{start_col}]:[{end_col}]], 1,))'

        mandatory_col_options = [n for n in local_range if n.get_info('mandatory')]
        if len(mandatory_col_options) > 0:
            mandatory_col_groups.append(mandatory_col_options)
        if i > 0:
            formula += '+'
        formula += local_formula
    if len(mandatory_col_groups) > 0:
        s = mk_mandatory_col_condition(mandatory_col_groups, **config)
        if s:
            formula = f'IF({s}, {formula}, "")'
    if max_points:
        formula = f'MIN({max_points},{formula})'
    if with_equals:
        formula = '=' + formula
    return formula, False


def mk_sum_formula_range(summary_range: Iterable[GradableNode]) -> tuple[list[list[GradableNode]], float]:
    local_max_pts = 0
    ranges = []
    range_start, range_end = (None, None)
    local_range = []
    gap = True
    for j, c in enumerate(summary_range):
        if not c.get_info('bonus') and not c.get_info('skip') and not c.get_info('skip_in_total'):
            local_max_pts += c.pts

        if c.get_info('skip') or c.get_info('skip_in_formula'):
            if not gap:
                assert local_range[0] == range_start
                assert local_range[-1] == range_end
                ranges.append(local_range)
            local_range = []
            range_start = None
            gap = True
        else:
            if gap:
                local_range = []
                range_start = c
                gap = False
        range_end = c
        local_range.append(c)
    if not gap:
        assert local_range[0] == range_start
        assert local_range[-1] == range_end
        ranges.append(local_range)
    return ranges, local_max_pts


def mk_header_info(spec: GradableSpec, cutoff_level: str | int | None = None, totals_level: str | int | None = None,
                   **config) -> tuple[
    pd.MultiIndex, list[str], list[float], list[tuple[str, ...]]]:
    if cutoff_level is not None:
        if type(cutoff_level) is str:
            cutoff_level = spec.levels.index(cutoff_level)
        spec = spec.cutoff(cutoff_level)
        if config['verbose']:
            print(f'Trimmed spec to depth {cutoff_level}')
            print(spec)
    point_tree = spec.tree  # assumed to be `complete()`
    if totals_level is not None:
        if type(totals_level) is str:
            totals_level = spec.levels.index(totals_level)
        point_tree.add_summaries(totals_level)
    max_pts = sum(n.pts for n in point_tree.leaves_iter() if not n.get_info('bonus') and not n.get_info('skip'))
    pts_list = list(map(lambda n: n.pts, point_tree.leaves_iter()))
    paths = list(point_tree.paths_iter(lambda n: n.label))
    depth = max(map(len, paths))
    paths_list = [equalize(p, depth) for p in paths]
    header_index = pd.MultiIndex.from_tuples(paths_list, names=spec.levels[:depth])
    column_names_list = [mk_node_name(n) for n in point_tree.leaves_iter()]
    return header_index, column_names_list, pts_list, paths_list


def mk_initialization_df(spec: GradableSpec, column_names_list: list[str], **config) -> pd.DataFrame:
    index_columns = config.get('index_columns', config['DEFAULT_INDEX_COLUMNS'])
    df = None
    if (data_df := config.get('data_df')) is not None:
        df = data_df
    elif (data_file := config.get('data_file')) is not None:
        df = read_generic_table(data_file, sheet_name=config.pop('data_sheet', None),
                                table_name=config.pop('data_table', None))
        df = df.set_index(index_columns, drop=True)
    if df is not None:
        keep = {mk_node_name(n) for n in spec.tree.leaves_iter() if not n.get_info('skip')}
        keep = [c for c in df.columns if c in keep]
        initialization_df = df[keep].reindex(columns=column_names_list)
    else:
        if index_file := config.get('index_file'):
            df = read_generic_table(index_file,
                                    columns=(index_columns if 'index_columns' in config else None),
                                    sheet_name=config.pop('index_sheet', None),
                                    table_name=config.pop('index_table', None))
            data_index = pd.MultiIndex.from_frame(df)
        else:
            data_index = pd.MultiIndex.from_tuples(
                [tuple(i for _ in index_columns) for i in range(config.get('placeholder_row_count', 1))],
                names=index_columns)
        initialization_df = pd.DataFrame(data=None, columns=column_names_list, dtype='Float64').reindex(data_index)
    return initialization_df

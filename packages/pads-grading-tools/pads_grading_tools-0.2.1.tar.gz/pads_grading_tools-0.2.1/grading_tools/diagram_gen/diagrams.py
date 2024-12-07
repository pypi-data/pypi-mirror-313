import argparse
import os

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from grading_tools.common.commands import CommandModule
from grading_tools.common.defaults import NamingDictionary
from grading_tools.common.gradable_spec import load_spec
from grading_tools.common.utils import read_generic_table, get_possible_grades


def save_plot(fig: go.Figure, name, **config):
    fig.write_image(os.path.join(config['output'], name), format=config['output_format'])


def gen_overview_figs(grades_file: str,
                      naming_dictionary: NamingDictionary,
                      **config):
    scores_plot_title = config['SCORES_TITLE']
    grades_plot_title = config['GRADES_TITLE']
    df = read_generic_table(grades_file, table_name=config.pop('grades_table', None),
                            sheet_name=config.pop('grades_sheet', None))

    melted_scores = df.melt(id_vars=[naming_dictionary.MATR_COL],
                            value_vars=[naming_dictionary.ASSIGNMENT_SCORE_COL, naming_dictionary.EXAM_SCORE_COL,
                                        naming_dictionary.COURSE_SCORE_COL],
                            var_name='Kind', value_name='Score')

    fig_scores_a = px.histogram(melted_scores, x='Score', template='plotly_white', color='Kind', barmode='group',
                                title=scores_plot_title,
                                nbins=25)
    fig_scores_b = px.histogram(melted_scores, x='Score', template='plotly_white', facet_row='Kind',
                                title=scores_plot_title,
                                nbins=25)
    save_plot(fig_scores_a, f'scores-overview-a.png', **config)
    save_plot(fig_scores_b, f'scores-overview-b.png', **config)

    melted_grades = df.melt(id_vars=[naming_dictionary.MATR_COL],
                            value_vars=[naming_dictionary.EXAM_GRADE_COL, naming_dictionary.COURSE_GRADE_COL],
                            var_name='Kind',
                            value_name='Grade')

    possible_grades = get_possible_grades(absent=False)
    # simply append the other statuses, e.g., "did not show"
    possible_grades.extend(
        (set(df[naming_dictionary.EXAM_GRADE_COL].unique()) | set(
            df[naming_dictionary.COURSE_GRADE_COL].unique())) - set(possible_grades))

    fig_grades_a = px.histogram(melted_grades, x='Grade', template='plotly_white', color='Kind', barmode='group',
                                title=grades_plot_title, category_orders={'Grade': possible_grades})
    fig_grades_b = px.histogram(melted_grades, x='Grade', template='plotly_white', facet_row='Kind',
                                title=grades_plot_title,
                                category_orders={'Grade': possible_grades})

    return fig_grades_a, fig_grades_b


def gen_overview(**config):
    fig_grades_a, fig_grades_b = gen_overview_figs(**config)
    save_plot(fig_grades_a, f'grades-overview-1.png', **config)
    save_plot(fig_grades_b, f'grades-overview-2.png', **config)


def gen_per_question_fig(gradable_spec: str, grading_file: str, naming_dictionary: NamingDictionary, **config):
    spec = load_spec(gradable_spec)
    points_df = read_generic_table(grading_file, table_name=config.pop('grading_table', None),
                                   sheet_name=config.pop('grading_sheet', None))

    for c in points_df.columns:
        if c.startswith('Q') and '-' not in c:
            points_df[c + '-Total'] = points_df[c]
    total_cols = [c for c in points_df.columns if c.startswith('Q') and c.endswith('-Total')]  # ouch
    question_totals = points_df[[naming_dictionary.MATR_COL] + total_cols]

    melted_question_totals = question_totals.melt(id_vars=[naming_dictionary.MATR_COL], var_name='Question',
                                                  value_name='Points')

    total_cols_ordered = [q.label + '-Total' for q in spec.get_level('Question')]
    fig = make_subplots(rows=len(total_cols), subplot_titles=total_cols_ordered, x_title='Points')

    for i, q in enumerate(spec.get_level('Question'), 1):
        col = q.label + '-Total'
        g = go.Histogram(x=melted_question_totals[melted_question_totals['Question'] == col]['Points'], name=col,
                         xbins=dict(start=-0.5, end=int(np.ceil(q.pts + 0.5)), size=1))
        fig.add_trace(g, row=i, col=1)
        fig.update_xaxes(range=[0, q.pts], tick0=0, row=i, col=1)

    fig.update_layout(height=2000, title_text='Points per Question', template='plotly_white')
    return fig


def gen_per_question(**config):
    fig = gen_per_question_fig(**config)
    save_plot(fig, f'points-per-question.png', **config)


def configure_parser_per_question(parser: argparse.ArgumentParser, **defaults):
    parser.add_argument('-gs', '--gradable-spec', required=True, help='Path to the specification of this gradable.')
    parser.add_argument('-gp', '--grading-file', required=True, help='Path to grading file with per-question points.')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-gpsh', '--grading-sheet', required=False, help='Optionally, excel sheet within grading file.')
    group.add_argument('-gpt', '--grading-table', required=False, help='Optionally, excel table within grading file.')


def configure_parser_overview(parser: argparse.ArgumentParser, naming_dictionary: NamingDictionary, **defaults) -> None:
    parser.add_argument('-gr', '--grades-file', required=True, help='Path to the grading/scores file.', dest='grades_file')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-grsh', '--grades-sheet', required=False, help='Optionally, excel sheet within grades file.')
    group.add_argument('-grt', '--grades-table', required=False, help='Optionally, excel table within grades file.',
                       default=naming_dictionary.OVERVIEW_TABLE_NAME)

    parser.add_argument('--assignment-score-column', required=False, help='Column with assignment score.',
                        default=naming_dictionary.ASSIGNMENT_SCORE_COL, dest='ASSIGNMENT_SCORE_COL')
    parser.add_argument('--exam-score-column', required=False, help='Column with exam score.',
                        default=naming_dictionary.EXAM_SCORE_COL, dest='EXAM_SCORE_COL')
    parser.add_argument('--course-score-column', required=False, help='Column with course total score.',
                        default=naming_dictionary.COURSE_SCORE_COL, dest='COURSE_SCORE_COL')
    parser.add_argument('--exam-grade-column', required=False, help='Column with exam grade.',
                        default=naming_dictionary.EXAM_GRADE_COL, dest='EXAM_GRADE_COL')
    parser.add_argument('--course-grade-column', required=False, help='Column with course grade.',
                        default=naming_dictionary.COURSE_GRADE_COL, dest='COURSE_GRADE_COL')


def configure_base_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('-o', '--output', required=False, help='Path to output directory.', default='./')
    parser.add_argument('-of', '--output-format', required=False, choices=['png', 'svg', 'jpg', 'pdf'],
                        help='Image file format to use.', default='png')


def configure_all(parser: argparse.ArgumentParser, naming_dictionary: NamingDictionary, **defaults) -> None:
    configure_parser_overview(parser, naming_dictionary)
    configure_parser_per_question(parser)


def gen_all(**config):
    gen_overview(**config)
    gen_per_question(**config)


class GenDiagram(CommandModule):
    module_name = 'gen-diagrams'
    commands = [('overview', configure_parser_overview, gen_overview),
                ('per-question', configure_parser_per_question, gen_per_question),
                ('all', configure_all, gen_all)]
    additional_config = {'SCORES_TITLE': 'Scores Overview', 'GRADES_TITLE': 'Grades Overview'}

    def register_command_base(self, parser: argparse.ArgumentParser, **defaults) -> None:
        configure_base_parser(parser)


if __name__ == '__main__':
    GenDiagram().as_program('gen').parse_and_run()

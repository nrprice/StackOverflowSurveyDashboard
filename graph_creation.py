from load_data import survey_data, language_info
from app import comp_group_ordering, get_job_sat_percent
import pandas as pd
import plotly.graph_objs as go

plot_background_color = "rgba(180, 180, 180, 0.0)"
custom_blue = '#0069D9'


def figure_settings_salary_graph(figure):

    figure.update_layout(autosize=True,
                         paper_bgcolor=plot_background_color,
                         plot_bgcolor=plot_background_color,
                         yaxis_range=[0, 250000],
                         xaxis_visible=False,
                         margin=dict(l=0, r=0, t=20, b=0),
                         title='Salaries',
                         title_font_size=25,
                         )
    # y axis Settings
    figure.update_layout(yaxis=dict(tickfont=dict(size=18),
                                    ticklabelposition='inside', ))
    figure.update_layout(xaxis=({'showgrid': False}))
    # Legend Settings
    figure.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.05,
        xanchor="right",
        x=.94,
        font=dict(size=20)))

    return figure


def empty_salary_graph(figure, survey_data):
    print ('Empty Salary Graph Function')
    figure.add_trace(go.Scatter(x=survey_data['Respondent'],
                                y=survey_data['ConvertedComp'],
                                mode='markers',
                                opacity=0.4,
                                name='All Respondents',
                                marker_color='grey',
                                showlegend=True))
    return figure


def all_salaries_graph(figure, survey_data, people_like_you, higher_earners):
    print ('All Salaries Graph Function')
    figure.add_trace(go.Scatter(x=survey_data['Respondent'],
                                y=survey_data['ConvertedComp'],
                                mode='markers',
                                opacity=0.1,
                                name='Everyone Else',
                                marker_color='grey',
                                showlegend=False))

    figure.add_trace(go.Scatter(x=people_like_you['Respondent'],
                                y=people_like_you['ConvertedComp'],
                                mode='markers',
                                marker_color='#0069D9',
                                name='People Like You',
                                marker_size=10))

    figure.add_trace(go.Scatter(x=higher_earners['Respondent'],
                                y=higher_earners['ConvertedComp'],
                                mode='markers',
                                marker_color='green',
                                name='Higher Earners',
                                marker_size=10))

    return figure


def age_comparison_graph(figure, survey_data, age):

    # Category Creation

    survey_data['ConvertedCompGroup'] = pd.Categorical(survey_data['ConvertedCompGroup'],
                                                categories=comp_group_ordering,
                                                ordered=True)

    survey_data = survey_data.sort_values('ConvertedCompGroup', ascending=False)
    # Data Manip

    age_group = survey_data.groupby('ConvertedCompGroup')['Age'].mean().reset_index().sort_values('ConvertedCompGroup')

    age_group['Age'] = round(age_group['Age'])
    age_group_comp_categories = survey_data['ConvertedCompGroup'].unique()
    max_age = age_group['Age'].max()
    print(age_group)
    print (max_age)
    age_group_length = len(age_group_comp_categories)
    # Graph Settings


    figure.update_layout(autosize=True,
                         paper_bgcolor=plot_background_color,
                         plot_bgcolor=plot_background_color,
                         margin=dict(l=0, r=0, t=20, b=0),
                         title='Average Age by Comp Group',
                         title_font_size=25,
                         )

    # y axis Settings
    figure.update_layout(yaxis=dict(tickfont=dict(size=18)))
    figure.update_layout(xaxis=({'showgrid': False}))
    # Legend Settings
    figure.update_layout(legend=dict(
        orientation="v",
        yanchor="bottom",
        y=1.01,
        xanchor="right",
        x=1.09,
        font=dict(size=18)))

    # Chart creation
    figure.add_trace(go.Bar(y=age_group_comp_categories,
                            x=age_group['Age'],
                            orientation='h',
                            marker_color='grey',
                            name='Average Age'))

    figure.add_trace(go.Bar(y=['You'],
                            x=[age],
                            orientation='h',
                            name='You!',
                            marker_color=custom_blue))

    # figure.update_layout(barmode='stack')

    y_tick_text = ['$0 to $24K', '$25K to $49K', '$50K to $74K', '$75K to $99K', '$100K to $124K', '$125K to $149K', '$150K to $174K', '$175K to $199K', '$200K to $224K', '$225K to $250K']
    y_tick_text = y_tick_text[::-1]

    figure.update_yaxes(tickmode='array',
                     tickvals=list(age_group_comp_categories) + ['You'],
                     ticktext=y_tick_text)

    return figure


def language_comparison_graph(figure, survey_data, languages):
    print ('Language Comparison Graph Function')

    language_not_known = [x for x in language_info if x not in languages]
    one_language_more = survey_data[(survey_data['OneLanguageMore'] == 1)]
    one_language_more = one_language_more[['ConvertedComp'] + language_not_known]
    melted = one_language_more.melt(value_vars=language_not_known, id_vars='ConvertedComp',
                                    value_name='count', var_name='language')
    melted = melted[melted['count'] == 1]
    melted_group = melted.groupby('language')['ConvertedComp'].agg(['min', 'max', 'mean', 'count']).sort_values('count', ascending=False)


    melted_group_top = melted_group.iloc[[0]]
    melted_group = melted_group[1:5].sort_values('count', ascending=True)

    figure.add_trace(go.Bar(y=melted_group.index,
                            x=melted_group['count'],
                            orientation='h',
                            marker_color='grey',
                            showlegend=False))

    figure.add_trace(go.Bar(y=melted_group_top.index,
                            x=melted_group_top['count'],
                            orientation='h',
                            marker_color=custom_blue,
                            showlegend=False))

    figure.update_layout(autosize=True,
                         paper_bgcolor=plot_background_color,
                         plot_bgcolor=plot_background_color,
                         margin=dict(l=0, r=0, t=70, b=0),
                         title='What other language do people like you know?',
                         title_font_size=22,
                         )

    # y axis Settings
    figure.update_layout(yaxis=dict(tickfont=dict(size=18),
                                    ticklabelposition='outside left'))
    figure.update_layout(xaxis=(dict(showgrid=False, title='Count', title_font=dict(size=20))))

    return figure


def jobsat_comparison_graph(figure, data, people_like_you, higher_earners):
    print('JobSat Comparison Graph Function')
    job_sat_perc_people_like_you = get_job_sat_percent(people_like_you) / 100
    job_sat_perc_higher_earners = get_job_sat_percent(higher_earners) / 100

    print(job_sat_perc_people_like_you, job_sat_perc_higher_earners)

    figure.add_trace(go.Bar(x=['People Like You'],
                            y=[job_sat_perc_people_like_you],
                            showlegend=False))

    figure.add_trace(go.Bar(x=['Higher Earners'],
                            y=[job_sat_perc_higher_earners],
                            showlegend=False))

    figure.update_layout(autosize=True,
                         paper_bgcolor=plot_background_color,
                         plot_bgcolor=plot_background_color,
                         margin=dict(l=0, r=0, t=70, b=0),
                         title='What Percentage of People Are Satisfied<br>in their current role?',
                         title_font_size=25,
                         )

    # y axis Settings
    figure.update_layout(yaxis=dict(tickfont=dict(size=18), tickformat='0%'))
    # y axis Settings
    figure.update_layout(xaxis=dict(tickfont=dict(size=18)))

    return figure






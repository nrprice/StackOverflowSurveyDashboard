from app import get_job_sat_percent, language_info
import pandas as pd
import plotly.graph_objs as go

plot_background_color = "rgba(180, 180, 180, 0.0)"

custom_grey = "rgba(180, 180, 180, 0.6)"
custom_blue = '#0069D9'

comp_group_ordering = ['$0 to $24999',
                       '$25000 to $49999',
                       '$50000 to $74999',
                       '$75000 to $99999',
                       '$100000 to $124999',
                       '$125000 to $149999',
                       '$150000 to $174999',
                       '$175000 to $199999',
                       '$200000 to $224999',
                       '$225000 to $249999']

def figure_settings_salary_graph(figure):

    """
    :param figure: A blank figure created in the select_graph function in app.py
    :return: A figure with the correct settings for the salary graph.
    """

    figure.update_layout(autosize=True,
                         paper_bgcolor=plot_background_color,
                         plot_bgcolor=plot_background_color,
                         yaxis_range=[0, 350000],
                         xaxis_visible=False,
                         margin=dict(l=30, r=30, t=90, b=0),
                         title='<b>Salaries</b>',
                         title_font_size=25,
                         )
    # Y Axis Settings
    figure.update_layout(yaxis=dict(tickfont=dict(size=18),
                                    ticklabelposition='inside'))
    # X Axis Settings
    figure.update_layout(xaxis=({'showgrid': False}))
    # Legend Settings
    figure.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.09,
        xanchor="right",
        x=.98,
        font=dict(size=20)))

    return figure


def empty_salary_graph(figure, survey_data):

    """
    :param figure: Whichever figure is currently active when this function is called.
    :param survey_data: The original data from the database. Unaltered.
    :return: A figure containing a graph of just the
             ConvertComp values for all respondents in the original data
    """
    # print ('Empty Salary Graph Function')
    figure.add_trace(go.Scatter(x=survey_data['Respondent'],
                                y=survey_data['ConvertedComp'],
                                mode='markers',
                                opacity=0.4,
                                name='All Respondents',
                                marker_color=custom_grey,
                                showlegend=True))
    return figure


def all_salaries_graph(figure, survey_data, people_like_you, higher_earners):

    """
    :param figure: Whichever figure is currently active when this function is called.
    :param survey_data: The original data from the database. Unaltered.
    :param people_like_you: A data frame created in the create_data function from app.py
                            Contains information about respondents who share identical languages
                            and ConvertedCompGroup to the user input.
    :param higher_earners: A data frame created in the create_data function from app.py
                            Contains information about respondents who share identical languages,
                            but have a higher ConvertedCompGroup to the user input.
    :return: A figure containing a graph of ConvertedComp values split into two groups:
             people_like_you & higher_earners
    """
    # print ('All Salaries Graph Function')

    # Graph Creation
    figure.add_trace(go.Scatter(x=survey_data['Respondent'],
                                y=survey_data['ConvertedComp'],
                                mode='markers',
                                opacity=0.1,
                                name='Everyone Else',
                                marker_color=custom_grey,
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

    """
    :param figure: Whichever figure is currently active when this function is called.
    :param survey_data: The original data from the database. Unaltered.
    :param age: Integer value of the inputted user age
    :return: A figure containing a graph of average ages of each ConvertedCompGroup
            as well as a bar for the users inputted age.
    """

    # Category Creation
    survey_data['ConvertedCompGroup'] = pd.Categorical(survey_data['ConvertedCompGroup'],
                                                categories=comp_group_ordering,
                                                ordered=True)

    survey_data = survey_data.sort_values('ConvertedCompGroup', ascending=False)

    # Data Manipulation
    age_group = survey_data.groupby('ConvertedCompGroup')['Age'].mean().reset_index()
    age_group = age_group.sort_values('ConvertedCompGroup')

    age_group['Age'] = round(age_group['Age'])
    age_group_comp_categories = survey_data['ConvertedCompGroup'].unique()
    max_age = age_group['Age'].max()

    # Graph Creation
    figure.add_trace(go.Bar(y=age_group_comp_categories,
                            x=age_group['Age'],
                            orientation='h',
                            marker_color=custom_grey,
                            name='Average Age'))

    figure.add_trace(go.Bar(y=['You'],
                            x=[age],
                            orientation='h',
                            name='You',
                            marker_color=custom_blue))

    # Graph Settings
    figure.update_layout(autosize=True,
                         paper_bgcolor=plot_background_color,
                         plot_bgcolor=plot_background_color,
                         margin=dict(l=0, r=0, t=20, b=0),
                         title='<b>Average Age by Comp Group</b>',
                         title_font_size=20,
                         )

    # Y Axis Settings
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

    # Custom Y Ticks
    y_tick_text = ['$0 to $24K', '$25K to $49K', '$50K to $74K', '$75K to $99K', '$100K to $124K', '$125K to $149K', '$150K to $174K', '$175K to $199K', '$200K to $224K', '$225K to $250K']
    y_tick_text = y_tick_text[::-1]

    figure.update_yaxes(tickmode='array',
                     tickvals=list(age_group_comp_categories) + ['You'],
                     ticktext=y_tick_text)

    return figure


def language_comparison_graph(figure, survey_data, languages):
    """
    :param figure: Whichever figure is currently active when this function is called.
    :param survey_data: The original data from the database. Unaltered.
    :param languages: Value of the languages checkboxes
    :return: A figure containing a graph of the most common 5th languages
             respondents with identical languages knew
    """

    # print ('Language Comparison Graph Function')

    # Repeated code from give_advice function in app.py
    # Possibly worth converting to a function because it's used twice indentically

    # List of languages not known by the user
    language_not_known = [x for x in language_info if x not in languages]

    # OneLanguageMore is a column created during create_data in app.py
    # Is a tag for respondents who know 1 language more than the user specified.
    one_language_more = survey_data[(survey_data['OneLanguageMore'] == 1)]
    one_language_more = one_language_more[['ConvertedComp'] + language_not_known]

    # Melt data to have the languages user does not know as a the variable grouping
    melted = one_language_more.melt(value_vars=language_not_known, id_vars='ConvertedComp',
                                    value_name='count', var_name='language')

    # Returns the language the respondent knows and their salary
    melted = melted[melted['count'] == 1]

    # Groups the languages to get summary statistics
    melted_group = melted.groupby('language')['ConvertedComp'].agg(['min', 'max', 'mean', 'count'])
    melted_group = melted_group.sort_values('count', ascending=False)

    # Used to color the top language differently to the others
    # Top performing language as chosen by popularity
    melted_group_top = melted_group.iloc[[0]]
    # Next four
    melted_group = melted_group[1:5].sort_values('count', ascending=True)

    # Graph Creation
    figure.add_trace(go.Bar(y=melted_group.index,
                            x=melted_group['count'],
                            orientation='h',
                            marker_color=custom_grey,
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
                         title='<b>What other language do people like you know?</b>',
                         title_font_size=20,
                         )

    # Y Axis Settings
    figure.update_layout(yaxis=dict(tickfont=dict(size=18),
                                    ticklabelposition='outside left'))
    # X Axis Settings
    figure.update_layout(xaxis=(dict(showgrid=False, title='Count', title_font=dict(size=20))))

    return figure


def jobsat_comparison_graph(figure, people_like_you, higher_earners):
    """
    :param figure: Whichever figure is currently active when this function is called.
    :param people_like_you: A data frame created in the create_data function from app.py
                            Contains information about respondents who share identical languages
                            and ConvertedCompGroup to the user input.
    :param higher_earners: A data frame created in the create_data function from app.py
                            Contains information about respondents who share identical languages,
                            but have a higher ConvertedCompGroup to the user input.
    :return: A figure containing a graph of percentage comparisons of Job Satisfacation rates
            in two groups, people_like_you and higher_earners
    """

    # print('JobSat Comparison Graph Function')
    # Function from app.py. Takes a dataf rame and returns percentage value.
    job_sat_perc_people_like_you = get_job_sat_percent(people_like_you)
    job_sat_perc_higher_earners = get_job_sat_percent(higher_earners)

    # Check to know which value was higher, colors appropriately
    if job_sat_perc_people_like_you > job_sat_perc_higher_earners:
        people_like_you_color = custom_blue
        higher_earners_color = custom_grey
        max = job_sat_perc_people_like_you
    else:
        people_like_you_color = custom_grey
        higher_earners_color = custom_blue
        max = job_sat_perc_higher_earners

    # Graph Creation
    figure.add_trace(go.Bar(x=['People Like You'],
                            y=[job_sat_perc_people_like_you],
                            marker_color=people_like_you_color,
                            showlegend=False,
                            text=f'{job_sat_perc_people_like_you}%',
                            textfont=dict(size=20),
                            textposition='inside'))

    figure.add_trace(go.Bar(x=['Higher Earners'],
                            y=[job_sat_perc_higher_earners],
                            marker_color=higher_earners_color,
                            showlegend=False,
                            text=[f'{job_sat_perc_higher_earners}%'],
                            textfont=dict(size=20),
                            textposition='inside'))

    # Graph Settings
    figure.update_layout(autosize=True,
                         yaxis_visible=False,
                         paper_bgcolor=plot_background_color,
                         plot_bgcolor=plot_background_color,
                         margin=dict(l=30, r=30, t=70, b=0),
                         title='<b>Percentage Satisfied<br>in Their Current Role?</b>',
                         title_font_size=20,
                         )

    # Y Axis Settings
    figure.update_layout(yaxis=dict(tickfont=dict(size=18), ticksuffix='%'))
    # X Axis Settings
    figure.update_layout(xaxis=(dict(showgrid=False, tickfont=dict(size=20))))

    return figure






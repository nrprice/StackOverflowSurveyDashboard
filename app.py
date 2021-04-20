# Library Imports
from load_data import survey_data, language_info
from time import sleep
from graph_creation import *
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
pd.set_option("display.max_columns", 50)
pd.set_option("display.max_rows", 400000)
pd.set_option("display.width", 1000)

# Create app instance & server
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

def figure_to_dcc_object(figure):
    figure.update_layout(hovermode=False)
    return dcc.Graph(figure=figure,
                     config={'displayModeBar': False, 'responsive': True},
                     style={'height': '100%'})

# ----Old methods for reading in data prior to MongoDB implementation----
# data_path = '/Users/nathanprice/Dropbox/Python/Coursera/IBM Data Analyst/Capstone/Assets/'
# survey_data = pd.read_csv(f'{data_path}survey_data_modified.csv')
# survey_data.drop(columns='Unnamed: 0', inplace=True)
# language_list = open(f"{data_path}language_info_unique.txt", "r").read()
# language_list = sorted(language_list.split(','))


# Create Lists for Dropdown
language_list = language_info
comp_group_list = (list(survey_data['ConvertedCompGroup'].unique()))
age_group_list = sorted(list(survey_data['AgeGroup'].unique()))

ed_level_dict = {'I never completed any formal education': 0,
                     'Primary/elementary school': 1,
                     'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)': 2,
                     'Some college/university study without earning a degree': 3,
                    'Bachelor’s degree (BA, BS, B.Eng., etc.)': 4,
                     'Associate degree': 4,
                    'Master’s degree (MA, MS, M.Eng., MBA, etc.)': 5,
                    'Other doctoral degree (Ph.D, Ed.D., etc.)': 6,
                    'Professional degree (JD, MD, etc.)': 6,
                    np.nan: 0}



# Create list for for ordering ConvertedCompGroup Categories
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
survey_data['ConvertedCompGroup'] = pd.Categorical(survey_data['ConvertedCompGroup'],
                                                   categories=comp_group_ordering,
                                                   ordered=True)

# Styling Dicts
main_style = {'display': 'flex',
              'justify-content': 'center',
              'align-items': 'center',
              'height': '100%', 'width': '100%',
              'background-color': 'red'}

background_color = "rgba(180, 180, 180, 0.2)"

button_style = {'margin-left': '20px', 'margin-right': '20px', 'margin-bottom': '20px'}

# Layout
# all_salaries_graph = dbc.Spinner(children=dcc.Graph(id='all_salaries_graph',
#                                        config={'displayModeBar': False, 'responsive': True},
#                                        style={'height': '100%'}),
#                     size='lg', color="blue", type="border")

comp_dropdown = dcc.Dropdown(id='comp',
                             options=[{'label': x, 'value': x} for x in comp_group_ordering],
                             placeholder='Salary Range',
                             style={'width': '75%', 'textAlign': 'left'},
                             value=None)

age_input = dcc.Input(id='age',
                      placeholder='Age',
                      type='number',
                      maxLength='2',
                      inputMode='numeric',
                      style={'width': '25%', 'textAlign': 'left'},
                      value=None)

education_input = dcc.Dropdown(id='edlevel',
                               options=[{'label': k, 'value': v} for k, v in ed_level_dict.items()],
                               placeholder='Education',
                               style={'width': '100%', 'textAlign': 'left'},
                               value=None)

languages_checkbox = dcc.Dropdown(id='languages',
                                  options=[{'label': x, 'value': x} for x in language_list],
                                  placeholder='Languages',
                                  style={'width': '75%', 'textAlign': 'left'},
                                  multi=True,
                                  value=None)

# languages_checkbox = dcc.Checklist(id='languages',
#                                    options=[{'label': x, 'value': x} for x in language_list],
#                                    inputStyle={"margin-right": "5px", 'margin-left': '12px'},
#                                    value=['Python'],
#                                    style={'fontSize': '18px'},
#                                    labelClassName='Butt',
#                                    )

advice_list = html.Div(id='advice_text', style={'line-height': '180%'})

hidden_json = html.Div(id='hidden_json', style={'display': 'none'})

title = html.H1('Salary Comparison', style={'textAlign': 'center'})

col_1_layout = html.P('''
                This dashboard allows users to compare their current skill set to other programmers across the world.
                It also outputs information unique to the user giving them a breakdown of the differences between
                them, and the other respondents.
                '''),\
               html.P('''
                The data is a survey conducted by Stack Overflow asking over 11,000 users questions
                about their careers, education, current expertise, desired future expertise etc.
                '''),\
               html.P("""
                The data is hosted on a MongoDB server and is retrieved on page load.
                We then perform a 'doppleganger' search on the users information. Returning a graph showing
                'people like you' which are respondents who have similar characteristics to the user.
                """),\
               html.P('''
                Click below to see the slide deck, the github repository for this project, and the Jupyter Notebook
                where the initial data analysis was done.
                ''')

col_2_div_style = {'margin-top': '15px'}
col_2_layout = [html.Div([html.H5('Please input age:'), age_input]),
                html.Div([html.H5('Please select education level:', style=col_2_div_style), education_input]),
                html.Div([html.H5('Please select languages known', style=col_2_div_style), languages_checkbox]),
                html.Div([html.H5('Please select salary range:', style=col_2_div_style), comp_dropdown]),
                html.Div(html.Br())
                ]

app.layout = dbc.Container([
                            dbc.Row([
                                    dbc.Col([
                                        dbc.Card([
                                            dbc.CardBody(title)])

                                    ], width={"size": 4, "offset": 4})
                                    ], className='m-4'),
                            dbc.Row([
                                    dbc.Col([
                                        dbc.Card([
                                            dbc.CardBody(col_1_layout, style={"display": "flex",
                                                                              'flex-direction': 'column',
                                                                              'justify-content': 'space-between',
                                                                              'height': '100%'}),
                                            html.Div([dbc.Button("Github",
                                                                 href='https://github.com/nrprice/StackOverflowSurveyDashboard',
                                                                 color='primary', style=button_style),
                                                     dbc.Button("PowerPoint Slides",
                                                                href='https://github.com/nrprice/StackOverflowSurveyDashboard/blob/main/Capstone%20Presentation.pdf',
                                                                color='primary',
                                                                style=button_style),
                                                     dbc.Button("Jupyter Notebook",
                                                                href='https://github.com/nrprice/StackOverflowSurveyDashboard/blob/main/Final%20Presentation.ipynb',
                                                                color='primary',
                                                                style=button_style)],
                                                     style={"display": "flex",
                                                            'justify-content': 'center',
                                                            'margin-left': '15px',
                                                            'margin-right': '15px'})],
                                            style={'height': '100%'})
                                    ], width={"size": 7, "offset": 1}),
                                    dbc.Col([
                                        dbc.Card([
                                            dbc.CardBody(col_2_layout)], style={"display": "flex",
                                                                                'flex-direction': 'column',
                                                                                'justify-content': 'space-between',
                                                                                'height': '100%'})
                                    ], width={"size": 3, "offset": 0}, style={})
                                    ], className='m-4'),
                            dbc.Row([
                                    dbc.Col([
                                        dbc.Card([
                                            dbc.CardHeader([
                                                dcc.Tabs(id='tab', value='all_salaries_graph',
                                                         children=[dcc.Tab(label='Compensation Comparison',
                                                                           value='all_salaries_graph'),
                                                                   dcc.Tab(label='Average Age',
                                                                           value='age_comparison_graph'),
                                                                   dcc.Tab(label='Languages Known',
                                                                           value='language_comparison_graph'),
                                                                   dcc.Tab(label='Job Satisfaction Rates',
                                                                           value='jobsat_comparison_graph')]),
                                                dbc.CardBody([dbc.Spinner(html.Div(id='tab_content'),
                                                                          size='lg',
                                                                          color="blue",
                                                                          type="border")
                                                              ])
                                            ]
                                            )], style={"display": "flex",
                                                       'flex-direction': 'column',
                                                       'justify-content': 'center',
                                                       'height': '100%'})
                                    ], width={"size": 4, "offset": 1}, style={}),
                                    dbc.Col([
                                        dbc.Card([
                                            dbc.CardBody(dbc.Spinner(advice_list,
                                                                     size='lg',
                                                                     color="blue",
                                                                     type="border"), style={"display": "flex",
                                                                                          'flex-direction': 'column',
                                                                                          'justify-content': 'center',
                                                                                          'align-items': 'center',
                                                                                          'height': '100%'})
                                        ], style={"display": "flex",
                                                  'flex-direction': 'column',
                                                  'justify-content': 'center',
                                                  'align-items': 'center',
                                                  'height': '100%'})
                                    ], width={"size": 6})
                                    ], className='m-4'),
                            dbc.Row(hidden_json, style={'display': 'none'})



], fluid=True, style={'height': '100vh', 'width': '100vw'})


@app.callback(
    # Outputs
    Output(component_id='hidden_json', component_property='children'),

    # Inputs

    Input(component_id='age', component_property='value'),
    Input(component_id='edlevel', component_property='value'),
    Input(component_id='languages', component_property='value'),
    Input(component_id='comp', component_property='value'),

)
def create_data(age, edlevelval, languages, comp):
    none_check_list = [age, edlevelval, languages, comp]
    """
    
    :param age: value of the inputted user age
    :param edlevelval:  Integer valued returned from the edlevel val dropdown.
                        Strings are the keys, with a matching integer value
    :param languages: Value of the languages checkboxes
    :param comp: Value of the Salary Dropdown
    :return: Json file to be hidden on the page in a div
             and then reread by future functions
    """
    # Check if user has entered choices
    if None in none_check_list:
        json_data = survey_data.to_json(orient='split')
        return json_data

    # Returns a DF of every language someone knows
    language_match = survey_data[survey_data[language_list] == 1]

    # Sums each row to get a total count of languages known
    language_match['total_all'] = language_match.sum(axis=1)

    # Returns a DF of only the languages specified + the total that respondent knows
    language_match = language_match[languages + ['total_all']]

    # Sums the total known languages of the languages specified
    language_match['total_to_check'] = language_match[languages].sum(axis=1)

    # If the sum of all languages known matches the sum of specified
    # matches known we can say this individual only knows the languages specified
    same_languages_known = language_match[(language_match['total_all'] == len(languages)) &
                                          (language_match['total_to_check'] == len(languages))]

    # People who know one language more will have the same total_to_check
    # as they were positive for the specified languages
    # but their overall total will be one greater
    one_language_more = language_match[(language_match['total_all'] == len(languages) + 1) &
                                       (language_match['total_to_check'] == len(languages))]

    # Data contains respondents who match the languages the user specified.
    data = survey_data[survey_data.index.isin(same_languages_known.index)].copy()

    # Tags those in original data who know 1 language more than the user
    survey_data['OneLanguageMore'] = 0
    for row in one_language_more.index:
        survey_data.at[row, 'OneLanguageMore'] = 1

    # Nested np.where to create status tag
    data['status'] = np.where(data['ConvertedCompGroup'] > comp, 'Higher Earner',
                              np.where(data['ConvertedCompGroup'] < comp, 'Lower Earner',
                              np.where(data['ConvertedCompGroup'] == comp, 'People Like You', 0)))

    # Outputs data as a json to a hidden div on the page, to be read by later functions
    json_data = data.to_json(orient='split')
    return json_data


# @app.callback(
#     Output(component_id='all_salaries_graph', component_property='figure'),
#     Input(component_id='hidden_json', component_property='children'),
#     Input(component_id='comp', component_property='value')
# )
# def interactive_graph(hidden_json_data, comp):
#     """
#
#     :param hidden_json_data: The return value of the create_data function.
#     :param comp: Value of the Salary Dropdown
#     :return: A plotly figure to be displayed with id='graph
#     """
#
#     figure = go.Figure()
#     figure.update_layout(autosize=True,
#                          paper_bgcolor=plot_background_color,
#                          plot_bgcolor=plot_background_color,
#                          yaxis_range=[0, 250000],
#                          xaxis_visible=False,
#                          margin=dict(l=0, r=0, t=0, b=0),
#                          title='Salaries',
#                          title_font_size=25,
#                          )
#     # y axis Settings
#     figure.update_layout(yaxis=dict(tickfont=dict(size=18),
#                                     ticklabelposition='inside',))
#     figure.update_layout(xaxis=({'showgrid': False}))
#     # Legend Settings
#     figure.update_layout(legend=dict(
#         orientation="h",
#         yanchor="bottom",
#         y=1.05,
#         xanchor="right",
#         x=.94,
#         font=dict(size=20)))
#
#     if comp is None:
#         figure.add_trace(go.Scatter(x=survey_data['Respondent'],
#                                     y=survey_data['ConvertedComp'],
#                                     mode='markers',
#                                     opacity=0.4,
#                                     name='All Respondents',
#                                     marker_color='grey',
#                                     showlegend=True))
#         return figure
#
#     data = pd.read_json(hidden_json_data, orient='split')
#
#     data['ConvertedCompGroup'] = pd.Categorical(data['ConvertedCompGroup'],
#                                                 categories=comp_group_ordering,
#                                                 ordered=True)
#
#     higher_earners = data[data['status'] == 'Higher Earner']
#     people_like_you = data[data['status'] == 'People Like You']
#
#     figure.add_trace(go.Scatter(x=survey_data['Respondent'],
#                                 y=survey_data['ConvertedComp'],
#                                 mode='markers',
#                                 opacity=0.1,
#                                 name='Everyone Else',
#                                 marker_color='grey',
#                                 showlegend=False))
#
#     figure.add_trace(go.Scatter(x=people_like_you['Respondent'],
#                                 y=people_like_you['ConvertedComp'],
#                                 mode='markers',
#                                 marker_color='#0069D9',
#                                 name='People Like You',
#                                 marker_size=10))
#
#     figure.add_trace(go.Scatter(x=higher_earners['Respondent'],
#                                 y=higher_earners['ConvertedComp'],
#                                 mode='markers',
#                                 marker_color='green',
#                                 name='Higher Earners',
#                                 marker_size=10))
#
#     return figure


@app.callback(
    Output(component_id='advice_text', component_property='children'),
    Input(component_id='hidden_json', component_property='children'),
    Input(component_id='languages', component_property='value'),
    Input(component_id='age', component_property='value'),
    Input(component_id='comp', component_property='value'),
    Input(component_id='edlevel', component_property='value')
)
def give_advice(hidden_json_data, languages, age, comp, edlevelval):

    # Adding this so the advice just doesn't POP in aggressively.
    # At least make it look like it's doing something right?
    sleep(0.5)
    none_check_list = [age, edlevelval, languages, comp]

    """

    :param hidden_json_data: The return value of the create_data function.
    :param languages:  Value of the languages checkboxes
    :param age: value of the inputted user age
    :param comp: Value of the Salary Dropdown
    :return: A list containing strings and HTML formatting
             to be put into the div with id='advice_text
    """
    data = pd.read_json(hidden_json_data, orient='split')

    while None in none_check_list:
        return html.H3('Please enter age & salary to see individual advice', style={'textAlign': 'center'})

    # Creates dataframes  based on user information
    higher_earners = data[data['status'] == 'Higher Earner']
    people_like_you = data[data['status'] == 'People Like You']
    # lower_earners = data[data['status'] == 'Lower Earner']

    if len(people_like_you) == 0:
        return "Whoops! Look like we can't find anyone like you!"

    if len(people_like_you) == 1:
        return "Looks like you're one of a kind! We couldn't find anyone else like you."

    # Create string for age comparison
    average_age_val = round(higher_earners['Age'].mean() - age)
    most_common_age_val = higher_earners['AgeGroup'].value_counts().index[:1].values[0]

    average_age_string = ''

    if average_age_val > 0:
        average_age_string = f"{average_age_val} years older than you"
    if average_age_val < 0:
        average_age_string = f"{abs(average_age_val)} years younger than you"
    if average_age_val == 0:
        average_age_string = f"the same age as you"

    age_string = f'Respondents with a higher salary were, on average, {average_age_string} than you.' \
                 f' With most being {most_common_age_val} years old.'

    # Create string for country information
    most_common_country = higher_earners['Country'].value_counts()
    most_common_country_name = most_common_country.index[0]
    most_common_country_val = most_common_country.values[0]

    country_suffix = ''
    if most_common_country_val < 5:
        country_suffix = 'Best stay put! Only '
    if most_common_country_val > 5:
        country_suffix = "Looks like it's time to pack your bags! "
    people_or_person = 'people'
    if most_common_country_val == 1:
        people_or_person = 'person'
    country_string = f"{country_suffix}{most_common_country_val} {people_or_person} in {most_common_country_name} " \
                     f"have a higher salary than you."

    # Create string for language advice
    language_not_known = [x for x in language_list if x not in languages]
    one_language_more = survey_data[(survey_data['OneLanguageMore'] == 1)]
    one_language_more = one_language_more[['ConvertedComp'] + language_not_known]
    melted = one_language_more.melt(value_vars=language_not_known, id_vars='ConvertedComp',
                                    value_name='count', var_name='language')
    melted = melted[melted['count'] == 1]
    melted_group = melted.groupby('language')['ConvertedComp'].agg(['min', 'max', 'mean', 'count']).sort_values('count', ascending=False)

    highest_value_language_name = melted_group.iloc[[0]].index[0]
    highest_value_language_min = add_comma(melted_group['min'].values[0])
    highest_value_language_max = add_comma(melted_group['max'].values[0])
    highest_value_language_mean = add_comma(melted_group['mean'].values[0])

    language_string = f"The most popular language people like you learn is {highest_value_language_name}. " \
                      f"You could increase your salary by " \
                      f"{highest_value_language_min} to {highest_value_language_max}. " \
                      f"On average it raises salaries by {highest_value_language_mean}"

    # Create Job Satisfaction String
    percent_satisfied_high_earners = get_job_sat_percent(higher_earners)
    percent_satisfied_people_like_you = get_job_sat_percent(people_like_you)

    string_suffix = ''
    if percent_satisfied_high_earners > percent_satisfied_people_like_you:
        string_suffix = f"It might be time for a job move!"
    if percent_satisfied_high_earners < percent_satisfied_people_like_you:
        string_suffix = f"The grass isn't always greener! Only "
    if percent_satisfied_high_earners == percent_satisfied_people_like_you:
        string_suffix = 'Not gonna get better, but not gonna get worse either!'

    job_sat_string = f"{string_suffix} {percent_satisfied_high_earners}% of higher earners report being satisifed" \
                     f" in their job compared to {percent_satisfied_people_like_you}% of people similar to you"

    # Education Level
    edu_high_earners = higher_earners[higher_earners['EdLevelVal'] >= edlevelval].groupby(['EdLevel', 'EdLevelVal'])['Respondent'].count().reset_index().sort_values('Respondent', ascending=False)
    most_common_edu_level = edu_high_earners.iloc[[0]]['EdLevel'].values[0]
    most_common_edu_level = most_common_edu_level.split('(')[0]

    percent_higher_edlevelval = edu_high_earners[edu_high_earners['EdLevelVal'] > edlevelval]['Respondent'].sum() / edu_high_earners['Respondent'].sum()
    percent_higher_edlevelval = round(percent_higher_edlevelval, 2) * 100

    ed_level_string = ''
    if percent_higher_edlevelval > 0:
        ed_level_string_suffix = f"Schools in session!"
        ed_level_string = f"{ed_level_string_suffix} {percent_higher_edlevelval}% have a higher level of education than you." \
                          f" With the most common being a {most_common_edu_level}"
    if percent_higher_edlevelval == 0:
        ed_level_string = "School is not the problem! Those earning more than you have the same level of education."

    # Merge and return the various strings
    return_string_list = [country_string, age_string, language_string, job_sat_string, ed_level_string]
    return_options_list = ['Location', 'Age', 'Languges', 'Job Satisfaction', 'Education Level']
    return_string = [html.Div([html.H5(title_options), html.P(advice)]) for
                     advice, title_options in zip(return_string_list, return_options_list)]
    return_string.insert(0, html.H1('Advice'))
    return_string.insert(1, html.Br())

    return return_string


@app.callback(
    Output(component_id='tab_content', component_property='children'),
    Input(component_id='hidden_json', component_property='children'),
    Input(component_id='tab', component_property='value'),
    Input(component_id='age', component_property='value'),
    Input(component_id='edlevel', component_property='value'),
    Input(component_id='languages', component_property='value'),
    Input(component_id='comp', component_property='value'),
            )
def select_graph(hidden_json_data, tab, age, edlevelval, languages, comp):
    """
    :param hidden_json_data: The return value of the create_data function.
    :param tab: The currently active dbc.tab in the layout.
    :param age: Integer value of the inputted user age
    :param edlevelval:  integer valued returned from the edlevel val dropdown.
                        Strings are the keys, with a matching integer value
    :param languages: List of values of the user input in the languages checkboxes
    :param comp: String value of user choice from Salary Dropdown
    :return: A figure to be inserted into the currently active tab.
    """

    # Check if user has made an input or not
    none_check_list = [age, edlevelval, languages, comp]

    # Creates figure to be passed to the functions from create_graph.py
    figure = go.Figure()

    # ----All Graph Creation is handled by graph_creation.py----
    # The output of those functions are then passed back within each if statement

    # Insert Graph if user makes no choices
    if tab == 'all_salaries_graph' and comp is None:
        figure = figure_settings_salary_graph(figure)
        figure = empty_salary_graph(figure, survey_data)

        return figure_to_dcc_object(figure)

    # Graphs & Data for when user has selected options:

    if None not in none_check_list:

        # Data contains the slice of only respondents similar to the user.
        data = pd.read_json(hidden_json_data, orient='split')

        # Following slices are self explanatory
        higher_earners = data[data['status'] == 'Higher Earner']
        people_like_you = data[data['status'] == 'People Like You']

        # Required to be able to order by categories.
        data['ConvertedCompGroup'] = pd.Categorical(data['ConvertedCompGroup'],
                                                    categories=comp_group_ordering,
                                                    ordered=True)

        if len(data) == 0:
            return html.H3("You're too unique! We can't find anyone like you.")

    # String to be returned while elements of none_check_list remain == None
    error_string = html.H3('Please enter user information for more detail.')

    # Checks current active tab and if user has made all choices
    # If both are true passes the data and figure created above to the functions from create_graphs.py
    # If user has not made all choices, returns error_string

    # All Salaries Graph Creation
    if tab == 'all_salaries_graph':
        if None not in none_check_list:
            figure = figure_settings_salary_graph(figure)
            figure = all_salaries_graph(figure, survey_data, people_like_you, higher_earners)
            return figure_to_dcc_object(figure)
        else:
            return error_string

    # Age Comparison Graph Creation
    if tab == 'age_comparison_graph':
        if None not in none_check_list:
            figure = age_comparison_graph(figure, survey_data, age)
            return figure_to_dcc_object(figure)
        else:
            return error_string

    # Language Comparison Graph Creation
    if tab == 'language_comparison_graph':
        if None not in none_check_list:
            language_comparison_graph(figure, survey_data, languages)
            return figure_to_dcc_object(figure)
        else:
            return error_string

    # Job Satisfaction Comparison Graph Creation
    if tab == 'jobsat_comparison_graph':
        if None not in none_check_list:
            figure = jobsat_comparison_graph(figure, people_like_you, higher_earners)
            return figure_to_dcc_object(figure)
        else:
            return error_string

if __name__ == '__main__':
    app.run_server()
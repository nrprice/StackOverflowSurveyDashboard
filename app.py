# Library Imports
from mongodb import survey_data, language_info
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


def add_comma(number):

    """
    Takes a integer or float
    Returns a string with the apppropriate comma position
    """

    number = round(number)
    number = str(number)
    comma_position_dict = {4: 1, 5: 2, 6: 3}
    comma_position = comma_position_dict[len(number)]
    return f"${number[:comma_position]},{number[comma_position:]}"


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

# Create app instance & server
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

main_style = {'display': 'flex',
              'justify-content': 'center',
              'align-items': 'center',
              'height': '100%', 'width': '100%',
              'background-color': 'red'}
# Layout
graph = dbc.Spinner(children=dcc.Graph(id='graph', config={'displayModeBar': False}), size='lg', color="blue", type="border")

comp_dropdown = dcc.Dropdown(id='comp',
                             options=[{'label': x, 'value': x} for x in comp_group_ordering],
                             placeholder='Salary Range',
                             style={'width': '50%', 'textAlign': 'left'})

age_input = dcc.Input(id='age',
                      placeholder='Age',
                      type='number',
                      maxLength='2',
                      inputMode='numeric',
                      style={'width': '10%', 'textAlign': 'left'})

languages_checkbox = dcc.Checklist(id='languages',
                                   options=[{'label': x, 'value': x} for x in language_list],
                                   inputStyle={"margin-right": "5px", 'margin-left': '12px'},
                                   value=['Python'],
                                   style={'fontSize': '18px'},
                                   labelClassName='Butt')

advice_list = html.Div(id='advice_text', style={'line-height': '180%'})

hidden_json = html.Div(id='hidden_json', style={'display': 'none'})

col_1_layout = [html.Div([html.Br(), html.Br(), html.H1('Salary Comparison & Career Advice')]),
                html.Div(html.P('''
                Initially this project was a simple analysis for the final module of the 
                IBM Data Analyst Professional certificate. 
                Once I was finished I wanted to explore what else was possible with this data-set.
                                I prefer to make projects that serve a purpose, or answer a specific question.
                ''')),
                html.Div(html.P('''
                The data is a survey conducted by Stack Overflow asking over 11,000 users questions 
                about their careers, education, current expertise, desired future expertise etc. 
                With this dashboard users are able to see where they lie in relation to other programmers 
                by specifying their salary range, age and current skill set.
                ''')),
                html.Div(html.P("""
                Behind the scenes we're doing a doppleganger search. 
                Looking for respondents similar to the user. 
                By default the graph shows all respondents salary information, 
                when the user enters their information they are able to see their 'dopplegangers' 
                who have a similar skill set and salary range. As well as respondents who reported a higher salary.
                """)),
                html.Div(html.P('''
                In the advice section users can see unique advice detailing the difference 
                between them, and respondents with a higher salary.
                '''))]

col_2_layout = [html.Div([html.Br(), html.Br(), html.H1('User Information')]),
                html.Div([html.H4('Please select salary range:'), comp_dropdown]),
                html.Div([html.H4('Please input age:'), age_input]),
                html.Div([html.H4('Please select languages known'), languages_checkbox]),
                html.Div(html.Br())
                ]

background_color = "rgba(180, 180, 180, 0.2)"

plot_background_color = "rgba(180, 180, 180, 0.0)"


app.layout = dbc.Container([
                    dbc.Row([
                            dbc.Col(col_1_layout,
                                    width=6,
                                    style={'display': 'flex',
                                           'flex-direction': 'column',
                                           "background-color": background_color,
                                           'justify-content': 'space-around',
                                           'height': '100%',
                                           'margin-top': '0px',
                                           'margin-bottom': '0px',
                                           'font-size': '2.5ch'}),
                            dbc.Col(col_2_layout,
                                    width=6,
                                    style={'display': 'flex',
                                           'flex-direction': 'column',
                                           "background-color": background_color,
                                           'justify-content': 'space-around',
                                           'height': '100%',
                                           'margin-top': '0px',
                                           'margin-bottom': '0px'})],
                            className='h-50'),
                    dbc.Row([
                        dbc.Col(graph,
                                width=6,
                                style={'display': 'flex',
                                       'flex-direction': 'column',
                                       "background-color": background_color,
                                       'justify-content': 'center',
                                       'height': '100%',
                                       'width': '100%',
                                       'margin': '0'}),
                        dbc.Col([advice_list],
                                width=6,
                                style={'display': 'inline-flex',
                                       'flex-direction': 'column',
                                       "background-color": background_color,
                                       'justify-content': 'center',
                                       'height': '100%',
                                       'margin': '0px',
                                       'line-height': '140%',
                                       'font-size': 'large'})

                    ], className='h-50'),
                    dbc.Row(hidden_json, className='h-0', style={'display': 'none'}),


], fluid=True, style={'height': '100vh', 'width': '100vw'})


@app.callback(
    # Outputs
    Output(component_id='hidden_json', component_property='children'),

    # Inputs
    Input(component_id='comp', component_property='value'),
    Input(component_id='languages', component_property='value'),
    Input(component_id='age', component_property='value')
)
def create_data(comp, languages, age):

    """

    :param comp: Value of the Salary Dropdown
    :param languages:  Value of the langauges checkboxes
    :param age: value of the inputted user age
    :return: Json file to be hidden on the page in a div
             and then reread by future functions
    """

    if comp is None and age is None:
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

    data['status'] = np.where(data['ConvertedCompGroup'] > comp, 'Higher Earner',
                              np.where(data['ConvertedCompGroup'] < comp, 'Lower Earner',
                              np.where(data['ConvertedCompGroup'] == comp, 'People Like You', 0)))

    # Outputs data as a json to a hidden div on the page, to be read by later functions
    json_data = data.to_json(orient='split')
    return json_data


@app.callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='hidden_json', component_property='children'),
    Input(component_id='comp', component_property='value')
)
def interactive_graph(hidden_json_data, comp):
    """

    :param hidden_json_data: The return value of the create_data function.
    :param comp: Value of the Salary Dropdown
    :return: A plotly figure to be displayed with id='graph
    """


    figure = go.Figure()
    figure.update_layout(autosize=True,
                         paper_bgcolor=plot_background_color,
                         plot_bgcolor=plot_background_color,
                         yaxis_range=[0, 250000],
                         xaxis_visible=False,
                         margin=dict(l=0, r=0, t=50, b=0),
                         title='Salaries',
                         title_font_size=25,
                         )
    # y axis Settings
    figure.update_layout(yaxis=dict(tickfont=dict(size=18),
                                    ticklabelposition='inside',))
    figure.update_layout(xaxis=({'showgrid': False}))
    # Legend Settings
    figure.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.05,
        xanchor="right",
        x=.94,
        font=dict(size=20)))

    if comp is None:
        figure.add_trace(go.Scatter(x=survey_data['Respondent'],
                                    y=survey_data['ConvertedComp'],
                                    mode='markers',
                                    opacity=0.4,
                                    name='All Respondents',
                                    marker_color='grey',
                                    showlegend=True))
        return figure

    data = pd.read_json(hidden_json_data, orient='split')

    data['ConvertedCompGroup'] = pd.Categorical(data['ConvertedCompGroup'],
                                                categories=comp_group_ordering,
                                                ordered=True)

    higher_earners = data[data['status'] == 'Higher Earner']
    people_like_you = data[data['status'] == 'People Like You']

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
                                marker_color='blue',
                                name='People Like You',
                                marker_size=10))

    figure.add_trace(go.Scatter(x=higher_earners['Respondent'],
                                y=higher_earners['ConvertedComp'],
                                mode='markers',
                                marker_color='green',
                                name='Higher Earners',
                                marker_size=10))

    return figure


@app.callback(
    Output(component_id='advice_text', component_property='children'),
    Input(component_id='hidden_json', component_property='children'),
    Input(component_id='languages', component_property='value'),
    Input(component_id='age', component_property='value'),
    Input(component_id='comp', component_property='value')
)
def give_advice(hidden_json_data, languages, age, comp):
    """

    :param hidden_json_data: The return value of the create_data function.
    :param languages:  Value of the languages checkboxes
    :param age: value of the inputted user age
    :param comp: Value of the Salary Dropdown
    :return: A list containing strings and HTML formatting
             to be put into the div with id='advice_text
    """
    data = pd.read_json(hidden_json_data, orient='split')
    while age is None and comp is None:
        return html.P('Please enter age & salary to see individual advice', style={'textAlign': 'center'})
    higher_earners = data[data['status'] == 'Higher Earner']
    lower_earners = data[data['status'] == 'Lower Earner']
    people_like_you = data[data['status'] == 'People Like You']

    if len(people_like_you) == 0:
        return "Whoops! Look like we can't find anyone like you!"

    if len(people_like_you) == 1:
        return "Looks like you're one of a kind! We couldn't find anyone else like you."

    # Create string for age comparison
    average_age_val = round(higher_earners['Age'].mean() - age)
    most_common_age_val = higher_earners['AgeGroup'].value_counts().index[:1].values[0]

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
    def get_percent(jobsat, option='satisfied'):

        if option == 'satisfied':
            mood = ['Very satisfied', 'Slightly satisfied']
        else:
            mood = ['Very dissatisfied', 'Slightly dissatisfied']
        jobsat = jobsat.groupby('JobSat')['Respondent'].count()
        total = jobsat.sum()
        mood_total = jobsat[jobsat.index.isin(mood)].count()
        mood_percentage = (mood_total / total) * 100

        return round(mood_percentage)

    percent_satisfied_high_earners = get_percent(higher_earners)
    percent_satisfied_people_like_you = get_percent(people_like_you)

    if percent_satisfied_high_earners > percent_satisfied_people_like_you:
        string_suffix = f"It might be time for a job move!"
    if percent_satisfied_high_earners < percent_satisfied_people_like_you:
        string_suffix = f"The grass isn't always greener! Only "
    if percent_satisfied_high_earners == percent_satisfied_people_like_you:
        string_suffix = 'Not gonna get better, but not gonna get worse either!'

    job_sat_string = f"{string_suffix} {percent_satisfied_high_earners}% of higher earners report being satisifed" \
                     f" in their job compared to {percent_satisfied_people_like_you}% of people similar to you"

    return_string_list = [country_string, age_string, language_string, job_sat_string]
    return_options_list = ['Location', 'Age', 'Languges', 'Job Satisfaction']
    return_string = [html.Div([html.H5(title), html.P(advice)]) for
                     advice, title in zip(return_string_list, return_options_list)]
    return_string.insert(0, html.H1('Advice'))
    return_string.insert(1, html.Br())

    return return_string


if __name__ == '__main__':
    app.run_server()
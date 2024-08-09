import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the Olympics data using pandas
data = pd.read_csv('Summer-Olympic-medals-1976-to-2008.csv', encoding='ISO-8859-1')

# Filter out null or None values from the Country list
unique_countries = data['Country'].dropna().unique()

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Summer Olympics Medals Dashboard"

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Overall Statistics', 'value': 'Overall Statistics'},
    {'label': 'Statistics by Country', 'value': 'Statistics by Country'}
]

# Create the layout of the app
app.layout = html.Div([
    html.H1("Summer Olympics Medals Dashboard", style={'text-align': 'center', 'color': '#000080', 'font-weight': 'bold'}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='stat-type',
            options=dropdown_options,
            value='Overall Statistics',
            placeholder='Select Statistics'
        )
    ]),
    html.Div([
        dcc.Dropdown(
            id='select-country',
            options=[{'label': country, 'value': country} for country in unique_countries],
            value='United States',  # Default country
        )
    ]),
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flex-wrap': 'wrap'})
    ])
])

# Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-country', component_property='disabled'),
    Input(component_id='stat-type', component_property='value')
)
def update_input_container(selected_statistics):
    return selected_statistics != 'Statistics by Country'

@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-country', component_property='value'), 
     Input(component_id='stat-type', component_property='value')]
)
def update_output_container(selected_country, stat_type):
    if stat_type == 'Overall Statistics':
        # Overall medal counts by gender
        medal_counts_gender = data['Gender'].value_counts().reset_index()
        medal_counts_gender.columns = ['Gender', 'Count']  # Rename columns
        chart1 = dcc.Graph(
            figure=px.bar(medal_counts_gender, 
                           x='Gender', 
                           y='Count', 
                           title='Number of Medals Won by Gender'))

        # Overall medals by year
        medals_by_year = data.groupby('Year').size().reset_index(name='Medal Count')
        chart2 = dcc.Graph(
            figure=px.line(medals_by_year, 
                           x='Year', 
                           y='Medal Count', 
                           title='Number of Medals Won Over the Years'))
        
        # Overall medals by country
        medals_by_country = data['Country'].value_counts().reset_index()
        medals_by_country.columns = ['Country', 'Count']
        chart3 = dcc.Graph(
            figure=px.bar(medals_by_country, 
                           x='Country', 
                           y='Count', 
                           title='Total Medals Won by Country'))

        # Overall distribution of medals by type
        medal_distribution = data['Medal'].value_counts().reset_index()
        medal_distribution.columns = ['Medal', 'Count']
        chart4 = dcc.Graph(
            figure=px.pie(medal_distribution, 
                           values='Count', 
                           names='Medal', 
                           title='Overall Distribution of Medals by Type'))

        return [
            html.Div(className='chart-item', children=[chart1], style={'width': '48%'}),
            html.Div(className='chart-item', children=[chart2], style={'width': '48%'}),
            html.Div(className='chart-item', children=[chart3], style={'width': '48%'}),
            html.Div(className='chart-item', children=[chart4], style={'width': '48%'})
        ]

    elif stat_type == 'Statistics by Country':
        # Filter data for the selected country
        country_data = data[data['Country'] == selected_country]

        # Medals by year for the selected country
        medals_by_year = country_data.groupby('Year').size().reset_index(name='Medal Count')
        chart1 = dcc.Graph(
            figure=px.line(medals_by_year, 
                           x='Year', 
                           y='Medal Count', 
                           title=f'Medals Won by {selected_country} Over the Years'))

        # Total medals by type for the selected country
        medal_counts = country_data['Medal'].value_counts().reset_index()
        medal_counts.columns = ['Medal', 'Count']  # Rename columns
        chart2 = dcc.Graph(
            figure=px.pie(medal_counts, 
                           values='Count', 
                           names='Medal', 
                           title=f'Distribution of Medals by Type for {selected_country}'))

        # Medals by sport for the selected country
        medals_by_sport = country_data['Sport'].value_counts().reset_index()
        medals_by_sport.columns = ['Sport', 'Count']
        chart3 = dcc.Graph(
            figure=px.bar(medals_by_sport, 
                           x='Sport', 
                           y='Count', 
                           title=f'Medals Won by {selected_country} by Sport'))

        # Medals by gender for the selected country
        medals_by_gender = country_data['Gender'].value_counts().reset_index()
        medals_by_gender.columns = ['Gender', 'Count']
        chart4 = dcc.Graph(
            figure=px.bar(medals_by_gender, 
                           x='Gender', 
                           y='Count', 
                           title=f'Medals Won by {selected_country} by Gender'))

        return [
            html.Div(className='chart-item', children=[chart1], style={'width': '48%'}),
            html.Div(className='chart-item', children=[chart2], style={'width': '48%'}),
            html.Div(className='chart-item', children=[chart3], style={'width': '48%'}),
            html.Div(className='chart-item', children=[chart4], style={'width': '48%'})
        ]
    
    return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

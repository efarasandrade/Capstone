# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1: Dropdown for launch site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
        ],
        value='ALL',  # Default value
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    # TASK 2: Pie chart for launch success count
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: RangeSlider for Payload Mass selection
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={int(i): str(i) for i in range(int(min_payload), int(max_payload)+1, 1000)},
        value=[min_payload, max_payload]
    ),
    html.Br(),

    # TASK 4: Scatter chart for Payload Mass vs. Launch Outcome
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])


# TASK 2: Callback function for Pie Chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(site):
    if site == 'ALL':
        # Pie chart for all launch sites
        fig = px.pie(
            spacex_df,
            names='Launch Site',
            title='Total Successful Launches for All Sites'
        )
    else:
        # Filter data for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f"Success vs. Failure for {site}"
        )
    return fig


# TASK 4: Callback function for Scatter Chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(site, payload_range):
    low, high = payload_range
    # Filter data for the selected payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if site == 'ALL':
        # Scatter chart for all sites
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Launch Site',
            title='Correlation Between Payload and Success for All Sites'
        )
    else:
        # Scatter chart for selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == site]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='class',
            title=f"Correlation Between Payload and Success for {site}"
        )
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

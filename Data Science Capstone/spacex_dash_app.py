# Import required libraries
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children = [
    html.H1('SpaceX Launch Records Dashboard, Check',
        style = {'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    dcc.Dropdown(
        ["All Sites"] +[site for site in spacex_df['Launch Site'].unique()],
        'ALL Sites', id='site-dropdown', placeholder='Select Site', searchable=True),
    html.Br(),


    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),


    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload]),


    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ])


@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value'))
def pie_function(selected_site):
    filtered_df = spacex_df

    if selected_site=="All Sites":
        fig = px.pie(
            spacex_df, values='class',
            names='Launch Site', 
            title='Pie Chart for All Launch Sites')
        fig.update()
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==selected_site].groupby(['Launch Site', 'class']).size().reset_index(name='class count')
        fig = px.pie(
            filtered_df, values='class count',
            names='class',
            title=f"Pie Chart for {selected_site}")
        return fig

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    Input('site-dropdown', 'value'),
    Input('payload-slider', 'value'))
def payload_read(site, payload):
    filt_df = spacex_df[(spacex_df['Payload Mass (kg)'] > payload[0]) & (spacex_df['Payload Mass (kg)'] < payload[1])]
    
    if site == "All Sites":
        fig = px.scatter(filt_df, x="Payload Mass (kg)", y="class", 
            color='Booster Version Category',
            title=' Payload Vs Success Scatter Plot for all Sites')
        return fig
    else:
        filt_df = spacex_df[spacex_df['Launch Site']==site]
        fig = px.scatter(
            filt_df, x='Payload Mass (kg)',
            y='class', color ='Booster Version',
            title=f"Payload Vs Success for {site}")
        return fig

if __name__ == '__main__':
    app.run_server(debug=True)

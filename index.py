from dash2 import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

df = pd.read_csv('Sample_Superstore.csv')

app = Dash(__name__,external_stylesheets=[dbc.themes.VAPOR])

myTitle = dcc.Markdown(children='## Analyzing Super Store')

myGraph = dcc.Graph(figure={})

dropDown = dcc.Dropdown(options=['Bar Plot','Scatter Plot'],
                        value='Bar Plot',
                        clearable=False)

app.layout = dbc.Container([myTitle,myGraph,dropDown,])

@app.callback(
    Output(myGraph, component_property='figure'),
    Input(dropDown, component_property='value')
)

def update_graph(user_input):
    if user_input == 'Bar Plot':
        fig = px.bar(data_frame=df,x="Category",y="Quantity",title="Total Sales")
        
    elif user_input == 'Scatter Plot':
        fig = px.scatter(data_frame=df, x="Profit", y="Sales")
        
    return fig

# fig = px.bar(df,x="Category",y="Quantity",title="Total Sales")

# app.layout = html.Div(children=[
#     html.H1(children="Sales by Category"),
#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
# ]
# )

if __name__ == '__main__':
    app.run_server(port=8051)
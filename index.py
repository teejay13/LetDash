from dash2 import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
from numerize import numerize
import pandas as pd

import plotly.express as px

df = pd.read_csv('Sample_Superstore.csv')

df.columns = df.columns.str.replace(" ", "_").str.lower()

df['order_date']=pd.to_datetime(df['order_date'])
df['ship_date']=pd.to_datetime(df['ship_date'])
df['quantity'] = df['quantity'].astype(float)

print(df.sample(3))

# print(df.info())

total_customers = df['customer_id'].agg(['count']).reset_index()

def gen_total_bans(df,column):
        return df[column].sum()

Sales_by_Category=df.groupby('category')['sales'].sum().reset_index()

print(Sales_by_Category)

# sales_category_pie =px.pie(Sales_by_Category, values='sales', 
#              names='category', 
#              hole=0.5, 
#              color_discrete_sequence=px.colors.qualitative.Pastel)

sales_category_bar = px.bar(df, x="sales", y="category", orientation='h')

#sales_category_pie.update_traces(textposition='inside', textinfo='percent+label')

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

sales = dbc.Card(
    [
        html.Div(
            [
                # dcc.Graph(id="pie-graph",figure=sales_category_bar),
                dbc.CardBody(
                [
                    html.H1(f"${numerize.numerize(gen_total_bans(df,'sales'), 1)} ", className="card-title"),
                    html.H6("Total Sales", className="card-title"),
                ])
            ]
        ),
    ],
    body=True,
)

discount = dbc.Card(
    [
        html.Div(
            [
                # dcc.Graph(id="pie-graph",figure=sales_category_bar),
                dbc.CardBody(
                [
                    html.H1(f"${numerize.numerize(gen_total_bans(df,'discount'),1)}", className="card-title"),
                    html.H6("Total Discount", className="card-title"),
                ])
            ]
        ),
    ],
    body=True,
)

profit = dbc.Card(
    [
        html.Div(
            [
                # dcc.Graph(id="pie-graph",figure=sales_category_bar),
                dbc.CardBody(
                [
                    html.H1(f"${numerize.numerize(gen_total_bans(df,'profit'),1)}", className="card-title"),
                    html.H6("Total Profit", className="card-title"),
                ])
            ]
        ),
    ],
    body=True,
)

quantity = dbc.Card(
    [
        html.Div(
            [
                # dcc.Graph(id="pie-graph",figure=sales_category_bar),
                dbc.CardBody(
                [
                    html.H1(numerize.numerize(gen_total_bans(df,'quantity'),1), className="card-title"),
                    html.H6("Total Quantity", className="card-title"),
                ])
            ]
        ),
    ],
    body=True,
)


app.layout = html.Div(
    [
        dcc.Location(id="url"),
        dbc.NavbarSimple(
            children=[
                dbc.NavLink("Overview", href="/", active="exact"),
                dbc.NavLink("Product Analysis", href="/page-1", active="exact"),
                dbc.NavLink("Regional Analysis", href="/page-2", active="exact"),
                dbc.NavLink("Order Details", href="/page-3", active="exact"),
            ],
            brand="Superstore Dashboard",
            color="primary",
            dark=True,
        ),
        dbc.Container(id="page-content", className="pt-4"),
    ]
)

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return dbc.Row(
            children = [
                dbc.Row([
                    dbc.Col(sales, md=3),
                    dbc.Col(discount, md=3),
                    dbc.Col(profit, md=3),
                    dbc.Col(quantity, md=3),
                ]),
                dbc.Row([
                    #dbc.Col(ok, md=6),
                    dbc.Col(dcc.Graph(id="cluster-graph"), md=6),
                ])
            ],
            align="center",
        )
    elif pathname == "/page-1":
        return html.P("THey Yay!")
    elif pathname == "/page-2":
        return html.P("wE MOVE")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


# def update_graph(path):
#     if user_input == 'Bar Plot':
#         fig = px.bar(data_frame=df,x="Category",y="Quantity",title="Total Sales")
        
#     elif user_input == 'Scatter Plot':
#         fig = px.scatter(data_frame=df, x="Profit", y="Sales")
        
#     return fig

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
    app.run_server(debug=True,port=8555)
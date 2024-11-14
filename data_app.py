import pandas as pd
import plotly.express as px
from dash import Dash, html, dash_table, dcc, callback, Output, Input
from dash.exceptions import PreventUpdate

# Load data (consider caching for large datasets)
df = pd.read_csv("C:/Users/arpan/OneDrive/Desktop/newhouse.csv")

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Housing Data Dashboard', style={'textAlign': 'center'}),
    dash_table.DataTable(
        id='data-table',
        data=df.to_dict('records'),
        page_size=20,
        style_table={'overflowX': 'auto'}
    ),
    html.Div([
        html.Label('Select Feature:'),
        dcc.Dropdown(
            id='feature-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns],
            value=df.columns[0]
        )
    ], style={'width': '50%', 'margin': 'auto', 'padding': '20px'}),
    dcc.Graph(id='histogram')
])

@callback(
    Output('histogram', 'figure'),
    Input('feature-dropdown', 'value')
)
def update_histogram(selected_feature):
    if not selected_feature:
        raise PreventUpdate
    
    try:
        fig = px.histogram(df, x=selected_feature)
        fig.update_layout(
            title=f'Histogram of {selected_feature}',
            xaxis_title=selected_feature,
            yaxis_title='Frequency',
            template='plotly_white'
        )
        return fig
    except Exception as e:
        return px.scatter(title=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)

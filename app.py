import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from lib import plot_powerline as ppl

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets
                )

server = app.server

app.layout = html.Div([
    html.H2("Some plots"),
    html.Div(["r (Ohm/m): ",
              dcc.Input(id='res-in', value='21.0e-6', type='text'),]),
    html.Div(["l (H/m): ",
              dcc.Input(id='ind-in', value='0.8591e-6', type='text'),]),
    html.Div(["c (F/m): ",
              dcc.Input(id='cap-in', value='13e-12', type='text'),]),
    html.Div(["g (S/m): ",
              dcc.Input(id='cond-in', value='13.13e-12', type='text'),]),
    html.Br(),
    html.Div(id='res-out'),

    dcc.Graph(id='graph'),
])


@app.callback(
    Output(component_id='res-out', component_property='children'),
    Input(component_id='res-in', component_property='value')
)
def update_output_div(input_value):
    return 'r (Ohm/m): {}'.format(input_value)

@app.callback(
    Output('graph', 'figure'),
    Input('res-in', 'value'))
def update_figure(R):
    fig = ppl.plot_V_I()
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
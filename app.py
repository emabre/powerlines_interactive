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
    html.Div(["R (Ohm): ",
              dcc.Input(id='my-input', value='50.0', type='text')]),
    html.Br(),
    html.Div(id='my-output'),

    dcc.Graph(id='graph'),

])


@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)

@app.callback(
    Output('graph', 'figure'),
    Input('my-input', 'value'))
def update_figure(R):
    fig = ppl.plot_V_I()
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
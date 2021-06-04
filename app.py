import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from lib import plot_powerline as ppl
from lib import transmission as tr

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets
                )

server = app.server

app.layout = html.Div([
    html.H2("Some plots"),
    html.Div(["r (Ohm/m): ",
              dcc.Input(id='res-in', value=21.0e-6, type='number'),]),
    html.Div(["l (H/m): ",
              dcc.Input(id='ind-in', value=0.8591e-6, type='number'),]),
    html.Div(["c (F/m): ",
              dcc.Input(id='cap-in', value=13e-12, type='number'),]),
    html.Div(["g (S/m): ",
              dcc.Input(id='cond-in', value=13.13e-12, type='number'),]),
    html.Div(["freq-in (Hz): ",
              dcc.Input(id='freq-in', value=50.0, type='number'),]),
    html.Br(),
    html.Div(id='Zc'),
    html.Div(id='k'),

    dcc.Graph(id='graph'),
])


@app.callback(
    Output(component_id='k', component_property='children'),
    Output(component_id='Zc', component_property='children'),
    Input(component_id='res-in', component_property='value'),
    Input(component_id='ind-in', component_property='value'),
    Input(component_id='cond-in', component_property='value'),
    Input(component_id='cap-in', component_property='value'),
    Input(component_id='freq-in', component_property='value'),
)
def update_kZc(res, ind, cond, cap, freq):
    k, Zc = tr.xy_to_kZc(res, ind, cond, cap, freq)
    return 'k (Ohm/m): {:.3g}\n'.format(k), 'Zc (Ohm): {:.3g}\n'.format(Zc)

# @app.callback(
#     Output('graph', 'figure'),
#     Input('res-in', 'value'))
# def update_figure(R):
#     fig = ppl.plot_V_I()
#     return fig


if __name__ == '__main__':
    app.run_server(debug=True)
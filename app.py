import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from lib import plot_powerline as ppl
from lib import transmission as tr
from lib import utils as ut

#%% Settings
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets
                )

server = app.server

#%% Layout
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
    html.Div(["d (m): ",
              dcc.Input(id='d-in', value=100.0, type='number'),]),
    html.Br(),
    html.Div(['Zc (Ohm):', dcc.Input(id='Zc', value=0, type='number')]),
    html.Div(['k (1/m):', dcc.Input(id='k', value=0, type='number')]),
    # html.Table([html.Tr([html.Td(['Zc (Ohm):']), html.Td(id='Zc')]),
    #             html.Tr([html.Td(['k (Ohm/m):']), html.Td(id='k')]),]),
    dcc.Graph(id='graph'),
])

#%% Callbacks
@app.callback(
    Output(component_id='k', component_property='value'),
    Output(component_id='Zc', component_property='value'),
    Input(component_id='res-in', component_property='value'),
    Input(component_id='ind-in', component_property='value'),
    Input(component_id='cond-in', component_property='value'),
    Input(component_id='cap-in', component_property='value'),
    Input(component_id='freq-in', component_property='value'),
)
def update_kZc(res, ind, cond, cap, freq):
    k, Zc = tr.xy_to_kZc(res, ind, cond, cap, freq)
    return k.imag, Zc.real
# def update_kZc(res, ind, cond, cap, freq):
#     k, Zc = tr.xy_to_kZc(res, ind, cond, cap, freq)
#     return '{:.3g}'.format(k), '{:.3g}'.format(Zc)

@app.callback(
    Output('graph', 'figure'),
    Input('Zc', 'value'),
    Input('k', 'value'),
    Input('d-in', 'value')
    )
def update_figure(Zc_str, k_str, d):
    fig = ppl.plot_V_I(*ut.to_numbers(Zc_str, k_str), d)
    return fig


#%% Testing
if __name__ == '__main__':
    app.run_server(debug=True)
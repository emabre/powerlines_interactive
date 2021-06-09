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
    html.Div(['Zc = ',
              dcc.Input(id='Re(Zc)', value=11, type='number'),
              ' + j',
              dcc.Input(id='Im(Zc)', value=22, type='number'),
              ' Ohm']),
    html.Div(['k = ',
              dcc.Input(id='Re(k)', value=33, type='number'),
              ' + j',
              dcc.Input(id='Im(k)', value=44, type='number'),
              ' 1/m']),
    # html.Table([html.Tr([html.Td(['Zc (Ohm):']), html.Td(id='Zc')]),
    #             html.Tr([html.Td(['k (Ohm/m):']), html.Td(id='k')]),]),
    dcc.Graph(id='graph'),
])

#%% Callbacks
@app.callback(
    Output(component_id='Re(k)', component_property='value'),
    Output(component_id='Im(k)', component_property='value'),
    Output(component_id='Re(Zc)', component_property='value'),
    Output(component_id='Im(Zc)', component_property='value'),
    Input(component_id='res-in', component_property='value'),
    Input(component_id='ind-in', component_property='value'),
    Input(component_id='cond-in', component_property='value'),
    Input(component_id='cap-in', component_property='value'),
    Input(component_id='freq-in', component_property='value'),
)
def update_kZc(res, ind, cond, cap, freq):
    k, Zc = tr.xy_to_kZc(res, ind, cond, cap, freq)
    return k.real, k.imag, Zc.real, Zc.imag
# def update_kZc(res, ind, cond, cap, freq):
#     k, Zc = tr.xy_to_kZc(res, ind, cond, cap, freq)
#     return '{:.3g}'.format(k), '{:.3g}'.format(Zc)

@app.callback(
    Output('graph', 'figure'),
    Input('Re(Zc)', 'value'),
    Input('Im(Zc)', 'value'),
    Input('Re(k)', 'value'),
    Input('Im(k)', 'value'),
    Input('d-in', 'value')
    )
def update_figure(Zc_real, Zc_imag, k_real, k_imag, d):
    fig = ppl.plot_V_I(Zc_real + 1j*Zc_imag,
                       k_real + 1j*k_imag, d)
    return fig


#%% Testing
if __name__ == '__main__':
    app.run_server(debug=True)
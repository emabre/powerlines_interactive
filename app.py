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
    html.Div(["r = ",
              dcc.Input(id='res-in', value=12.5e-6, type='number'),
              " Ohm/m"]),
    html.Div(["l = ",
              dcc.Input(id='ind-in', value=0.576e-6, type='number'),
              " H/m"]),
    html.Div(["c = ",
              dcc.Input(id='cap-in', value=234e-12, type='number'),
              " F/m"]),
    html.Div(["g = ",
              dcc.Input(id='cond-in', value=51.459e-12, type='number'),
              " S/m"]),
    html.Div(["f = ",
              dcc.Input(id='freq-in', value=50.0, type='number'),
              " Hz"]),
    html.Div(["d = ",
              dcc.Input(id='d-in', value=100.0, type='number'),
              " m"]),
    html.Br(),
    html.Div(['k = ',
              dcc.Input(id='Re(k)', value=33, type='number'),
              ' + j',
              dcc.Input(id='Im(k)', value=44, type='number'),
              ' 1/m']),
    html.Div(['Zc = ',
              dcc.Input(id='Re(Zc)', value=11, type='number'),
              ' + j',
              dcc.Input(id='Im(Zc)', value=22, type='number'),
              ' Ohm']),
    dcc.Graph(id='graph'),
])

#%% Callbacks
@app.callback(
    Output('res-in', 'value'),
    Output('ind-in', 'value'),
    Output('cond-in', 'value'),
    Output('cap-in', 'value'),
    Output('freq-in', 'value'),
    Output('Re(k)', 'value'),
    Output('Im(k)', 'value'),
    Output('Re(Zc)', 'value'),
    Output('Im(Zc)', 'value'),

    Input('res-in', 'value'),
    Input('ind-in', 'value'),
    Input('cond-in', 'value'),
    Input('cap-in', 'value'),
    Input('freq-in', 'value'),
    Input('Re(Zc)', 'value'),
    Input('Im(Zc)', 'value'),
    Input('Re(k)', 'value'),
    Input('Im(k)', 'value'),
)
def update_kZc_xy(res, ind, cond, cap, freq,
                  Zc_real, Zc_imag, k_real, k_imag):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    xyf = ('res-in', 'ind-in', 'cond-in','cap-in', 'freq-in')

    if trigger_id in xyf:
        k, Zc = tr.xy_to_kZc(res, ind, cond, cap, freq)
        
        res_out, ind_out, con_out, cap_out, freq_out = res, ind, cond, cap, freq
        k_real_out, k_imag_out = k.real, k.imag
        Zc_real_out, Zc_imag_out,  = Zc.real, Zc.imag
    else:
        res_out, ind_out, cond_out, cap_out = tr.kZc_to_xy(Zc_real + 1j*Zc_imag,
                                                           k_real + 1j*k_imag)
        k_real_out, k_imag_out = k_real, k_imag
        Zc_real_out, Zc_imag_out = Zc_real, Zc_imag
    
    return (res_out, ind_out, con_out, cap_out, freq_out,
            Zc_real_out, Zc_imag_out, k_real_out, k_imag_out)

# @app.callback(
#     Output(component_id='Re(k)', component_property='value'),
#     Output(component_id='Im(k)', component_property='value'),
#     Output(component_id='Re(Zc)', component_property='value'),
#     Output(component_id='Im(Zc)', component_property='value'),
#     Input(component_id='res-in', component_property='value'),
#     Input(component_id='ind-in', component_property='value'),
#     Input(component_id='cond-in', component_property='value'),
#     Input(component_id='cap-in', component_property='value'),
#     Input(component_id='freq-in', component_property='value'),
# )
# def update_kZc(res, ind, cond, cap, freq):
#     k, Zc = tr.xy_to_kZc(res, ind, cond, cap, freq)
#     return k.real, k.imag, Zc.real, Zc.imag

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
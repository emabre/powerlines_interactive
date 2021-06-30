import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from lib import plot_powerline as ppl
from lib import transmission as tr
from lib import utils as ut

#%% Settings
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__,
#                 external_stylesheets=external_stylesheets
#                 )

app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])

app.title = "Power line"

server = app.server

#%% Layout
app.layout = dbc.Container([
                            dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Row(
                                                    [
                                                        html.H2("Electrical quantities along a power line")
                                                    ]
                                                ),
                                                html.Div(["r = ",
                                                            dcc.Input(id='res', value=12.5e-3, type='number'),
                                                        " Ohm/km"]
                                                ),
                                                html.Div(["l = ",
                                                        dcc.Input(id='ind', value=0.576e-3, type='number'),
                                                        " H/km"]
                                                ),
                                                html.Div(["c = ",
                                                        dcc.Input(id='cap', value=234e-9, type='number'),
                                                        " F/km"]),
                                                html.Div(["g = ",
                                                        dcc.Input(id='cond', value=51.459e-9, type='number'),
                                                        " S/km"]),
                                                html.Div(["f = ",
                                                        dcc.Input(id='freq', value=50.0, type='number'),
                                                        " Hz"]),
                                                html.Div(["d = ",
                                                        dcc.Input(id='d', value=100.0, type='number'),
                                                        " km"]),
                                                html.Br(),
                                                html.Div(['k = ',
                                                        dcc.Input(id='Re(k)', value=0.12718e-3, type='number'),
                                                        ' + j',
                                                        dcc.Input(id='Im(k)', value=3.6494e-3, type='number'),
                                                        ' 1/km']),
                                                html.Div(['Zc = ',
                                                        dcc.Input(id='Re(Zc)', value=49.644, type='number'),
                                                        ' + j',
                                                        dcc.Input(id='Im(Zc)', value=-1.695, type='number'),
                                                        ' Ohm']),
                                                html.Div(['Vs = ',
                                                        dcc.Input(id='Re(Vs)', value=20.0e3, type='number'),
                                                        ' + j',
                                                        dcc.Input(id='Im(Vs)', value=0.0, type='number'),
                                                        ' V']),
                                                html.Div(['Vs = ',
                                                        dcc.Input(id='Re(Is)', value=100.0, type='number'),
                                                        ' + j',
                                                        dcc.Input(id='Im(Is)', value=10.0, type='number'),
                                                        ' A']),
                                            ]
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Graph(id='graph'),
                                            ]
                                        )
                                    ]
                            )
                            
                        ],
                        )

#%% Callbacks
@app.callback(
    Output('res', 'value'),
    Output('ind', 'value'),
    Output('cond', 'value'),
    Output('cap', 'value'),
    Output('freq', 'value'),
    Output('Re(k)', 'value'),
    Output('Im(k)', 'value'),
    Output('Re(Zc)', 'value'),
    Output('Im(Zc)', 'value'),

    Input('res', 'value'),
    Input('ind', 'value'),
    Input('cond', 'value'),
    Input('cap', 'value'),
    Input('freq', 'value'),
    Input('Re(k)', 'value'),
    Input('Im(k)', 'value'),
    Input('Re(Zc)', 'value'),
    Input('Im(Zc)', 'value'),
)
def update_kZc_xy(res, ind, cond, cap, freq,
                  k_real, k_imag, Zc_real, Zc_imag):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    xyf = ('res', 'ind', 'cond','cap', 'freq')

    if trigger_id in xyf:
        k, Zc = tr.xy_to_kZc(res, ind, cond, cap, freq)
        k_real_out, k_imag_out = k.real, k.imag
        Zc_real_out, Zc_imag_out,  = Zc.real, Zc.imag

        res_out, ind_out, cond_out, cap_out, freq_out = res, ind, cond, cap, freq

    else:
        res_out, ind_out, cond_out, cap_out = tr.kZc_to_xy(k_real + 1j*k_imag, 
                                                           Zc_real + 1j*Zc_imag,
                                                           freq)
        k_real_out, k_imag_out = k_real, k_imag
        Zc_real_out, Zc_imag_out = Zc_real, Zc_imag
        freq_out = freq
    
    return (res_out, ind_out, cond_out, cap_out, freq_out,
            k_real_out, k_imag_out, Zc_real_out, Zc_imag_out,)

@app.callback(
    Output('graph', 'figure'),
    Input('Re(k)', 'value'),
    Input('Im(k)', 'value'),
    Input('Re(Zc)', 'value'),
    Input('Im(Zc)', 'value'),
    Input('d', 'value'),
    Input('Re(Vs)', 'value'),
    Input('Im(Vs)', 'value'),
    Input('Re(Is)', 'value'),
    Input('Im(Is)', 'value'),
)
def update_figure(k_real, k_imag,
                  Zc_real, Zc_imag,
                  d,
                  Vs_real, Vs_imag,
                  Is_real, Is_imag):
    fig = ppl.plot_V_I(k_real + 1j*k_imag,
                       Zc_real + 1j*Zc_imag,
                       d,
                       Vs_real + 1j*Vs_imag,
                       Is_real + 1j*Is_imag)
    return fig


#%% Testing
if __name__ == '__main__':
    app.run_server(debug=True)
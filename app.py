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

app = dash.Dash(external_stylesheets=[dbc.themes.CERULEAN])

app.title = "Power line"

server = app.server

#%% Layout

kZc_card = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Zc (Ohm)"),
                dbc.Row(
                    [
                        dbc.Col([dbc.Input(id="Re(Zc)", value=49.644, type='number')], width=5),
                        dbc.Col([html.Div(' + j')], width=2),
                        dbc.Col([dbc.Input(id="Im(Zc)", value=-1.695, type='number')], width=5),
                    ]
                )
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("k (1/km)"),
                dbc.Row(
                    [
                        dbc.Col([dbc.Input(id="Re(k)", value=0.12718e-3, type='number')], width=5),
                        dbc.Col([html.Div(' + j')], width=2),
                        dbc.Col([dbc.Input(id="Im(k)", value=3.6494e-3, type='number')], width=5),
                    ]
                )
            ]
        ),
    ],
    body=True,
)

VsIs_card = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Vs (V)"),
                dbc.Row(
                    [
                        dbc.Col([dbc.Input(id="Re(Vs)", value=20e3, type='number')], width=5),
                        dbc.Col([html.Div(' + j')], width=2),
                        dbc.Col([dbc.Input(id="Im(Vs)", value=0, type='number')], width=5),
                    ]
                )
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Is (A)"),
                dbc.Row(
                    [
                        dbc.Col([dbc.Input(id="Re(Is)", value=100.0, type='number')], width=5),
                        dbc.Col([html.Div(' + j')], width=2),
                        dbc.Col([dbc.Input(id="Im(Is)", value=10.0, type='number')], width=5),
                    ]
                )
            ]
        ),
    ],
    body=True,
)

rlgc_card = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.FormGroup(
                            [
                                dbc.Label("r (Ohm/km)"),
                                dbc.Input(id='res', value=12.5e-3, type='number')
                            ]
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        dbc.FormGroup(
                            [
                                dbc.Label("l (H/km)"),
                                dbc.Input(id='ind', value=0.576e-3, type='number')
                            ]
                        ),
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.FormGroup(
                            [
                                dbc.Label("g (S/km)"),
                                dbc.Input(id='cond', value=51.459e-9, type='number')
                            ]
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        dbc.FormGroup(
                            [
                                dbc.Label("c (F/km)"),
                                dbc.Input(id='cap', value=234e-9, type='number')
                            ]
                        ),
                    ]
                )
            ]
        ) 
    ],
    body=True,
)

fd_card = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.FormGroup(
                            [
                                dbc.Label("f (Hz)"),
                                dbc.Input(id='freq', value=50.0, type='number')
                            ]
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        dbc.FormGroup(
                            [
                                dbc.Label("d (km)"),
                                dbc.Input(id='d', value=100.0, type='number')
                            ]
                        ),
                    ]
                )
            ]
        )
    ],
    body=True,
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                html.H2("Electrical quantities along a power line"),
            ]
        ),
        dbc.Row(
            [
                html.H4("Given the state (V, I) at the sending end, and the line properties (r, l, g, c or Zc and k)"),                                                        
            ]
        ),     
        dbc.Row(
            [
                dbc.Col(
                    [
                        kZc_card,
                        rlgc_card,
                        VsIs_card,
                        fd_card
                    ],
                    width = 5
                ),
                dbc.Col(
                    [
                        dcc.Graph(id='graph'),
                    ],
                    width = 7
                )
            ]
        ),
    ],
    # fluid = True
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
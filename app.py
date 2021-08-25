import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from lib import plot_powerline as ppl
from lib import transmission as tr

#%% Settings
app = dash.Dash(external_stylesheets=[dbc.themes.CERULEAN])
app.title = "Power line"
server = app.server

#%% Layout

VsText = html.Div(["V", html.Sub(["s"]), " (V)"])
IsText = html.Div(["I", html.Sub(["s"]), " (A)"])
ZcText = html.Div(["Z", html.Sub(["c"]), " (Ω)"])

# Settings for using more practical units
milli = {'conversion fact':1e-3, 'unit specifier': 'm'}
nano = {'conversion fact':1e-9, 'unit specifier': 'n'}
u = {'conversion fact':1.0, 'unit specifier': ''}
res_units = milli
ind_units = milli
cond_units = nano
cap_units = nano


kZc_card = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label(ZcText),
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
                dbc.Label(VsText),
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
                dbc.Label(IsText),
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
                                dbc.Label("r ({}Ω/km)".format(res_units['unit specifier'])),
                                dbc.Input(id='res', value=12.5e-3, type='number')
                            ]
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        dbc.FormGroup(
                            [
                                dbc.Label("l ({}H/km)".format(ind_units['unit specifier'])),
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
                                dbc.Label("g ({}S/km)".format(cond_units['unit specifier'])),
                                dbc.Input(id='cond', value=51.459e-9, type='number')
                            ]
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        dbc.FormGroup(
                            [
                                dbc.Label("c ({}F/km)".format(cap_units['unit specifier'])),
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
                                dbc.Label("frequency (Hz)"),
                                dbc.Input(id='freq', value=50.0, type='number')
                            ]
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        dbc.FormGroup(
                            [
                                dbc.Label("line length (km)"),
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
                html.H2("Electrical quantities along a three-phase power line"),
            ]
        ),
        dbc.Row(
            [
                html.H4(["Given the phase voltage and current at the sending end, and the line properties"]),                                                        
            ]
        ),
        dbc.Row(
            [
                html.H6([dcc.Link("Source code and references",
                         href="https://github.com/emabre/powerlines_interactive")],
                         style = {"text-decoration": "underline",
                                #   "font-family":'Arial'
                                  }),
            ]
        ),
        html.Hr(),   
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

    xyf = ('res', 'ind', 'cond', 'cap', 'freq')

    if trigger_id in xyf:
        # Transform r,l,c,g to usual SI units
        res_out = res * res_units['conversion fact']
        ind_out = ind * ind_units['conversion fact']
        cond_out = cond * cond_units['conversion fact']
        cap_out = cap * cap_units['conversion fact']

        freq_out = freq
        
        k, Zc = tr.xy_to_kZc(res_out,
                             ind_out,
                             cond_out,
                             cap_out,
                             freq)
        k_real_out, k_imag_out = k.real, k.imag
        Zc_real_out, Zc_imag_out = Zc.real, Zc.imag
        
    else:
        res_out, ind_out, cond_out, cap_out = tr.kZc_to_xy(k_real + 1j*k_imag, 
                                                           Zc_real + 1j*Zc_imag,
                                                           freq)
        k_real_out, k_imag_out = k_real, k_imag
        Zc_real_out, Zc_imag_out = Zc_real, Zc_imag
        freq_out = freq
    
    # Return transforming back r,l,g,c to convenient units
    return (res_out / res_units['conversion fact'],
            ind_out / ind_units['conversion fact'],
            cond_out / cond_units['conversion fact'],
            cap_out / cap_units['conversion fact'],
            freq_out,
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


#%%
if __name__ == '__main__':
    app.run_server(debug=False) 
    # app.run_server(debug=True)  # Testing
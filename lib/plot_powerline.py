import numpy as np
from lib import transmission as tr
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_V_I(k, Zc, L, Vs, Is):
    #%% Units in SI if not otherwise specified
    N = 100

    #%%
    d = np.linspace(0,L, N)

    A, B, C, D = tr.hybrid(k, Zc, d)

    ws = np.array([Vs, Is])
    w_l = [ws]
    T_l = []  # Obviously T has lenght shorter by 1 than the lenght of ws
    for ii in range(len(d)):
        T_l.append(np.array(((A[ii], B[ii]),
                            (C[ii], D[ii]))))
        w_l.append(np.dot(T_l[ii], ws))


    w = np.array(w_l)
    T = np.array(T_l)

    w_abs = np.abs(w)

    I_abs = w_abs[:,1]
    V_abs = w_abs[:,0]

    I_phase = np.angle(w[:,1])
    V_phase = np.angle(w[:,0])

    S = w[:,0] * np.conj(w[:,1])
    P = np.real(S)
    Q = np.imag(S)
    A = np.abs(S)

    #%%
    # Create figure with secondary y-axis
    fig = make_subplots(rows = 2,
                        cols = 1, 
                        specs=[[{"secondary_y": True}],
                               [{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x = d,
                            y = V_abs,
                            mode = 'lines',
                            name = '|V|',
                            line = {'color': 'blue'}),
                  secondary_y = False,
                  )
    fig.add_trace(go.Scatter(x = d,
                            y = I_abs,
                            mode = 'lines',
                            name = '|I|',
                            line = {'color': 'red'}),
                  secondary_y = True,
                  row = 1,
                  col = 1
                 )
    fig.add_trace(go.Scatter(x = d,
                            y = I_phase,
                            mode = 'lines',
                            name = 'φ_I',
                            line = {'color': 'red',
                                    'dash' : 'dash'}),
                 row = 2,
                 col = 1
                 )
    fig.add_trace(go.Scatter(x = d,
                            y = V_phase,
                            mode = 'lines',
                            name = 'φ_V',
                            line = {'color': 'blue',
                                    'dash' : 'dash'}),
                 row = 2,
                 col = 1
                 )
    fig.add_trace(go.Scatter(x = d,
                            y = P,
                            mode = 'lines',
                            name = 'P',
                            line = {'color': 'green'}),
                secondary_y = True,
                 row = 2,
                 col = 1
                 )
    fig.add_trace(go.Scatter(x = d,
                            y = Q,
                            mode = 'lines',
                            name = 'Q',
                            line = {'color': 'gray'}),
                secondary_y = True,
                 row = 2,
                 col = 1
                 )

    fig.update_yaxes(title_text="Voltage / V",
                     showgrid = False,
                     zeroline = False,
                      secondary_y=False,
                     row = 1, col = 1)
    fig.update_yaxes(title_text="Current / A",
                     showgrid = False,
                     zeroline = False,
                     secondary_y=True,
                     row = 1, col = 1)
    fig.update_yaxes(title_text="Phase / rad",
                     showgrid = False,
                     zeroline = False,
                     secondary_y=False,
                     row = 2, col = 1)
    fig.update_yaxes(title_text="Power / W",
                     showgrid = False,
                     secondary_y=True,
                     zeroline = False,
                     row = 2, col = 1)
    fig.update_xaxes(title_text="Distance / m",
                     row = 2, col = 1)
    
    fig.update_layout(legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=0.5
                ))
    
    return fig
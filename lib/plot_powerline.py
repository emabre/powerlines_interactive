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
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x = d,
                            y = V_abs,
                            mode = 'lines',
                            name = '|V|'),
                  secondary_y=False,
                  )
    fig.add_trace(go.Scatter(x = d,
                            y = I_abs,
                            mode = 'lines',
                            name = '|I|'),
                  secondary_y = True,
                 )

    fig.update_yaxes(title_text="Voltage / V", secondary_y=False)
    fig.update_yaxes(title_text="Current / A", secondary_y=True)
    
    return fig
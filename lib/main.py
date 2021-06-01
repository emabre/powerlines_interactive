import numpy as np
import transmission as tr
import constants as c

#%% Units in SI if not otherwise specified
L = 1000e3
N = 100

# Electrical quantities at the source (s)
phi0 = -0.1*np.pi
Vs = 20.0e3
Is = 100. * np.exp(1j*phi0)

#%%
d = np.linspace(0,L, N)
tr.hybrid(c.Zc, c.k, d)

A, B, C, D = tr.hybrid(c.Zc, c.k, d)

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
# import matplotlib.pyplot as plt
# plt.ion()
# fig, ax = plt.subplots(nrows = 2)
# ax[0].plot(d[:100], V_abs[1:101], label = '|V|')
# ax[0].plot(d[:100], I_abs[1:101], label = '|I|')

# ax_rad = ax[0].twinx()
# ax_rad.plot(d[:100],
#             (V_phase - I_phase)[1:101],
#             label = 'φ_V - φ_I',
#             color = 'black')
# ax_rad.set_ylim([-np.pi, +np.pi])

# ax[1].plot(d[:100], P[1:101], label = 'Power', color = 'navy')
# ax[1].plot(d[:100], Q[1:101], ':', label = 'Reactive power', color = 'gray')
# ax[1].plot(d[:100], A[1:101], '--', label = 'Apparent power', color = 'red')

# specs = 'line with Zc = {:.3g}, k = {:.3g}'.format(c.Zc, c.k)
# title = 'Requirements at the source, given the condition at the receiving end\n' + specs
# fig.suptitle(title)

# fig.legend()
# fig.tight_layout()

#%%
import plotly.graph_objects as go

traces = [go.Scatter(x = d[:100],
                     y = V_abs[1:101],
                     mode = 'lines'),
          go.Scatter(x = d[:100],
                     y = I_abs[1:101],
                    mode = 'lines')
          ]
fig = go.Figure(data = traces)

fig.show()
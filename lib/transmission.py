import numpy as np

def hybrid(Zc, k, d):
    '''
    The hybrid/transmission matrix parameters of a well symmetrized
    line, at the positive sequence.
    Input:
    d: (scalar or array-like) space locations where the parameters have to be computed
    Returns:
    A, B, C, D: parameters (arrays if d is array-like)
                of the hybrid/transmission matrix
    '''

    kd = k*d

    A = np.cosh(kd)
    B = Zc * np.sin(kd)
    C = np.sin(kd) / Zc
    D = A  # Because of symmetry
    
    return A, B, C, D
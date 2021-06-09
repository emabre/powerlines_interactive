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

def xy_to_kZc(r, l, g, c, freq):
    '''
    Compute the parameters k and Zc of a powerline,
    give the r, l, c, g parameters and the power frequency
    '''

    x = r + 1j * 2*np.pi*freq * l
    y = g + 1j * 2*np.pi*freq * c

    k = np.sqrt(x*y)
    Zc = np.sqrt(x/y)
    
    # np.sqrt(c) returns the only solution to x**2 = c that has positive real part.
    # But I add here a check just in case...
    if np.real(Zc) < 0:
        raise ValueError('real part of Zc appears to be negative, fix this!')
    if np.real(k) < 0:
        raise ValueError('real part of k appears to be negative, fix this!')
    
    return k, Zc

if __name__ == '__main__':

    r = 21.0e-6
    l = 0.8591e-6
    g = 13e-12
    c = 13.13e-12
    freq = 50.0

    k, Zc = xy_to_kZc(r, l, g, c, freq)
import numpy as np
import scipy.fftpack as fftpack

def TransFourierPower(s, t=None):
    """
    Transformée de Fourier d'un signal s normalisée par la puissance.

    La version standard `trans_fourier` calcule la TF d'un signal s de L²(R) (normalisation par l'énergie).
    Cette version normalise par la puissance moyenne.

    Parameters
    ----------
    s : array_like
        Vecteur de taille N contenant les N échantillons s[n] du signal à analyser.
    t : array_like, optional
        Vecteur de taille N contenant les instants d'échantillonnage de s.
        Par défaut, t = [0, 1, 2, ..., N-1].

    Returns
    -------
    S : numpy.ndarray
        Vecteur de taille N contenant les coefficients de la transformée de Fourier du signal s normalisée par la puissance.
    f : numpy.ndarray
        Vecteur de taille N contenant les fréquences correspondant aux coefficients de S : S[n] = S(f[n]).

    Raises
    ------
    ValueError
        Si les vecteurs `s` et `t` n'ont pas la même longueur.
        Si `t` n'est pas linéairement croissant avec un pas constant.
    """
    s = np.asarray(s).flatten()
    N = len(s)

    if t is None:
        t = np.arange(N)
    else:
        t = np.asarray(t).flatten()

    if N != len(t):
        raise ValueError('Les vecteurs "s" et "t" doivent être de même longueur.')

    dt = t[1] - t[0]
    if not np.allclose(np.diff(t), dt, atol=1e-12, rtol=0):
        raise ValueError('Le vecteur "t" doit être linéairement croissant avec un pas constant.')

    Fe = 1.0 / dt
    D = (np.max(t) - np.min(t)) + dt  # Durée du signal
    indices_positive = t >= 0
    indices_negative = t < 0
    sshift = np.concatenate((s[indices_positive], s[indices_negative]))

    # Calcul de la FFT
    S = np.fft.fft(sshift, n=N)
    S = np.fft.fftshift(S) * dt

    # Normalisation par la puissance moyenne
    S = S / D

    # Calcul des fréquences
    f = np.linspace(-Fe/2, Fe/2, N+1)[:-1]

    return S, f
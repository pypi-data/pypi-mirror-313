import numpy as np
import scipy.fftpack as fftpack

def TransFourier(s, t=None):
    """
    Calcul de la transformée de Fourier d'un signal s.

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
        Vecteur de taille N contenant les coefficients de la transformée de Fourier du signal s.
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

    # Décaler le signal pour que t=0 soit au centre
    indices_positive = t >= 0
    indices_negative = t < 0
    sshift = np.concatenate((s[indices_positive], s[indices_negative]))

    # Calcul de la FFT
    S = np.fft.fft(sshift, n=N)
    S = np.fft.fftshift(S) * dt

    # Calcul des fréquences
    f = np.linspace(-Fe/2, Fe/2, N+1)[:-1]

    return S, f

# # Exemple d'utilisation
# import matplotlib.pyplot as plt
#
# # Générer un signal sinusoidal pour l'exemple
# t = np.linspace(0, 1, 1000)  # Temps
# s = np.sin(2 * np.pi * 10 * t)  # Signal sinusoidal à 10 Hz
#
# # Calcul de la transformée de Fourier
# S, f = TransFourier(s, t)
#
# # Affichage des résultats avec Plotly
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=f, y=np.abs(S), mode='lines', name='Module de S(f)'))
# fig.update_layout(title='Transformée de Fourier d\'un Signal',
#                   xaxis_title='Fréquence (Hz)',
#                   yaxis_title='Module de S(f)')
# pio.show(fig)
import numpy as np
import scipy.fftpack as fftpack


def TransFourierInv(S, f=None):
    """
    Transformée de Fourier inverse d'un signal S.

    Parameters
    ----------
    S : array_like
        Vecteur de taille N contenant les coefficients de la transformée de Fourier S.
    f : array_like, optional
        Vecteur de taille N contenant les fréquences correspondant aux coefficients de S : S[n] = S(f[n]).
        Le vecteur `f` doit être symétrique autour de f=0: f = [-fmax, -fmax+df, ..., 0, ..., fmax-df].

    Returns
    -------
    s : numpy.ndarray
        Vecteur de taille N contenant les N échantillons s[n] de la transformée de Fourier inverse de S.
    t : numpy.ndarray
        Vecteur de taille N contenant les instants d'échantillonnage de s.
        s[n] = s(t[n]).

    Raises
    ------
    ValueError
        Si les vecteurs `S` et `f` n'ont pas la même longueur.
        Si `f` n'est pas linéairement croissant avec un pas constant.
        Si le vecteur `f` n'est pas symétrique autour de 0.
    """
    S = np.asarray(S).flatten()
    M = len(S)

    if f is None:
        f = np.arange(-M/2, M/2)
    else:
        f = np.asarray(f).flatten()

    if M != len(f):
        raise ValueError('Les vecteurs "S" et "f" doivent être de même longueur.')

    if not np.allclose(np.diff(f), f[1] - f[0], atol=1e-12, rtol=0):
        raise ValueError('Le vecteur "f" doit être linéairement croissant avec un pas constant.')

    df = f[1] - f[0]
    Fe = 2 * abs(np.min(f))  # Assuming f is symmetric around 0

    if not np.allclose(f[0] + (f[-1] + df), 0, atol=1e-12):
        raise ValueError('Le vecteur "f" doit être symétrique autour de f=0.')

    # Décaler les coefficients pour la FFT inverse
    Sshift = np.concatenate((S[f >= 0], S[f < 0]))
    Sshift = Sshift * Fe

    # Calcul de l'IFFT
    s = np.fft.ifft(Sshift, n=M)
    s = np.fft.fftshift(s)

    # Générer le vecteur d'instants t
    t = np.arange(-M/2, M/2) / Fe

    return s, t


# # Exemple d'utilisation
# import matplotlib.pyplot as plt
#
# # Générer un signal à partir de sa transformée de Fourier
# f = np.linspace(-10, 10, 1000)  # Fréquences
# S = np.sinc(f)  # Transformée de Fourier du signal sinc
#
# # Reconstruction du signal dans le domaine temporel
# s, t = TransFourierInv(S, f)
#
# # Affichage des résultats avec Plotly
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=t, y=np.real(s), mode='lines', name='Reconstruction du signal'))
#
# fig.update_layout(title='Reconstruction de Signal à partir de Transformée de Fourier',
#                   xaxis_title='Temps',
#                   yaxis_title='Amplitude')
#
# pio.show(fig)

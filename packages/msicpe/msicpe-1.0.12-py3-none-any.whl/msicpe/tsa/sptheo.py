import numpy as np
import scipy.signal as signal
import scipy.fftpack as fftpack
from scipy.io import loadmat
import os
LPbutt = os.path.join(os.path.dirname(__file__), 'LPbutt.mat')

def nextpow2(n):
    return np.ceil(np.log2(np.abs(n))).astype('long')

def sptheo(Q, method, fenetre=None):
    """
    Calcule dans le cadre du TP Estimation spectrale :

    - Gth : la valeur en dB de la DSPM du bruit blanc filtré entre 0 et 0,5.
    - Gbiais : la valeur en dB de Gth convolué par la grandeur régissant le biais attaché à la 'method'.
    - f : un vecteur fréquence réduite de même taille que Gth et Gbiais.

    Parameters
    ----------
    Q : int
        Pour 'simple', représente la longueur de l'échantillon analysé.
        Pour 'moyenne' ou 'welch', représente la longueur d'une tranche.

    method : {'simple', 'moyenne', 'welch'}
        Méthode d'estimation spectrale à utiliser.

    fenetre : str, optional
        Nom de la fenêtre à utiliser si method='welch'. Ignoré pour 'simple' et 'moyenne'.

    Returns
    -------
    Gth : ndarray
        Valeur en dB de la DSPM du bruit blanc filtré entre 0 et 0,5.

    Gbiais : ndarray
        Valeur en dB de Gth convolué par la grandeur régissant le biais.

    f : ndarray
        Vecteur fréquence réduite.

    Notes
    -----
    Cette fonction calcule différentes valeurs théoriques dans le cadre de l'estimation spectrale,
    en fonction de la méthode choisie ('simple', 'moyenne' ou 'welch') et des paramètres associés.

    Example
    -------
    >>> from msicpe.tsa import sptheo
    >>> sptheo(1024, 'welch', 'hamming')
    """
    # Coefficients du filtre
    data = loadmat(LPbutt)
    b = data['b'].flatten()
    a = data['a'].flatten()
    if method in ['simple', 'moyenne']:
        # Dans le cas 'simple' et 'moyenne', tranches de longueur Q
        LBart = 2 * Q - 1
        fenetre = 'bartlett'
        # Recherche de la puissance de 2 supérieure à la taille de la fenêtre
        np2 = nextpow2(LBart)
        ntfr = 2 ** np2
        # Spectre théorique complet entre 0 et 0.5
        fth, H = signal.freqz(b, a, worN=ntfr // 2, fs=1)
        H2 = np.abs(H) ** 2
        Gth = 10 * np.log10(H2)
        # Élaboration du vecteur de la DSPM entre 0 et 1
        spth = np.concatenate([H2, [0], np.flipud(H2[1:ntfr // 2])])
        # Calcul de son antécédent en temps
        tspth = np.real(fftpack.ifft(spth))
        # Calcul de la fenêtre paire de Bartlett
        wQ = signal.get_window(fenetre, LBart, False)
        # Positionnement correct entre t=0 et
        wBQ = np.concatenate([wQ[Q-1:], np.zeros(ntfr - LBart), wQ[:Q-1]])
        # Multiplication des deux séquences en temps
        z = tspth * wBQ
        # Retour en fréquence entre 0 et 1
        Gbiais = np.real(fftpack.fft(z))
        # Limitation entre 0 et 0,5 et mise en dB
        Gbiais = 10 * np.log10(Gbiais[:len(Gbiais) // 2])
    elif method == 'welch':
        Lf = Q
        # Recherche de la puissance de 2 supérieure à la taille de la fenêtre
        np2 = nextpow2(Lf)
        nfft = 2 ** np2
        fth, h = signal.freqz(b, a, nfft, fs=1)
        mag2 = np.abs(h) ** 2
        Gth = 10 * np.log10(mag2)
        # Calcul du spectre théorique biaisé
        spth = np.concatenate([mag2, [0], np.flipud(mag2[1:nfft])])
        tspth = np.real(fftpack.ifft(spth))  # Son antécédent en temps
        # Calcul de la fenêtre
        wf = signal.get_window(fenetre, Lf,False)
        # Calcul de la TF de la fenêtre
        Hf = fftpack.fft(wf, 2 * nfft)
        P = (np.abs(Hf) ** 2) / np.sum(wf ** 2)
        p = fftpack.ifft(P)
        # Multiplication des deux séquences en temps
        z = tspth * np.real(p)
        # Retour en fréquence
        spconv = np.real(fftpack.fft(z))
        Gbiais = 10 * np.log10(spconv[:len(spconv) // 2])

    return Gth, Gbiais, fth


#
# # Exemple d'utilisation
# Q = 1000
# method = 'welch'
# fenetre = 'hann'
#
# Gth, Gbiais, fth = sptheo(Q, method, fenetre)
# #Q = 1000
# method = 'welch'
# fenetre = 'hann'
#
# Gth, Gbiais, fth = sptheo(Q, method, fenetre)
# #
# # Plotting the results using Plotly
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=fth, y=Gth, mode='lines', name='Gth'))
# fig.add_trace(go.Scatter(x=fth, y=Gbiais, mode='lines', name='Gbiais'))
# fig.update_layout(title='Spectral Analysis',
#                   xaxis_title='Frequency (Hz)',
#                   yaxis_title='Magnitude (dB)')
# pio.show(fig)

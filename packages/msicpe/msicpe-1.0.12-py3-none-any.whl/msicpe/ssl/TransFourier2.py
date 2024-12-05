import numpy as np

def TransFourier2(s, t=None, fmax=None):
    """
    Calcul de la transformée de Fourier d'un signal s sur un intervalle de fréquences spécifié.

    Parameters
    ----------
    s : array_like
        Vecteur de taille N contenant les N échantillons s[n] du signal à analyser.
    t : array_like, optional
        Vecteur de taille N contenant les instants d'échantillonnage de s.
        Par défaut, t = [0, 1, 2, ..., N-1].
    fmax : float, optional
        Fréquence maximale pour la transformée de Fourier. Peut être supérieure à Fe/2.

    Returns
    -------
    S : numpy.ndarray
        Vecteur de taille N contenant les coefficients de la transformée de Fourier du signal s sur l'intervalle spécifié.
    f : numpy.ndarray
        Vecteur de taille N contenant les fréquences correspondant aux coefficients de S : S[n] = S(f[n]).

    Raises
    ------
    ValueError
        Si `t` n'est pas linéairement croissant avec un pas constant.
    """
    
    s = s.flatten()


    N = len(s)

    if np.std(np.diff(t)) > 1000 * np.finfo(float).eps:
        raise ValueError('The vector "t" must be linearly increasing with a constant step')

    dt=t[1]-t[0]
    Fe=1/dt
    sshift=np.concatenate((s[t>=0],s[t<0]))
    M=N
    S=np.fft.fft(sshift,M)
    S=np.fft.fftshift(S)
    S=S*dt
    f=np.linspace(-Fe/2,Fe/2,M+1)
    f=f[:-1]

    if 'fmax' in locals():
        f = np.arange(-fmax, fmax, Fe / M)  # Generate frequency range from -fmax to fmax-Fe/M
        f2 = np.mod(f + Fe / 2, Fe)         # Map frequencies into the range [0, Fe)
        indices = np.floor(f2 / (Fe / M)).astype(int)  # Compute indices for re-sampling
        S2 = S[indices]                     # Re-sample the spectrum
        S = S2    

    return S, f
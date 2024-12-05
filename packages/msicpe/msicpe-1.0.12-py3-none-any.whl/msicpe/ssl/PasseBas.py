import numpy as np
from scipy.signal import butter, lfilter

def PasseBas(z, Fe, Fc, ordre=9):
    """
    Applique un filtre passe-bas Butterworth d'ordre spécifié à un signal.

    Parameters
    ----------
    z : array_like
        Vecteur contenant les échantillons du signal à filtrer.
    Fe : float
        Fréquence d'échantillonnage du signal en Hz.
    Fc : float
        Fréquence de coupure du filtre passe-bas en Hz.
    ordre : int, optional
        Ordre du filtre Butterworth. Par défaut, ordre=9.

    Returns
    -------
    s : numpy.ndarray
        Signal filtré.

    Raises
    ------
    ValueError
        Si les fréquences de coupure ne sont pas dans la plage valide.
    """
    # Vérifications des entrées
    if Fc <= 0 or Fc >= Fe / 2:
        raise ValueError('La fréquence de coupure Fc doit être comprise entre 0 et Fe/2.')

    if ordre <= 0:
        raise ValueError('L\'ordre du filtre doit être un entier positif.')

    # Calcul de la fréquence de coupure normalisée
    Wc = 2 * Fc / Fe

    # Conception du filtre Butterworth
    B, A = butter(ordre, Wc, btype='low', analog=False)

    # Application du filtre avec filtrage sans décalage de phase
    s = lfilter(B, A, z)

    return s

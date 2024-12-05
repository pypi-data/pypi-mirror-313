import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

def FilTel(x, fs):
    """
    Filtrage d'un signal dans la bande téléphonique (300-3400 Hz).
    
    Parameters
    ----------
    x : array_like
        Vecteur contenant le signal d'entrée.
    fs : float
        Fréquence d'échantillonnage du signal en Hz.
    
    Returns
    -------
    y : numpy.ndarray
        Signal filtré dans la bande 300-3400 Hz.
    
    Raises
    ------
    ValueError
        Si les fréquences de coupure ne sont pas dans la plage valide.
    """
    # Fréquences de coupure pour la bande téléphonique
    Fc_low = 300   # Hz
    Fc_high = 3400 # Hz
    ordre = 6      # Ordre du filtre (3 pour chaque section, total 6)

    # Vérifications des entrées
    if Fc_low <= 0 or Fc_high >= fs / 2:
        raise ValueError("Les fréquences de coupure doivent être comprises entre 0 et fs/2.")
    if Fc_low >= Fc_high:
        raise ValueError("La fréquence de coupure basse Fc_low doit être inférieure à Fc_high.")
    if ordre <= 0:
        raise ValueError("L'ordre du filtre doit être un entier positif.")
    if not isinstance(ordre, int):
        raise ValueError("L'ordre du filtre doit être un entier.")

    # Calcul des fréquences de coupure normalisées
    Wc_low = Fc_low / (fs / 2)   # Normalisation par Nyquist
    Wc_high = Fc_high / (fs / 2)

    # Conception du filtre passe-bande Butterworth
    B, A = butter(ordre, [Wc_low, Wc_high], btype='band')

    # Application du filtre avec filtrage sans décalage de phase
    y = filtfilt(B, A, x)

    return y
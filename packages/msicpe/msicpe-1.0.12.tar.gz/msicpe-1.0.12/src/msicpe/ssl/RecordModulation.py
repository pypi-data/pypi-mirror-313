import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt



def RecordModulation(Fe, T=5):
    """
    Enregistre un message audio, le visualise et permet de le sauvegarder au format .wav.

    Parameters
    ----------
    Fe : int
        Fréquence d'échantillonnage (doit être un multiple de 8000 Hz et ≤ 96000 Hz).
    T : float, optional
        Durée de l'enregistrement en secondes. Par défaut, T=5.

    Returns
    -------
    nomfic : str or None
        Nom du fichier .wav dans lequel le message a été enregistré. Retourne `None` si non sauvegardé.
    Signal : numpy.ndarray
        Tableau contenant les échantillons du message enregistré.
    t : numpy.ndarray
        Vecteur temporel correspondant au tableau Signal.
    """
    # Vérifications des entrées
    if Fe % 8000 != 0:
        raise ValueError('La fréquence d\'échantillonnage Fe doit être un multiple de 8000 Hz.')
    if not (8000 <= Fe <= 96000):
        raise ValueError('La fréquence d\'échantillonnage Fe doit être ≤ 96000 Hz.')

    bits = 16
    channels = 1  # Mono

    nomfic = None  # Initialisation du nom de fichier

    while True:
        print('------  Parlez !!!  ------')
        try:
            # Enregistrement audio
            Signal = sd.rec(int(T * Fe), samplerate=Fe, channels=channels, dtype='int16')
            sd.wait()  # Attendre la fin de l'enregistrement
            print('------  STOP !!!  ------')

            # Lecture de l'enregistrement
            print('Lecture de l\'enregistrement...')
            sd.play(Signal, Fe)
            sd.wait()  # Attendre la fin de la lecture

            # Conversion des données en float
            Signal = Signal.flatten().astype(np.float32)
            Signal_normalized = Signal / np.max(np.abs(Signal))  # Normalisation pour l'affichage

            # Création du vecteur temporel
            N = len(Signal)
            t = np.linspace(0, T, N, endpoint=False)

            # Affichage du signal
            plt.figure(figsize=(12, 6))
            plt.plot(t, Signal_normalized)
            plt.title('Signal Enregistré')
            plt.xlabel('Temps (s)')
            plt.ylabel('Amplitude Normalisée')
            plt.grid(True)
            plt.show()

            # Demander à l'utilisateur s'il souhaite sauvegarder
            save_input = input('Sauvegarder dans un fichier ? oui=1 non=0 : ').strip()
            if save_input == '1':
                nomfic = input('Nom du fichier (sans extension) : ').strip()
                if not nomfic:
                    print('Nom de fichier invalide. Tentative de sauvegarde annulée.')
                else:
                    nomficwav = f"{nomfic}.wav"
                    sf.write(nomficwav, Signal, Fe, subtype='PCM_16')
                    print(f'Enregistrement sauvegardé sous {nomficwav}')
            elif save_input == '0':
                print('Enregistrement non sauvegardé.')
            else:
                print('Entrée invalide. Réessayez.')

            # Sortir de la boucle après une tentative
            break

        except Exception as e:
            print(f'Une erreur est survenue : {e}')
            retry = input('Voulez-vous réessayer ? oui=1 non=0 : ').strip()
            if retry != '1':
                break

    return nomfic, Signal, t

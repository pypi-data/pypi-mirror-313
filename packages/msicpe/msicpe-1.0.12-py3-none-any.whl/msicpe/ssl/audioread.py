import soundfile as sf
import sounddevice as sd

def audioread(file_path, play_audio=False):
    """
    Lit un fichier audio et retourne les échantillons ainsi que la fréquence d'échantillonnage, avec une option pour lire l'audio.
 
    Parameters
    ----------
    file_path : str
        Le chemin d'accès au fichier audio à lire (par exemple 'votre_audio.wav').
       
    play_audio : bool, optional
        Si True, le fichier audio sera joué après sa lecture (par défaut False).
 
    Returns
    -------
    data : numpy.ndarray
        Tableau contenant les échantillons audio. Chaque colonne représente un canal (mono ou stéréo).
       
    sample_rate : int
        Fréquence d'échantillonnage du fichier audio (en Hertz).
 
    Example
    -------
    >>> audio_file_path = 'votre_audio.wav'
    >>> data, fs = audioread_equivalent(audio_file_path, play_audio=True)
    >>> print(f"Sample Rate: {fs} Hz")
    >>> print(f"Audio Data Shape: {data.shape}")
   
    Notes
    -----
    - Cette fonction utilise les bibliothèques `soundfile` et `sounddevice` pour lire et éventuellement jouer le fichier audio.
    - Assurez-vous que les bibliothèques `soundfile` et `sounddevice` sont installées:
      pip install soundfile sounddevice
    """
    # Lire le fichier audio avec la bibliothèque soundfile
    data, sample_rate=sf.read(file_path)
   
    # Si play_audio est True, jouer le fichier audio avec sounddevice
    if play_audio:
        sd.play(data, sample_rate)
        sd.wait()  # Attendre jusqu'à ce que la lecture soit terminée
 
    return data, sample_rate
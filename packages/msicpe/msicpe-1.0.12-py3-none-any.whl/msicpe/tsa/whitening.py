import numpy as np
from scipy.signal.windows import hann

def whitening_old(x, Fs=1, freq=None):
    """
    Cette fonction réalise le blanchiment d'un signal donné,  soit pour toute la plage de 0 à 0.5 (en fréquences réduites), soit pour une bande de fréquence définie par l'utilisateur. 
    
    Parameters
    ----------
        x : numpy array
            Signal d'entrée (doit être un tableau 1D).
        Fs : float
            Fréquence d'échantillonnage (défaut : 1)
        freq : list
            Limite de fréquence pour le blanchiment en Hz (par exemple, None pour une gamme complète ou [0.1, 20]).
             
    Returns
    -------
        x_white : numpy array
            Signal spectralement blanchi.
    """
    if freq is None:
        print("Warning: 'freq' is specified as None. Defaulting to 0 to 0.5 in reduced frequencies.")
        freq = [0, Fs / 2]
    
    L = len(x)
    
    # L-point symmetric Hann window
    W = hann(L)
    
    # Apply Hann window and take FFT
    xf = np.fft.fft(W * x, n=L)
    
    # Magnitude vector
    mag = np.abs(xf)
    
    # Phase vector
    phase = np.unwrap(np.angle(xf))
    
    # Frequency vector
    f = np.linspace(0,L,L) * (Fs / L)
    
    # Find indices corresponding to the specified frequency range
    index_lower = np.argmin(np.abs(f - freq[0]))
    index_upper = np.argmin(np.abs(f - freq[1]))
    print(index_lower,index_upper)
    # Flatten the spectrum within the specified range
    mag[index_lower:index_upper + 1] = 1.0
    
    # Inverse FFT to reconstruct the signal
    x_white = np.fft.irfft(mag * np.exp(1j * phase), n=L)
    
    return x_white

def whitening(x,color):
# passage par un filtre blanchisseur (fonction whiten qu'on leur donne)
    """
    Cette fonction réalise le blanchiment d'un signal donne, sur toute la plage fréquentielle de 0 à 0.5 (en fréquences réduites).
   
    Parameters
    ----------
        x : numpy array
            Signal d'entrée (doit être un tableau 1D).
        color : string
            Couleur du bruit (rouge, rose, blanc, bleu, violet)
             
    Returns
    -------
        x_white : numpy array
            Signal spectralement blanchi.
    """
    freq = np.fft.rfftfreq(len(x))
    one_over_tf_noise = 0
    match color:
        case 'violet':
            one_over_tf_noise = 1/np.where(freq == 0, float('inf'), freq)
        case 'bleu':
            one_over_tf_noise = 1/np.where(freq == 0, float('inf'), np.sqrt(freq))
        case 'rose':
            one_over_tf_noise = np.sqrt(freq)
        case 'rouge':
            one_over_tf_noise = freq
        case 'blanc':
            one_over_tf_noise = np.ones(freq.shape)
            
    # Normalize S -> makes sure that the colored noise will preserve the energy of the white noise.
    # dsp_noise /= np.sqrt(np.mean(dsp_noise)**2)
    one_over_tf_noise /= np.trapz(one_over_tf_noise,dx=freq[1]-freq[0])
    
    tf_x = np.fft.rfft(x,n=len(x))
    
    x_white = np.fft.irfft(tf_x*one_over_tf_noise)
    return x_white


# from transmit import transmit
# import matplotlib.pyplot as plt
# import scipy.signal as signal

# b = transmit(2*np.sin(2*np.pi*1000*np.arange(10000)/4000),11)

# def estimateur_welch(x, window, M, Noverlap, nfft):
#     f, DSPest3 = signal.welch(x, window=signal.get_window(window,M), noverlap=Noverlap, nfft=nfft, return_onesided=True)
#     DSPest3 = 10 * np.log10(DSPest3)
#     return DSPest3,f

# DSP,f=estimateur_welch(b,'hann',1000,500,2048)
# bw2=whiten(b,'violet')
# DSPw2,_=estimateur_welch(bw2,'hann',1000,500,2048)
# plt.figure()
# plt.subplot(3, 1, 1)
# plt.plot(f[1:],DSP[1:])
# plt.title("DSP originale")
# plt.subplot(3, 1, 2)
# plt.plot(f[1:],DSPw[1:])
# plt.title("DSP blanchie spectralement (Matlab)")
# plt.subplot(3, 1, 3)
# plt.plot(f[1:],DSPw2[1:])
# plt.title("DSP blanchie spectralement (*1/DSP bruit)")
# plt.tight_layout()
# plt.show()
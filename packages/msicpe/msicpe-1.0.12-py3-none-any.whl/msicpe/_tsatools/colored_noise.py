import numpy as np
# generate Additive White Noise
# from: https://stackoverflow.com/questions/67085963/generate-colors-of-noise-in-python
# The function PSDGenrator takes as input a function and returns another function that will
# produce a random signal with the power spectrum shaped accordingly to the given function.
def noise_psd(N, psd = lambda f: 1):
        X_white = np.fft.rfft(np.random.randn(N))
        S = psd(np.fft.rfftfreq(N))
        # Normalize S -> makes sure that the colored noise will preserve the energy of the white noise.
        S = S / np.sqrt(np.mean(S**2))
        X_shaped = X_white * S
        return np.fft.irfft(X_shaped)

def PSDGenerator(f):
    return lambda N: noise_psd(N, f)

@PSDGenerator
def white_noise(f):
    return 1

@PSDGenerator
def blue_noise(f):
    return np.sqrt(f)

@PSDGenerator
def violet_noise(f):
    return f

@PSDGenerator
def brownian_noise(f):
    return 1/np.where(f == 0, float('inf'), f)

@PSDGenerator
def pink_noise(f):
    return 1/np.where(f == 0, float('inf'), np.sqrt(f))


###TODO: vu que ça donne les DSP théoriques, il faudrait pouvoir la récuperer qq part


########################################################################################################################
# alternatively: use colorednoise librairy
###!pip install colorednoise
# import colorednoise as cn

# beta = 0         # the exponent: 0=white noite; 1=pink noise;  2=red noise (also "brownian noise")
# samples = 2**16  # number of samples to generate (time series extension)

# colored_noise = cn.powerlaw_psd_gaussian(beta, samples)
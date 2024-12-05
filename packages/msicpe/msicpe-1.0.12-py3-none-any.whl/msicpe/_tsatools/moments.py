import numpy as np
import scipy as sci


def getMoments(x):
    moments = dict()
    moments["mean"] = np.mean(x)
    moments["std"] = np.std(x)
    moments["pow"] = moments["std"] ** 2

    return moments


# Rk: numpy.correlate may perform slowly in large arrays
# (i.e. n = 1e5) because it does not use the FFT to
# compute the convolution; in that case,
# scipy.signal.correlate might be preferable.

def xcorr(x, sampling_rate):
    N = len(x)
    lags = np.arange(-N + 1, N)
    if N < 1e5:
        gamma_x = np.correlate(x, x, mode='full')
    else:
        gamma_x = sci.signal.correlate(x, x, mode='full')

    return gamma_x / sampling_rate, lags / sampling_rate


def intercorr(x, y, sampling_rate):
    N = len(x)
    lags = np.arange(-N + 1, N)
    if N < 1e5:
        gamma_xy = np.correlate(x, x, mode='full')
    else:
        gamma_xy = sci.signal.correlate(x, x, mode='full')

    return gamma_xy / sampling_rate, lags / sampling_rate
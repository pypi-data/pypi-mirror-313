import scipy as sci
# PSD estimators
def estimatePSD_simple(x,fs, nfft=None):
    f, psd = sci.signal.welch(x, fs, window='boxcar', nperseg=len(x), noverlap=0, nfft=nfft)
    return f,psd

def estimatePSD_moyenne(x,fs, nperseg=None, nfft=None):
    f, psd = sci.signal.welch(x, fs, window='boxcar', nperseg=nperseg, noverlap=0, nfft=nfft)
    return f,psd

def estimatePSD_welch(x,fs, window='hann', nperseg=None, noverlap=None, nfft=None):
    f, psd = sci.signal.welch(x, fs, window=window, nperseg=nperseg, noverlap=noverlap, nfft=nfft)
    return f, psd
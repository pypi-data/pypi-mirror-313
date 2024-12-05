import numpy as np
import scipy.signal as signal
import plotly.graph_objects as go
from .tracord import tracord


def detsin(M, ssb):
    """
    Détection d'un signal périodique dans un bruit.

    Le signal est un signal sinusoïdal de fréquence 227 Hz à phase équipartie.
    Le bruit est un bruit blanc gaussien centré, filtré dans la bande 150-300 Hz.
    On dispose d'un signal de référence périodique de même période que le signal.

    Le tout est échantillonné à 1 KHz.

    Parameters
    ----------
        M : int
            Nombre de points à analyser (> 100).
        ssb : float
            Rapport signal sur bruit en dB (< 20 dB).

    Affiche
    -------
        - Le mélange signal + bruit.
        - Le signal de référence.
        - L'autocorrélation estimée du mélange signal + bruit.
        - L'intercorrélation estimée entre signal + bruit et la référence.

    Notes
    -----
    Cette fonction est conçue pour détecter un signal sinusoïdal périodique dans un environnement de bruit,
    en utilisant un signal de référence pour comparer et extraire le signal d'intérêt.

    Example
    -------
    >>> from msicpe.tsa import detsin
    >>> detsin(1000, 15)
    """
    nue = 1000  # Hz
    if -20 <= ssb <= 20 and M > 100:
        # Synthesis of the filter
        b, a = signal.butter(8, [0.15 * 2, 0.3 * 2], btype='bandpass')
        L = 2 ** np.ceil(np.log2(2 * M - 1))

        # Generation of the signal with equal phase distribution
        phi = np.random.rand()
        sig = np.sin(2 * np.pi * 0.227 * np.arange(M) + np.pi * phi)

        # Generation of the reference signal
        ref = np.sin(2 * np.pi * 0.227 * np.arange(M))

        # Generation of white noise with unit variance
        br = np.random.randn(M + 150)

        # Filtering the white noise
        brf = signal.lfilter(b, a, br)

        # Removing 150 points due to the transient response of the filter
        br = brf[150:M + 150]
        sb = np.std(br)
        ss = np.std(sig)
        ssth = sb * (10 ** (ssb / 20))
        gain = ssth / ss
        bseul = br / gain
        mbs = sig + br / gain
        ormin, ormax = tracord(mbs)

        abstrace = np.arange(M)  # gives a trace in ms
        labelx = 'milliseconds'
        limx = [0, M - 1]

        if M > 10000:
            abstrace = abstrace / nue
            labelx = 'seconds'
            limx = [0, (M - 1) / nue]

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=abstrace, y=bseul, mode='lines', name='Signal Absent'))
        fig1.update_layout(
            title='Received Signal - SIGNAL ABSENT',
            xaxis=dict(title=labelx, range=limx),
            yaxis=dict(range=[ormin, ormax])
        )

        fig1.add_trace(go.Scatter(x=abstrace, y=mbs, mode='lines', name='Signal Present'))
        fig1.update_layout(
            title=f'Received Signal - SIGNAL PRESENT with (S/B) = {ssb} dB',
            xaxis=dict(title=labelx, range=limx),
            yaxis=dict(range=[ormin, ormax])
        )

        tau = np.arange(-100, 101)
        cseul = np.correlate(bseul, bseul, 'full') / M
        icseul = np.correlate(bseul, ref, 'full') / M
        c = np.correlate(mbs, mbs, 'full') / M
        ic = np.correlate(mbs, ref, 'full') / M
        minc, maxc = tracord(c)
        minicseul, maxicseul = tracord(icseul)
        minic, maxic = tracord(ic)
        a = max(maxic, maxicseul)
        b = min(minic, minicseul)

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=tau, y=cseul[M - 100:M + 101], mode='lines', name='Autocorrelation Signal Absent'))
        fig2.update_layout(
            title='Estimated Autocorrelation of Received Signal - SIGNAL ABSENT',
            xaxis=dict(title='Delays in milliseconds', range=[tau[0], tau[-1]]),
            yaxis=dict(range=[minc, maxc])
        )

        fig2.add_trace(go.Scatter(x=tau, y=c[M - 100:M + 101], mode='lines', name='Autocorrelation Signal Present'))
        fig2.update_layout(
            title=f'Autocorrelation - SIGNAL PRESENT - (S/B) = {ssb} dB - Signal Duration {M - 1} ms',
            xaxis=dict(title='Delays in milliseconds', range=[tau[0], tau[-1]]),
            yaxis=dict(range=[minc, maxc])
        )

        fig2.add_trace(
            go.Scatter(x=tau, y=icseul[M - 100:M + 101], mode='lines', name='Intercorrelation Signal Absent'))
        fig2.update_layout(
            title='Estimated Intercorrelation between Received Signal and Reference - SIGNAL ABSENT',
            xaxis=dict(title='Delays in milliseconds', range=[tau[0], tau[-1]]),
            yaxis=dict(range=[b, a])
        )

        fig2.add_trace(go.Scatter(x=tau, y=ic[M - 100:M + 101], mode='lines', name='Intercorrelation Signal Present'))
        fig2.update_layout(
            title='Estimated Intercorrelation - SIGNAL PRESENT',
            xaxis=dict(title='Delays in milliseconds', range=[tau[0], tau[-1]]),
            yaxis=dict(range=[b, a])
        )

        fig1.show()
        fig2.show()

    elif ssb > 20:
        print('Signal-to-noise ratio too high')
    elif ssb < -20:
        print('Signal-to-noise ratio too low')
    elif M <= 100:
        print('Duration too short: must be greater than 100 samples')

# Example usage
# detsin(1000, 10) # M=1000 points, ssb=10 dB
import numpy as np
import plotly.graph_objects as go
from scipy.signal import square
import scipy.stats as stats


def carbr(moy, ecartype, N):
    """
    Estime la densité de probabilité de la somme d'un signal carré de fréquence 110 Hz
    et d'un bruit blanc gaussien, échantillonné à 100 KHz.

    Parameters
    ----------
        moy : float
            Moyenne du bruit.
        ecartype : float
            Écart-type du bruit.
        N : int
            Nombre de points du signal à analyser.


    Affiche le mélange signal + bruit et la densité de probabilité estimée.

    Notes
    -----
    Cette fonction estime la densité de probabilité de la somme d'un signal carré et d'un bruit blanc gaussien,
    supposant que le signal carré a une fréquence de 110 Hz et est échantillonné à 100 KHz.

    Example
    -------
    >>> from msicpe.tsa import carbr
    >>> carbr(0, 1, 1000)
    """
    t = np.arange(N)
    x = square(2 * np.pi * 0.0011 * t)

    # Generate Gaussian white noise
    br = np.random.randn(N)
    sig = (br * ecartype) + moy + x

    # Estimate the histogram and the probability density function
    Nbre, bins = np.histogram(sig, bins=30, density=False)
    pas = bins[1] - bins[0]
    ddpest = Nbre / (N * pas)
    bin_centers = 0.5 * (bins[1:] + bins[:-1])

    # Create the time vector in milliseconds
    t_ms = t / 100.0

    # Determine plotting limits
    ormin, ormax = min(sig), max(sig)

    # Plot the mixed signal (signal + noise)
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=t_ms, y=sig, mode='lines', name='Signal + Noise'))
    fig1.update_layout(title=f'Signal carré + bruit - moyenne {moy} écart-type {ecartype}',
                       xaxis_title='millisecondes',
                       yaxis_title='Amplitude',
                       xaxis=dict(range=[0, t_ms[-1]]),
                       yaxis=dict(range=[ormin, ormax]))

    # Plot the estimated probability density function
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=bin_centers, y=ddpest, mode='lines+markers', name='Estimated PDF'))
    fig2.update_layout(title=f'DDP estimée avec {N} points',
                       xaxis_title='Amplitude',
                       yaxis_title='Density',
                       xaxis=dict(range=[bin_centers[0] - pas, bin_centers[-1] + pas]),
                       yaxis=dict(range=[0, 1.1 * max(ddpest)]))

    # Show plots
    fig1.show()
    fig2.show()
    return sig

# Example usage
#carbr(0, 1, 2000)

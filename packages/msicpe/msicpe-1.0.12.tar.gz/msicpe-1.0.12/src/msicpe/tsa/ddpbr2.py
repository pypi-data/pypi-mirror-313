import numpy as np
import scipy.signal as signal
import plotly.graph_objects as go


def ddpbr2(ecartype, N):
    """
    Estimation de la densité de probabilité d'un bruit gaussien élevé au carré,
    de moyenne nulle.

    Parameters
    ----------
        ecartype : float
            Écart-type du bruit.
        N : int
            Nombre de points à générer (doit être supérieur à 500).

    Affiche
    -------
        - 400 points du bruit élevé au carré.
        - La densité de probabilité estimée.
        - La densité de probabilité théorique en fonction de l'écart-type choisi.

    Notes
    -----
    Cette fonction estime la densité de probabilité d'un bruit gaussien élevé au carré,
    supposant que le bruit initial a une bande passante de 2000 Hz et est échantillonné à 10 KHz.

    Example
    -------
    >>> from msicpe.tsa import ddpbr2
    >>> ddpbr2(1, 1000)
    """
    if N < 500:
        print('Nombre de points trop faible')
        return

    # Generation of Gaussian noise
    br0 = np.random.randn(N)

    # Filter design
    wp = 2 * 0.2
    ws = 2 * 0.25
    ord, wn = signal.buttord(wp, ws, 1, 40)
    b, a = signal.butter(ord, wn)

    # Filtering the noise
    br1 = signal.lfilter(b, a, br0)
    br = br1 * ecartype / np.sqrt(2 * 0.2)
    br2 = br ** 2

    # Histogram calculation
    pas = ((3 * ecartype) ** 2) / 50
    x = np.arange(0, 51 * pas, pas)
    Nbre, _ = np.histogram(br2, bins=x)

    t = np.arange(400) / 10
    br2_segment = br2[100:500]

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=t, y=br2_segment[:400], mode='lines', name='Squared Gaussian Noise'))
    fig1.update_layout(
        title=f'400 points de bruit gaussien élevé au carré de moyenne 0 et d\'écart-type {ecartype}',
        xaxis=dict(title='Millisecondes', range=[0, t[-1]]),
        yaxis=dict(range=[0, 1.1 * np.max(br2_segment)])
    )

    ddpest = Nbre / N / pas
    z = np.arange(pas / 2, 51 * pas, pas / 2)
    ecarg = ecartype
    g = np.exp(-z / (2 * ecarg * ecarg)) / np.sqrt(2 * np.pi * z) / ecarg

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=x[:-1], y=ddpest, mode='markers', name='Estimated PDF'))
    fig2.add_trace(go.Scatter(x=z, y=g, mode='lines', name='Theoretical PDF', line=dict(color='cyan')))
    fig2.update_layout(
        title=f'DDP estimée avec {N} points et DDP théorique',
        xaxis=dict(title='Amplitude', range=[x[0] - pas, x[-1]]),
        yaxis=dict(range=[0, 1.1 * np.max(ddpest)])
    )

    fig1.show()
    fig2.show()


# Example usage
#ddpbr2(1, 3000)  # e.g., ecartype=1, N=3000
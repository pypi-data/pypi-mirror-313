import numpy as np
import scipy.signal as signal
import plotly.graph_objects as go
from .tracord import tracord
def ddpbr2f(ecartype, N):
    """
    Estimation de la densité de probabilité d'un bruit gaussien de moyenne nulle,
    élevé au carré et filtré passe-bas.

    Parameters
    ----------
        ecartype : float
            Écart-type du bruit.
        N : int
            Nombre de points à générer (doit être supérieur à 2500).

    Le bruit de départ a une bande passante de 2000 Hz et est échantillonné à 10 KHz.

    Pendant l'exécution du programme, la fréquence de coupure du filtre passe-bas est choisie.

    Affiche
    -------
        - 400 points du bruit initial.
        - 400 points du bruit élevé au carré.
        - La densité spectrale du bruit élevé au carré.
        - Le gain complexe du filtre passe-bas choisi.
        - Le bruit élevé au carré filtré passe-bas.
        - La densité de probabilité estimée du bruit élevé au carré filtré.

    Notes
    -----
    Cette fonction estime la densité de probabilité d'un bruit gaussien élevé au carré,
    filtré par un filtre passe-bas.

    Example
    -------
    >>> from msicpe.tsa import ddpbr2f
    >>> ddpbr2f(1, 3000)
    """
    if N < 2500:
        print('Nombre de points trop faible : il faut plus de 2500 points')
        return

    fe = 1e4  # Sampling frequency
    Nplus = 1000  # Number of points to add for steady state
    br0 = np.random.randn(N + Nplus)

    # Filtering the noise for a given band (2000 Hz for noise sampled at 10 KHz)
    b, a = signal.butter(12, 2 * 0.20)
    br1 = signal.lfilter(b, a, br0)
    br = br1 * ecartype / np.sqrt(2 * 0.20)

    # Displaying 400 points of noise and its squared version
    t = np.arange(400) / fe
    br2 = br ** 2

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=t, y=br[Nplus:Nplus + 400], mode='lines', name='Gaussian Noise'))
    fig1.update_layout(
        title=f'400 pts de bruit gaussien centré de bande 2000 Hz d\'écart-type {ecartype}',
        xaxis=dict(title='Seconds', range=[0, t[-1]]),
        yaxis=dict(range=[np.min(br), np.max(br)])
    )

    fig1.add_trace(go.Scatter(x=t, y=br2[Nplus:Nplus + 400], mode='lines', name='Squared Noise'))
    fig1.update_layout(
        title='Le même bruit élevé au carré',
        xaxis=dict(title='Seconds', range=[0, t[-1]]),
        yaxis=dict(range=[np.min(br2), np.max(br2)])
    )

    fig1.show()

    while True:
        chnup = input(
            "Fréquence de coupure du filtre intégrateur (1: 1000 Hz, 2: 500 Hz, 3: 200 Hz, 4: 50 Hz, 5: fin): ")

        if chnup == '1':
            fp = 1000 / fe  # Cutoff frequency
            fs = 1700 / fe  # Band limit
            orpb = 9  # Filter order
        elif chnup == '2':
            fp = 500 / fe
            fs = 900 / fe
            orpb = 9
        elif chnup == '3':
            fp = 200 / fe
            fs = 360 / fe
            orpb = 9
        elif chnup == '4':
            fp = 50 / fe
            fs = 100 / fe
            orpb = 8
        elif chnup == '5':
            break
        else:
            continue

        # Spectral density of squared noise
        # Assuming `dsp.mat` content is loaded as `nu` and `sp`
        # In actual implementation, load `nu` and `sp` from a .mat file using scipy.io.loadmat

        # Placeholder for actual data
        nu = np.linspace(0, fe / 2, 32818)
        sp = np.random.rand(32818)  # Random data for spectral density

        sp2 = sp * (ecartype ** 4)

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=nu, y=sp2, mode='lines', name='Spectral Density'))
        fig2.update_layout(
            title=f'Densité spectrale du bruit d\'écart-type {ecartype} élevé au carré',
            xaxis=dict(title='Hz', range=[0, nu[-1]]),
            yaxis=dict(range=[0, 1.1 * np.max(sp2)])
        )

        bb, ab = signal.butter(orpb, 2 * fp)
        w, hpb = signal.freqz(bb, ab, 256, fe)

        fig2.add_trace(go.Scatter(x=w, y=np.abs(hpb), mode='lines', name='|H(nu)|'))
        fig2.update_layout(
            title=f'|H(nu)| fréquence de coupure {fp * fe} Hz',
            xaxis=dict(title='Hz', range=[0, w[-1]]),
            yaxis=dict(range=[0, 1.1 * np.max(np.abs(hpb))])
        )

        fig2.show()

        brf = signal.lfilter(bb, ab, br2)
        y = brf[Nplus:N + Nplus]
        lg = len(y)

        fig1.add_trace(go.Scatter(x=t, y=y[:400], mode='lines', name='Filtered Squared Noise'))
        ormin, ormax = tracord(y)
        fig1.update_layout(
            title=f'Bruit élevé au carré filtré passe-bas à {fp * fe} Hz',
            xaxis=dict(title='Seconds', range=[0, t[-1]]),
            yaxis=dict(range=[ormin, ormax])
        )

        fig1.show()

        pas = (np.max(y) - np.min(y)) / 30
        kmin = int(np.floor(np.min(y) / pas)) - 1
        kmax = int(np.ceil(np.max(y) / pas)) + 1
        x_hist = np.arange(kmin, kmax + 1) * pas
        Nbre, _ = np.histogram(y, bins=x_hist)

        ddpest = Nbre / (N * pas)

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=np.arange(lg) / fe, y=y, mode='lines', name='Filtered Squared Noise'))
        fig3.update_layout(
            title=f'(Bruit)² filtré passe-bas à {fp * fe} Hz écart-type du bruit: {ecartype}',
            xaxis=dict(title='Seconds', range=[0, lg / fe]),
            yaxis=dict(range=[ormin, ormax])
        )

        fig3.add_trace(go.Scatter(x=x_hist[:-1], y=ddpest, mode='markers', name='Estimated PDF'))
        fig3.update_layout(
            title=f'DDP estimée avec {N} points',
            xaxis=dict(title='Amplitude', range=[x_hist[0] - pas, x_hist[-1] + pas]),
            yaxis=dict(range=[0, 1.1 * np.max(ddpest)])
        )

        fig3.show()

# Example usage
# ddpbr2f(1, 3000)  # e.g., ecartype=1, N=3000
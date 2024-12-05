import numpy as np
import scipy.signal as signal
import plotly.graph_objs as go
import plotly.io as pio
from scipy.io import loadmat
import os
LPbutt = os.path.join(os.path.dirname(__file__), 'LPbutt.mat')

def canal_test(init=None,filtered=False):
    """
        Modélisation d'un canal de transmission ayant un bruit blanc additif gaussien centré réduit sur une bande passante limitée
         pour un signal nul en entrée.

        Parameters
        ----------
            init : number
                Valeur d'initialisation de la graine aléatoire https://numpy.org/doc/2.0/reference/random/generated/numpy.random.seed.html
            filtered : boolean
                Indique si la sortie brf est filtrée ou non (sortie à ne pas filtrer pour estimer la DDP et sortie a filtrer pour estimer la DSP) 
        Returns
        -------
        brf : ndarray
            Séquence de bruit de 100000 points.

        Notes
        -----
        Ce programme est utilisé pour générer un bruit blanc gaussien centré réduit sur une bande passante limitée.

        Example
        -------
        >>> from msicpe.tsa import canal_test
        >>> canal_test()
        """
    # Génération d'une réalisation de bruit blanc gaussien
    N = 100000
    #print(f"Génération d'une réalisation de bruit blanc gaussien de moyenne nulle et de variance unité de {2 * N} échantillons")

    np.random.seed(init)
    al = np.random.randn(2 * N)
    al = (al - np.mean(al)) / np.std(al)

    # # Affichage de l'histogramme du bruit blanc N(0,1)
    # p, z = np.histogram(al, bins=30)
    # hist_fig = go.Figure(data=[go.Bar(x=z[:-1], y=p)])
    # hist_fig.update_layout(
    #     title=f"Histogramme de la réalisation blanche gaussienne de {2 * N} échantillons",
    #     xaxis_title="Valeur",
    #     yaxis_title="Fréquence"
    # )
    # pio.show(hist_fig)
    # input('Appuyez sur une touche pour continuer...')

    # Filtrage
    #print(f"Filtrage du bruit blanc et affichage de la séquence de {N} échantillons")
    if filtered:
        # Charger les coefficients du filtre Butterworth
        data = loadmat(LPbutt)
        b = data['b'].flatten()
        a = data['a'].flatten()

        fal = signal.lfilter(b, a, al)

        # Extraction des N points
        brf = fal[N // 2:N // 2 + N]
    else:
        brf = al
    # Affichage
    # plot_fig = go.Figure(data=[go.Scatter(x=np.arange(N), y=brf)])
    # plot_fig.update_layout(
    #     title="Le bruit filtré passe-bas à analyser",
    #     xaxis_title="Indices",
    #     yaxis_title="Amplitude"
    # )
    # pio.show(plot_fig)
    # input('Appuyez sur une touche pour terminer...')

    return brf


# Example usage:
# brf = genbrfill()
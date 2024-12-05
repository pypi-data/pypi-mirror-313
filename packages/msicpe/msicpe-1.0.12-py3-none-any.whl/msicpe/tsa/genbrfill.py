import numpy as np
import scipy.signal as signal
import plotly.graph_objs as go
import plotly.io as pio
from scipy.io import loadmat
import os
LPbutt = os.path.join(os.path.dirname(__file__), 'LPbutt.mat')

def genbrfill():
    """
        Génération d'un bruit blanc gaussien centré de variance unitaire, filtré passe-bas de 100000 points.
        Affiche la séquence de bruit générée.

        Returns
        -------
        brf : ndarray
            Séquence de bruit filtré passe-bas de 100000 points.

        Notes
        -----
        Ce programme est utilisé pour générer un bruit blanc gaussien centré, le filtrer avec un filtre passe-bas,
        et afficher la séquence de bruit résultante.

        Example
        -------
        >>> from msicpe.tsa import genbrfill
        >>> genbrfill()
        """
    # Génération d'une réalisation de bruit blanc gaussien
    N = 100000
    print(
        f"Génération d'une réalisation de bruit blanc gaussien de moyenne nulle et de variance unité de {2 * N} échantillons")

    # Initialisation du générateur de bruit gaussien
    init = int(input("Donnez un entier pour initialiser le générateur de bruit blanc gaussien : "))
    np.random.seed(init)
    al = np.random.randn(2 * N)
    al = (al - np.mean(al)) / np.std(al)

    # Affichage de l'histogramme du bruit blanc N(0,1)
    p, z = np.histogram(al, bins=30)
    hist_fig = go.Figure(data=[go.Bar(x=z[:-1], y=p)])
    hist_fig.update_layout(
        title=f"Histogramme de la réalisation blanche gaussienne de {2 * N} échantillons",
        xaxis_title="Valeur",
        yaxis_title="Fréquence"
    )
    pio.show(hist_fig)
    input('Appuyez sur une touche pour continuer...')

    # Filtrage
    print(f"Filtrage du bruit blanc et affichage de la séquence de {N} échantillons")

    # Charger les coefficients du filtre Butterworth
    data = loadmat(LPbutt)
    b = data['b'].flatten()
    a = data['a'].flatten()

    fal = signal.lfilter(b, a, al)

    # Extraction des N points
    brf = fal[N // 2:N // 2 + N]

    # Affichage
    plot_fig = go.Figure(data=[go.Scatter(x=np.arange(N), y=brf)])
    plot_fig.update_layout(
        title="Le bruit filtré passe-bas à analyser",
        xaxis_title="Indices",
        yaxis_title="Amplitude"
    )
    pio.show(plot_fig)
    input('Appuyez sur une touche pour terminer...')

    return brf


# Example usage:
# brf = genbrfill()
import numpy as np
import scipy.signal as signal
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def fenetre(nfen=40):
    """
    Programme fenetre.

    Étude des fenêtres de pondération.

    Ce module permet de :
        - Visualiser l'allure de 6 fenêtres de pondération.
        - Afficher leur spectre en échelle linéaire.
        - Afficher leur spectre en échelle logarithmique.

    Les fenêtres ont une longueur de `nfen` points.

    Parameters
    ----------
    nfen : int
        Longueur des fenêtres à étudier.

    Affiche
    -------
    Les 6 fenêtres de pondération.
    L'autocorrélation de chacune des fenêtre de pondération
    Le spectre de l'autocorrélation de chaque fenêtre en échelle linéaire.
    Le spectre de l'autocorrélation de chaque fenêtre en échelle logarithmique.

    Notes
    -----
    Ce programme est utilisé pour analyser visuellement et spectrale les caractéristiques des fenêtres de pondération,
    souvent utilisées en traitement du signal pour des tâches comme la fenêtrage de signaux temporels.

    Example
    -------
    >>> from msicpe.tsa import fenetre
    >>> fenetre(256)
    """
  # Définir les fenêtres
    w1 = np.ones(nfen)
    w2 = np.bartlett(nfen)
    w3 = np.hanning(nfen)
    w4 = np.hamming(nfen)
    w5 = np.blackman(nfen)
    w6 = signal.windows.gaussian(nfen, std=7)

    windows = [w1, w2, w3, w4, w5, w6]
    windows_autocorr = [signal.correlate(w1,w1,'full','fft'), \
            signal.correlate(w2,w2,'full','fft'),\
            signal.correlate(w3,w3,'full','fft'),\
            signal.correlate(w4,w4,'full','fft'),\
            signal.correlate(w5,w5,'full','fft'),\
            signal.correlate(w6,w6,'full','fft')]
    
    k = np.arange(windows_autocorr[0].size) - windows_autocorr[0].size / 2 + 1 
    
    titles = ['Fenêtre Rectangulaire', 'Fenêtre Triangulaire', 'Fenêtre de Hann',
              'Fenêtre de Hamming', 'Fenêtre de Blackman', 'Fenêtre de Gauss']

    # Analyse fréquentielle
    nfft = 16 * 2 ** int(np.ceil(np.log2(nfen)))
    nfft = 16 * 2 ** int(np.ceil(np.log2(k.size)))
    freqs = np.fft.fftfreq(nfft, d=1)[:1+nfft // 2]

    spectra = []
    for w in windows_autocorr:
        sp = np.abs(np.fft.fft(w, nfft))
        sp = np.concatenate((sp[:1+nfft // 2], sp[:1+nfft // 2]))
        spectra.append(sp)

    colors=[
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
]
    # Créer une figure avec des sous-figures
    fig = make_subplots(rows=1, cols=4,
                        subplot_titles=(
                            'Fenêtres de pondération',
                            'Autocorrélation <br> des fenêtres',
                            'Spectre de l\'autocorrélation <br> en échelle linéaire',
                            'Spectre de l\'autocorrélation <br> en échelle logarithmique'
                        ))

    # Tracer les fenêtres de pondération
    for i, w in enumerate(windows):
        fig.add_trace(go.Scatter(
            x=np.arange(-2, nfen + 2),
            y=np.concatenate(([0, 0], w, [0, 0])),
            mode='lines',
            name=titles[i],
            legendgroup=titles[i],
            line=dict(color=colors[i])
        ), row=1, col=1)
    # Tracer les fenêtres de pondération
    for i, w in enumerate(windows_autocorr):
        fig.add_trace(go.Scatter(
            # x=np.arange(-2, nfen + 2),
            x = k,
            y=w,
            mode='lines',
            name=titles[i],
            legendgroup=titles[i],
            line=dict(color=colors[i]),
            showlegend=False
        ), row=1, col=2)

    # Tracer le spectre en échelle linéaire
    for i, sp in enumerate(spectra):
        fig.add_trace(go.Scatter(
            x=freqs,
            y=sp[:nfft // 2],
            mode='lines',
            name=titles[i],
            legendgroup=titles[i],
            line=dict(color=colors[i]),
            showlegend=False
        ), row=1, col=3)

    # Tracer le spectre en échelle logarithmique
    for i, sp in enumerate(spectra):
        fig.add_trace(go.Scatter(
            x=freqs,
            y=20 * np.log10(sp[:nfft // 2] / np.max(sp)),
            mode='lines',
            name=titles[i],
            legendgroup=titles[i],
            line=dict(color=colors[i]),
            showlegend=False
        ), row=1, col=4)

    # Mise à jour de la mise en page
    fig.update_layout(
        title='Analyse des Fenêtres de Pondération',
        width=1600,
        height=800,
        showlegend=True
    )

    fig.update_xaxes(title_text="Points", row=1, col=1)
    fig.update_yaxes(title_text="Amplitude", row=1, col=1)

    fig.update_xaxes(title_text="Points", row=1, col=2)
    fig.update_yaxes(title_text="Amplitude", row=1, col=2)

    fig.update_xaxes(title_text="Fréquence", row=1, col=3)
    fig.update_yaxes(title_text="Amplitude", row=1, col=3)
    
    fig.update_xaxes(title_text="Fréquence", row=1, col=4)
    fig.update_yaxes(range=[-100,10], row=1, col=4)
    fig.update_yaxes(title_text="Amplitude (dB)", row=1, col=4)
    fig.update_layout(legend=dict(groupclick="togglegroup"))

    fig.show()


# Call the function to visualize the windows
# fenetre(80)

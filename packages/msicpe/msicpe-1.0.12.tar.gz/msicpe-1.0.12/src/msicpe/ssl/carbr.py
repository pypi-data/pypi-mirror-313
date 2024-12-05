import numpy as np
import plotly.graph_objs as go

def carbr(moy, ecartype, N):
    """
    Estime la densité de probabilité de la somme d'un signal carré de fréquence 110 Hz et d'un bruit blanc gaussien.

    Le tout est échantillonné à 100 KHz.

    Parameters
    ----------
    moy : float
        Moyenne du bruit.
    ecartype : float
        Écart-type du bruit.
    N : int
        Nombre de points de signal à analyser.

    Description
    -----------
    Cette fonction affiche le mélange signal + bruit ainsi que la densité de probabilité estimée.
    """
    # Générer le signal carré à 110 Hz échantillonné à 100 kHz
    t = np.arange(0, N) / 100000
    x = np.sign(np.sin(2 * np.pi * 110 * t))

    # Générer le bruit blanc gaussien
    br = np.random.randn(N)

    # Calculer le signal combiné (signal carré + bruit)
    sig = (br * ecartype) + moy + x

    # Estimer la densité de probabilité (ddp)
    Nbre, y = np.histogram(sig, bins=30, density=True)
    pas = y[1] - y[0]
    ddpest = Nbre / pas

    # Calculer les limites pour l'axe y des graphiques
    ormin, ormax = np.min(sig), np.max(sig)

    # Créer les tracés avec Plotly
    fig = go.Figure()

    # Tracer le signal carré + bruit
    fig.add_trace(go.Scatter(
        x=t * 1000, y=sig,
        mode='lines',
        name='Signal carré + bruit',
        line=dict(color='blue', width=1)
    ))

    # Paramètres du premier subplot
    fig.update_layout(
        title=f"Signal carré + bruit - moyenne {moy}, écart-type {ecartype}",
        xaxis=dict(title='millisecondes'),
        yaxis=dict(title='amplitude', range=[ormin, ormax]),
        xaxis2=dict(title='amplitude'),
        yaxis2=dict(title='densité de probabilité estimée', range=[0, 1.1 * np.max(ddpest)]),
        showlegend=False
    )

    # Tracer la densité de probabilité estimée
    fig.add_trace(go.Scatter(
        x=y[:-1], y=ddpest,
        mode='lines',
        name='Densité de probabilité estimée',
        line=dict(color='red', width=1)
    ))

    # Paramètres du second subplot
    fig.update_layout(
        title=f"Densité de probabilité estimée avec {N} points",
        xaxis2=dict(title='amplitude', range=[y[0] - pas, y[-1] + pas]),
        yaxis2=dict(title='densité de probabilité estimée', range=[0, 1.1 * np.max(ddpest)]),
        showlegend=False
    )

    # Afficher la figure
    fig.show()

# Exemple d'utilisation avec des valeurs arbitraires
#carbr(moy=0, ecartype=0.5, N=100000)

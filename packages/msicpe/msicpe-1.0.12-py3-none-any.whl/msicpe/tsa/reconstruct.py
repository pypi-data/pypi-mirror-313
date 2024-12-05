import numpy as np


def reconstruct(sb, Nbits):
    """
    RECONSTRUCT Reconstruction d'un signal à partir d'une séquence binaire.

    Parameters:
    ----------
    sb : array-like
        signal binaire
    Nbits : int
        nombre de bits sur lequel est encodé le signal binaire sb

    Returns:
    ----------
    sr : numpy array
        signal reconstruit
    """
    Nsymb = len(sb) // Nbits
    sc = np.array(sb).reshape((Nsymb, Nbits)).astype(int)
    sc_str = [''.join(map(str, row)) for row in sc]
    sr = np.array([int(b, 2) for b in sc_str])
    return sr

#
# # Exemple d'utilisation
# sb = [1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1]  # Signal binaire
# Nbits = 4  # Nombre de bits
#
# sr = reconstruct(sb, Nbits)
#
# # Affichage des résultats
# import plotly.graph_objs as go
# import plotly.io as pio
#
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=np.arange(len(sr)), y=sr, mode='lines+markers', name='Signal reconstruit'))
#
# fig.update_layout(title='Reconstruction de Signal à partir de Séquence Binaire',
#                   xaxis_title='Indice',
#                   yaxis_title='Valeur')
#
# pio.show(fig)

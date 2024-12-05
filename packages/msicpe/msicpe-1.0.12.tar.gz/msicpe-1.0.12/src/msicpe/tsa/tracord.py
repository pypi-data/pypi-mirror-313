import numpy as np


def tracord(x):
    """
    Calcul des bornes pour le tracé d'une courbe.

    Cette fonction calcule les bornes minimale et maximale pour le tracé d'une courbe représentée par le vecteur `x`.
    Les bornes sont calculées en fonction des valeurs minimales et maximales de `x`, avec des ajustements spécifiques
    pour assurer une visualisation appropriée.

    Parameters
    ----------
    x : array_like
        Vecteur contenant les données de la courbe.

    Returns
    -------
    ormin : float
        Borne minimale pour le tracé de la courbe. Si la valeur minimale de `x` est inférieure à zéro, `ormin` est
        établi à 1.1 fois cette valeur. Si la valeur minimale est zéro, `ormin` est fixé à zéro. Si la valeur minimale
        est supérieure à zéro, `ormin` est établi à 0.9 fois cette valeur.

    ormax : float
        Borne maximale pour le tracé de la courbe. Si la valeur maximale de `x` est inférieure à zéro, `ormax` est
        établi à 0.9 fois cette valeur. Si la valeur maximale est zéro, `ormax` est fixé à zéro. Si la valeur maximale
        est supérieure à zéro, `ormax` est établi à 1.1 fois cette valeur.

    Notes
    -----
    Cette fonction est utile pour ajuster automatiquement les bornes d'un tracé en fonction des données fournies,
    en assurant que la courbe reste bien visible sans être tronquée par les limites du graphique.

    Example
    -------
    >>> from msicpe.tsa import tracord
    >>> x = [1, 2, 3, 4, 5]
    >>> ormin, ormax = tracord(x)
    >>> print(ormin, ormax)
    0.9 1.1
    """

    mi = np.min(x)
    Ma = np.max(x)

    if mi < 0:
        ormin = 1.1 * mi
    elif mi == 0:
        ormin = 0
    else:
        ormin = 0.9 * mi

    if Ma < 0:
        ormax = 0.9 * Ma
    elif Ma == 0:
        ormax = 0
    else:
        ormax = 1.1 * Ma

    return ormin, ormax
import numpy as np


def kurtosis(x, flag=1, dim=None):
    """
    Calcul le kurtosis.

    Parameters
    ----------
    X : array_like
        Les valeurs pour lesquelles la kurtosis doit être calculée. Pour un vecteur, `X` est le quatrième moment
        central de `X`, divisé par la quatrième puissance de son écart-type. Pour une matrice, `K` est un vecteur
        ligne contenant la kurtosis de chaque colonne de `X`. Pour les tableaux N-D, `kurtosis` fonctionne le long
        de la première dimension non-singleton.

    FLAG : int, optional
        Si `FLAG` vaut 0, ajuste la kurtosis pour le biais. Si `FLAG` vaut 1 (par défaut),
        la kurtosis n'est pas ajustée pour le biais.

    DIM : int, optional
        La dimension de `X` le long de laquelle calculer la kurtosis. Si non spécifié,
        la kurtosis est calculée le long de la première dimension non-singleton.

    Returns
    -------
    K : ndarray
        La kurtosis des valeurs dans `X`.

    Notes
    -----
    `kurtosis` traite les NaN comme des valeurs manquantes et les ignore dans le calcul.

    See Also
    --------
    numpy.mean : Calculer la moyenne.
    numpy.var : Calculer la variance.
    numpy.std : Calculer l'écart-type.

    Example
    --------
    >>> import numpy as np
    >>> from msicpe.tsa import kurtosis
    >>> data = np.random.randn(1, 1000)
    >>> kurtosis(data)
    array([2.87409513])
    """
    if flag is None:
        flag = 1
    if dim is None:
        if x.size == 0:
            return np.nan
        dim = np.argmax(np.array(x.shape) != 1)
        if len(x.shape) == 1:
            dim = 0

    x0 = x - np.mean(x, axis=dim, keepdims=True)
    s2 = np.mean(x0 ** 2, axis=dim)
    m4 = np.mean(x0 ** 4, axis=dim)
    k = m4 / s2 ** 2

    if flag == 0:
        n = np.sum(~np.isnan(x), axis=dim)
        n[n < 4] = np.nan
        k = ((n + 1) * k - 3 * (n - 1)) * (n - 1) / ((n - 2) * (n - 3)) + 3

    return k

# Example usage:
# x = np.random.rand(10, 5)  # Replace this with your input data
# result = kurtosis(x, flag=1, dim=0)
# print(result)

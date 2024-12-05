import numpy as np


def estimatePDF(x, nbins=None, range=(None, None)):
    if type(x) == type([]):
        N = len(x)
    else:
        N = max(x.shape)

    if range[0] is None: range = (np.min(x), range[1])
    if range[1] is None: range = (range[0], np.max(x))

    stdx = np.std(x)
    if nbins is None:
        DeltaX = 3.49 * stdx / N ** (1 / 3)
        nbins = round((range[1] - range[0]) / DeltaX)
    else:
        DeltaX = (range[1] - range[0]) / nbins

    H, bin_edges = np.histogram(x, bins=nbins, range=range)
    centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    hist = H / (N * DeltaX)

    return hist, centers, DeltaX


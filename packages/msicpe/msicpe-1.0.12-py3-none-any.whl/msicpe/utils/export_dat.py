import csv
from itertools import cycle, zip_longest

def export_dat(ll, oname, header_list=[], delimiter='\t'):
    """
    Export des éléments de la liste de liste ll au format spécifié dans oname

    Parameters
    ----------
    ll : liste de liste contenant les champs à écrire (attention : ne pas mettre de liste de numpy array)
        Les éléments seront écrits colonne par colonne
    oname : str
        Nom du fichier de sortie
    header_list : liste de str contenant autant d'éléments que ll
        Servira de header à chaque colonne. Défaut : []
    delimiter : str
        Délimiteur entre les colonnes. Défaut : '\t'

    Returns
    -------
    None

    Examples
    --------
    >>> from msicpe.utils import *
    >>> l1 = [1,2,3,4]
    >>> l2 = [1,2,3]
    >>> l3 = np.array([1,2])
    >>> ll = [l1, l2, l3.tolist()]
    >>> export_dat(ll, 'myfile.dat', header_list=['list1','list2','list3'], delimiter='\t'):
    """

    with open(oname,'w') as f:
        writer = csv.writer(f,delimiter ='\t')
        if header_list: #if a header_list is provided
            writer.writerow(header_list)
        for x in zip_longest(*ll):
            writer.writerow(x)
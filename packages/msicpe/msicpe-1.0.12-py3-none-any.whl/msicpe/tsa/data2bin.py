import struct
import numpy as np


def data2bin(s,dtype='int8'):
    """Convert data s of type dtype into binary representation

    Args:
        s (np.array): data 
        dtype (str, optional): datatype. Defaults to 'int8'.
    """
        
    def _binary(num):
        return ''.join('{:0>8b}'.format(c) for c in struct.pack('!i', num))


    def _float_to_bin(value):  # For testing.
        """ Convert float to 32-bit binary string. """
        [d] = struct.unpack("!I", struct.pack("!f", value))
        return '{:032b}'.format(d)
    binary_repr_v=None
    
    if 'int' in dtype:
        # if s.dtype!=np.uint8:
        #     s=np.round((s-np.min(s))*255/(np.max(s)-np.min(s))).astype(np.uint8)
        binary_v = np.vectorize(np.binary_repr)
        return np.array([int(x) for i in binary_v(s.astype(dtype),8) for x in i])
    elif 'float' in dtype:
        binary_repr_v = np.vectorize(_float_to_bin)
        # Conversion de la chaine de caractère (représentation binaire) en suite d'int
        return np.array([int(x) for i in binary_repr_v(s.astype(dtype)) for x in i])
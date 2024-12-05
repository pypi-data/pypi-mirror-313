import struct
import numpy as np
from codecs import decode


def bin2data(sb,dtype='int'):
    """Convert binary data sb into array of type dtype

    Args:
        sb (np.array): binary data 
        dtype (str, optional): datatype. Defaults to 'int'.
    """        
    def _bin_to_float(b):
        """ Convert binary string to a float. """
        if type(b)==str:
            bf = int_to_bytes(int(b, 2), 4)  # 8 bytes needed for IEEE 754 binary64.
            out=struct.unpack('!f', bf)[0]
        elif type(b)==np.ndarray:
            out=np.array([])
            b=b.tolist()
            b=[str(i) for i in b]
            for i in range(0,len(b),32):        
                bf = _int_to_bytes(int(''.join(b[i:i+32]), 2), 4)
                out=np.append(out,struct.unpack('!f', bf)[0])
        return out


    def _int_to_bytes(n, length):  # Helper function
        """ Int/long to byte string.

            Python 3.2+ has a built-in int.to_bytes() method that could be used
            instead, but the following works in earlier versions including 2.x.
        """
        return decode('%%0%dx' % (length << 1) % n, 'hex')[-length:]
    
    if 'int' in dtype:
        if sb.dtype!=np.uint8:
            sb=sb.astype(np.uint8)
        return np.packbits(sb).astype(dtype)
    elif dtype=='float':
        return _bin_to_float(sb.astype(int))
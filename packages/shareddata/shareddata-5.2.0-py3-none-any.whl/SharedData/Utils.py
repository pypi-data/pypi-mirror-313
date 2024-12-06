import pandas as pd
import os
from multiprocessing import resource_tracker

# TODO: CHANGE FIX REGISTER/UNREGISTER TO INCLUDE SEMAPHORES
def remove_shm_from_resource_tracker():
    """Monkey-patch multiprocessing.resource_tracker so SharedMemory won't be tracked

    More details at: https://bugs.python.org/issue38119
    """

    def fix_register(name, rtype):
        if rtype == "shared_memory":
            return
        return resource_tracker._resource_tracker.register(self, name, rtype)
    resource_tracker.register = fix_register

    def fix_unregister(name, rtype):
        if rtype == "shared_memory":
            return
        return resource_tracker._resource_tracker.unregister(self, name, rtype)
    resource_tracker.unregister = fix_unregister

    if "shared_memory" in resource_tracker._CLEANUP_FUNCS:
        del resource_tracker._CLEANUP_FUNCS["shared_memory"]


if os.name == 'posix':
    from cffi import FFI
    # atomic semaphore operation
    ffi = FFI()
    ffi.cdef("""    
    unsigned char long_compare_and_swap(long mem_addr, long seek, long oldvalue, long newvalue);
    """)
    cpp = ffi.verify("""    
    unsigned char long_compare_and_swap(long mem_addr, long seek, long oldvalue, long newvalue) {
        long * mem_ptr = (long *) mem_addr;
        mem_ptr += seek;
        return __sync_bool_compare_and_swap(mem_ptr, oldvalue, newvalue);
    };    
    """)

elif os.name == "nt": 
    import sys
    sys.path.append(os.path.dirname(__file__))   
    import sharedmutexwin as cpp
    


# check if partition is a date
def datetype(x):
    if x == '':
        return ''
    
    if len(x) == 8:
        try:
            pd.to_datetime(x,format='%Y%m%d')
            return 'day'
        except:
            pass

    if len(x) == 6:
        try:                
            pd.to_datetime(x,format='%Y%m')
            return 'month'
        except:
            pass

    if len(x) == 4:
        try:                
            pd.to_datetime(x,format='%Y')
            return 'year'
        except:
            pass

    return ''


from pandas.core.internals import BlockManager, make_block
class BlockManagerUnconsolidated(BlockManager):
    def __init__(self, *args, **kwargs):
        BlockManager.__init__(self, *args, **kwargs)
        self._is_consolidated = False
        self._known_consolidated = False

    def _consolidate_inplace(self): pass
    def _consolidate(self): return self.blocks

import numpy as np
def mmaparray2df(arr, indexcols):
    blocks = []    
    p = 0
    _len = None
    for n in arr.dtype.names[indexcols:]:
        a = arr[n]
        blk = make_block(values=a.reshape((1,len(a))), placement=(p,))
        blocks.append(blk)
        p += 1

    blocks = tuple(blocks)
    columns = pd.Index(arr.dtype.names[indexcols:])
    idxnames = arr.dtype.names[:indexcols]
    idxdtype = [arr.dtype[n] for n in idxnames]
    index = pd.DatetimeIndex(arr['date'])
    if indexcols > 1:
        idxarr = []
        i=0
        for n in idxnames:
            if ('|S' in str(idxdtype[i])):
                decoded = arr[n].astype(str)
                idxarr.append(decoded)
            elif (idxdtype[i] == np.dtype('<M8[ns]')):
                idxarr.append(pd.to_datetime(arr[n]))
            else:
                idxarr.append(arr[n])
            i+=1            
        index = pd.MultiIndex.from_arrays(idxarr,names=idxnames)    
        
    mgr = BlockManagerUnconsolidated(blocks=blocks, axes=[columns, index])
    return pd.DataFrame(mgr, copy=False)

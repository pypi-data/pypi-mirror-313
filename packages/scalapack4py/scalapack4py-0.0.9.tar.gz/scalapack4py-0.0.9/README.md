# Dynamic ScaLAPACK wrapper for Python

Python wrapper for dynamically loaded ScaLAPACK and BLACS libraries

```
from scalapack4py import ScaLAPACK4py, parprint, ordprint
from ctypes import cast, py_object, CDLL, RTLD_GLOBAL

scalapack_lib = CDLL('libscalapack-openmpi.so.2.0', mode=RTLD_GLOBAL)
sl = ScaLAPACK4py(scalapack_lib)


descr = sl.wrap_blacs_desc(descr)
locshape = (descr.locrow, descr.loccol)
data = np.ctypeslib.as_array(data, shape=locshape)
sl.scatter(data_src, descr, data)

```

Or

```
# run as:  mpiexec -n 2 python3 -u test_scatter_complex.py
import numpy as np, os
from mpi4py import MPI
from scalapack4py import ScaLAPACK4py
from ctypes import CDLL, RTLD_GLOBAL, POINTER, c_int, c_double

sl = ScaLAPACK4py(CDLL('libscalapack-openmpi.so.2.0', mode=RTLD_GLOBAL))

n = 5
dtype=np.complex128
a = np.arange(n*n, dtype=dtype).reshape((n,n), order='F') * (MPI.COMM_WORLD.rank+1) if MPI.COMM_WORLD.rank==0 else None

print (a)

MP, NP = 2,1

ctx = sl.make_blacs_context(sl.get_default_system_context(), MP, NP)
descr = sl.make_blacs_desc(ctx, n, n)
print("descr", descr, descr.locrow, descr.loccol)

b = np.zeros((descr.locrow, descr.loccol), dtype=dtype)

sl.scatter_numpy(a, POINTER(c_int)(descr), b.ctypes.data_as(POINTER(c_double)), b.dtype)
print (b)


c = sl.gather_numpy(POINTER(c_int)(descr), b, (n, n))
print (c)

```

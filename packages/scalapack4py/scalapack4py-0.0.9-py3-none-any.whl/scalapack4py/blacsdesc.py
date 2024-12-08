from ctypes import cdll, CDLL, RTLD_LOCAL, Structure
from ctypes import POINTER, byref, c_int, c_int64, c_char, c_bool, c_char_p, c_double, c_void_p, CFUNCTYPE, py_object, cast, byref
import numpy as np
from numpy.ctypeslib import ndpointer


def nullable_ndpointer(*args, **kwargs):
  # solution from here: https://stackoverflow.com/a/37664693/3213940
  # TODO look for this isssue: https://github.com/numpy/numpy/issues/6239
  base = ndpointer(*args, **kwargs)
  def from_param(cls, obj):
    if obj is None:
      return obj
    return base.from_param(obj)
  return type(base.__name__, (base,), {'from_param': classmethod(from_param)})

def ctypes2ndarray(data, shape):
  '''
     Convert ctypes POINTER(c_double) to ndarray of complex128 or float64 
     depending on shape dimensionality, that can be 2 (float64) or 3 (complex128)
  '''
  res = np.ctypeslib.as_array(data, shape=shape)
  if len(shape) == 3:
    res = res.view(np.complex128).reshape((shape[0], shape[1]))

  assert len(res.shape) == 2
  return res


DLEN_ = 9
class blacs_desc(Structure): # https://www.netlib.org/scalapack/slug/node68.html
  _fields_ = [("dtype", c_int),
              ("ctxt", c_int),
              ("m", c_int),
              ("n", c_int),
              ("mb", c_int),
              ("nb", c_int),
              ("rsrc", c_int),
              ("csrc", c_int),
              ("lld", c_int)]
  def __init__(self, lib, blacs_ctx=-1, m=0, n=0, mb=1, nb=1, rsrc=0, csrc=0, lld=None, buf=None):
    super().__init__()
    self.lib = lib
    
    if buf is not None:
      if not hasattr(buf, '__get_index__'):
        buf = np.ctypeslib.as_array(buf, shape=(DLEN_,))
      self.dtype, self.ctxt, self.m, self.n, self.mb, self.nb, self.rsrc, self.csrc, self.lld = (*buf,)
      return # wrapped copy

    if blacs_ctx == -1: # stub for non-participating process
      self.dtype=1
      self.ctxt=blacs_ctx
      self.m = 0
      self.n = 0
      self.mb = 0
      self.nb = 0
      self.rsrc = 0
      self.csrc = 0
      self.lld = 0
      return # default, zero-intitalized

    assert m > 0, m
    assert n > 0, n
    if lld is None: # calc default lld
      nprow, _, myrow, _ = self.lib.blacs_gridinfo(blacs_ctx)
      lld = self.lib.numroc(m, mb, myrow, rsrc, nprow)
      lld = max(1, lld) # ldd is not less than 1

    self.lib.descinit(self, m, n, mb, nb, rsrc, csrc, blacs_ctx, lld)
    
  @property
  def myrow(self):
    _, _, myrow, _ = self.lib.blacs_gridinfo(self.ctxt)
    return myrow

  @property
  def mycol(self):
    _, _, _, mycol = self.lib.blacs_gridinfo(self.ctxt)
    return mycol

  @property
  def nprow(self):
    nprow, _, _, _ = self.lib.blacs_gridinfo(self.ctxt)
    return nprow

  @property
  def npcol(self):
    _, npcol, _, _ = self.lib.blacs_gridinfo(self.ctxt)
    return npcol

  @property
  def is_distributed(self):
    nprow, npcol, _, _ = self.lib.blacs_gridinfo(self.ctxt)
    return (nprow * npcol) > 1

  @property
  def locrow(self):
    nprow, _, myrow, _ = self.lib.blacs_gridinfo(self.ctxt)
    return self.lib.numroc(self.m, self.mb, myrow, self.rsrc, nprow)

  @property
  def loccol(self):
    _, npcol, _, mycol = self.lib.blacs_gridinfo(self.ctxt)
    return self.lib.numroc(self.n, self.nb, mycol, self.csrc, npcol)

  def alloc_zeros(self, dtype):
    res = self.alloc(dtype)
    res[:,:] = 0
    return res
  
  def alloc(self, dtype):
    return np.ndarray(shape=(self.locrow, self.loccol), order='F', dtype=dtype)

  def __repr__(self):
    return f"{self.dtype} {self.ctxt} {self.m} {self.n} {self.mb} {self.nb} {self.rsrc} {self.csrc} {self.lld}"


class ScaLAPACK4py:
  def __init__(self, blacs):
    """
      blacs: Library loaded via CTypes with BLACS and ScaLAPACK functions
    """
    self.blacs = blacs
    blacs.blacs_get_.restype = None
    blacs.blacs_get_.argtypes = [POINTER(c_int), POINTER(c_int), POINTER(c_int)]
    blacs.blacs_gridinit_.restype = None
    blacs.blacs_gridinit_.argtypes = [POINTER(c_int), POINTER(c_char), POINTER(c_int), POINTER(c_int)]
    blacs.blacs_gridexit_.restype = None
    blacs.blacs_gridexit_.argtypes = [POINTER(c_int)]
    blacs.blacs_gridinfo_.restype = None
    blacs.blacs_gridinfo_.argtypes = [POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
    blacs.numroc_.restype = c_int
    blacs.numroc_.argtypes = [POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]

    blacs.descinit_.restype = None
    #descinit_:   DESC, M, N, MB, NB, IRSRC, ICSRC, ICTXT, LLD, INFO
    blacs.descinit_.argtypes = [POINTER(blacs_desc), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)] 

    #EXTERN void pdgemr2d_(int *m , int *n , double *a , int *ia , int *ja , int *desca , double *b , int *ib , int *jb , int *descb , int *ictxt);
    blacs.pdgemr2d_.restype = None
    blacs.pdgemr2d_.argtypes = [POINTER(c_int), POINTER(c_int), 
                                nullable_ndpointer(dtype=np.float64, ndim=2, flags='F_CONTIGUOUS'), POINTER(c_int), POINTER(c_int), POINTER(blacs_desc), 
                                nullable_ndpointer(dtype=np.float64, ndim=2, flags='F_CONTIGUOUS'), POINTER(c_int), POINTER(c_int), POINTER(blacs_desc), 
                                POINTER(c_int)]

    blacs.pzgemr2d_.argtypes = [POINTER(c_int), POINTER(c_int), 
                                nullable_ndpointer(dtype=np.complex128, ndim=2, flags='F_CONTIGUOUS'), POINTER(c_int), POINTER(c_int), POINTER(blacs_desc), 
                                nullable_ndpointer(dtype=np.complex128, ndim=2, flags='F_CONTIGUOUS'), POINTER(c_int), POINTER(c_int), POINTER(blacs_desc), 
                                POINTER(c_int)]
    #EXTERN void pzgemr2d_(int *m , int *n , double_complex_t *a , int *ia , int *ja , int *desca , double_complex_t *b , int *ib , int *jb , int *descb , int *ictxt);
  
  def descinit(self, desc, m, n, mb, nb, rsrc, csrc, blacs_ctx, lld):
    m = c_int(m)
    n = c_int(n)
    mb = c_int(mb)
    nb = c_int(nb)
    irsrc = c_int(rsrc)
    icsrc = c_int(csrc)
    blacs_ctx = c_int(blacs_ctx)
    lld = c_int(lld)
    info = c_int()
    self.blacs.descinit_(desc, m, n, mb, nb, irsrc, icsrc, blacs_ctx, lld, info)
    assert info.value == 0, info.value
  
  def pdgemr2d(self, m, n, a, ia, ja, desca, b, ib, jb, descb, blacs_ctx):
    m = c_int(m)
    n = c_int(n)
    ia = c_int(ia)
    ja = c_int(ja)
    ib = c_int(ib)
    jb = c_int(jb)
    blacs_ctx = c_int(blacs_ctx)
    self.blacs.pdgemr2d_(m, n, a, ia, ja, desca, b, ib, jb, descb, blacs_ctx)

  def pzgemr2d(self, m, n, a, ia, ja, desca, b, ib, jb, descb, blacs_ctx):
    m = c_int(m)
    n = c_int(n)
    ia = c_int(ia)
    ja = c_int(ja)
    ib = c_int(ib)
    jb = c_int(jb)
    blacs_ctx = c_int(blacs_ctx)
    self.blacs.pzgemr2d_(m, n, a, ia, ja, desca, b, ib, jb, descb, blacs_ctx)

  def get_default_system_context(self):
    zero = c_int(0)
    system_context = c_int()
    self.blacs.blacs_get_(zero, zero, system_context)
    return system_context.value

  def get_system_context(self, blacs_ctx): # get system context of the blacs_context
    blacs_ctx = c_int(blacs_ctx)
    what = c_int(10)
    val = c_int()
    self.blacs.blacs_get_(blacs_ctx, what, val)
    return val.value

  def make_blacs_context(self, sys_context, MP, NP):
    order = c_char(b'R')
    context_inout = c_int(sys_context)
    c_MP = c_int(MP)
    c_NP = c_int(NP)
    self.blacs.blacs_gridinit_(context_inout, byref(order), c_MP, c_NP)
    return context_inout.value
  
  def close_blacs_context(self, blacs_ctx):
    if blacs_ctx == -1:
      return
    blacs_ctx = c_int(blacs_ctx)
    self.blacs.blacs_gridexit_(blacs_ctx)

  def make_blacs_desc(self, blacs_ctx, m, n, mb=1, nb=1, rsrc=0, csrc=0, lld=None):
    return blacs_desc(self, blacs_ctx, m, n, mb, nb, rsrc, csrc, lld)

  def wrap_blacs_desc(self, buf):
    return blacs_desc(self, buf=buf)

  def blacs_gridinfo(self, blacs_ctx):
    c_blacs_ctx = c_int(blacs_ctx)
    nprow = c_int()
    npcol = c_int()
    myrow = c_int()
    mycol = c_int()
    self.blacs.blacs_gridinfo_(c_blacs_ctx, nprow, npcol, myrow, mycol)
    return nprow.value, npcol.value, myrow.value, mycol.value

  def numroc(self, n, nb, iproc, isrcproc, nprocs):
    n = c_int(n)
    nb = c_int(nb)
    iproc = c_int(iproc)
    isrcproc = c_int(isrcproc)
    nprocs = c_int(nprocs)
    return self.blacs.numroc_(n, nb, iproc, isrcproc, nprocs)

  def scatter(self, src_data, dest_desc, dest_data):
    m = dest_desc.m
    n = dest_desc.n
    common_blacs_ctx = dest_desc.ctxt
    src_blacs_ctx = self.make_blacs_context(self.get_system_context(common_blacs_ctx), 1, 1)
    if src_blacs_ctx != -1:
      assert m == src_data.shape[0]
      assert n == src_data.shape[1]
    else:
      assert src_data is None, f"src_data must be None if src_blacs_ctx == -1"
    src_desc = self.make_blacs_desc(src_blacs_ctx, m, n)
    if dest_data.dtype==np.float64:
      self.pdgemr2d(m, n, src_data, 1, 1, src_desc, dest_data, 1, 1, dest_desc, common_blacs_ctx)
    elif dest_data.dtype==np.complex128:
      self.pzgemr2d(m, n, src_data, 1, 1, src_desc, dest_data, 1, 1, dest_desc, common_blacs_ctx)
    else:
      assert False
    self.close_blacs_context(src_blacs_ctx)

  def gather(self, src_desc, src_data, dest_data):
    m = src_desc.m
    n = src_desc.n
    common_blacs_ctx = src_desc.ctxt
    gatherer_blacs_ctx = self.make_blacs_context(self.get_system_context(common_blacs_ctx), 1, 1)
    if gatherer_blacs_ctx != -1:
      assert m == dest_data.shape[0]
      assert n == dest_data.shape[1]
    else:
      assert dest_data is None, dest_data
    dest_desc = self.make_blacs_desc(gatherer_blacs_ctx, m, n)
    
    if src_data.dtype==np.float64:
      self.pdgemr2d(m, n, src_data, 1, 1, src_desc, dest_data, 1, 1, dest_desc, common_blacs_ctx)
    elif src_data.dtype==np.complex128:
      self.pzgemr2d(m, n, src_data, 1, 1, src_desc, dest_data, 1, 1, dest_desc, common_blacs_ctx)
    else:
      assert False
    self.close_blacs_context(gatherer_blacs_ctx)

  def gather_numpy(self, descr, data, shape):
    '''
    Gather BLACS array to the process in 0-th row and column in a BLACS process grid
    and returns it as a numpy.ndarray
    
    :param descr: Pointer to BLACS descriptor or NULL if data not distributed
    :param data:  Pointer to the array or its part in the current process
    :param shape: Expected shape of the total array
    :type descr:  ctypes.POINTER(c_int)
    :type data:   ctypes.POINTER
    :type shape:  (int, int)
    :return:      Gathered numpy.ndarray for the process (0,0); None for other processes
    '''
    single_proc = False
    if descr:
      descr = self.wrap_blacs_desc(descr)
      single_proc = (descr.nprow * descr.npcol == 1)
    else:
      single_proc = True
    if single_proc:
      return ctypes2ndarray(data, shape).T
    
    if len(shape) == 3:
      data = ctypes2ndarray(data, (descr.locrow, descr.loccol, 2)).T
      shape = shape[0], shape[1]
    else:
      data = ctypes2ndarray(data, (descr.locrow, descr.loccol)).T

    res = np.zeros(shape, dtype=data.dtype).T if (descr.myrow==0 and descr.mycol==0) else None
    self.gather(descr, data, res)
    return res

  def scatter_numpy(self, src, descr, dst, dtype):
    '''
    Scatters numpy.ndarray over BLACS descriptor
    :param src:   Source numpy.ndarray on a root process, must be None on non-root processes
    :param descr: Pointer to BLACS descriptor of the destination (`dst`) or NULL if data not distributed
    :param dst:   Pointer to the destination BLACS array
    :param dtype: type of dst data: np.float64 or np.complex128
    :type src:    numpy.ndarray
    :type descr:  ctypes.POINTER(c_int)
    :type data:   ctypes.POINTER
    :type dtype:  numpy.dtype
    '''
    if not descr:
      if dtype==np.float64:
        dst_shape = src.shape
      elif dtype==np.complex128:
        dst_shape = (*src.shape, 2)
      else:
        assert False
      dst = np.ctypeslib.as_array(dst, shape=dst_shape)

      if src.dtype==np.float64:
        dst[:,:] = src
      elif src.dtype==np.complex128:
        dst[:,:,0] = src.T.real
        dst[:,:,1] = src.T.imag
      else:
        assert False
      
      return

    descr = self.wrap_blacs_desc(descr)

    if dtype==np.float64:
      dst_shape = (descr.locrow, descr.loccol)
    elif dtype==np.complex128:
      dst_shape = (descr.locrow, descr.loccol, 2)
    else:
      assert False

    dst = ctypes2ndarray(dst, shape=dst_shape).T
    self.scatter(src, descr, dst)

  def is_root(self, descr):
    '''
    Returns True if descr is NULL or if the current process grid index is (0,0). False otherwise.
    :param descr: Pointer to BLACS descriptor or NULL if data not distributed
    :type descr:  ctypes.POINTER(c_int)
    :return:      True if descr is NULL or if the current process grid index is (0,0). False otherwise.
    '''
    if not descr:
      return True
    descr = self.wrap_blacs_desc(descr)
    return (descr.myrow==0 and descr.mycol==0)

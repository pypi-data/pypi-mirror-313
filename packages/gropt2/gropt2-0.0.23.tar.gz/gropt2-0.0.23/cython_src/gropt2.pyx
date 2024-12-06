# distutils: language = c++
import time

from libcpp.string cimport string
from libcpp.vector cimport vector

import numpy as np
cimport numpy as np
np.import_array()

cimport c_gropt2

# Prepare numpy array for memory view, with as few copies as possible
def array_prep(A, dtype, linear=True):
    if not A.flags['C_CONTIGUOUS']:
        A = np.ascontiguousarray(A)
    
    A = A.astype(dtype, order='C', copy=False)
     
    if linear:
        A = A.ravel()

    return A 

cdef vector_to_nparray(vector[double] &vec, dtype=np.double):
    np_out = np.empty(vec.size(), dtype)
    for i in range(vec.size()):
        np_out[i] = vec[i]
    return np_out

cdef vector_to_nparray_int(vector[int] &vec, dtype=int):
    np_out = np.empty(vec.size(), dtype)
    for i in range(vec.size()):
        np_out[i] = vec[i]
    return np_out

def get_girf_ec_pc_response(G, H, excite_idx, dt = 10e-6, tile_pre = 4, tile_post = 2, mode = 1):
    
    cdef double[::1] G_view = array_prep(G, np.float64)
    cdef double complex[::1] H_view = array_prep(H, np.complex128)

    cdef vector[double] out_vec

    c_gropt2.get_girf_ec_pc_response(G.size, &G_view[0], H.size, &H_view[0], excite_idx, dt, out_vec, tile_pre, tile_post, mode)

    return np.hstack([np.zeros(excite_idx), vector_to_nparray(out_vec)]) 


def get_SAFE(G, dt, tau1=None, tau2=None, tau3=None, a1=None, a2=None, a3=None, stim_limit=None, g_scale=None, true_safe = True):
    
    cdef double[::1] G_view = array_prep(G, np.float64)
    cdef vector[double] out_vec

    if G.ndim == 1:
        N = G.size
        Naxis = 1
    else:
        N = G.shape[1]
        Naxis = G.shape[0]

    if tau1 is not None:
        c_gropt2.get_SAFE(N, Naxis, &G_view[0], dt, out_vec, true_safe, tau1, tau2, tau3, a1, a2, a3, stim_limit, g_scale)
    else:
        c_gropt2.get_SAFE(N, Naxis, &G_view[0], dt, out_vec, true_safe)

    return vector_to_nparray(out_vec)


def get_bval(G, TE, dt):
    cdef double[::1] G_view = array_prep(G, np.float64)
    return c_gropt2.get_bval(G.size, &G_view[0], int(np.floor(TE/dt/2.0)), dt)

cdef class GroptParams:
    cdef c_gropt2.GroptParams c_gparams

    def __init__(self):
        self.c_gparams = c_gropt2.GroptParams() 

    def init_N(self, N, dt):
        self.c_gparams.init_N(N, dt)

    def init_simple_diffusion(self, T_90, T_180, T_readout, TE, dt=10e-6):
        self.c_gparams.init_simple_diffusion(dt, T_90, T_180, T_readout, TE)

    def init_crusher_diffusion(self, T_90, T_180, T_readout, TE, N_slew = 0, N_flat = 0, amp = 0, dt=10e-6):
        self.c_gparams.init_crusher_diffusion(dt, T_90, T_180, T_readout, TE, N_slew, N_flat, amp)

    def init_set_vals(self, set_vals):
        cdef double[::1] set_vals_view = array_prep(set_vals, np.float64)
        self.c_gparams.init_set_vals(&set_vals_view[0], set_vals.size)

    def add_gmax(self, gmax):
        self.c_gparams.add_gmax(gmax)

    def add_smax(self, smax):
        self.c_gparams.add_smax(smax)

    def add_obj_bval(self, weight):
        self.c_gparams.add_obj_bval(weight)

    def add_op_bval(self, bval):
        self.c_gparams.add_op_bval(bval)

    def add_moment(self, *args):
        if len(args) == 2:
            self.c_gparams.add_moment(args[0], args[1])
        elif len(args) == 7:
            self.c_gparams.add_moment(args[0], args[1], args[2], args[3], args[4], args[5], args[6])

    def add_girf_ec_pc(self, H0, excite_idx, win0_idx, win1_idx, tol, weight, tile_pre = 4, tile_post = 2, mode = 1):
        cdef double complex[::1] H0_view = array_prep(H0, np.complex128)
        
        self.c_gparams.add_girf_ec_pc(H0.size, &H0_view[0], 
                                        excite_idx[0], excite_idx[1], win0_idx[0], win0_idx[1], win1_idx[0], win1_idx[1],
                                        tol, weight, tile_pre, tile_post, mode)

    def add_fft_sqdiff_mod(self, mod):
        cdef double[::1] mod_view = array_prep(mod, np.float64)
        self.c_gparams.add_fft_sqdiff_mod(mod.size, &mod_view[0])

    def add_op_eddy(self, lam = 80e-3, tol = 1e-2):
        self.c_gparams.add_op_eddy(lam, tol)

    def add_op_pns(self, thresh = 1.0):
        self.c_gparams.add_op_PNS(thresh)

    def add_op_SAFE(self, thresh):
        self.c_gparams.add_op_SAFE(thresh)

    def add_op_SAFE_wparams(self, tau1, tau2, tau3, a1, a2, a3, stim_limit, g_scale, stim_thresh):
        self.c_gparams.add_op_SAFE(tau1, tau2, tau3, a1, a2, a3, stim_limit, g_scale, stim_thresh)

    def optimize(self, x0 = None):
        cdef double[::1] x0_view
        if x0 is not None:
            x0_view = array_prep(x0, np.float64)
            self.c_gparams.optimize(x0.size, &x0_view[0])
        else:
            self.c_gparams.optimize()

    def get_out(self):
        cdef vector[double] out_vec
        self.c_gparams.get_out(out_vec)
        return vector_to_nparray(out_vec)

    def get_opt_time(self):
        return self.c_gparams.get_opt_time()

    def get_debugger(self):
        cdef vector[int] sizes
        cdef vector[double] out_x0
        cdef vector[double] out_x1
        cdef vector[double] out_x2
        cdef vector[double] out_weights
        cdef vector[int] out_cgiter
        cdef vector[string] out_names

        self.c_gparams.get_debugger(sizes, out_x0, out_x1, out_x2, out_weights, out_cgiter, out_names)

        np_sizes = vector_to_nparray_int(sizes)
        np_out_x0 = vector_to_nparray(out_x0)
        np_out_x1 = vector_to_nparray(out_x1)
        np_out_x2 = vector_to_nparray(out_x2)
        np_out_weights = vector_to_nparray(out_weights)
        np_cgiter = vector_to_nparray_int(out_cgiter)

        np_out_x0 = np.reshape(np_out_x0, np_sizes[0:2])
        np_out_x1 = np.reshape(np_out_x1, np_sizes[0:2])
        np_out_x2 = np.reshape(np_out_x2, np_sizes[0:2])
        np_out_weights = np.reshape(np_out_weights, np_sizes[2:5])

        out_names_l = list(out_names)
        out_names_l = [x.decode('utf-8') for x in out_names_l if x]

        res = {'x': [np_out_x0, np_out_x1, np_out_x2],
                'op_names': out_names_l,
               'weights': np_out_weights,
               'cgiter': np_cgiter,}

        return res 

    def set_verbose(self, level):
        self.c_gparams.set_verbose(level)

    
    @property
    def N_iter(self):
        return self.c_gparams.N_iter
    @N_iter.setter
    def N_iter(self, N_iter):
        self.c_gparams.N_iter = N_iter

    @property
    def solver_type(self):
        return self.c_gparams.solver_type
    @solver_type.setter
    def solver_type(self, solver_type):
        self.c_gparams.solver_type = solver_type.encode('UTF-8')

    @property
    def final_good(self):
        return self.c_gparams.final_good
    @final_good.setter
    def final_good(self, final_good):
        self.c_gparams.final_good = final_good

    @property
    def d_obj_thresh(self):
        return self.c_gparams.d_obj_thresh
    @d_obj_thresh.setter
    def d_obj_thresh(self, d_obj_thresh):
        self.c_gparams.d_obj_thresh = d_obj_thresh

    @property
    def weight_min(self):
        return self.c_gparams.weight_min
    @weight_min.setter
    def weight_min(self, weight_min):
        self.c_gparams.weight_min = weight_min

    @property
    def weight_max(self):
        return self.c_gparams.weight_max
    @weight_max.setter
    def weight_max(self, weight_max):
        self.c_gparams.weight_max = weight_max

    @property
    def rw_scalelim(self):
        return self.c_gparams.rw_scalelim
    @rw_scalelim.setter
    def rw_scalelim(self, rw_scalelim):
        self.c_gparams.rw_scalelim = rw_scalelim

    @property
    def rw_interval(self):
        return self.c_gparams.rw_interval
    @rw_interval.setter
    def rw_interval(self, rw_interval):
        self.c_gparams.rw_interval = rw_interval

    @property
    def rw_eps(self):
        return self.c_gparams.rw_eps
    @rw_eps.setter
    def rw_eps(self, rw_eps):
        self.c_gparams.rw_eps = rw_eps

    @property
    def grw_interval(self):
        return self.c_gparams.grw_interval
    @grw_interval.setter
    def grw_interval(self, grw_interval):
        self.c_gparams.grw_interval = grw_interval

    @property
    def grw_start(self):
        return self.c_gparams.grw_start
    @grw_start.setter
    def grw_start(self, grw_start):
        self.c_gparams.grw_start = grw_start

    @property
    def grw_scale(self):
        return self.c_gparams.grw_scale
    @grw_scale.setter
    def grw_scale(self, grw_scale):
        self.c_gparams.grw_scale = grw_scale

    @property
    def cg_niter(self):
        return self.c_gparams.cg_niter
    @cg_niter.setter
    def cg_niter(self, cg_niter):
        self.c_gparams.cg_niter = cg_niter

    @property
    def cg_rtol(self):
        return self.c_gparams.cg_rtol
    @cg_rtol.setter
    def cg_rtol(self, cg_rtol):
        self.c_gparams.cg_rtol = cg_rtol

    @property
    def cg_shift(self):
        return self.c_gparams.cg_shift
    @cg_shift.setter
    def cg_shift(self, cg_shift):
        self.c_gparams.cg_shift = cg_shift

    @property
    def e_corr(self):
        return self.c_gparams.e_corr
    @e_corr.setter
    def e_corr(self, e_corr):
        self.c_gparams.e_corr = e_corr

    @property
    def total_n_feval(self):
        return self.c_gparams.total_n_feval
    @total_n_feval.setter
    def total_n_feval(self, total_n_feval):
        self.c_gparams.total_n_feval = total_n_feval

    @property
    def total_n_iter(self):
        return self.c_gparams.total_n_iter
    @total_n_iter.setter
    def total_n_iter(self, total_n_iter):
        self.c_gparams.total_n_iter = total_n_iter

    @property
    def N_feval(self):
        return self.c_gparams.N_feval
    @N_feval.setter
    def N_feval(self, N_feval):
        self.c_gparams.N_feval = N_feval

    @property
    def verbose(self):
        return self.c_gparams.verbose
    @verbose.setter
    def verbose(self, verbose):
        self.c_gparams.verbose = verbose



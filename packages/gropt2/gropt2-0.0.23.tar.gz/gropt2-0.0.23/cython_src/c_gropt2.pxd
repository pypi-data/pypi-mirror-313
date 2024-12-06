from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp cimport bool


cdef extern from "gropt_params.hpp" namespace "Gropt":

    cdef cppclass GroptParams:

        GroptParams() except +

        int grw_interval
        int grw_start
        double grw_scale

        double rw_scalelim
        double rw_interval
        double rw_eps
        double e_corr
        double weight_min
        double weight_max

        int cg_niter
        double cg_rtol
        double cg_shift

        double d_obj_thresh
        int verbose

        double total_n_feval
        double total_n_iter
        

        int N_feval
        int final_good

        int N_iter
        string solver_type

        void init_N(int N_in, double _dt)
        void init_simple_diffusion(double _dt, double T_90, double T_180, double T_readout, double TE)
        void init_crusher_diffusion(double _dt, double T_90, double T_180, double T_readout, double TE, int N_slew, int N_flat, double amp)
        void init_set_vals(double *set_val_in, int N_in)

        void add_gmax(double gmax)
        void add_smax(double smax)

        void add_moment(double order, double target)
        void add_moment(double axis, double order, double ref0, double start, double stop, double target, double tol0)
        double get_opt_time()


        void add_girf_ec_pc(int N_H, double complex *H_in, 
                            int excite0, int excite1, int win00, int win01, int win10, int win11, 
                            double tol, double weight, int tile_pre, int tile_post, int mode)

        void add_fft_sqdiff_mod(int N_in, double *mod_in)

        void add_obj_bval(double weight)
        void add_op_bval(double _bval)

        void add_op_SAFE(double _thresh)
        void add_op_SAFE(double _tau1, double _tau2, double _tau3, double _a1, double _a2, double _a3, double _stim_limit, double _g_scale, double _stim_thresh)

        void add_op_eddy(double _lam_in, double _tol_in)
        void add_op_eddy(double _lam_in)
        void add_op_PNS(double stim_thresh)

        void optimize()
        void optimize(int N_X0, double *_X0)

        void get_out(vector[double] &out_vec)
        void get_debugger(vector[int] &sizes, vector[double] &out_x0, vector[double] &out_x1, vector[double] &out_x2,
                            vector[double] &out_weights, vector[int] &out_cgiter, vector[string] &out_names)

        void set_verbose(int level)


cdef extern from "gropt_utils.hpp" namespace "Gropt":
    
    double get_bval(int N, double *G_in, int idx_inv, double dt)

    void get_SAFE(int N, int Naxis, double *G_in, double dt, vector[double] &out_vec, bool true_safe)

    void get_SAFE(int N, int Naxis, double *G_in, double dt, vector[double] &out_vec, bool true_safe, double tau1, double tau2, double tau3, double a1, double a2, double a3, double stim_limit, double g_scale)

    void get_girf_ec_pc_response(int N, double *G_in, int N_H, double complex *H_in, int excite, double dt,
                                 vector[double] &out_vec, int tile_pre, int tile_post, int mode)
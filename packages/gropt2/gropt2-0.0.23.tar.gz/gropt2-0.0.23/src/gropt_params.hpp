#ifndef GROPT_PARAMS_H
#define GROPT_PARAMS_H

#include <iostream> 
#include <string>
#include <vector>
#include <chrono>
#include <math.h>  
#include "Eigen/Dense"

#include "op_main.hpp"
#include "debugger.hpp"

namespace Gropt {

class GroptParams
{
    public:
        std::vector<GroptOperator*> all_op;
        std::vector<GroptOperator*> all_obj;

        Eigen::VectorXd inv_vec;
        Eigen::VectorXd set_vals;
        Eigen::VectorXd fixer;

        Eigen::VectorXd X0;
        Eigen::VectorXd out;

        double dt;
        int N;
        int Naxis;

        double gmax;

        int grw_interval;
        int grw_start;
        double grw_scale;

        double rw_scalelim;
        double rw_interval;
        double rw_eps;
        double e_corr;
        double weight_min;
        double weight_max;

        bool do_gamma;
        bool do_weight;
        bool do_scalelim; 

        double weight_init;
        double gamma_init;

        int N_iter;  // Maximum number of outer iterations
        int N_feval; // Maximum number of function evaluations (includes CG iterations)

        std::chrono::steady_clock::time_point start_time;
        std::chrono::steady_clock::time_point stop_time;
        std::chrono::duration<double, std::micro> elapsed_us;

        int obj_min;
        double obj_scale;

        int cg_niter;
        double cg_shift;
        double cg_rtol;

        double d_obj_thresh;

        double total_n_feval;
        double total_n_iter;
        int last_iiter;

        bool do_init;
        int verbose;
        int verbose_interval;

        int final_good;

        std::string solver_type;

        // Some helper storage to build up moment arrays before making operator
        std::vector<double> moment_axis;
        std::vector<double> moment_order;
        std::vector<double> moment_ref0;
        std::vector<double> moment_start;
        std::vector<double> moment_stop;
        std::vector<double> moment_target;
        std::vector<double> moment_tol0;

        Debugger debugger;


        // Functions
        GroptParams();
        ~GroptParams();

        void init_N(int N_in, double dt_in);
        void init_simple_diffusion(double _dt, double T_90, double T_180, double T_readout, double TE);
        void init_crusher_diffusion(double _dt, double T_90, double T_180, double T_readout, double TE, int N_slew, int N_flat, double amp);
        void init_set_vals(double *set_val_in, int N_in);

        void nonconvex_settings();
        void defaults_diffusion();


        void add_gmax(double gmax);

        void add_smax(double smax);

        void add_moment(double order, double target);
        void add_moment(double axis, double order, double ref0, double start, double stop, double target, double tol0);
        void finish_moments();
        void finish_moments_ones();

        void add_girf_ec_pc(int N_H, std::complex<double> *H_in, 
                            int excite0, int excite1, int win00, int win01, int win10, int win11, 
                            double tol, double weight);
        void add_girf_ec_pc(int N_H, std::complex<double> *H_in, 
                                int excite0, int excite1, int win00, int win01, int win10, int win11, 
                                double tol, double weight, int tile_pre, int tile_post, int mode);

        void add_obj_duty(double weight);

        void add_obj_bval(double weight);
        void add_op_bval(double _bval);

        void add_sqdiff_ref(std::vector<double> &ref_in);

        void add_op_SAFE(double safe_thresh);
        void add_op_SAFE(double _tau1, double _tau2, double _tau3, double _a1, double _a2, double _a3, double _stim_limit, double _g_scale, double _stim_thresh);

        void add_fft_sqdiff_mod(int N_in, double *mod_in);

        void add_op_eddy(double _lam_in);
        void add_op_eddy(double _lam_in, double _tol_in);

        void add_op_PNS(double stim_thresh);


        void update_vals();
        void set_vecs();
        void init_all_vals();
        void set_constraint_vals(std::string op_name, double target_in, double tol_in, double cushion_in);

        void optimize();
        void optimize(int N_X0, double *_X0);

        void get_out(std::vector<double> &out);
        void get_debugger(std::vector<int> &sizes, std::vector<double> &out_x0, 
        std::vector<double> &out_x1, 
                                std::vector<double> &out_x2, std::vector<double> &out_weights, std::vector<int> &out_cgiter, std::vector<std::string> &out_names);
        double get_opt_time();

        void set_verbose(int level);

        void interp_from_gparams(GroptParams &gparams, Eigen::VectorXd &X_in);

};

}  // end namespace Gropt

#endif
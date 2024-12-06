#include "gropt_params.hpp"
#include "optimize.hpp"

#include "op_gradient.hpp"
#include "op_slew.hpp"
#include "op_moments.hpp"
#include "op_girfec_pc.hpp" 
#include "op_duty.hpp"
#include "op_bval.hpp"
#include "op_sqdist.hpp"
#include "op_eddy.hpp"
#include "op_pns.hpp"
#include "op_safe.hpp"
#include "op_fft_sqdist.hpp"
#include "logging.hpp"

namespace Gropt {

GroptParams::GroptParams() {
    N = 1;
    Naxis = 1;
    gmax = .01;
    dt = 10e-6;

    N_iter = 10000;
    N_feval = 100000;

    obj_min = 0;
    obj_scale = 1.0;

    grw_interval = 16;
    grw_start = 32;
    grw_scale = 8.0;

    // reweighting defaults here
    rw_scalelim = 10;
    rw_interval = 4;
    rw_eps = 1.0e-8;
    e_corr = 0.5;

    weight_min = 1.0e-8; 
    weight_max = 1.0e16;

    do_gamma = true;
    do_weight = true;
    do_scalelim = true;

    weight_init = 1.0;
    gamma_init = 1.0;


    d_obj_thresh = 1e-4;

    do_init = true;
    verbose = 0;
    verbose_interval = 20;

    final_good = 0;

    solver_type = "cg";
    cg_shift = 0.0;
    cg_rtol = 1e-6;
    cg_niter = 500;

    debugger.debug_active = true;
    
}

GroptParams::~GroptParams() {
    for (int i = 0; i < all_op.size(); i++) {
        delete all_op[i];
    }

    for (int i = 0; i < all_obj.size(); i++) {
        delete all_obj[i];
    }
}

void GroptParams::nonconvex_settings()
{
    do_gamma = false; 
    gamma_init = 1.0;
}


void GroptParams::init_N(int _N, double _dt)
{   
    if (!all_op.empty()) {
        std::cout << "WARNING:  Setting N after operators exists is a bad idea" << std::endl;
    }

    N = _N;
    dt = _dt;

    int Ntot = N*Naxis;

    // This should match what is in the op_main.cpp Constructor 
    // TODO: Have this pass through instead so we don't need to keep them in sync
    fixer.setOnes(Ntot);
    set_vals.setOnes(Ntot);
    set_vals.array() *= NAN;
    for (int j = 0; j < Naxis; j++) {
        fixer((j*N)) = 0.0;
        fixer((j*N)+(N-1)) = 0.0;

        set_vals((j*N)) = 0.0;
        set_vals((j*N) + (N-1)) = 0.0;
    }

    inv_vec.setOnes(Ntot);
}

void GroptParams::init_simple_diffusion(double _dt, double T_90, double T_180, double T_readout, double TE)
{   
    if (!all_op.empty()) {
        std::cout << "WARNING:  Setting N after operators exists is a bad idea" << std::endl;
    }

    dt = _dt;
    N = (int)((TE-T_readout)/dt) + 1;
    
    int Ntot = N*Naxis;


    int ind_inv = (int)(TE/2.0/dt);
    inv_vec.setOnes(Ntot);
    for (int j = 0; j < Naxis; j++) {
        for(int i = j*N+ind_inv; i < (j+1)*N; i++) {
            inv_vec(i) = -1.0;
        }
    }


    int ind_90_end, ind_180_start, ind_180_end;
    ind_90_end = ceil(T_90/dt);
    ind_180_start = floor((TE/2.0 - T_180/2.0)/dt);
    ind_180_end = ceil((TE/2.0 + T_180/2.0)/dt);

    set_vals.setOnes(Ntot);
    set_vals.array() *= NAN;
    for (int j = 0; j < Naxis; j++) {
        for(int i = j*N; i <= j*N+ind_90_end; i++) {
            set_vals(i) = 0.0;
        }
        for(int i = j*N+ind_180_start; i <= j*N+ind_180_end; i++) {
            set_vals(i) = 0.0;
        }
        set_vals(j*N+0) = 0.0;
        set_vals(j*N+N-1) = 0.0;
    }


    fixer.setOnes(Ntot);
    for(int i = 0; i < Ntot; i++) {
        if (!isnan(set_vals(i))) {
            fixer(i) = 0.0;
        }
    }
}


void GroptParams::init_crusher_diffusion(double _dt, double T_90, double T_180, double T_readout, double TE, int N_slew, int N_flat, double amp)
{   
    if (!all_op.empty()) {
        std::cout << "WARNING:  Setting N after operators exists is a bad idea" << std::endl;
    }

    dt = _dt;
    N = (int)((TE-T_readout)/dt) + 1;
    
    int Ntot = N*Naxis;


    int ind_inv = (int)(TE/2.0/dt);
    inv_vec.setOnes(Ntot);
    for (int j = 0; j < Naxis; j++) {
        for(int i = j*N+ind_inv; i < (j+1)*N; i++) {
            inv_vec(i) = -1.0;
        }
    }


    int ind_90_end, ind_180_start, ind_180_end;
    ind_90_end = ceil(T_90/dt);
    ind_180_start = floor((TE/2.0 - T_180/2.0)/dt);
    ind_180_end = ceil((TE/2.0 + T_180/2.0)/dt);

    set_vals.setOnes(Ntot);
    set_vals.array() *= NAN;
    for (int j = 0; j < Naxis; j++) {
        for(int i = j*N; i <= j*N+ind_90_end; i++) {
            set_vals(i) = 0.0;
        }
        for(int i = j*N+ind_180_start; i <= j*N+ind_180_end; i++) {
            set_vals(i) = 0.0;
        }
        set_vals(j*N+0) = 0.0;
        set_vals(j*N+N-1) = 0.0;
    }


    for (int j = 0; j < Naxis; j++) {
        int ind_start = j*N+ind_180_start;
        int ind_stop = j*N+ind_180_end;
        
        for(int i = 0; i < N_slew; i++) {
            set_vals(ind_start + i) = amp*i/(N_slew-1);
            set_vals(ind_stop - i) = amp*i/(N_slew-1);
        }

        for(int i = 0; i < N_flat; i++) {
            set_vals(ind_start + N_slew + i) = amp;
            set_vals(ind_stop - N_slew - i) = amp;
        }

        for(int i = 0; i < N_slew; i++) {
            set_vals(ind_start + N_slew + N_flat + i) = amp*(N_slew-1-i)/(N_slew-1);
            set_vals(ind_stop - N_slew - N_flat - i) = amp*(N_slew-1-i)/(N_slew-1);
        }
    }

    fixer.setOnes(Ntot);
    for(int i = 0; i < Ntot; i++) {
        if (!isnan(set_vals(i))) {
            fixer(i) = 0.0;
        }
    }
}


void GroptParams::init_set_vals(double *set_val_in, int N_in)
{
    
    if (N*Naxis != N_in) {
        std::cout << "ERROR!!!!  setting set vals, but N doesn't match" << std::endl;
    } else {
        
        for (int i = 0; i < N_in; i++) {
            set_vals(i) = set_val_in[i];
            if (isnan(set_vals(i))) {
                fixer(i) = 1.0;
            } else {
                fixer(i) = 0.0;
            }
        }
    }

}

//////////////////////////////
// --------------------------- op_gradient

void GroptParams::add_gmax(double gmax_in)
{
   Op_Gradient *opG = new Op_Gradient(N, Naxis, dt);
   opG->set_params(gmax_in);
   all_op.push_back(opG);
   gmax = gmax_in;
}

//////////////////////////////
// --------------------------- op_slew

void GroptParams::add_smax(double smax)
{
   Op_Slew *opS = new Op_Slew(N, Naxis, dt);
   opS->set_params(smax);
   all_op.push_back(opS);
}

//////////////////////////////
// --------------------------- op_moments

void GroptParams::add_moment(double order, double target)
{
    moment_axis.push_back(0);
    moment_order.push_back(order);
    moment_ref0.push_back(0);
    moment_start.push_back(0);
    moment_stop.push_back(0);
    moment_target.push_back(target);
    moment_tol0.push_back(1e-6);
}

void GroptParams::add_moment(double axis, double order, double ref0, double start, double stop, double target, double tol0)
{
    moment_axis.push_back(axis);
    moment_order.push_back(order);
    moment_ref0.push_back(ref0);
    moment_start.push_back(start);
    moment_stop.push_back(stop);
    moment_target.push_back(target);
    moment_tol0.push_back(tol0); 
}

void GroptParams::finish_moments()
{
    int Nm = moment_axis.size();
    if (Nm < 1) {std::cout << "WARNING:  No moments to finalize" << std::endl;}

    if (moment_order.size() != Nm) {std::cout << "ERROR:  Size mismatch with moment_order" << std::endl;}
    if (moment_ref0.size() != Nm) {std::cout << "ERROR:  Size mismatch with moment_ref0" << std::endl;}
    if (moment_start.size() != Nm) {std::cout << "ERROR:  Size mismatch with moment_start" << std::endl;}
    if (moment_stop.size() != Nm) {std::cout << "ERROR:  Size mismatch with moment_stop" << std::endl;}
    if (moment_target.size() != Nm) {std::cout << "ERROR:  Size mismatch with moment_target" << std::endl;}
    if (moment_tol0.size() != Nm) {std::cout << "ERROR:  Size mismatch with moment_tol0" << std::endl;}

    Op_Moments *opM = new Op_Moments(N, Naxis, dt, Nm);
    opM->set_params(moment_axis, moment_order, moment_ref0, moment_start, moment_stop, moment_target, moment_tol0);
    all_op.push_back(opM);
    
    // Free these vectors in case we want to add a second set of moments for whatever reason
    moment_axis.clear();
    moment_order.clear();
    moment_ref0.clear();
    moment_start.clear();
    moment_stop.clear();
    moment_target.clear();
    moment_tol0.clear();
}


// This is a special case for comparing to a reference implementation
void GroptParams::finish_moments_ones()
{
    int Nm = moment_axis.size();
    if (Nm < 1) {std::cout << "WARNING:  No moments to finalize" << std::endl;}

    if (moment_order.size() != Nm) {std::cout << "ERROR:  Size mismatch with moment_order" << std::endl;}
    if (moment_ref0.size() != Nm) {std::cout << "ERROR:  Size mismatch with moment_ref0" << std::endl;}
    if (moment_start.size() != Nm) {std::cout << "ERROR:  Size mismatch with moment_start" << std::endl;}
    if (moment_stop.size() != Nm) {std::cout << "ERROR:  Size mismatch with moment_stop" << std::endl;}
    if (moment_target.size() != Nm) {std::cout << "ERROR:  Size mismatch with moment_target" << std::endl;}
    if (moment_tol0.size() != Nm) {std::cout << "ERROR:  Size mismatch with moment_tol0" << std::endl;}

    Op_Moments *opM = new Op_Moments(N, Naxis, dt, Nm);
    opM->set_params(moment_axis, moment_order, moment_ref0, moment_start, moment_stop, moment_target, moment_tol0);
    opM->prep_A_ones();
    all_op.push_back(opM);
    
    // Free these vectors in case we want to add a second set of moments for whatever reason
    moment_axis.clear();
    moment_order.clear();
    moment_ref0.clear();
    moment_start.clear();
    moment_stop.clear();
    moment_target.clear();
    moment_tol0.clear();
}

//////////////////////////////
// --------------------------- op_girfec_pc

void GroptParams::add_girf_ec_pc(int N_H, std::complex<double> *H_in, 
                                int excite0, int excite1, int win00, int win01, int win10, int win11, 
                                double tol, double weight)
{
    Eigen::VectorXcd H0;
    H0.setZero(N_H);
    for (int i=0; i<N_H; i++) {
        H0(i) = H_in[i];
    }

    int win_width = win10 - win00;
    Op_GirfEC_PC *opEC = new Op_GirfEC_PC(N, 1, dt, H0, win_width, 4, 2);
    opEC->set_params(excite0, excite1, win00, win01, win10, win11);
    opEC->set_params(tol);
    // opEC->spec_norm2(0) = weight;

    all_op.push_back(opEC);
}


void GroptParams::add_girf_ec_pc(int N_H, std::complex<double> *H_in, 
                                int excite0, int excite1, int win00, int win01, int win10, int win11, 
                                double tol, double weight, int tile_pre, int tile_post, int mode)
{
    Eigen::VectorXcd H0;
    H0.setZero(N_H);
    for (int i=0; i<N_H; i++) {
        H0(i) = H_in[i];
    }

    int win_width = win10 - win00;

   if (mode == 1) {
        Op_GirfEC_PC *opEC = new Op_GirfEC_PC(N, 1, dt, H0, win_width, tile_pre, tile_post);
        opEC->set_params(excite0, excite1, win00, win01, win10, win11);
        opEC->set_params(tol);
        // opEC->spec_norm2(0) = weight;
        all_op.push_back(opEC);
    }
}

//////////////////////////////
// --------------------------- op_sqdist

void GroptParams::add_sqdiff_ref(std::vector<double> &ref_in)
{
    if (ref_in.size() != N) {
        std::cout << "Warning!!! add_sqdiff_ref ref.size() != N" << std::endl;
    }

    Op_SqDist *opSQ = new Op_SqDist(N, Naxis, dt);
    opSQ->ref = Eigen::VectorXd::Map(&ref_in[0], ref_in.size());
    all_op.push_back(opSQ);

    std::cout << ref_in.size() << "  " << ref_in[0] << std::endl;

}


//////////////////////////////
// --------------------------- op_fft_sqdist

void GroptParams::add_fft_sqdiff_mod(int N_in, double *mod_in)
{
    
    Eigen::VectorXd mod;
    mod.setZero(N_in);
    for (int i=0; i<N_in; i++) {
        mod(i) = mod_in[i];
    }
    
    
    if (N_in != N) {
        std::cout << "Warning!!! add_fft_sqdiff_ref N_in != N" << std::endl;
    }

    Op_FFT_SqDist *opFSQ = new Op_FFT_SqDist(N, Naxis, dt);
    opFSQ->mod = mod;
    all_op.push_back(opFSQ);
}

//////////////////////////////
// --------------------------- op_duty

void GroptParams::add_obj_duty(double weight)
{
    Op_Duty *opD = new Op_Duty(N, Naxis, dt);
    opD->weight(0) = weight;
    all_obj.push_back(opD);
}


//////////////////////////////
// --------------------------- op_bval
void GroptParams::add_obj_bval(double weight)
{
    Op_BVal *opB = new Op_BVal(N, Naxis, dt);
    opB->weight(0) = weight;
    opB->set_set_vals(set_vals);
    opB->set_inv_vec(inv_vec);
    opB->set_fixer(fixer);
    all_obj.push_back(opB);
}


void GroptParams::add_op_bval(double _bval)
{
    Op_BVal *opB = new Op_BVal(N, Naxis, dt);
    opB->set_params(_bval);
    // opB->disable_checks = true;
    all_op.push_back(opB);
}


//////////////////////////////
// --------------------------- op_SAFE
void GroptParams::add_op_SAFE(double safe_thresh)
{
    Op_SAFE *opF = new Op_SAFE(N, Naxis, dt);
    opF->set_params(safe_thresh);   
    all_op.push_back(opF);
}

void GroptParams::add_op_SAFE(double _tau1, double _tau2, double _tau3, double _a1, double _a2, double _a3, double _stim_limit, double _g_scale, double _stim_thresh)
{
    Op_SAFE *opF = new Op_SAFE(N, Naxis, dt);
    opF->set_params(_tau1, _tau2, _tau3, _a1, _a2, _a3, _stim_limit, _g_scale, _stim_thresh);   
    all_op.push_back(opF);
}


//////////////////////////////
// --------------------------- op_eddy
void GroptParams::add_op_eddy(double _lam_in, double _tol_in)
{
    Op_Eddy *opE = new Op_Eddy(N, Naxis, dt, 1);
    opE->prep_A(_lam_in, _tol_in);
    all_op.push_back(opE); 
}

void GroptParams::add_op_eddy(double _lam_in)
{
    this->add_op_eddy(_lam_in, 1.e-2);
}


//////////////////////////////
// --------------------------- op_PNS
void GroptParams::add_op_PNS(double stim_thresh)
{
    Op_PNS *opP = new Op_PNS(N, Naxis, dt);
    opP->set_params(stim_thresh);
    all_op.push_back(opP); 
}




void GroptParams::set_constraint_vals(std::string op_name, double target_in, double tol_in, double cushion_in)
{
    for(unsigned int i = 0; i < all_op.size(); i++)
    {
        if (all_op[i]->name == op_name) {
            if (all_op[i]->tol.size() > 1) {
                std::cout << "Warning!!! The set_constraint_vals function only operates on the first value" << std::endl;
            }

            all_op[i]->cushion = cushion_in;

            all_op[i]->target(0) = target_in;
            all_op[i]->tol0(0) = tol_in;
            all_op[i]->tol(0) = (1.0-all_op[i]->cushion) * all_op[i]->tol0(0);

            if (all_op[i]->balanced) {
                all_op[i]->balance_mod(0) = 1.0 / all_op[i]->tol(0);
            } else {
                all_op[i]->balance_mod(0) = 1.0;
            }
        }
    }
}




void GroptParams::optimize()
{
    if (!moment_axis.empty()) {
        finish_moments();
    }

    X0.setOnes(Naxis*N);
    X0.array() *= inv_vec.array() * fixer.array() * gmax/10.0;

    for(int i = 0; i < Naxis*N; i++) {
        if (!isnan(set_vals(i))) {
            X0(i) = set_vals(i);
        }
    }

    run_optimization(*this, out);

}

void GroptParams::optimize(int N_X0, double *_X0)
{
    if (!moment_axis.empty()) {
        finish_moments();
    }
    
    if (N_X0 != Naxis*N) {
        std::cout << "Warning!!! add_fft_sqdiff_ref N_in != N" << std::endl;
    }

    X0.setOnes(N_X0);
    
    for (int i=0; i<N_X0; i++) {
        X0(i) = _X0[i];
    }
    
    for(int i = 0; i < Naxis*N; i++) {
        if (!isnan(set_vals(i))) {
            X0(i) = set_vals(i);
        }
    }

    run_optimization(*this, out);

}

double GroptParams::get_opt_time() 
{
    return elapsed_us.count();
}

void GroptParams::get_out(std::vector<double> &out_vec)
{
    out_vec.resize(out.size());
    for(int i = 0; i < out.size(); i++) {
        out_vec[i] = out(i);
    }
}

void GroptParams::get_debugger(std::vector<int> &sizes, 
                                std::vector<double> &out_x0, 
                                std::vector<double> &out_x1, 
                                std::vector<double> &out_x2, 
                                std::vector<double> &out_weights,
                                std::vector<int> &out_cgiter,  
                                std::vector<std::string> &out_names)
{

    int N, Nx, Nw;

    // -------- Copy X  
    N = debugger.hist_x0.size();
    Nx = debugger.hist_x0[0].size();

    sizes.push_back(N);
    sizes.push_back(Nx);

    std::cout << "N = " << N << "  Nx = " << Nx << std::endl;

    out_x0.resize(N*Nx);
    out_x1.resize(N*Nx);
    out_x2.resize(N*Nx);
    for(int i = 0; i < N; i++) {
        for(int j = 0; j < Nx; j++) {
            out_x0[i*Nx + j] = debugger.hist_x0[i](j);
            out_x1[i*Nx + j] = debugger.hist_x1[i](j);
            out_x2[i*Nx + j] = debugger.hist_x2[i](j);
        }
    }

    // -------- Copy names
    N = debugger.op_names.size();
    out_names.resize(N);
    for(int i = 0; i < N; i++) {
        out_names[i] = debugger.op_names[i];
    }

    // -------- Copy weights
    N = debugger.hist_weight.size();
    Nx = debugger.hist_weight[0].size();
    Nw = 5;

    sizes.push_back(N);
    sizes.push_back(Nx);
    sizes.push_back(Nw);


    out_weights.resize(N*Nx*Nw);
    for(int i = 0; i < N; i++) {
        for(int j = 0; j < Nx; j++) {
            out_weights[i*Nx*Nw + j*Nw + 0] = debugger.hist_weight[i][j];
            out_weights[i*Nx*Nw + j*Nw + 1] = debugger.hist_gamma[i][j];
            out_weights[i*Nx*Nw + j*Nw + 2] = debugger.hist_feas[i][j];
            out_weights[i*Nx*Nw + j*Nw + 3] = debugger.hist_pre_resid[i][j];
            out_weights[i*Nx*Nw + j*Nw + 4] = debugger.hist_post_resid[i][j];
        }
    }

    // -------- Copy cgiter
    N = debugger.hist_cgiter.size();
    out_cgiter.resize(N);
    for(int i = 0; i < N; i++) {
        out_cgiter[i] = debugger.hist_cgiter[i];
    }
}   

void GroptParams::init_all_vals()
{
    for (int i = 0; i < all_op.size(); i++) {
        all_op[i]->init_vals( e_corr, rw_eps, rw_scalelim, rw_interval, weight_min, weight_max, 
                              do_gamma, do_weight, do_scalelim, weight_init, gamma_init,
                              set_vals, inv_vec, fixer);
    }

    for (int i = 0; i < all_obj.size(); i++) {
        all_obj[i]->init_vals( e_corr, rw_eps, rw_scalelim, rw_interval, weight_min, weight_max, 
                              do_gamma, do_weight, do_scalelim, weight_init, gamma_init,
                              set_vals, inv_vec, fixer);
    }
}

// Use this function to propogate the values to the individual constraints
void GroptParams::update_vals()
{
    for (int i = 0; i < all_op.size(); i++) {
        all_op[i]->rw_scalelim = rw_scalelim;
        all_op[i]->rw_interval = rw_interval;
        all_op[i]->rw_eps = rw_eps;
        all_op[i]->e_corr = e_corr;
        all_op[i]->weight_min = weight_min;
        all_op[i]->weight_max = weight_max;
    }
}

void GroptParams::set_vecs()
{
    for (int i = 0; i < all_op.size(); i++) {
        all_op[i]->set_set_vals(set_vals);
        all_op[i]->set_inv_vec(inv_vec);
        all_op[i]->set_fixer(fixer);
    }

    for (int i = 0; i < all_obj.size(); i++) {
        all_obj[i]->set_set_vals(set_vals);
        all_obj[i]->set_inv_vec(inv_vec);
        all_obj[i]->set_fixer(fixer);
    }
}

void GroptParams::defaults_diffusion()
{
    rw_scalelim = 1.5;
    rw_interval = 16;
    rw_eps = 1.0e-16;

    grw_interval = 16;
    grw_start = 32;
    grw_scale = 8.0;

    cg_niter = 50;

    e_corr = 0.6;
    weight_min = 1.0e-4;
    weight_max = 1.0e64;
    d_obj_thresh = 1e-4;

    update_vals();
}

void GroptParams::set_verbose(int level) {
    LOG_LEVEL = static_cast<log_level_t>(level);
}

void GroptParams::interp_from_gparams(GroptParams &gparams_in, Eigen::VectorXd &X_in)
{
    double mod = 0.5;
    interp_vec2vec(X_in, X0);
    for (int i = 0; i < all_op.size(); i++) {
        all_op[i]->weight = gparams_in.all_op[i]->weight; 
        // all_op[i]->weight.setOnes();
        // all_op[i]->gamma = gparams_in.all_op[i]->gamma; 
        all_op[i]->gamma.setOnes();
        interp_vec2vec(gparams_in.all_op[i]->U0, all_op[i]->U0);
        interp_vec2vec(gparams_in.all_op[i]->Y0, all_op[i]->Y0);
        std::cout << "interp_from_gparams " << i << "  " << gparams_in.all_op[i]->U0.squaredNorm() << "  " << all_op[i]->U0.squaredNorm() << std::endl;
        if (all_op[i]->do_rw) {
            all_op[i]->weight *= mod;
            gparams_in.all_op[i]->U0 *= mod;
        }
    }

    for (int i = 0; i < all_obj.size(); i++) {        
        all_obj[i]->weight = gparams_in.all_obj[i]->weight;  
        // all_obj[i]->gamma = gparams_in.all_obj[i]->gamma; 
        // all_obj[i]->weight.setOnes();
        all_obj[i]->gamma.setOnes();
        interp_vec2vec(gparams_in.all_obj[i]->U0, all_obj[i]->U0);
        interp_vec2vec(gparams_in.all_obj[i]->Y0, all_obj[i]->Y0);
        std::cout << "interp_from_gparams " << i << "  " << all_obj[i]->U0.squaredNorm() << std::endl;
    }

}

}  // end namespace Gropt
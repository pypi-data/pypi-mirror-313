#include <iostream> 
#include <string>
#include <math.h>  
#include <Eigen/Dense>

#include "op_main.hpp"
#include "logging.hpp"

#define N_HIST_MAX 100000

namespace Gropt {

GroptOperator::GroptOperator(int N, int Naxis, double dt, int Nc, int Ax_size, bool row_constraints) 
    : N(N),
    Naxis(Naxis), 
    dt(dt), 
    Nc(Nc), 
    Ax_size(Ax_size), 
    row_constraints(row_constraints)
{
    name = "OperatorMain";

    cushion = 1.0e-3;

    Ntot = Naxis * N;

    rot_variant = true;
    balanced = true;
    do_rw = false;

    // We can maybe start weights at 10?
    weight.setOnes(Nc);
    gamma.setOnes(Nc);

    tol0.setOnes(Nc);
    tol.setOnes(Nc);
    target.setOnes(Nc);
    
    spec_norm2.setOnes(Nc);
    spec_norm.setOnes(Nc);
    balance_mod.setOnes(Nc);

    // These should just be std vectors and dynamicaly sized?
    hist_check.setZero(Nc, N_HIST_MAX);
    hist_feas.setZero(Nc, N_HIST_MAX);
    hist_obj.setZero(Nc, N_HIST_MAX);

    x_temp.setZero(Ntot);
    Ax_temp.setZero(Ax_size);

    Y0.setZero(Ax_size);
    Y1.setZero(Ax_size);
    U0.setZero(Ax_size);
    U1.setZero(Ax_size);

    s.setZero(Ax_size);
    xbar.setZero(Ax_size);

    Uhat00.setZero(Ax_size);
    U00.setZero(Ax_size);
    s00.setZero(Ax_size);
    Y00.setZero(Ax_size);

    r_feas.setZero(Nc);
    feas_temp.setZero(Ax_size);
    feas_check.setZero(Nc);

    // Everything below here will generally be reset from gparams during init(), so changing
    // anything might have no effect
    e_corr = 0.5;
    rw_eps = 1e-6;
    rw_scalelim = 2.0;
    rw_interval = 8;

    weight_min = 1.0e-4;
    weight_max = 1.0e4;

    do_gamma = true;
    do_weight = true;
    do_scalelim = true; 

    weight_init = 1.0;
    gamma_init = 1.0;

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


    allocate_rwvecs();
}

GroptOperator::~GroptOperator() {}

void GroptOperator::allocate_rwvecs()
{
    int alloc_size;
    if (!(row_constraints)) {
        alloc_size = Ax_size;
    } else {
        alloc_size = 1;
    }
    
    uhat1.setZero(alloc_size);
    duhat.setZero(alloc_size);
    du.setZero(alloc_size);
    dhhat.setZero(alloc_size);
    dghat.setZero(alloc_size);
}


void GroptOperator::reweight(int iiter)
{
    for (int ii = 0; ii < Nc; ii++) {
        // if (hist_check(ii,iiter) == 0) {continue;}

        double rho0 = weight(ii);

        if (!(row_constraints)) {
            uhat1.array() = U0.array() + rho0*(Y0.array() - s.array());
            duhat.array() = uhat1.array() - Uhat00.array();
            du.array() = U1.array() - U00.array();
            dhhat.array() = s.array() - s00.array();
            dghat.array() = -(Y1.array() - Y00.array());
        } else {
            // These "vectors" are just 1 element doubles, but keep 
            // them vectors for compatibility with the rest of this function
            uhat1(0) = U0(ii) + rho0*(Y0(ii) - s(ii));
            duhat(0) = uhat1(0) - Uhat00(ii);
            du(0) = U1(ii) - U00(ii);
            dhhat(0) = s(ii) - s00(ii);
            dghat(0) = -(Y1(ii) - Y00(ii));
        }

        double norm_dhhat_duhat = dhhat.norm()*duhat.norm();
        double dot_dhhat_dhhat = dhhat.dot(dhhat);
        double dot_dhhat_duhat = dhhat.dot(duhat);

        
        double alpha_corr = 0.0;
        if ((norm_dhhat_duhat > rw_eps) 
            && (dot_dhhat_dhhat > rw_eps) 
            && (dot_dhhat_duhat > rw_eps)) {
                alpha_corr = dot_dhhat_duhat/norm_dhhat_duhat;
            }

        double norm_dghat_du = dghat.norm()*du.norm();
        double dot_dghat_dghat = dghat.dot(dghat);
        double dot_dghat_du = dghat.dot(du);

        double beta_corr = 0.0;
        if ((norm_dghat_du > rw_eps) 
            && (dot_dghat_dghat > rw_eps) 
            && (dot_dghat_du > rw_eps)) {
                beta_corr = dot_dghat_du/norm_dghat_du;
            }

        bool pass_alpha = false;
        bool pass_beta = false;

        double alpha = 0.0;
        if (alpha_corr > e_corr) {
            pass_alpha = true;
            double alpha_mg = dot_dhhat_duhat/dot_dhhat_dhhat;
            double alpha_sd = duhat.dot(duhat)/dot_dhhat_duhat;
            if (2.0*alpha_mg > alpha_sd) {
                alpha = alpha_mg;
            } else {
                alpha = alpha_sd - 0.5*alpha_mg;
            }
        }

        double beta = 0.0;
        if (beta_corr > e_corr) {
            pass_beta = true;
            double beta_mg = dot_dghat_du/dot_dghat_dghat;
            double beta_sd = du.dot(du)/dot_dghat_du;
            if (2.0*beta_mg > beta_sd) {
                beta = beta_mg;
            } else {
                beta = beta_sd - 0.5*beta_mg;
            }
        }

        double step_g1 = 0.0;
        double gamma1 = 0.0;
        if ((pass_alpha == true) && (pass_beta == true)) {
            step_g1 = sqrt(alpha*beta);
            gamma1 = 1.0 + 2.0*sqrt(alpha*beta)/(alpha+beta);
        } else if ((pass_alpha == true) && (pass_beta == false)) {
            step_g1 = alpha;
            gamma1 = 1.9;
        } else if ((pass_alpha == false) && (pass_beta == true)) {
            step_g1 = beta;
            gamma1 = 1.1;
        } else {
            step_g1 = rho0;
            gamma1 = 1.5;
        }

        if (do_weight == true) {
            if ((do_scalelim == true) && (step_g1 > rw_scalelim*weight(ii))) {
                weight(ii) *= rw_scalelim;
            } else if ((do_scalelim == true) && (rw_scalelim*step_g1 < weight(ii))) {
                weight(ii) *= 1.0/rw_scalelim;
            } else {   
                weight(ii) = step_g1;
            }
        }

        if (do_gamma == true) {
            gamma(ii) = gamma1;
        }

        if (!(row_constraints)) {
            Uhat00 = uhat1;
            U00 = U1;
            s00 = s;
            Y00 = Y1;
        } else {
            Uhat00(ii) = uhat1(0);
            U00(ii) = U1(ii);
            s00(ii) = s(ii);
            Y00(ii) = Y1(ii);
        }

        log_print(LOG_DEBUG, "iiter: %d  name: %s  ii: %d  alpha_corr: %.2e  beta_corr: %.2e", iiter, name.c_str(), ii, alpha_corr, beta_corr);
        log_print(LOG_DEBUG, "      weight: %.2e -> %.2e", rho0, weight(ii));
    }
}


void GroptOperator::check(Eigen::VectorXd &X, int iiter)
{
    if ((row_constraints)) {
        feas_check.array() = (X.array()/balance_mod.array()*spec_norm.array() - target.array()).abs();
    } else {
        feas_check(0) = (X.array()/balance_mod(0)*spec_norm(0) - target(0)).abs().maxCoeff();
    }

    for (int i = 0; i < feas_check.size(); i++) {
        if (feas_check[i] > tol0[i]) {
            hist_check(i, iiter) = 1.0;
        } else {
            hist_check(i, iiter) = 0.0;
        }
    }
}


// This is for warm starting (many vectors should not be zero here, they are previously computed)
// From trial and error all we really need is U0, weights and gamma to carry over.
// Y0 needs to be carried over, or reinitialized from X0, I am not sure which works better yet.
void GroptOperator::soft_init(Eigen::VectorXd &X)
{   
    // weight.setOnes();
    // gamma.setOnes();
    
    hist_check.setZero();
    hist_feas.setZero();
    hist_obj.setZero();

    x_temp.setZero();
    Ax_temp.setZero();

    // Y0.setZero();
    Y1.setZero();
    // U0.setZero();
    U1.setZero();

    s.setZero();
    xbar.setZero();

    Uhat00.setZero();
    U00.setZero();
    s00.setZero();
    Y00.setZero();
    
    uhat1.setZero();
    duhat.setZero();
    du.setZero();
    dhhat.setZero();
    dghat.setZero();
    
    // prep_y(X);
}


// This resets all of the vectors, but keeps the parameters in place
void GroptOperator::init(Eigen::VectorXd &X, bool do_init)
{   
    if (!do_init) {
        soft_init(X);
    } else {
        weight.setOnes();
        weight *= weight_init;
        gamma.setOnes();
        gamma *= gamma_init;
        
        hist_check.setZero();
        hist_feas.setZero();
        hist_obj.setZero();

        x_temp.setZero();
        Ax_temp.setZero();

        Y0.setZero();
        Y1.setZero();
        U0.setZero();
        U1.setZero();

        s.setZero();
        xbar.setZero();

        Uhat00.setZero();
        U00.setZero();
        s00.setZero();
        Y00.setZero();
        
        uhat1.setZero();
        duhat.setZero();
        du.setZero();
        dhhat.setZero();
        dghat.setZero();
        prep_y(X);
    }
}


// This resets all of the vectors, but keeps the parameters in place, sets additional things from
// gropt_params
void GroptOperator::init_vals(double e_corr_in, double rw_eps_in, 
                                double rw_scalelim_in, int rw_interval_in, 
                                double weight_min_in, double weight_max_in,
                                bool do_gamma_in, bool do_weight_in, bool do_scalelim_in, double weight_init_in, double gamma_init_in,
                                Eigen::VectorXd &set_vals_in,
                                Eigen::VectorXd &inv_vec_in,
                                Eigen::VectorXd &fixer_in)
{   

    e_corr = e_corr_in;
    rw_eps = rw_eps_in;
    rw_scalelim = rw_scalelim_in;
    rw_interval = rw_interval_in;

    weight_min = weight_min_in;
    weight_max = weight_max_in;
    
    this->set_inv_vec(inv_vec_in);
    this->set_set_vals(set_vals_in);
    this->set_fixer(fixer_in);

    do_gamma = do_gamma_in;
    do_weight = do_weight_in;
    do_scalelim = do_scalelim_in;

    weight_init = weight_init_in;
    gamma_init = gamma_init_in;
}


void GroptOperator::prep_y(Eigen::VectorXd &X)
{   
    forward(X, Y0, 0, 1, false);
    Y00 = Y0;
}


void GroptOperator::forward(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool no_balance)
{
    out = X;
}


void GroptOperator::transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool repeat_balance)
{
    log_print(LOG_WARNING, "WARNING: GroptOperator::transpose(), this shouldnt happen");
    out = X;
}


void GroptOperator::prox(Eigen::VectorXd &X)
{
}


void GroptOperator::get_obj(Eigen::VectorXd &X, int iiter)
{
}


void GroptOperator::update(Eigen::VectorXd &X, int iiter)
{
    forward(X, s, 0, 1, false);

    check(s, iiter);

    // Is there a better way to handle the single element gamma?  
    // We could switch it back to doubles, but I don't like the type mixing.
    if (!(row_constraints)) {
        xbar = gamma(0) * s + (1.0-gamma(0))*Y0;
        Y1 = xbar - U0/weight(0);
    } else {
        xbar.array() = gamma.array() * s.array() + (1.0-gamma.array())*Y0.array();
        Y1.array() = xbar.array() - U0.array()/weight.array();
    }

    prox(Y1);

    if (!(row_constraints)) {
        U1.array() = U0 + weight(0)*(Y1-xbar);
    } else {
        U1.array() = U0.array() + weight.array()*(Y1.array()-xbar.array());
    }

    // Update feasibility metrics

    get_feas(s, iiter);

    // cout << "Reweighting " << name << "  --  " << weight.transpose() << "  --  " << gamma.transpose() <<endl;
    // Do reweighting of weight and gamma
    if ((do_rw) && (iiter > rw_interval) && (iiter%rw_interval == 0)) {
        reweight(iiter);
    }

    // Clip weights between weight_min and weight_max
    for (int i = 0; i < weight.size(); i++) {
        weight(i) = weight(i) < weight_min ? weight_min:weight(i);
        weight(i) = weight(i) > weight_max ? weight_max:weight(i);
    }

    // cout << "            " << name << "  --  " << weight.transpose() << "  --  " << gamma.transpose() <<endl;

    U0 = U1;
    Y0 = Y1;

}


void GroptOperator::add2b(Eigen::VectorXd &b)
{
    Ax_temp.setZero();
    x_temp.setZero();
    
    if (!(row_constraints)) {
        Ax_temp = U0 + weight(0)*Y0;
    } else {
        Ax_temp.array() = U0.array() + weight.array()*Y0.array();
    }
    transpose(Ax_temp, x_temp, 0, 1, false);
    b += x_temp;
}

void GroptOperator::obj_add2b(Eigen::VectorXd &b)
{
    return;
}

Eigen::VectorXd GroptOperator::get_b()
{   
    Eigen::VectorXd b;
    
    if (!(row_constraints)) {
        b = U0/sqrt(weight(0)) + sqrt(weight(0))*Y0;
    } else {
        b.array() = U0.array()/weight.array().sqrt() + weight.array().sqrt()*Y0.array();
    }
    // log_print(LOG_DEBUG, "get_b   U0 = %8.1e   weight = %8.1e  Y0 = %8.1e",U0.norm(), weight.norm(), Y0.norm());
    return b;
}

Eigen::VectorXd GroptOperator::get_obj_b()
{   
    Ax_temp.setZero();
    return Ax_temp;
}

void GroptOperator::get_feas(Eigen::VectorXd &s, int iiter)
{
    feas_temp = s;
    prox(feas_temp);
    feas_temp = s - feas_temp;
    if (Nc == 1) {
        r_feas(0) = feas_temp.norm()/(s.norm() + 1.0e-10);
    } else {
        r_feas.array() = feas_temp.array()/(s.array() + 1.0e-10);
    }
    hist_feas.col(iiter) = r_feas;
}



Eigen::VectorXd GroptOperator::get_AtAx(Eigen::VectorXd &X, int apply_weight)
{   
    Ax_temp.setZero();
    x_temp.setZero();
    forward(X, Ax_temp, apply_weight, 2, false);
    transpose(Ax_temp, x_temp, 0, 0, false);
    return x_temp;
}


void GroptOperator::add2AtAx(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight)
{
    Ax_temp.setZero();
    x_temp.setZero();
    forward(X, Ax_temp, apply_weight, 2, false);
    transpose(Ax_temp, x_temp, 0, 0, false);
    out += x_temp;
}


void GroptOperator::add2AtAx(Eigen::VectorXd &X, Eigen::VectorXd &out)
{
    add2AtAx(X, out, 2);
}


void GroptOperator::set_inv_vec(Eigen::VectorXd &inv_vec_in)
{
    inv_vec = inv_vec_in;
}


void GroptOperator::set_fixer(Eigen::VectorXd &fixer_in)
{
    fixer = fixer_in;
}

void GroptOperator::set_set_vals(Eigen::VectorXd &set_vals_in)
{
    set_vals = set_vals_in;
}

void GroptOperator::change_cushion(double cushion_in)
{
    cushion = cushion_in;
    
    for (int i = 0; i < tol0.size(); i++) {
    
        tol(i) = (1.0-cushion) * tol0(i);
            
        if (balanced) {
            balance_mod(i) = 1.0 / tol(i);
        } else {
            balance_mod(i) = 1.0;
        }

    }
}


}  // close "namespace Gropt"
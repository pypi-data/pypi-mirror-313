#include <iostream> 
#include <string>
#include <math.h>  
#include "Eigen/Dense"

#include "op_safe.hpp"
#include "logging.hpp"

namespace Gropt {

Op_SAFE::Op_SAFE(int N, int Naxis, double dt) 
    : GroptOperator(N, Naxis, dt, 1, 3*Naxis*N, false)
{
    name = "SAFE";
    do_rw = true; 
    rot_variant = true;
    
    // Proper SAFE model is not stable in Krylov optimization, Setting to false removes the abs(), which
    // makes it converge nicely, but does not give the proper SAFE, though in every example I have tried
    // it still matches *PEAK* SAFE (it is the lower safe values that might not match up)
    true_safe = false;  

    stim_thresh = 1.0;

    signs.setZero(Naxis*N);
    stim1.setZero(Naxis*N);
    stim2.setZero(Naxis*N);
    stim3.setZero(Naxis*N);

    spec_norm2(0) = 4.0/dt/dt;
    spec_norm(0) = sqrt(spec_norm2(0));
}

void Op_SAFE::set_params() {
    set_params(1.0);
}

void Op_SAFE::set_params(double _stim_thresh) 
{
    stim_thresh = _stim_thresh;

    tau1(0) = 0.2/1000.0;
    tau2(0) = 0.03/1000.0;
    tau3(0) = 3/1000.0;
    a1(0) = 0.4;
    a2(0) = 0.1;
    a3(0) = 0.5;
    stim_limit(0) = 30;
    g_scale(0) = 0.35;

    tau1(1) = 1.5/1000.0;
    tau2(1) = 2.5/1000.0;
    tau3(1) = 0.15/1000.0;
    a1(1) = 0.55;
    a2(1) = 0.15;
    a3(1) = 0.3;
    stim_limit(1) = 15;
    g_scale(1) = 0.31;

    tau1(2) = 2/1000.0;
    tau2(2) = 0.12/1000.0;
    tau3(2) = 1/1000.0;
    a1(2) = 0.42;
    a2(2) = 0.4;
    a3(2) = 0.18;
    stim_limit(2) = 25;
    g_scale(2) = 0.25;

    for (int i = 0; i < 3; i++) {
        alpha1(i) = dt/(tau1(i) + dt);
        alpha2(i) = dt/(tau2(i) + dt);
        alpha3(i) = dt/(tau3(i) + dt);
    }

    target(0) = 0;
    tol0(0) = stim_thresh;
    tol(0) = (1.0-cushion) * tol0(0);

    if (balanced) {
        balance_mod(0) = 1.0 / tol(0);
    } else {
        balance_mod(0) = 1.0;
    }
}

void Op_SAFE::set_params(double _tau1, double _tau2, double _tau3, double _a1, double _a2, double _a3, double _stim_limit, double _g_scale, double _stim_thresh)
{

    tau1(0) = _tau1;
    tau2(0) = _tau2;
    tau3(0) = _tau3;
    a1(0) = _a1;
    a2(0) = _a2;
    a3(0) = _a3;
    stim_limit(0) = _stim_limit;
    g_scale(0) = _g_scale;

    alpha1(0) = dt/(tau1(0) + dt);
    alpha2(0) = dt/(tau2(0) + dt);
    alpha3(0) = dt/(tau3(0) + dt);

    target(0) = 0;
    tol0(0) = _stim_thresh;
    tol(0) = (1.0-cushion) * tol0(0);

    if (balanced) {
        balance_mod(0) = 1.0 / tol(0);
    } else {
        balance_mod(0) = 1.0;
    }
    
}

void Op_SAFE::forward(Eigen::VectorXd &X, Eigen::VectorXd &out, 
                         int apply_weight, int norm, bool no_balance)
{
    for (int j = 0; j < Naxis; j++) {
        out(j*N) = X(j*N)/dt;
        for (int i = 1; i < N; i++) {
            out(j*N+i) = (X(j*N+i) - X(j*N+i-1))/dt;
        }
    }


    for (int i = 0; i < signs.size(); i++) {
        if (out(i) < 0) {signs(i) = -1.0;}
        else {signs(i) = 1.0;}
    }


    stim1.setZero();
    for (int j = 0; j < Naxis; j++) {
        stim1(j*N) = alpha1(j) * out(j*N);
        for (int i = 1; i < N; i++) {
            stim1(j*N+i) = alpha1(j) * out(j*N+i) + (1.0-alpha1(j)) * stim1(j*N+i-1);
        }
    }
    if (true_safe) {
        for (int i = 0; i < stim1.size(); i++) {
            stim1(i) = abs(stim1(i));
        }
    }


    stim2.setZero();
    for (int j = 0; j < Naxis; j++) {
        stim2(j*N) = alpha2(j) * abs(out(j*N));
        for (int i = 1; i < N; i++) {
            stim2(j*N+i) = alpha2(j) * abs(out(j*N+i)) + (1.0-alpha2(j)) * stim2(j*N+i-1);
        }
    }
    if (!true_safe) {
        for (int i = 0; i < stim2.size(); i++) {
            stim2(i) = signs(i) * stim2(i);
        }
    }



    stim3.setZero();
    for (int j = 0; j < Naxis; j++) {
        stim3(j*N) = alpha3(j) * out(j*N);
        for (int i = 1; i < N; i++) {
            stim3(j*N+i) = alpha3(j) * out(j*N+i) + (1.0-alpha3(j)) * stim3(j*N+i-1);
        }
    }
    if (true_safe) {
        for (int i = 0; i < stim3.size(); i++) {
            stim3(i) = abs(stim3(i)); 
        }
    }



    // for (int j = 0; j < Naxis; j++) {
    //     for (int i = 0; i < N; i++) {
    //         out(j*N+i) = (a1(j)*stim1(j*N+i) + a2(j)*stim2(j*N+i) + a3(j)*stim3(j*N+i)) / stim_limit(j) * g_scale(j);
    //     }
    // }


    for (int j = 0; j < Naxis; j++) {
        for (int i = 0; i < N; i++) {
            out(j*3*N+i) = a1(j)*stim1(j*N+i) / stim_limit(j) * g_scale(j);
            out(j*3*N+i+N) = a2(j)*stim2(j*N+i) / stim_limit(j) * g_scale(j);
            out(j*3*N+i+2*N) = a3(j)*stim3(j*N+i) / stim_limit(j) * g_scale(j);
        }
    }



    if (apply_weight == 2) {
        out.array() *= weight(0);
    } else if (apply_weight == 1) {
        out.array() *= sqrt(weight(0));
    }

    if (balanced && !no_balance) {
        out.array() *= balance_mod(0);
    }

    if (norm == 2) {
        out.array() /= spec_norm2(0);
    } else if (norm == 1) {
        out.array() /= spec_norm(0);
    }

}

void Op_SAFE::transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, 
                           int apply_weight, int norm, bool repeat_balance)
{
    x_temp.setZero();
    for (int j = 0; j < Naxis; j++) {
        for (int i = 0; i < N; i++) {
            x_temp(j*N+i) = X(j*3*N+i) + X(j*3*N+i+N) + X(j*3*N+i+2*N);
        }
    }

    
    for (int i = 0; i < signs.size(); i++) {
        if (x_temp(i) < 0) {signs(i) = -1.0;}
        else {signs(i) = 1.0;}
    }

    // for (int j = 0; j < Naxis; j++) {
    //     for (int i = 0; i < N; i++) {
    //         if (X(j*3*N+i+N) < 0) {signs(j*N+i) = -1.0;}
    //         else {signs(j*N+i) = 1.0;}
    //     }
    // }


    stim1.setZero();
    for (int j = 0; j < Naxis; j++) {
        stim1(j*N+N-1) = alpha1(j) * x_temp(j*N+N-1);
        for (int i = N-2; i >= 0; i--) {
            stim1(j*N+i) = alpha1(j) * x_temp(j*N+i) + (1-alpha1(j)) * stim1(j*N+i+1);
        }
    }
    if (true_safe) {
        for (int i = 0; i < x_temp.size(); i++) {
            stim1(i) = abs(stim1(i));
        }
    }


    stim2.setZero();
    for (int j = 0; j < Naxis; j++) {
        stim2(j*N+N-1) = alpha2(j) * abs(x_temp(j*N+N-1));
        for (int i = N-2; i >= 0; i--) {
            stim2(j*N+i) = alpha2(j) * abs(x_temp(j*N+i)) + (1-alpha2(j)) * stim2(j*N+i+1);
        }
    }
    if (!true_safe) {
        for (int i = 0; i < x_temp.size(); i++) {
            stim2(i) = signs(i) * stim2(i);
        }
    }



    stim3.setZero();
    for (int j = 0; j < Naxis; j++) {
        stim3(j*N+N-1) = alpha3(j) * x_temp(j*N+N-1);
        for (int i = N-2; i >= 0; i--) {
            stim3(j*N+i) = alpha3(j) * x_temp(j*N+i) + (1-alpha3(j)) * stim3(j*N+i+1);
        }
    }
    if (true_safe) {
        for (int i = 0; i < x_temp.size(); i++) {
            stim3(i) = abs(stim3(i));
        }
    }


    for (int j = 0; j < Naxis; j++) {
        for (int i = 0; i < N; i++) {
            // out(j*N+i) = signs(j*N+i) * (a1(j)*stim1(j*N+i) + a2(j)*stim2(j*N+i) + a3(j)*stim3(j*N+i)) / stim_limit(j) * g_scale(j);
            out(j*N+i) = (a1(j)*stim1(j*N+i) + a2(j)*stim2(j*N+i) + a3(j)*stim3(j*N+i)) / stim_limit(j) * g_scale(j);
        }
    }


    for (int j = 0; j < Naxis; j++) {
        for (int i = 0; i < N-1; i++) {
            out(j*N+i) = (out(j*N+i) - out(j*N+i+1))/dt;
        }
        out(j*N+N-1) = out(j*N+N-1)/dt;
    }
    

    if (norm == 2) {
        out.array() /= spec_norm2(0);
    } else if (norm == 1) {
        out.array() /= spec_norm(0);
    }

    if (balanced) {
        if (repeat_balance) {
            out.array() *= balance_mod(0);
        } else {
            out.array() /= balance_mod(0);
        }
    }

    if (apply_weight == 2) {
        out.array() *= weight(0);
    } else if (apply_weight == 1) {
        out.array() *= sqrt(weight(0));
    }
 
    out.array() *= fixer.array();

}


void Op_SAFE::prox(Eigen::VectorXd &X)
{

    x_temp.setZero();
    for (int j = 0; j < Naxis; j++) {
        for (int i = 0; i < N; i++) {
            // x_temp(j*N+i) = X(j*3*N+i) + X(j*3*N+i+N) + X(j*3*N+i+2*N);
            x_temp(j*N+i) = abs(X(j*3*N+i)) + abs(X(j*3*N+i+N)) + abs(X(j*3*N+i+2*N));
        }
    }

    if (rot_variant) {
        double lower_bound = balance_mod(0) / spec_norm(0) * (target(0)-tol(0));
        double upper_bound = balance_mod(0) / spec_norm(0) * (target(0)+tol(0));

        for (int j = 0; j < Naxis; j++) {
        for (int i = 0; i < N; i++) {
            
            double val = abs(x_temp(j*N+i));

            if (val > upper_bound) {
                X(j*3*N+i) *= (upper_bound/val);
                X(j*3*N+i+N) *= (upper_bound/val);
                X(j*3*N+i+2*N) *= (upper_bound/val);
            }
        }
        }   
    } else {
        for (int i = 0; i < N; i++) {
            double upper_bound = balance_mod(0) / spec_norm(0) * (target(0)+tol(0));
            
            double val = 0.0;
            for (int j = 0; j < Naxis; j++) {
                val += X(j*N+i)*X(j*N+i);
            }
            val = sqrt(val);

            if (val > upper_bound) {
                for (int j = 0; j < Naxis; j++) {
                    X(j*N+i) *= (upper_bound/val);
                }
            }
        }
    }
}

void Op_SAFE::check(Eigen::VectorXd &X, int iiter)
{
    double check = 0.0;

    x_temp.setZero();
    for (int j = 0; j < Naxis; j++) {
        for (int i = 0; i < N; i++) {
            // x_temp(j*N+i) = X(j*3*N+i) + X(j*3*N+i+N) + X(j*3*N+i+2*N);
            x_temp(j*N+i) = abs(X(j*3*N+i)) + abs(X(j*3*N+i+N)) + abs(X(j*3*N+i+2*N));
        }
    }

    if (rot_variant) {
        for (int i = 0; i < x_temp.size(); i++) {
            double lower_bound = balance_mod(0) / spec_norm(0) * (target(0)-tol0(0));
            double upper_bound = balance_mod(0) / spec_norm(0) * (target(0)+tol0(0));

            if (((x_temp(i) < lower_bound) || (x_temp(i) > upper_bound)) && ((fixer(i) > 0) || (fixer(i+1) > 0))){
                check = 1.0;
            }
        }   
    } else {
        for (int i = 0; i < N; i++) {
            double upper_bound = balance_mod(0) / spec_norm(0) * (target(0)+tol0(0));
            
            double val = 0.0;
            for (int j = 0; j < Naxis; j++) {
                val += x_temp(j*N+i)*x_temp(j*N+i);
            }
            val = sqrt(val);

            if ((val > upper_bound) && ((fixer(i) > 0) || (fixer(i+1) > 0))) {
                check = 1.0;
            }
        }
    }

    hist_check(0, iiter) = check;
}

}  // end namespace Gropt
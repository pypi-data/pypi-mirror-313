#include <iostream> 
#include <string>
#include <math.h>  
#include "Eigen/Dense"

#include "op_gradient.hpp"

namespace Gropt {

Op_Gradient::Op_Gradient(int N, int Naxis, double dt) 
    : GroptOperator(N, Naxis, dt, 1, Naxis*N, false)
{
    name = "Gradient"; 
    do_rw = true;
    balanced = false;
}

void Op_Gradient::set_params(double gmax_in)
{

    target(0) = 0;
    tol0(0) = gmax_in;
    tol(0) = (1.0-cushion) * tol0(0);

    if (balanced) {
        balance_mod(0) = 1.0 / tol(0);
    } else {
        balance_mod(0) = 1.0;
    }

    spec_norm2(0) = 1.0;
    spec_norm(0) = 1.0;
    gmax = gmax_in;

}

void Op_Gradient::forward(Eigen::VectorXd &X, Eigen::VectorXd &out, 
                         int apply_weight, int norm, bool no_balance)
{
    out = X;

    if (apply_weight == 2) {
        out.array() *= weight(0);
    } else if (apply_weight == 1) {
        out.array() *= sqrt(weight(0));
    }

    if (balanced && !no_balance) {
        out.array() *= balance_mod(0);
    }
}

void Op_Gradient::transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, 
                           int apply_weight, int norm, bool repeat_balance)
{
    out = X;

    if (balanced) {
        out.array() /= balance_mod(0);
    }

    
}



void Op_Gradient::prox(Eigen::VectorXd &X)
{

    if (rot_variant) {
        for (int i = 0; i < X.size(); i++) {
            double lower_bound = balance_mod(0) * (target(0)-tol(0));
            double upper_bound = balance_mod(0) * (target(0)+tol(0));
            X(i) = X(i) < lower_bound ? lower_bound:X(i);
            X(i) = X(i) > upper_bound ? upper_bound:X(i);
            
            // This is specific to the Op_Gradient operator
            if (!isnan(set_vals(i))) {
                X(i) = set_vals(i) * balance_mod(0);
            }
        }   
    } else {
        for (int i = 0; i < N; i++) {
            double upper_bound = balance_mod(0) * (target(0)+tol(0));
            
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

        // This is specific to the Op_Gradient operator
        for (int i = 0; i < X.size(); i++) {
            if (!isnan(set_vals(i))) {
                X(i) = set_vals(i) * balance_mod(0);
            }
        }
    }
}


void Op_Gradient::check(Eigen::VectorXd &X, int iiter)
{
    double check = 0.0;

    if (rot_variant) {
        for (int i = 0; i < X.size(); i++) {
            double lower_bound = balance_mod(0) * (target(0)-tol0(0));
            double upper_bound = balance_mod(0) * (target(0)+tol0(0));

            if ((X(i) < lower_bound) || (X(i) > upper_bound) && isnan(set_vals(i))) {
                check = 1.0;
            }
        }   
    } else {
        for (int i = 0; i < N; i++) {
            double upper_bound = balance_mod(0) * (target(0)+tol0(0));
            
            double val = 0.0;
            for (int j = 0; j < Naxis; j++) {
                val += X(j*N+i)*X(j*N+i);
            }
            val = sqrt(val);

            if ((val > upper_bound) && isnan(set_vals(i))) {
                check = 1.0;
            }
        }
    }

    hist_check(0, iiter) = check;

}

}  // close "namespace Gropt"
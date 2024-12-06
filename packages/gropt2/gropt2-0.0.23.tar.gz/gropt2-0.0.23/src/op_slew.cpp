#include <iostream> 
#include <string>
#include <math.h>  
#include "Eigen/Dense"

#include "op_slew.hpp"
#include "logging.hpp"

namespace Gropt {

Op_Slew::Op_Slew(int N, int Naxis, double dt) 
    : GroptOperator(N, Naxis, dt, 1, Naxis*(N-1), false)
{
    name = "Slew";
    do_rw = true; 
}

void Op_Slew::set_params(double smax_in)
{

    target(0) = 0;
    tol0(0) = smax_in;
    tol(0) = (1.0-cushion) * tol0(0);

    if (balanced) {
        balance_mod(0) = 1.0 / tol(0);
    } else {
        balance_mod(0) = 1.0;
    }

    spec_norm2(0) = 4.0/dt/dt;
    spec_norm(0) = sqrt(spec_norm2(0));
    smax = smax_in;

}

void Op_Slew::forward(Eigen::VectorXd &X, Eigen::VectorXd &out, 
                         int apply_weight, int norm, bool no_balance)
{
    for (int j = 0; j < Naxis; j++) {
        for (int i = 0; i < (N-1); i++) {
            out(j*(N-1)+i) = (X(j*N+i+1) - X(j*N+i))/dt;
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

void Op_Slew::transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, 
                           int apply_weight, int norm, bool repeat_balance)
{
    for (int j = 0; j < Naxis; j++) {
        out(j*N+0) = -X(j*(N-1)+0) / dt;
        for (int i = 1; i < (N-1); i++) {
            out(j*N+i) = (X(j*(N-1)+i-1) - X(j*(N-1)+i)) / dt;
        }
        out(j*N+N-1) = X(j*(N-1)+N-2) / dt;
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


void Op_Slew::prox(Eigen::VectorXd &X)
{
    if (rot_variant) {
        for (int i = 0; i < X.size(); i++) {
            double lower_bound = balance_mod(0) / spec_norm(0) * (target(0)-tol(0));
            double upper_bound = balance_mod(0) / spec_norm(0) * (target(0)+tol(0));
            X(i) = X(i) < lower_bound ? lower_bound:X(i);
            X(i) = X(i) > upper_bound ? upper_bound:X(i);
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

void Op_Slew::check(Eigen::VectorXd &X, int iiter)
{
    double check = 0.0;

    if (rot_variant) {
        for (int i = 0; i < X.size(); i++) {
            double lower_bound = balance_mod(0) / spec_norm(0) * (target(0)-tol0(0));
            double upper_bound = balance_mod(0) / spec_norm(0) * (target(0)+tol0(0));

            if (((X(i) < lower_bound) || (X(i) > upper_bound)) && ((fixer(i) > 0) || (fixer(i+1) > 0))){
                check = 1.0;
            }
        }   
    } else {
        for (int i = 0; i < N; i++) {
            double upper_bound = balance_mod(0) / spec_norm(0) * (target(0)+tol0(0));
            
            double val = 0.0;
            for (int j = 0; j < Naxis; j++) {
                val += X(j*N+i)*X(j*N+i);
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
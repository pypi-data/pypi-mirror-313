#include <iostream> 
#include <string>
#include <math.h>  
#include "Eigen/Dense"

#include "op_duty.hpp"

namespace Gropt {

Op_Duty::Op_Duty(int N, int Naxis, double dt) 
    : GroptOperator(N, Naxis, dt, 1, Naxis*N, false)
{
    name = "Duty"; 

    do_rw = false;
    balanced = false;

    spec_norm2(0) = 1.0;
}

void Op_Duty::forward(Eigen::VectorXd &X, Eigen::VectorXd &out, 
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

    if (norm == 2) {
        out.array() /= spec_norm2(0);
    } else if (norm == 1) {
        out.array() /= spec_norm(0);
    }
}

void Op_Duty::transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, 
                           int apply_weight, int norm, bool repeat_balance)
{
    out = X;

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

void Op_Duty::prox(Eigen::VectorXd &X)
{
}

void Op_Duty::get_obj(Eigen::VectorXd &X, int iiter)
{
    Ax_temp.setZero();
    forward(X, Ax_temp, false, 0, true);
    current_obj = Ax_temp.squaredNorm();
    hist_obj(0, iiter) = current_obj;
    
}

}
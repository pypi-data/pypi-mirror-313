#ifndef OP_GRADIENT_H
#define OP_GRADIENT_H

/**
 * Constraint on gradient amplitude.  Supports the 'rot_variant' variable
 * to decide if gmax operates per axis or on the gradient magnitude
 * 
 * Checks 'set_vals' and forces those values if they are not NaN
 */

#include <iostream> 
#include <string>
#include "Eigen/Dense"

#include "op_main.hpp"

namespace Gropt {

class Op_Gradient : public GroptOperator
{  
    protected:
        double gmax;

    public:
        Op_Gradient(int N, int Naxis, double dt);
        virtual void set_params(double gmax_in);
        virtual void forward(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool no_balance);
        virtual void transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool repeat_balance);
        virtual void prox(Eigen::VectorXd &X);
        virtual void check(Eigen::VectorXd &X, int iiter);

};

}  // close "namespace Gropt"

#endif
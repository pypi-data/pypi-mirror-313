#ifndef OP_SLEW_H
#define OP_SLEW_H

/**
 * Constriant on slew rate, i.e. |dG/dt| <= smax
 * Supports the 'rot_variant" option to constrain either the individual slews
 * or the slew magnitude.
 */

#include <iostream> 
#include <string>
#include "Eigen/Dense"

#include "op_main.hpp"

namespace Gropt {

class Op_Slew : public GroptOperator
{  
    protected:
        double smax;

    public:
        Op_Slew(int N, int Naxis, double dt);
        virtual void set_params(double smax_in);
        virtual void forward(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool no_balance);
        virtual void transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool repeat_balance);
        virtual void prox(Eigen::VectorXd &X);
        virtual void check(Eigen::VectorXd &X, int iiter);

};

}  // end namespace Gropt


#endif
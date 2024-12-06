#ifndef OP_DUTY_H
#define OP_DUTY_H

/**
 * Objective function to minize the duty cycle.
 * i.e. minimize ||x||_2
 */

#include <iostream> 
#include <string>
#include "Eigen/Dense"
#include "op_main.hpp"

namespace Gropt {

class Op_Duty : public GroptOperator
{  
    public:
        Op_Duty(int N, int Naxis, double dt);
        virtual void forward(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool no_balance);
        virtual void transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool repeat_balance);
        virtual void prox(Eigen::VectorXd &X);
        virtual void get_obj(Eigen::VectorXd &X, int iiter);

};

}


#endif
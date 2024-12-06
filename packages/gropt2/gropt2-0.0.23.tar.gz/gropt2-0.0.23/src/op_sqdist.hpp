#ifndef OP_SQDIST_H
#define OP_SQDIST_H

/**
 * This is a constraint minimizing ||x-b||_2 
 * Here the array vector 'ref' is b
 * It is actually more used as an objective function than a constraint, but either works
 * 
 * It is mostly used liek the duty cycle constraint with b = 0,
 * but allows for other values to be set. 
 */

#include <iostream> 
#include <string>
#include "Eigen/Dense"
#include "op_main.hpp"

namespace Gropt {

class Op_SqDist : public GroptOperator
{  
    public:
        Eigen::VectorXd ref;

        Op_SqDist(int N, int Naxis, double dt);
        virtual void forward(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool no_balance);
        virtual void transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool repeat_balance);
        virtual void prox(Eigen::VectorXd &X);
        virtual void get_obj(Eigen::VectorXd &X, int iiter);
        virtual void get_feas(Eigen::VectorXd &s, int iiter);
        virtual void check(Eigen::VectorXd &X, int iiter);

};

}


#endif
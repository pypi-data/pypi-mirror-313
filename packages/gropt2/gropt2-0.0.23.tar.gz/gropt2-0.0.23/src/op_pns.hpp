#ifndef OP_PNS_H
#define OP_PNS_H

#include <iostream> 
#include <string>
#include "Eigen/Dense"
#include "op_main.hpp"

namespace Gropt {

class Op_PNS : public GroptOperator
{  
    protected:
        double stim_thresh;
        Eigen::VectorXd coeff;

    public:
        Op_PNS(int N, int Naxis, double dt);
        virtual void set_params(double stim_thresh_in);
        virtual void forward(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool no_balance);
        virtual void transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool repeat_balance);
        virtual void prox(Eigen::VectorXd &X);
        virtual void check(Eigen::VectorXd &X, int iiter);

};

}


#endif
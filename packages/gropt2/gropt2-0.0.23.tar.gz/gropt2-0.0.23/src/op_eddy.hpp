#ifndef OP_EDDY_H
#define OP_EDDY_H

/**
 * Constraint at on theeddy currents of a waveform, based on an 
 * exponential time decay model and the field at a certain point.
 */


#include <iostream> 
#include <string>
#include "Eigen/Dense"
#include "op_main.hpp"

namespace Gropt {

class Op_Eddy : public GroptOperator
{  
    public:
        int Neddy;
        int Nlam;
        Eigen::MatrixXd A;
        Eigen::VectorXd mod;

        Op_Eddy(int N, int Naxis, double dt, int Nc);
        virtual void forward(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool no_balance);
        virtual void transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool repeat_balance);
        virtual void prep_A(double lam, double tol_in);
        virtual void prep_A(Eigen::VectorXd &lam_in, double tol_in);
        virtual void prep_A(double lam, int eddy_start, int eddy_stop, double tol_in);
        virtual void prep_A(double lam, int eddy_stop, double tol_in);
        virtual void prep_A(Eigen::VectorXd &lam_in, int eddy_stop, double tol_in);
        virtual void prep_A_summation(double lam, double tol_in, int excite_idx, int inv_idx);
        virtual void prox(Eigen::VectorXd &X);
};

}


#endif
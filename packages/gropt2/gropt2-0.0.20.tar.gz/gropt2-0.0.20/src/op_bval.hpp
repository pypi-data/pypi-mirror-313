#ifndef OP_BVAL_H
#define OP_BVAL_H

/**
 * Objective function mainly used to maximize the b-value
 * Though also allows for constraints on b-value
 */


#include <iostream> 
#include <string>
#include "Eigen/Dense"
#include "op_main.hpp"


namespace Gropt {

class Op_BVal : public GroptOperator
{  
    protected:
        double GAMMA;
        double MAT_SCALE;
        double bval0;
        int start_ind;
        

    public:
        bool disable_checks;
        
        Op_BVal(int N, int Naxis, double dt);
        
        void set_start(int start_ind_in);
        void set_params(double bval_in);
        void set_params(double bval_in0, double bval_in1, double bval_in2);
        void check(Eigen::VectorXd &X, int iiter);
        
        virtual void forward(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool no_balance);
        virtual void transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool repeat_balance);
        virtual void prox(Eigen::VectorXd &X);
        virtual void get_obj(Eigen::VectorXd &X, int iiter);
        virtual void get_feas(Eigen::VectorXd &s, int iiter);
};

}


#endif
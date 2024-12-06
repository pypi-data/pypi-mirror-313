#ifndef OP_MOMENTS_H
#define OP_MOMENTS_H

/**
 * Constraint on gradient moments, can handle multiple axis, any order or moment
 * and different timing configurations and tolerances.
 * 
 * The operator supports a list of many constraints, or you could make 
 * separate operators.  (A single operator is probably moe efficient, but they should
 * otherwise return the same results)
 */

#include <iostream> 
#include <string>
#include <vector>
#include "Eigen/Dense"

#include "op_main.hpp"

namespace Gropt {

class Op_Moments : public GroptOperator
{  
    public:
        int N_moments;

        Eigen::VectorXd moment_axis;
        Eigen::VectorXd moment_order;
        Eigen::VectorXd moment_ref0;
        Eigen::VectorXd moment_start;
        Eigen::VectorXd moment_stop;
        Eigen::VectorXd moment_target;
        Eigen::VectorXd moment_tol0;

        Eigen::VectorXd mod;  // Temp array for solving the transpose

        Op_Moments(int N, int Naxis, double dt, int Nc);
        virtual void forward(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool no_balance);
        virtual void transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool repeat_balance);
        virtual void prep_A();
        virtual void prep_A_ones();
        virtual void prox(Eigen::VectorXd &X);
        virtual void set_inv_vec(Eigen::VectorXd &inv_vec_in);
        virtual void set_params(std::vector<double> m_axis,
                            std::vector<double> m_order,
                            std::vector<double> m_ref0,
                            std::vector<double> m_start,
                            std::vector<double> m_stop,
                            std::vector<double> m_target,
                            std::vector<double> m_tol0);
                            

};

}  // end namespace Gropt


#endif
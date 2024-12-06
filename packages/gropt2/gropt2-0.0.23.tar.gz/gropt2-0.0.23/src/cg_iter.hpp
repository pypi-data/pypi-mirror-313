#ifndef CG_ITER_H
#define CG_ITER_H

#include <iostream> 
#include <string>
#include <vector>
#include "Eigen/Dense"

#include "op_main.hpp"
#include "solver.hpp"

namespace Gropt {

class CG_Iter : public Solver
{
    public:
        Eigen::VectorXd x;
        Eigen::VectorXd b;
        Eigen::VectorXd Ax;
        Eigen::VectorXd Ap;
        Eigen::VectorXd r;
        Eigen::VectorXd p;

        int N;
        int max_iter;
        double tol;  // Tolerance on current residual/'b' before breaking
        
        CG_Iter(int N, int max_iter);
        // Runs conventional conjugate gradient, the output replaces x0, iiter is just the current iteration for logging
        Eigen::VectorXd solve(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &x0, int iiter);
        
};

}  // end namespace Gropt

#endif
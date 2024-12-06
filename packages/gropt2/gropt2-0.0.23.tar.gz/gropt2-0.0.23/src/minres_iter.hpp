#ifndef MINRES_ITER_H
#define MINRES_ITER_H

#include <iostream> 
#include <string>
#include <vector>
#include "Eigen/Dense"

#include "op_main.hpp"
#include "solver.hpp"

namespace Gropt {

class MINRES_Iter : public Solver
{
    public:
        Eigen::VectorXd b;
        Eigen::VectorXd y;
        Eigen::VectorXd Ax;
        Eigen::VectorXd x;
        Eigen::VectorXd r1;
        Eigen::VectorXd r2;
        Eigen::VectorXd w;
        Eigen::VectorXd w1;
        Eigen::VectorXd w2;
        Eigen::VectorXd v;

        int N;
        int max_iter;
        int istop;

        double rtol;
        double shift;
        
        MINRES_Iter(int N, int max_iter, double rtol, double shift);
        // Runs conventional conjugate gradient, the output replaces x0, iiter is just the current iteration for logging
        Eigen::VectorXd solve(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &x0, int iiter);
        
};

}  // end namespace Gropt

#endif
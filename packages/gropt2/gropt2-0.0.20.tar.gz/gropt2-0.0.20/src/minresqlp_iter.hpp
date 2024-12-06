#ifndef MINRESQLP_ITER_H
#define MINRESQLP_ITER_H

#include <iostream> 
#include <string>
#include <vector>
#include "Eigen/Dense"

#include "op_main.hpp"
#include "solver.hpp"

namespace Gropt {

class MINRESQLP_Iter : public Solver
{
    public:
        Eigen::VectorXd b;
        Eigen::VectorXd w;
        Eigen::VectorXd wl;
        Eigen::VectorXd r2;
        Eigen::VectorXd r3;
        Eigen::VectorXd wl2;
        Eigen::VectorXd xl2;
        Eigen::VectorXd Ax;
        Eigen::VectorXd x;
        Eigen::VectorXd r1;
        Eigen::VectorXd v;

        int N;
        int max_iter;
        int istop;

        double rtol;
        double shift;
        double maxxnorm;
        double TranCond;
        double Acondlim;
        
        MINRESQLP_Iter(int N, int max_iter, double rtol, double shift);
        // Runs conventional conjugate gradient, the output replaces x0, iiter is just the current iteration for logging
        Eigen::VectorXd solve(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &x0, int iiter);
        
        double sign(double x);
        void SymGivens(double a, double b, double &c, double &s, double &d);
};

}  // end namespace Gropt

#endif
#ifndef LSMR_ITER_H
#define LSMR_ITER_H

#include <iostream> 
#include <string>
#include <vector>
#include "Eigen/Dense"

#include "op_main.hpp"
#include "solver.hpp"

namespace Gropt {

class LSMR_Iter : public Solver
{
    public:
        int m;
        int n;

        int maxiters;
        double lambda;
        double conlim;
        double a_tol, b_tol;

        Eigen::VectorXd b;
        Eigen::VectorXd u;
        Eigen::VectorXd utemp;

        Eigen::VectorXd v;
        Eigen::VectorXd vtemp;
        Eigen::VectorXd h;
        Eigen::VectorXd hbar;
        Eigen::VectorXd x;


        LSMR_Iter(int n, std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, int maxiters);
        Eigen::VectorXd solve(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &x0, int iiter);
        
};

}  // end namespace Gropt

#endif
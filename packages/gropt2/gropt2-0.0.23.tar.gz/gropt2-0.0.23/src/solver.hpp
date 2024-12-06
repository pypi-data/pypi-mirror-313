#ifndef SOLVER_H
#define SOLVER_H

#include <iostream> 
#include <string>
#include <chrono>
#include <vector>
#include "Eigen/Dense"

#include "gropt_params.hpp"
#include "op_main.hpp"

namespace Gropt {

class Solver
{
    public: 

        std::string name;
        
        std::chrono::steady_clock::time_point start_time;
        std::chrono::steady_clock::time_point stop_time;
        std::chrono::duration<double, std::micro> elapsed_us;

        std::vector<int> hist_n_iter;  
        int n_iter;


        std::vector<double> get_stats(GroptParams &gparams, Eigen::VectorXd &X);
        std::vector<double> get_stats_normal(GroptParams &gparams, Eigen::VectorXd &X);
        void get_residual(GroptParams &gparams, Eigen::VectorXd &X, int mode);
        int get_n_iter();
        virtual Eigen::VectorXd solve(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &x0, int iiter) = 0;

        void get_AtAx_combined(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &X, Eigen::VectorXd &Ax);
        void get_AtAx_stats(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &X, Eigen::VectorXd &Ax);
        void get_AtAx_lims(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &X, Eigen::VectorXd &Ax);
        void get_AtAx_lims_init(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &X, Eigen::VectorXd &Ax);
        void get_Atb_combined(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &b);
        
};

}  // end namespace Gropt

#endif
#ifndef DEBUGGER_H
#define DEBUGGER_H

#include <stdarg.h>
#include <iostream>
#include <string>
#include <vector>
#include "Eigen/Dense"

namespace Gropt {

class Debugger
{
    public:

        bool debug_active;
        
        std::vector<std::string> op_names;

        std::vector<Eigen::VectorXd> hist_x0;
        std::vector<Eigen::VectorXd> hist_x1;
        std::vector<Eigen::VectorXd> hist_x2;

        std::vector<std::vector<double>> hist_weight;
        std::vector<std::vector<double>> hist_gamma;
        std::vector<std::vector<double>> hist_feas;
        std::vector<std::vector<double>> hist_pre_resid;
        std::vector<std::vector<double>> hist_post_resid;

        std::vector<int> hist_cgiter;


};

}  // close "namespace Gropt"

#endif
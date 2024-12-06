#ifndef LINESEARCH_H
#define LINESEARCH_H

#include <iostream> 
#include <string>
#include <chrono>
#include <vector>
#include "Eigen/Dense"

#include "gropt_params.hpp"
#include "op_main.hpp"

namespace Gropt {

class LineSearch
{
    public: 
        void linesearch(GroptParams &gparams, Eigen::VectorXd &X);
        double get_res(GroptParams &gparams, Eigen::VectorXd &X);
        double get_res2(GroptParams &gparams, Eigen::VectorXd &X);
};

}  // end namespace Gropt

#endif
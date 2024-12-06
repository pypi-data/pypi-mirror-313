#ifndef OPTIMIZE_H
#define OPTIMIZE_H

#include <iostream>
#include <vector>
#include "Eigen/Dense"

#include "gropt_params.hpp"
#include "cg_iter.hpp"
#include "lsmr_iter.hpp"

namespace Gropt {

void do_globalreweight(GroptParams &gparams, int iiter);

void logger(GroptParams &gparams, int iiter, Eigen::VectorXd &X, CG_Iter &cg, bool force_print);

int do_checks(GroptParams &gparams, int iiter, Eigen::VectorXd &X);

void run_optimization(GroptParams &gparams, Eigen::VectorXd &out);

void interp_vec2vec(Eigen::VectorXd &vec0, Eigen::VectorXd &vec1); 

}  // end namespace Gropt

#endif
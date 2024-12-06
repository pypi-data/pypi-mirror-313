#include <iostream> 
#include <string>
#include <math.h>  
#include "Eigen/Dense"
#include <vector>  

#include "op_main.hpp"
#include "cg_iter.hpp"
#include "logging.hpp"

#define N_HIST_MAX 100000

namespace Gropt {

CG_Iter::CG_Iter(int N, int max_iter) 
    : N(N), max_iter(max_iter)
{
    name = "CG";

    b.setZero(N);
    Ax.setZero(N);
    Ap.setZero(N);
    r.setZero(N);
    p.setZero(N);
    x.setZero(N);  
}

Eigen::VectorXd CG_Iter::solve(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &x0, int iiter)
{
    start_time = std::chrono::steady_clock::now();
    
    x = x0;
    double rnorm0;
    double bnorm0;
    double tol0;
    double pAp;
    double alpha; 
    double beta;
    double gamma;
    double res;
    
    Ax.setZero();
    Ap.setZero();

    b.setZero();
    get_Atb_combined(all_op, all_obj, b);

    // get_AtAx_combined(all_op, all_obj, x0, Ax);
    get_AtAx_lims_init(all_op, all_obj, x0, Ax);

    r = (b - Ax);
    rnorm0 = r.norm();
    bnorm0 = b.norm();

    tol0 = std::max(0.1*rnorm0/bnorm0, 1.0e-12);
    if (iiter > 3) {
        tol = std::min(tol0, tol);  // Dont allow tol to grow from last run of CG
    } else {
        tol = tol0;
    }
    
    p = r;
    gamma = r.dot(r);


    // Start actual CG
    int ii;
    for (ii = 0; ii < max_iter; ii++) {
        Ap.setZero();
        get_AtAx_lims(all_op, all_obj, p, Ap);  // Ap = A*p

        gamma = r.dot(r);
        pAp = p.dot(Ap);
        alpha = gamma / pAp;

        if ((pAp == 0) || (alpha < 0)) {break;}
        
        x += alpha * p;

        if ((ii > 0) && (ii%10 == 0)) {
            Ax.setZero();
            get_AtAx_lims(all_op, all_obj, x0, Ax);
            r = (b - Ax);
        } else {
            r -= alpha * Ap;
        }

        res = r.norm()/bnorm0;

        if (res <= tol) {break;}

        beta = r.dot(r) / gamma;

        p = beta * p + r;
    }

    stop_time = std::chrono::steady_clock::now();
    elapsed_us = stop_time - start_time;

    n_iter = ii+1;
    hist_n_iter.push_back(n_iter);

    return x;
}

}  // end namespace Gropt
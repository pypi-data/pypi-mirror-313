#include <iostream> 
#include <string>
#include <math.h>  
#include "Eigen/Dense"
#include <vector>  

#include "op_main.hpp"
#include "minres_iter.hpp"
#include "logging.hpp"

#define N_HIST_MAX 100000

namespace Gropt {

MINRES_Iter::MINRES_Iter(int N, int max_iter, double rtol, double shift) 
    : N(N), max_iter(max_iter), rtol(rtol), shift(shift)
{
    name = "MINRES";

    b.setZero(N);
    y.setZero(N);
    x.setZero(N);
    Ax.setZero(N);
    r1.setZero(N);
    r2.setZero(N);
    w.setZero(N);
    w1.setZero(N);
    w2.setZero(N);
    v.setZero(N);
}

Eigen::VectorXd MINRES_Iter::solve(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &x0, int iiter)
{   
    start_time = std::chrono::steady_clock::now();
    istop = 0;

    // Because the reference implementation does not have a x0 option, I will solve this as an iterative refinement problem to start with x = 0
    // ie solv Ax - b = r, then solve A(dx) = r, so that x_new = x_old + dx
    b.setZero();
    get_Atb_combined(all_op, all_obj, b);
    Ax.setZero();
    get_AtAx_combined(all_op, all_obj, x0, Ax);
    Ax += shift * x0;

    x.setZero();
    b = b - Ax;
    y = b;
    r1 = b;
    
    double beta1 = b.squaredNorm();
    if (beta1 <= 0) {
        n_iter = 1;
        hist_n_iter.push_back(n_iter);
        istop = 9;
        std::cout << "exact solution is 0" << std::endl;
        return x0;
    }
    beta1 = sqrt(beta1);

    double eps = 1e-15;

    double oldb   = 0;
    double beta   = beta1;   
    double dbar   = 0;       
    double epsln  = 0;
    double qrnorm = beta1;   
    double phibar = beta1;   
    double rhs1   = beta1;
    double rhs2   = 0;       
    double tnorm2 = 0;       
    double gmax   = 0;       
    double gmin   = 1.7e+308;
    double cs     = -1;      
    double sn     = 0;
    w.setZero();
    w2.setZero();
    r2 = r1;

    double s;
    double alfa;
    double oldeps;
    double delta;
    double gbar;
    double root;
    double Arnorm;
    double gamma;
    double phi;
    double denom;
    double z;
    double Anorm;  
    double ynorm; 
    double epsa;   
    double epsx;  
    double epsr;  
    double diag;   
    double rnorm;
    double test1;
    double test2;
    double Acond;
    double t1, t2;

    int iter = 0;
    while ((iter < max_iter) && (istop == 0)) {
        iter += 1;

        s = 1/beta;
        v = s*y;

        y.setZero();
        get_AtAx_combined(all_op, all_obj, v, y);
        y += shift * v;

        if (iter >= 2) {y -= (beta/oldb)*r1;}

        alfa = v.dot(y);
        y -= alfa/beta*r2;

        r1 = r2;
        r2 = y;

        oldb   = beta;
        beta   = r2.dot(y);

        if (beta < 0) {istop = 9; break;}
        beta   = sqrt(beta);
        tnorm2 += alfa*alfa + oldb*oldb + beta*beta;

        if ((iter == 1) && (beta/beta1 <= 10*eps)) {
            istop = -1;  // Dont break, do one iteration first
        }

        oldeps = epsln;
        delta  = cs*dbar + sn*alfa; // delta1 = 0         deltak
        gbar   = sn*dbar - cs*alfa; // gbar 1 = alfa1     gbar k
        epsln  =           sn*beta; // epsln2 = 0         epslnk+1
        dbar   =         - cs*beta; // dbar 2 = beta2     dbar k+1
        root   = sqrt(gbar*gbar + dbar* dbar);
        Arnorm = phibar*root;       // ||Ar{k-1}||


        gamma  = sqrt(gbar*gbar + beta*beta); // gammak
        gamma  = std::max(gamma, eps);
        cs     = gbar/gamma;        // ck
        sn     = beta/gamma;        // sk
        phi    = cs*phibar ;        // phik
        phibar = sn*phibar ;        // phibark+1


        denom = 1/gamma;
        w1    = w2;
        w2    = w;
        w     = (v - oldeps*w1 - delta*w2)*denom;
        x     += phi*w;


        gmax   = std::max(gmax, gamma);
        gmin   = std::min(gmin, gamma);
        z      = rhs1/gamma;
        rhs1   = rhs2 - delta*z;
        rhs2   =      - epsln*z;


        Anorm  = sqrt( tnorm2 );
        ynorm  = x.norm();
        epsa   = Anorm*eps;
        epsx   = Anorm*ynorm*eps;
        epsr   = Anorm*ynorm*rtol;
        diag   = gbar;
        
        if (diag==0) {diag = epsa;}

        qrnorm = phibar;
        rnorm  = qrnorm;

        test1  = rnorm/(Anorm*ynorm);
        test2  = root / Anorm;

        Acond  = gmax/gmin;

        t1 = 1 + test1;
        t2 = 1 + test2;
        
        if (t2 <= 1) {istop = 2;}
        if (t1 <= 1) {istop = 1;}
        if (iter   >= max_iter) {istop = 6;}
        if (Acond >= 0.1/eps) {istop = 4;}
        if (epsx  >= beta1) {istop = 3;}
        if (test2 <= rtol) {istop = 2;}
        if (test1 <= rtol) {istop = 1;}
    }

    stop_time = std::chrono::steady_clock::now();
    elapsed_us = stop_time - start_time;

    // std::cout << "Finished MINRES loop with istop = " << istop << "and Acond = " << Acond << std::endl;

    hist_n_iter.push_back(iter);
    return x0 + x;

}


}  // end namespace Gropt
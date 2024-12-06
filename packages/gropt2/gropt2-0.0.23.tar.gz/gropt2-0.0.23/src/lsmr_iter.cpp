#include <iostream> 
#include <string>
#include <math.h>  
#include "Eigen/Dense"
#include <vector>  

#include "op_main.hpp"
#include "lsmr_iter.hpp"
#include "logging.hpp"

#define N_HIST_MAX 100000

namespace Gropt {

void get_b(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &b) {
    int ii = 0;
    for (int i = 0; i < all_op.size(); i++) {
        b.segment(ii, all_op[i]->Ax_size) = all_op[i]->get_b();
        // log_print(LOG_DEBUG, "LSMR   get_b  %s  b norm = %8.1e   ii = %d   Ax_size = %d   spec_norm = %s", 
        //     all_op[i]->name, all_op[i]->get_b().norm(), ii, all_op[i]->Ax_size,
        //     eigen2str(all_op[i]->spec_norm2).c_str());
        ii += all_op[i]->Ax_size;
    }

    for (int i = 0; i < all_obj.size(); i++) {
        b.segment(ii, all_obj[i]->Ax_size) = all_obj[i]->get_obj_b();
        // log_print(LOG_DEBUG, "LSMR   get_b  %s  b norm = %8.1e   ii = %d   Ax_size = %d", 
        //     all_obj[i]->name, all_obj[i]->get_obj_b().norm(), ii, all_obj[i]->Ax_size);
        ii += all_obj[i]->Ax_size;
    }

}

void get_Atx(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &in, Eigen::VectorXd &out) {
    
    int ii = 0;
    out.setZero();

    for (int i = 0; i < all_op.size(); i++) {
        all_op[i]->x_temp.setZero();
        all_op[i]->Ax_temp = in.segment(ii, all_op[i]->Ax_size);
        all_op[i]->transpose(all_op[i]->Ax_temp, all_op[i]->x_temp, 1, 1, true);
        out += all_op[i]->x_temp;
        ii += all_op[i]->Ax_size;
    }

    for (int i = 0; i < all_obj.size(); i++) {
        all_obj[i]->x_temp.setZero();
        all_obj[i]->Ax_temp = in.segment(ii, all_obj[i]->Ax_size);
        all_obj[i]->transpose(all_obj[i]->Ax_temp, all_obj[i]->x_temp, 2, 1, true);
        out += all_obj[i]->x_temp;
        ii += all_obj[i]->Ax_size;
    }

}

void get_Ax(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &in, Eigen::VectorXd &out) {
    int ii = 0;

    for (int i = 0; i < all_op.size(); i++) {
        all_op[i]->Ax_temp.setZero();
        all_op[i]->forward(in, all_op[i]->Ax_temp, 1, 1, false);
        out.segment(ii, all_op[i]->Ax_size) = all_op[i]->Ax_temp;
        ii += all_op[i]->Ax_size;
    }

    for (int i = 0; i < all_obj.size(); i++) {
        all_obj[i]->Ax_temp.setZero();
        all_obj[i]->forward(in, all_obj[i]->Ax_temp, 0, 1, false);
        out.segment(ii, all_obj[i]->Ax_size) = all_obj[i]->Ax_temp;
        ii += all_obj[i]->Ax_size;
    }
}

LSMR_Iter::LSMR_Iter(int n, std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, int maxiters) 
    : n(n), maxiters(maxiters)
{
    name = "LSMR";
    
    m = 0;
    for (int i = 0; i < all_op.size(); i++) {
        m += all_op[i]->Ax_size;
    }

    for (int i = 0; i < all_obj.size(); i++) {
        m += all_obj[i]->Ax_size;
    }

    maxiters = 200;
    lambda = 0.0; 
    conlim = 1.0e8;
    a_tol = 1.0e-7;
    b_tol = 1.0e-7;

    b.setZero(m);
    u.setZero(m);
    utemp.setZero(m);

    v.setZero(n);
    vtemp.setZero(n);
    h.setZero(n);
    hbar.setZero(n);
    x.setZero(n);

    log_print(LOG_NOTHING, "intializing LSMR  m = %d  n = %d", m, n);
}

Eigen::VectorXd LSMR_Iter::solve(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &x0, int iiter)
{   

    start_time = std::chrono::steady_clock::now();
    get_b(all_op, all_obj, b);
    u = b;

    get_Ax(all_op, all_obj, x0, utemp);
    u -= utemp;

    double beta = u.norm();
    if (beta > 0) {
        u.normalize();
    }

    get_Atx(all_op, all_obj, u, v);

    double alpha = v.norm();
    if (alpha > 0) {
        v.normalize();
    }

    int iter = 0;
    double zetabar = beta*alpha;
    double alphabar = alpha;
    double rho = 1.0;
    double rhobar = 1.0;
    double cbar = 1.0;
    double sbar = 0.0;

    h = v;
    hbar.setZero();
    x = x0;

    double betadd = beta;
    double betad = 0.0;
    double rhodold = 1.0;
    double tautildeold = 0.0;
    double thetatilde = 0.0;
    double zeta = 0.0;
    double d = 0.0;

    double normA2 = alpha*alpha;
    double maxrbar = 0.0;
    double minrbar = 1e100;

    double normb = beta;
    double ctol = 0;
    if (conlim > 0) {ctol = 1.0/conlim;}
    double normr = beta;

    double normAr = alpha*beta;
    if (normAr == 0) {
        n_iter = 1;
        hist_n_iter.push_back(n_iter);

        std::cout << "exact solution is 0" << std::endl;
        return x;
    }


    while (iter < maxiters) {
        
        get_Ax(all_op, all_obj, v, utemp);
        u = utemp - alpha*u;
        

        beta = u.norm();
        if (beta > 0) {
            u.normalize();
            get_Atx(all_op, all_obj, u, vtemp);
            v = vtemp - beta*v;
            alpha = v.norm();
            if (alpha > 0) {v.normalize();}
        }

        double alphahat = sqrt(alphabar*alphabar + lambda*lambda);  // no regularization term
        double chat = alphabar/alphahat;
        double shat = lambda/alphahat;
        
        double rhoold = rho;
        rho = sqrt(alphahat*alphahat + beta*beta);
        double c = alphahat/rho;
        double s = beta/rho;
        double thetanew = s*alpha;
        alphabar = c*alpha;
            
        double rhobarold = rhobar;
        double zetaold = zeta;
        double thetabar = sbar*rho;
        double rhotemp = cbar*rho;
        rhobar = sqrt( cbar*rho*cbar*rho + thetanew*thetanew );
        cbar *= rho/rhobar;
        sbar = thetanew/rhobar;
        zeta = cbar*zetabar;
        zetabar = -sbar*zetabar;

        hbar = h - (thetabar*rho/(rhoold*rhobarold))*hbar;
        x += (zeta/(rho*rhobar))*hbar;
        h = v - (thetanew/rho)*h;

        double betaacute = chat*betadd;
        double betacheck = -shat*betadd;
        
        double betahat = c*betaacute;
        betadd = -s*betaacute;
        
        double thetatildeold = thetatilde;
        double rhotildeold = sqrt( rhodold*rhodold + thetabar*thetabar );
        double ctildeold = rhodold/rhotildeold;
        double stildeold = thetabar/rhotildeold;
        thetatilde = stildeold*rhobar;
        rhodold = ctildeold*rhobar;
        betad = -stildeold*betad + ctildeold*betahat;
        
        tautildeold = (zetaold - thetatildeold*tautildeold)/rhotildeold;
        double taud = (zeta - thetatilde*tautildeold)/rhodold;
        d = d + betacheck*betacheck;
        normr = sqrt(d + (betad - taud)*(betad - taud) + betadd*betadd);
        
        // estimate ||A||
        normA2 += beta*beta;
        double normA = sqrt(normA2);
        normA2 += alpha*alpha;
        
        maxrbar = std::max(maxrbar, rhobarold);
        if (iter > 1) {minrbar = std::min(minrbar, rhobarold);}
        double condA = std::max(maxrbar, rhotemp)/std::min(minrbar, rhotemp);


        // stopping crtierion
        normAr = abs(zetabar);
        double normx = x.norm();
        
        double test1 = normr/normb;
        double test2 = normAr / (normA*normr);
        double test3 = 1.0/condA;
        double t1 = test1 / (1 + normA*normx/normb);
        double rtol = b_tol + a_tol*normA*normx/normb;

        // check tests
        if ((iter > 1) && (test3 <= ctol || test2 <= a_tol || test1 <= rtol) ) {
            if (test1 <= rtol) {log_print(LOG_DEBUG, "LSMR   break test1");}
            if (test2 <= a_tol) {log_print(LOG_DEBUG, "LSMR   break test2  %e", test2);}
            if (test3 <= ctol) {log_print(LOG_DEBUG, "LSMR   break test3");}
            break;
        }
        
        iter++;

    }

    stop_time = std::chrono::steady_clock::now();
    elapsed_us = stop_time - start_time;

    n_iter = iter+1;
    hist_n_iter.push_back(n_iter);

    // log_print(LOG_DEBUG, "LSMR   iiter: %d  n_iter: %d", iiter, n_iter);

    return x; 
}


}  // end namespace Gropt
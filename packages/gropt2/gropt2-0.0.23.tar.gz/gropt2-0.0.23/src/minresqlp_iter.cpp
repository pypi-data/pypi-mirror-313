#include <iostream> 
#include <string>
#include <math.h>  
#include "Eigen/Dense"
#include <vector>  

#include "op_main.hpp"
#include "minresqlp_iter.hpp"
#include "logging.hpp"

#define N_HIST_MAX 100000

namespace Gropt {

MINRESQLP_Iter::MINRESQLP_Iter(int N, int max_iter, double rtol, double shift) 
    : N(N), max_iter(max_iter), rtol(rtol), shift(shift)
{

    name = "MINRES-QLP";

    b.setZero(N);
    w.setZero(N);
    wl.setZero(N);
    wl2.setZero(N);
    r2.setZero(N);
    r3.setZero(N);
    xl2.setZero(N);
    Ax.setZero(N);
    x.setZero(N);
    r1.setZero(N);
    v.setZero(N);

    maxxnorm = 1;
    TranCond = 1e7;
    Acondlim = 1e15;
}

double MINRESQLP_Iter::sign(double x) {
    if (x > 0) {return 1.0;}
    if (x < 0) {return -1.0;}
    return 0.0;
}

void MINRESQLP_Iter::SymGivens(double a, double b, double &c, double &s, double &d)
{
    double t;
    if (b == 0) {
        if (a == 0) {
            c = 1;
        } else {
            c = sign(a);
        }
        s = 0;
        d = abs(a);
    } else if (a == 0) {
        c = 0;
        s = sign(b);
        d = abs(b);
    } else if (abs(b) > abs(a)) {
        t = a/b;
        s = sign(b) / sqrt(1.0 + t*t); 
        c = s*t;
        d = b/s; 
    } else {
        t = b/a; 
        c = sign(a) / sqrt(1.0 + t*t); 
        s = c*t;
        d = a/c; 
  }

}

Eigen::VectorXd MINRESQLP_Iter::solve(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &x0, int iiter)
{   
    start_time = std::chrono::steady_clock::now();
    int istop0 = -2;     
    istop  = istop0;

    // Because the reference implementation does not have a x0 option, I will solve this as an iterative refinement problem to start with x = 0
    // ie solv Ax - b = r, then solve A(dx) = r, so that x_new = x_old + dx
    b.setZero();
    get_Atb_combined(all_op, all_obj, b);
    Ax.setZero();
    get_AtAx_combined(all_op, all_obj, x0, Ax);
    Ax += shift * x0;

    x.setZero();
    b = b - Ax;

    r2 = b;
    r3 = r2;

    double beta1 = b.norm();

    double eps = 1e-15;  
    double realmin = 2.2251e-308;
    int QLPiter  = 0;

    double lines    = 1;      
    double headlines= 20;
    double beta     = 0;      
    double tau      = 0;          
    double taul     = 0;      
    double phi      = beta1;
    double betan    = beta1;
    double betal = 0;  
    double gmin     = 0;          
    double cs       = -1;     
    double sn       = 0;
    double cr1      = -1;     
    double sr1      = 0;          
    double cr2      = -1;     
    double sr2      = 0;
    double dltan    = 0;      
    double eplnn    = 0;          
    double gama     = 0;      
    double gamal    = 0;
    double gamal2   = 0;  
    double gamal3   = 0;    
    double eta      = 0;          
    double etal     = 0;      
    double etal2    = 0;
    double vepln    = 0;      
    double veplnl   = 0;          
    double veplnl2  = 0;      
    double ul3      = 0;
    double ul2      = 0;      
    double ul       = 0;          
    double u        = 0;      
    double rnorm    = betan;
    double xnorm    = 0;      
    double xl2norm  = 0;          
    double Axnorm   = 0;
    double Anorm    = 0;      
    double Acond    = 1; 
    double relres   = rnorm / (beta1 + 1e-50);
    double alfa = 0;
    double pnorm = 0;

    double dbar;
    double dlta;    
    double epln;
    double gbar;         
    double dlta_QLP;  
    double gama_tmp;
    double taul2;
    double dlta_tmp;
    double xnorm_tmp;
    double xnorml;
    double ul4;
    double gamal_QLP;
    double vepln_QLP;
    double ul_QLP;
    double gamal_tmp;
    double gama_QLP;
    double u_QLP;
    double abs_gama;
    double Anorml;
    double gminl;
    double gminl2;
    double Acondl;
    double rnorml;
    double relresl;
    double rootl;
    double Arnorml;
    double relAresl;
    double epsx;
    double t1;
    double t2;

    w.setZero();
    wl.setZero();

    if (beta1 <= 0) {
        n_iter = 1;
        hist_n_iter.push_back(n_iter);
        istop = 0;
        std::cout << "exact solution is 0" << std::endl;
        return x0;
    }

    int iter = 0;
    while ((iter < max_iter) && (istop == istop0)) {
        iter += 1;
        betal = beta;        
        beta = betan;    
        v = r3*(1/beta);

        r3.setZero();
        get_AtAx_combined(all_op, all_obj, v, r3);
        r3 += shift * v;

        if (iter >= 2) {r3 -= (beta/betal)*r1;}

        alfa = r3.dot(v);
        r3 -= (alfa/beta)*r2;     
        r1 = r2;     
        r2 = r3;    

        betan = r3.norm();
        if (iter == 1) {
            if (betan == 0) {
                if (alfa == 0) {
                    istop=0; break;
                }else {
                    istop = -1;
                    x = b / alfa; 
                    break;
                }
            }
        }

        pnorm = sqrt(betal*betal + alfa*alfa + betan*betan);


        dbar = dltan;
        dlta = cs*dbar + sn*alfa;    
        epln = eplnn;
        gbar = sn*dbar - cs*alfa;    
        eplnn = sn*betan;
        dltan = -cs*betan;            
        dlta_QLP = dlta;  

        
        gamal3 = gamal2;     
        gamal2 = gamal;     
        gamal    = gama;     
        SymGivens(gbar, betan, cs, sn, gama);  
        gama_tmp = gama;
        taul2  = taul;       
        taul   = tau;       
        tau      = cs*phi;     
        Axnorm = sqrt(Axnorm*Axnorm + tau*tau);           
        phi      = sn*phi; 


        if (iter > 2) { 
            veplnl2  = veplnl;     
            etal2 = etal;     
            etal = eta; 
            dlta_tmp = sr2*vepln - cr2*dlta;
            veplnl   = cr2*vepln + sr2*dlta;
            dlta     = dlta_tmp;   
            eta = sr2*gama;   
            gama = -cr2*gama;
        }


        if (iter > 1) {
            SymGivens(gamal, dlta, cr1, sr1, gamal);
            vepln =   sr1*gama;
            gama  = - cr1*gama;
        }


        xnorml = xnorm;     
        ul4 = ul3;     
        ul3   = ul2;
        if (iter > 2) {
            ul2 = (taul2 - etal2*ul4 - veplnl2*ul3) / gamal2;
        }
        if (iter > 1) {
            ul = ( taul  - etal *ul3 - veplnl *ul2) / gamal;
        }
        xnorm_tmp = sqrt(xl2norm*xl2norm + ul2*ul2 + ul*ul);  
        if ((abs(gama) > realmin) && (xnorm_tmp < maxxnorm)) {
            u = (tau - eta*ul2 - vepln*ul) / gama; 
            if (sqrt(xnorm_tmp*xnorm_tmp + u*u) > maxxnorm) {
                u = 0;      
                istop = 6;
            }
        } else {
            u = 0;     
            istop = 9;
        } 
        xl2norm = sqrt(xl2norm*xl2norm + ul2*ul2);
        xnorm   = sqrt(xl2norm*xl2norm + ul*ul + u*u); 


        if ((Acond < TranCond) && (istop != istop0) && (QLPiter==0)) {  // MINRES update
            wl2 = wl;     
            wl = w;
            w   = (v - epln*wl2 - dlta_QLP*wl) * (1/gama_tmp);
            if (xnorm < maxxnorm) {
                x = x + tau*w;    
            } else {
                istop = 6;
            }

        } else {  // MINRES-QLP updates
            QLPiter = QLPiter + 1;
            if (QLPiter == 1) {
                xl2.setZero();      
                if  (iter > 1) {  
                    if (iter > 3) {
                        wl2 = gamal3*wl2 + veplnl2*wl + etal*w;
                    } 
                    if (iter > 2) {
                        wl = gamal_QLP*wl + vepln_QLP*w;
                    } 
                    w = gama_QLP*w;     xl2 = x - wl*ul_QLP - w*u_QLP;
                }
            }
            if (iter == 1) {
                wl2 = wl;      
                wl = v*sr1;     
                w  = -v*cr1;
            } else if (iter == 2) {
                wl2 = wl; 
                wl  = w*cr1 + v*sr1;
                w   = w*sr1 - v*cr1;
            } else {
                wl2 = wl;      
                wl = w;         
                w = wl2*sr2 - v*cr2;
                wl2 = wl2*cr2 + v*sr2;         
                v = wl *cr1 + w*sr1;    
                w = wl *sr1 - w*cr1;         
                wl = v;
            }
            xl2 = xl2 + wl2*ul2;
            x   = xl2 + wl *ul + w*u;    
        }

        gamal_tmp = gamal;
        SymGivens(gamal,eplnn,cr2,sr2,gamal); 


        gamal_QLP = gamal_tmp;     
        vepln_QLP = vepln;     
        gama_QLP = gama; 
        ul_QLP = ul;            
        u_QLP = u; 



        abs_gama = abs(gama);      
        Anorml = Anorm;
        Anorm = std::max(Anorm, std::max(pnorm, std::max(gamal, abs_gama)));                              
        if (iter == 1) {
            gmin   = gama;    
            gminl = gmin;
        } else if (iter > 1) {
            gminl2 = gminl;   
            gminl = gmin;    
            gmin = std::min(gminl2, std::min(gamal, abs_gama));
        }
        Acondl   = Acond;     
        Acond   = Anorm/gmin;
        rnorml   = rnorm;     
        relresl = relres;     
        if (istop != 9) {rnorm = phi;}    
        relres   = rnorm / (Anorm*xnorm + beta1);
        rootl    = sqrt(gbar*gbar + dltan*dltan);   
        Arnorml  = rnorml*rootl;
        relAresl = rootl / Anorm;           

        epsx = Anorm*xnorm*eps; 
        if ((istop == istop0) || (istop == 9)) {
            t1 = 1 + relres;
            t2 = 1 + relAresl;
            if (iter     >= max_iter   ) {istop = 8;}  // Too many itns
            if (Acond    >= Acondlim) {istop = 7;}  // Huge Acond  
            if (xnorm    >= maxxnorm) {istop = 6;}  // xnorm exceeded its limit
            if (epsx     >= beta1   ) {istop = 5;}  // x is an eigenvector
            if (t2       <= 1       ) {istop = 4;}  // Accurate LS solution
            if (t1       <= 1       ) {istop = 3;}  // Accurate Ax=b solution
            if (relAresl <= rtol    ) {istop = 2;}  // Good enough LS solution
            if (relres   <= rtol    ) {istop = 1;}  // Good enough Ax=b solution
        }
    }

    stop_time = std::chrono::steady_clock::now();
    elapsed_us = stop_time - start_time;

    // std::cout << "Finished MINRESQLP_Iter loop with istop = " << istop << " and Acond = " 
    //                   << Acond << " elapsed time = " << elapsed_us.count() << " us" << std::endl;

    hist_n_iter.push_back(iter);
    return x0 + x;

}

}  // end namespace Gropt
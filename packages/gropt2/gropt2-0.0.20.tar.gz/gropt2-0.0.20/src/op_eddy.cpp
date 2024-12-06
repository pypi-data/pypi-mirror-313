#include <iostream> 
#include <string>
#include <math.h>  
#include "Eigen/Dense"

#include "op_eddy.hpp"

namespace Gropt {


Op_Eddy::Op_Eddy(int N, int Naxis, double dt, int Nlam_in) 
    : GroptOperator(N, Naxis, dt, Naxis*Nlam_in, Naxis*Nlam_in, true)
{
    name = "Eddy";
    Nlam = Nlam_in;
    Neddy = Naxis*Nlam;

    A.setZero(Neddy, N);
    mod.setZero(Neddy);

    do_rw = true;     
}

void Op_Eddy::prep_A(double lam, double tol_in)
{
    A.setZero(Neddy, N);

    for (int i = 0; i < Naxis; i++) {
        
        for (int j = 0; j < N; j++) {
            double jj = N - j - 1;
            double val = exp(-(jj+1.0)*dt/lam) - exp(-jj*dt/lam);
            A(i, j) = val;
        }

        target(i) = 0.0;
        tol0(i) = tol_in;
        tol(i) = (1.0-cushion) * tol0(i);
        
        if (balanced) {
            balance_mod(i) = 1.0 / tol(i);
        } else {
            balance_mod(i) = 1.0;
        }

        spec_norm2(i) = A.row(i).squaredNorm();

    }

}


void Op_Eddy::prep_A_summation(double lam, double tol_in, int excite_idx, int inv_idx)
{
    A.setZero(Neddy, N);

    Eigen::VectorXd dh;
    dh.setZero(N);
    double val_h = 0.0;

    for (int i = 0; i < N; i++) {
        if (i== 0) {val_h = exp(-(float)i*dt/lam);}
        else {val_h = exp(-(float)i*dt/lam) - exp(-((float)i-1.0)*dt/lam);}
        dh(i) = val_h;
    }

    int i_axis = 0;
    double mod = 0.0;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N-i; j++) {
            if ((i+j) < excite_idx) {mod = 0.0;}
            else if ((i+j) < inv_idx) {mod = 1.0;}
            else {mod = -1.0;}
            A(i_axis,i) += dh(j) * mod;
        }
    }

    target(i_axis) = 0.0;
    tol0(i_axis) = tol_in;
    tol(i_axis) = (1.0-cushion) * tol0(i_axis);
    
    if (balanced) {
        balance_mod(i_axis) = 1.0 / tol(i_axis);
    } else {
        balance_mod(i_axis) = 1.0;
    }

    spec_norm2(i_axis) = A.row(i_axis).squaredNorm();

}

void Op_Eddy::prep_A(Eigen::VectorXd &lam_in, double tol_in)
{
    A.setZero(Neddy, N);

    for (int i = 0; i < Naxis; i++) {
        for (int i_lam = 0; i_lam < Nlam; i_lam++) {
            
            int ii = i_lam + i * Nlam;
            double lam = lam_in(i_lam);

            for (int j = 0; j < N; j++) {
                double jj = N - j - 1;
                double val = exp(-(jj+1.0)*dt/lam) - exp(-jj*dt/lam);
                A(ii, j) = val;
            }

            target(ii) = 0.0;
            tol0(ii) = tol_in;
            tol(ii) = (1.0-cushion) * tol0(ii);
            
            if (balanced) {
                balance_mod(ii) = 1.0 / tol(ii);
            } else {
                balance_mod(ii) = 1.0;
            }

            spec_norm2(ii) = A.row(ii).squaredNorm();

        }

    }
}

void Op_Eddy::prep_A(double lam, int eddy_stop, double tol_in)
{
    A.setZero(Neddy, N);

    for (int i = 0; i < Naxis; i++) {
        
        for (int j = 0; j < eddy_stop; j++) {
            double jj = eddy_stop - j - 1;
            double val = exp(-(jj+1.0)*dt/lam) - exp(-jj*dt/lam);
            A(i, j) = val;
        }

        target(i) = 0.0;
        tol0(i) = tol_in;
        tol(i) = (1.0-cushion) * tol0(i);
        
        if (balanced) {
            balance_mod(i) = 1.0 / tol(i);
        } else {
            balance_mod(i) = 1.0;
        }

        spec_norm2(i) = A.row(i).squaredNorm();
    }


}



void Op_Eddy::prep_A(double lam, int eddy_start, int eddy_stop, double tol_in)
{
    A.setZero(Neddy, N);

    for (int i = 0; i < Naxis; i++) {
        
        for (int j = eddy_start; j < eddy_stop; j++) {
            double jj = eddy_stop - j - 1;
            double val = exp(-(jj+1.0)*dt/lam) - exp(-jj*dt/lam);
            A(i, j) = val;
        }

        target(i) = 0.0;
        tol0(i) = tol_in;
        tol(i) = (1.0-cushion) * tol0(i);
        
        if (balanced) {
            balance_mod(i) = 1.0 / tol(i);
        } else {
            balance_mod(i) = 1.0;
        }

        spec_norm2(i) = A.row(i).squaredNorm();
    }


}


void Op_Eddy::prep_A(Eigen::VectorXd &lam_in, int eddy_stop, double tol_in)
{
    A.setZero(Neddy, N);

    for (int i = 0; i < Naxis; i++) {
        for (int i_lam = 0; i_lam < Nlam; i_lam++) {
            
            int ii = i_lam + i * Nlam;
            double lam = lam_in(i_lam);
        
            for (int j = 0; j < eddy_stop; j++) {
                double jj = eddy_stop - j - 1;
                double val = exp(-(jj+1.0)*dt/lam) - exp(-jj*dt/lam);
                A(ii, j) = val;
            }

            target(ii) = 0.0;
            tol0(ii) = tol_in;
            tol(ii) = (1.0-cushion) * tol0(ii);
            
            if (balanced) {
                balance_mod(ii) = 1.0 / tol(ii);
            } else {
                balance_mod(ii) = 1.0;
            }

            spec_norm2(ii) = A.row(ii).squaredNorm();

        }
        
    }
}


void Op_Eddy::forward(Eigen::VectorXd &X, Eigen::VectorXd &out, 
                         int apply_weight, int norm, bool no_balance)
{
    // TODO: Fix the Naxis Nlam selection
    for (int i = 0; i < Naxis; i++) {
        for (int i_lam = 0; i_lam < Nlam; i_lam++) {
            int ii = i_lam + i * Nlam;
            out(ii) = A.row(ii)*X.segment(i*N, N);
        }
    }

    if (apply_weight == 2) {
        out.array() *= weight(0);
    } else if (apply_weight == 1) {
        out.array() *= sqrt(weight(0));
    }

    if (balanced && !no_balance) {
        out.array() *= balance_mod(0);
    }

    if (norm == 2) {
        out.array() /= spec_norm2(0);
    } else if (norm == 1) {
        out.array() /= spec_norm(0);
    }

}

void Op_Eddy::transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, 
                           int apply_weight, int norm, bool repeat_balance)
{   
    mod.setOnes();

    if (norm == 2) {
        mod.array() /= spec_norm2.array();
    } else if (norm == 1) {
        mod.array() /= spec_norm.array();
    }

    if (balanced) {
        if (repeat_balance) {
            mod.array() *= balance_mod.array();
        } else {
            mod.array() /= balance_mod.array();
        }
    }

    if (apply_weight == 2) {
        mod.array() *= weight.array();
    } else if (apply_weight == 1) {
        mod.array() *= weight.array().sqrt();
    }

    // Just use mod as a temp solving array
    mod.array() *= X.array();

    out.setZero();
    
    for (int i = 0; i < Naxis; i++) {
        for (int i_lam = 0; i_lam < Nlam; i_lam++) {
            int ii = i_lam + i * Nlam;
            out.segment(i*N, N) += A.row(ii).transpose()*mod(ii);
        }
    }

    out.array() *= fixer.array();

}


void Op_Eddy::prox(Eigen::VectorXd &X)
{
    for (int i = 0; i < X.size(); i++) {
        double lower_bound = balance_mod(i) * (target(i)-tol(i));
        double upper_bound = balance_mod(i) * (target(i)+tol(i));
        X(i) = X(i) < lower_bound ? lower_bound:X(i);
        X(i) = X(i) > upper_bound ? upper_bound:X(i);
    }
}

}
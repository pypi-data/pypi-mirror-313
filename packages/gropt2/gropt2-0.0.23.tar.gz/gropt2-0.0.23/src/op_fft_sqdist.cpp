#include <iostream> 
#include <string>
#include <math.h>  
#include "Eigen/Dense"

#include "op_fft_sqdist.hpp"

namespace Gropt {

Op_FFT_SqDist::Op_FFT_SqDist(int N, int Naxis, double dt) 
    : GroptOperator(N, Naxis, dt, 1, 2*Naxis*N, false)
{
    name = "FFT_SqDist"; 

    do_rw = true;
    balanced = false;

    N_FT = N;

    // FFT params
    shape.push_back(N_FT);
    stride_cd.push_back(sizeof(std::complex<double>));
    axes.push_back(0);

    ft_c_vec0.setZero(N_FT);
    ft_c_vec1.setZero(N_FT);

    fft_helper = new FFT_Helper(N_FT);

    spec_norm2(0) = 1.0;
    ref.setZero(2*N);
    mod.setOnes(N);
}

void Op_FFT_SqDist::forward(Eigen::VectorXd &X, Eigen::VectorXd &out, 
                         int apply_weight, int norm, bool no_balance)
{
    fft_helper->fft(X, ft_c_vec1);
    
    for (int i = 0; i < N_FT; i++) {
        out(2*i) = ft_c_vec1(i).real() * mod(i);
        out(2*i+1) = ft_c_vec1(i).imag() * mod(i);
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

void Op_FFT_SqDist::transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, 
                           int apply_weight, int norm, bool repeat_balance)
{
    for (int i = 0; i < N_FT; i++) {
        ft_c_vec0(i) = std::complex<double>(X(2*i), X(2*i+1)) * mod(i);
    }

    fft_helper->ifft(ft_c_vec0, out); 

    if (norm == 2) {
        out.array() /= spec_norm2(0);
    } else if (norm == 1) {
        out.array() /= spec_norm(0);
    }

    if (balanced) {
        if (repeat_balance) {
            out.array() *= balance_mod(0);
        } else {
            out.array() /= balance_mod(0);
        }
    }

    if (apply_weight == 2) {
        out.array() *= weight(0);
    } else if (apply_weight == 1) {
        out.array() *= sqrt(weight(0));
    }

    out.array() *= fixer.array();
}



void Op_FFT_SqDist::prox(Eigen::VectorXd &X)
{
    X.array() = (X.array() * weight(0) + ref.array()) / (1.0 + weight(0));
}


// This is essentially more like an objective function, so we will say it is always passes the check
void Op_FFT_SqDist::check(Eigen::VectorXd &X, int iiter)
{
    // hist_check is already 0, so just do nothing
}


// This is essentially more like an objective function, so we will say it is always feasible
// NOTE: do we want this one?  Maybe it should be allowed to be in the global reweight?
// void Op_FFT_SqDist::get_feas(Eigen::VectorXd &s, int iiter)
// {   
//     // hist_feas is already 0, so just do nothing
// }


void Op_FFT_SqDist::get_obj(Eigen::VectorXd &X, int iiter)
{
    Ax_temp.setZero();
    forward(X, Ax_temp, false, 0, true);
    current_obj = Ax_temp.squaredNorm();
    hist_obj(0, iiter) = current_obj;
}

}
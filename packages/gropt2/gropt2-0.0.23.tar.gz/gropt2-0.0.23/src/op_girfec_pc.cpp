#include <iostream> 
#include <string>
#include <math.h>  
#include "Eigen/Dense"

#include "op_girfec_pc.hpp"

namespace Gropt {

Op_GirfEC_PC::Op_GirfEC_PC(int N, int Naxis, double dt, Eigen::VectorXcd &H_in, int win_width_in,
                            int tile_pre_in, int tile_post_in) 
    : GroptOperator(N, Naxis, dt, 1, win_width_in, false)  // For now N_H is N, but maybe this changes with padding or such
{
    name = "GirfEC_PC"; 

    do_rw = true;
    balanced = true;

    tile_pre = tile_pre_in;
    tile_post = tile_post_in;
    
    N_FT = N * (1 + tile_pre + tile_post);

    // FFT params
    shape.push_back(N_FT);
    stride_d.push_back(sizeof(std::complex<double>));
    stride_cd.push_back(sizeof(std::complex<double>));
    axes.push_back(0);

    ft_c_vec0.setZero(N_FT);
    ft_c_vec1.setZero(N_FT);
    temp_d.setZero(N_FT);

    H0 = H_in;
    win_width = win_width_in;

    fft_helper = new FFT_Helper(N_FT);

    resize_H();

    // spec_norm2(0) = (H0_c.squaredNorm() * win_width / N_FT);
    spec_norm2(0) = 1.0;
    spec_norm(0) = sqrt(spec_norm2(0));
}

void Op_GirfEC_PC::set_params(int excite0, int excite1, int win00, int win01, int win10, int win11)
{

    win_stop0 = win10;
    win_stop1 = win11;
    
    excite_tidx0 = excite0 + N*tile_pre;
    excite_tidx1 = excite1 + N*tile_pre;
    win_start_tidx0 = win00 + N*tile_pre;
    win_start_tidx1 = win01 + N*tile_pre;
    win_stop_tidx0 = win10 + N*tile_pre;   
    win_stop_tidx1 = win11 + N*tile_pre;

    N_conv = win_stop_tidx0 - excite_tidx0;
}

void Op_GirfEC_PC::set_params(double tol_in)
{
    target(0) = 0;
    tol0(0) = tol_in;
    tol(0) = (1.0-cushion) * tol0(0);

    if (balanced) {
        balance_mod(0) = 1.0 / tol(0);
    } else {
        balance_mod(0) = 1.0;
    }

}


void Op_GirfEC_PC::resize_H()
{
    int wr; // cropping radius

    // This is the output, but this is probbaly unessecarry 
    H0_c.setZero(N_FT);

    // prep FFT stuff for this specific one
    shape_resize.push_back(H0.size());

    Eigen::VectorXcd H0_ft;
    Eigen::VectorXcd h0;
    H0_ft.setZero(H0.size());
    h0.setZero(H0.size());

    // Transform base GMTF to GIRF
    H0_ft = H0;
    pocketfft::c2c(shape_resize, stride_cd, stride_d, axes, pocketfft::BACKWARD,
                    H0_ft.data(), h0.data(), 1.0/H0.size());


    // We will use these for the second FFT
    ft_c_vec0.setZero();
    ft_c_vec1.setZero();

    if (N_FT < H0.size()) {
        wr = N_FT/2;

        ft_c_vec0.segment(0,wr) = h0.segment(0, wr);
        ft_c_vec0.segment(ft_c_vec0.size()-wr,wr) = h0.segment(h0.size()-wr, wr);

        pocketfft::c2c(shape, stride_d, stride_cd, axes, pocketfft::FORWARD,
                    ft_c_vec0.data(), ft_c_vec1.data(), 1.);
        H0_c = ft_c_vec1;

    } else if (N_FT > H0.size()) {
        wr = H0.size()/2;

        ft_c_vec0.segment(0,wr) = h0.segment(0, wr);
        ft_c_vec0.segment(ft_c_vec0.size()-wr,wr) = h0.segment(h0.size()-wr, wr);

        pocketfft::c2c(shape, stride_d, stride_cd, axes, pocketfft::FORWARD,
                    ft_c_vec0.data(), ft_c_vec1.data(), 1.);
        H0_c = ft_c_vec1;

    } else {
        H0_c = H0;
    }

}

// Note: This will break with an odd number of points, but I dont think that is possible 
// with this use case
void Op_GirfEC_PC::fftshift(Eigen::VectorXcd &X)
{
    int center = X.size()/2;
    Eigen::VectorXcd temp = X;

    X.segment(center,center) = temp.segment(0, center);
    X.segment(0,center) = temp.segment(center, center);

}


void Op_GirfEC_PC::convolve_response(Eigen::VectorXd &X, Eigen::VectorXd &out)
{
    temp_d.setZero();
    for (int i = 0; i < (1 + tile_pre + tile_post); i++) {
        temp_d.segment(i*N, N) = X;
    }

    fft_helper->fft_convolve(temp_d, temp_d, H0_c, true, false);
    
    out = temp_d;
}

void Op_GirfEC_PC::forward(Eigen::VectorXd &X, Eigen::VectorXd &out, 
                         int apply_weight, int norm, bool no_balance)
{
    temp_d.setZero();
    for (int i = 0; i < (1 + tile_pre + tile_post); i++) {
        temp_d.segment(i*N, N) = X;
    }

    fft_helper->fft_convolve(temp_d, temp_d, H0_c, true, false);

    // Here is where we need to add the indexed convolution subtraction
    out.setZero();
    double c_ph0 = 0.0;
    double c_ph1 = 0.0;
    for (int i = 0; i < N_conv; i++) {
        c_ph0 += dt * temp_d(excite_tidx0+i);
        c_ph1 += dt * temp_d(excite_tidx1+i);

        int ii = i - (win_start_tidx0 - excite_tidx0);
        if (ii >= 0) {
            out(ii) = c_ph1 - c_ph0;
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


void Op_GirfEC_PC::transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, 
                           int apply_weight, int norm, bool repeat_balance)
{
    temp_d.setZero();

    double c_ph = 0.0;
    for (int i = 0; i < N_conv; i++) {
        if (i < win_width) {
            c_ph += dt * X(win_width - i - 1);
        }

        for (int j = 0; j < (1 + tile_pre + tile_post); j++) {
            temp_d(j*N + win_stop0 - i) = -c_ph;
            temp_d(j*N + win_stop1 - i) = c_ph;
        }
    }

    fft_helper->fft_convolve(temp_d, temp_d, H0_c, true, true);

    out = temp_d.segment(N*tile_pre,N);

    if (balanced) {
        out.array() /= balance_mod(0);
    }

    if (apply_weight == 2) {
        out.array() *= weight(0);
    } else if (apply_weight == 1) {
        out.array() *= sqrt(weight(0));
    }

    if (norm == 2) {
        out.array() /= spec_norm2(0);
    } else if (norm == 1) {
        out.array() /= spec_norm(0);
    }

    out.array() *= fixer.array();

}

void Op_GirfEC_PC::prox(Eigen::VectorXd &X)
{
    for (int i = 0; i < X.size(); i++) {
        double lower_bound = balance_mod(0) / spec_norm(0) * (target(0)-tol(0));
        double upper_bound = balance_mod(0) / spec_norm(0) * (target(0)+tol(0));
        X(i) = X(i) < lower_bound ? lower_bound:X(i);
        X(i) = X(i) > upper_bound ? upper_bound:X(i);
    }   
}

void Op_GirfEC_PC::check(Eigen::VectorXd &X, int iiter)
{
    double check = 0.0;


    for (int i = 0; i < X.size(); i++) {
        double lower_bound = balance_mod(0) / spec_norm(0) * (target(0)-tol0(0));
        double upper_bound = balance_mod(0) / spec_norm(0) * (target(0)+tol0(0));

        if ((X(i) < lower_bound) || (X(i) > upper_bound)) {
            check = 1.0;
        }
    }   

    hist_check(0, iiter) = check;

}

void Op_GirfEC_PC::get_obj(Eigen::VectorXd &X, int iiter)
{
    Ax_temp.setZero();
    forward(X, Ax_temp, false, 0, true);
    current_obj = Ax_temp.squaredNorm();
    hist_obj(0, iiter) = current_obj;
}

}  // end namespace Gropt
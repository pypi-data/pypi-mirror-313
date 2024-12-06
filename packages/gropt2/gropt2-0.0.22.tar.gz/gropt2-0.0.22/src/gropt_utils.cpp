#include "gropt_utils.hpp"
#include "op_girfec_pc.hpp" 
#include "op_fft_sqdist.hpp" 
#include "op_bval.hpp" 
#include "op_safe.hpp" 
#include "fft_helper.hpp"  


namespace Gropt {


void test_fft_convolve(int N, double *X_in, int N_H, std::complex<double> *H_in, std::vector<double> &out_vec, int tile_pre, int tile_post) {
    Eigen::VectorXd X;
    X.setZero(N);
    for (int i=0; i<N; i++) {
        X(i) = X_in[i];
    }

    Eigen::VectorXcd H0;
    H0.setZero(N_H);
    for (int i=0; i<N_H; i++) {
        H0(i) = H_in[i];
    }

    int N_tile = N;

    Eigen::VectorXd out;
    out.resize(N_tile);

    FFT_Helper fft_helper(N_tile);

    fft_helper.fft_convolve(X, out, H0, true, false);

    out_vec.resize(out.size());
    for(int i = 0; i < out.size(); i++) {
        out_vec[i] = out(i);
    }
    
}


void test_fft(int N, double *X_in, std::vector<std::complex<double>> &out_vec, int N_repeats) {
    
    Eigen::VectorXd X;
    X.setZero(N);
    for (int i=0; i<N; i++) {
        X(i) = X_in[i];
    }

    FFT_Helper fft_helper(N);
    
    Eigen::VectorXcd out;
    out.resize(N);

    for(int i = 0; i < N_repeats; i++) {
        fft_helper.fft(X, out);
    }

    out_vec.resize(out.size());
    for(int i = 0; i < out.size(); i++) {
        out_vec[i] = out(i);
    }

}


void test_ifft(int N, std::complex<double> *X_in, std::vector<double> &out_vec, int N_repeats) {
    
    Eigen::VectorXcd X;
    X.setZero(N);
    for (int i=0; i<N; i++) {
        X(i) = X_in[i];
    }

    FFT_Helper fft_helper(N);
    
    Eigen::VectorXd out;
    out.resize(N);

    for(int i = 0; i < N_repeats; i++) {
        fft_helper.ifft(X, out);
    }

    out_vec.resize(out.size());
    for(int i = 0; i < out.size(); i++) {
        out_vec[i] = out(i);
    }

}

void get_fft_sqdist(int N, double *G_in, double *mod_in, std::vector<double> &out_vec) {
    Eigen::VectorXd G;
    G.setZero(N);
    for (int i=0; i<N; i++) {
        G(i) = G_in[i];
    }

    Eigen::VectorXd mod;
    mod.setZero(N);
    for (int i=0; i<N; i++) {
        mod(i) = mod_in[i];
    }

    double dt = 10e-6;

    Op_FFT_SqDist opFQS(N, 1, dt);
    opFQS.mod = mod;

    Eigen::VectorXd temp;
    temp.setZero(opFQS.Y0.size());
    opFQS.forward(G, temp, false, 0, true);

    out_vec.resize(temp.size());
    for(int i = 0; i < temp.size(); i++) {
        out_vec[i] = temp(i);
    }
}

void get_girf_ec_pc_response(int N, double *G_in, int N_H, std::complex<double> *H_in, int excite, double dt,
                             std::vector<double> &out_vec, int tile_pre, int tile_post, int mode)
{
    Eigen::VectorXd G;
    G.setZero(N);
    for (int i=0; i<N; i++) {
        G(i) = G_in[i];
    }
    
    Eigen::VectorXcd H0;
    H0.setZero(N_H);
    for (int i=0; i<N_H; i++) {
        H0(i) = H_in[i];
    }

    int Nhalf = N/2;
    int win_width = Nhalf - excite;
    
    Eigen::VectorXd temp;

    if (mode == 1) {
        Op_GirfEC_PC opEC(N, 1, dt, H0, win_width, tile_pre, tile_post);
        opEC.set_params(excite, excite+Nhalf, excite, excite+Nhalf, Nhalf, N);

        
        temp.setZero(opEC.Y0.size());
        opEC.forward(G, temp, false, 0, true);
    } else if (mode == 2) {
        // Op_GirfEC_PC2 opEC(N, 1, dt, H0, win_width, tile_pre, tile_post);
        // opEC.set_params(excite, excite+Nhalf, excite, excite+Nhalf, Nhalf, N);

        // temp.setZero(opEC.Y0.size());
        // opEC.forward(G, temp, false, 0, true);
    } 

    out_vec.resize(temp.size());
    for(int i = 0; i < temp.size(); i++) {
        out_vec[i] = temp(i);
    }
}



void get_girf_ec_pc_convolve(int N, double *G_in, int N_H, std::complex<double> *H_in, int excite, double dt,
                             std::vector<double> &out_vec, int tile_pre, int tile_post, int mode)
{
    Eigen::VectorXd G;
    G.setZero(N);
    for (int i=0; i<N; i++) {
        G(i) = G_in[i];
    }
    
    Eigen::VectorXcd H0;
    H0.setZero(N_H);
    for (int i=0; i<N_H; i++) {
        H0(i) = H_in[i];
    }

    int Nhalf = N/2;
    int win_width = Nhalf - excite;
    
    Eigen::VectorXd temp;

    if (mode == 1) {
        Op_GirfEC_PC opEC(N, 1, dt, H0, win_width, tile_pre, tile_post);
        opEC.set_params(excite, excite+Nhalf, excite, excite+Nhalf, Nhalf, N);
        opEC.convolve_response(G, temp);
    }

    out_vec.resize(temp.size());
    for(int i = 0; i < temp.size(); i++) {
        out_vec[i] = temp(i);
    }
}


double get_bval(int N, double *G_in, int idx_inv, double dt)
{
    Eigen::VectorXd G;
    G.setZero(N);
    for (int i=0; i<N; i++) {
        G(i) = G_in[i];
    }

    Op_BVal opB(N, 1, dt);
    
    opB.inv_vec.setOnes(N);
    for(int i = idx_inv; i < N; i++) {
        opB.inv_vec(i) = -1.0;
    }
    
    opB.get_obj(G, 0);
    return opB.hist_obj(0,0);
}

void get_SAFE(int N, int Naxis, double *G_in, double dt, std::vector<double> &out_vec, bool true_safe)
{
    Eigen::VectorXd G;
    G.setZero(N);
    for (int i=0; i<N; i++) {
        G(i) = G_in[i];
    }

    Op_SAFE opF(N, Naxis, dt);
    opF.set_params();
    opF.true_safe = true_safe;
    
    Eigen::VectorXd temp;
    temp.setZero(opF.Y0.size());
    opF.forward(G, temp, false, 0, true);

    opF.x_temp.setZero();
    for (int j = 0; j < Naxis; j++) {
        for (int i = 0; i < N; i++) {
            opF.x_temp(j*N+i) = temp(j*3*N+i) + temp(j*3*N+i+N) + temp(j*3*N+i+2*N);
        }
    }

    out_vec.resize(opF.x_temp.size());
    for(int i = 0; i < opF.x_temp.size(); i++) {
        out_vec[i] = opF.x_temp(i);
    }

}


void get_SAFE(int N, int Naxis, double *G_in, double dt, std::vector<double> &out_vec, bool true_safe,
                double tau1, double tau2, double tau3, double a1, double a2, double a3, double stim_limit, double g_scale)
{
    Eigen::VectorXd G;
    G.setZero(N);
    for (int i=0; i<N; i++) {
        G(i) = G_in[i];
    }

    Op_SAFE opF(N, Naxis, dt);
    opF.set_params(tau1, tau2, tau3, a1, a2, a3, stim_limit, g_scale, 1.0);
    opF.true_safe = true_safe;
    
    Eigen::VectorXd temp;
    temp.setZero(opF.Y0.size());
    opF.forward(G, temp, false, 0, true);

    opF.x_temp.setZero();
    for (int j = 0; j < Naxis; j++) {
        for (int i = 0; i < N; i++) {
            opF.x_temp(j*N+i) = temp(j*3*N+i) + temp(j*3*N+i+N) + temp(j*3*N+i+2*N);
        }
    }

    out_vec.resize(opF.x_temp.size());
    for(int i = 0; i < opF.x_temp.size(); i++) {
        out_vec[i] = opF.x_temp(i);
    }

}


}  // end namespace Gropt
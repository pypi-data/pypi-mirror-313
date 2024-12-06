#ifndef GROPT_UTILS_H
#define GROPT_UTILS_H

/**
 * In general this is just a place for random usages of the GrOpt
 * operators for applications that aren't actual optimization.
 * 
 * i.e. GIRF respone calculation or spectral calcs, or getting a 
 * PNS curve for a waveform
 */

#include <iostream> 
#include <string>
#include <vector>
#include "Eigen/Dense"

namespace Gropt {

void get_fft_sqdist(int N, double *G_in, double *mod_in, std::vector<double> &out_vec);

void get_girf_ec_pc_response(int N, double *G_in, int N_H, std::complex<double> *H_in, int excite, double dt,
                             std::vector<double> &out_vec, int tile_pre, int tile_post, int mode);

void get_girf_ec_pc_convolve(int N, double *G_in, int N_H, std::complex<double> *H_in, int excite, double dt,
                             std::vector<double> &out_vec, int tile_pre, int tile_post, int mode);

void test_fft(int N, double *X_in, std::vector<std::complex<double>> &out_vec, int N_repeats);
void test_ifft(int N, std::complex<double> *X_in, std::vector<double> &out_vec, int N_repeats);
void test_fft_convolve(int N, double *X_in, int N_H, std::complex<double> *H_in, std::vector<double> &out_vec, int tile_pre, int tile_post);

double get_bval(int N, double *G_in, int idx_inv, double dt);
void get_SAFE(int N, int Naxis, double *G_in, double dt, std::vector<double> &out_vec, bool true_safe);
void get_SAFE(int N, int Naxis, double *G_in, double dt, std::vector<double> &out_vec, bool true_safe, double tau1, double tau2, double tau3, double a1, double a2, double a3, double stim_limit, double g_scale);
 

}  // close "namespace Gropt"

#endif
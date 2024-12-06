#ifndef OP_GIRFEC_PC_H
#define OP_GIRFEC_PC_H

/**
 * This is a constraint minimizing the predcited background phase of a PC-MRI sequence
 */

#include <iostream> 
#include <string>
#include "Eigen/Dense"

#include "fft_helper.hpp"
#include "op_main.hpp"
#include "pocketfft_hdronly.hpp"

namespace Gropt {

class Op_GirfEC_PC : public GroptOperator
{  
    public:
        unsigned long long N_FT;
        int win_width;
        Eigen::VectorXcd ft_c_vec0;
        Eigen::VectorXcd ft_c_vec1;
        Eigen::VectorXcd H0;  // Input GIRF
        Eigen::VectorXcd H0_c;  // GIRF resized to the size of the tiled (repeated) 'x'

        // For an FFT based convolution we pad the gradient with repeats of itself
        // before and after to better simulate a steady state signal
        int tile_pre;
        int tile_post;

        int N_conv;  // elements between excitation and end of window
        // _tidx variables are indexes after the tiling (repeating) happens
        // They then represent the positions of excitation, window starts, and window stops
        int excite_tidx0;
        int excite_tidx1;
        int win_start_tidx0;
        int win_start_tidx1;
        int win_stop_tidx0;
        int win_stop_tidx1;

        int win_stop0;
        int win_stop1;

        pocketfft::shape_t shape;
        pocketfft::shape_t shape_resize;
        pocketfft::stride_t stride_d;
        pocketfft::stride_t stride_cd;
        pocketfft::shape_t axes;

        Eigen::VectorXcd gg_tile;
        Eigen::VectorXd temp_d;

        FFT_Helper *fft_helper;


        Op_GirfEC_PC(int N, int Naxis, double dt, Eigen::VectorXcd &H_in, int win_width_in,
                        int tile_pre_in, int tile_post_in) ;
        
        // Resize the GIRF to be the same size as the tiled 'x'
        void resize_H();
        void fftshift(Eigen::VectorXcd &X);

        virtual void set_params(int excite0, int excite1, int win00, int win01, int win10, int win11);
        virtual void forward(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool no_balance);
        virtual void transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool repeat_balance);
        virtual void prox(Eigen::VectorXd &X);
        virtual void get_obj(Eigen::VectorXd &X, int iiter);
        virtual void check(Eigen::VectorXd &X, int iiter);
        virtual void set_params(double tol_in);
        virtual void convolve_response(Eigen::VectorXd &X, Eigen::VectorXd &out);

};

}  // end namespace Gropt


#endif
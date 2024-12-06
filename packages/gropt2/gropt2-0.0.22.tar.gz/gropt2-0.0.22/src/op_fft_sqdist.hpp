#ifndef OP_FFT_SQDIST_H
#define OP_FFT_SQDIST_H

/**
 * This is a constraint minimizing ||FFT(x)-b||_2 
 * Here the array vector 'ref' is b
 * It is actually more used as an objective function than a constraint, but either works
 * 
 */

#include <iostream> 
#include <string>
#include "Eigen/Dense"
#include "op_main.hpp"
#include "pocketfft_hdronly.hpp"
#include "fft_helper.hpp"

namespace Gropt {

class Op_FFT_SqDist : public GroptOperator
{  
    public:
        Eigen::VectorXd ref;
        Eigen::VectorXd mod;

        unsigned long long N_FT;
        Eigen::VectorXcd ft_c_vec0;
        Eigen::VectorXcd ft_c_vec1;

        pocketfft::shape_t shape;
        pocketfft::shape_t shape_resize;
        pocketfft::stride_t stride_cd;
        pocketfft::shape_t axes;

        FFT_Helper *fft_helper; 

        Op_FFT_SqDist(int N, int Naxis, double dt);
        virtual void forward(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool no_balance);
        virtual void transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool repeat_balance);
        virtual void prox(Eigen::VectorXd &X);
        virtual void get_obj(Eigen::VectorXd &X, int iiter);
        // virtual void get_feas(Eigen::VectorXd &s, int iiter);
        virtual void check(Eigen::VectorXd &X, int iiter);

};

}


#endif
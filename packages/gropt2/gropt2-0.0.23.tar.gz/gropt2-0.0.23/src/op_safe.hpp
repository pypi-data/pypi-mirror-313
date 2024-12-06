#ifndef OP_SAFE_H
#define OP_SAFE_H

/**
 * Constriant on slew rate, i.e. |dG/dt| <= smax
 * Supports the 'rot_variant" option to constrain either the individual slews
 * or the slew magnitude.
 */

#include <iostream> 
#include <string>
#include "Eigen/Dense"

#include "op_main.hpp"

namespace Gropt {

class Op_SAFE : public GroptOperator
{  
    protected:
        double stim_thresh;

        Eigen::VectorXd signs;
        Eigen::VectorXd stim1;
        Eigen::VectorXd stim2;
        Eigen::VectorXd stim3;

        Eigen::Vector3d tau1;
        Eigen::Vector3d tau2;
        Eigen::Vector3d tau3;
        Eigen::Vector3d alpha1;
        Eigen::Vector3d alpha2;
        Eigen::Vector3d alpha3;
        Eigen::Vector3d a1;
        Eigen::Vector3d a2;
        Eigen::Vector3d a3;
        Eigen::Vector3d stim_limit;
        Eigen::Vector3d g_scale;

    public:
        bool true_safe;

        Op_SAFE(int N, int Naxis, double dt);
        virtual void set_params(double _tau1, double _tau2, double _tau3, double _a1, double _a2, double _a3, double _stim_lim, double _g_scale, double _stim_thresh);
        
        virtual void set_params(double _stim_thresh);
        virtual void set_params();
        virtual void forward(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool no_balance);
        virtual void transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool repeat_balance);
        virtual void prox(Eigen::VectorXd &X);
        virtual void check(Eigen::VectorXd &X, int iiter);

};

}  // end namespace Gropt


#endif
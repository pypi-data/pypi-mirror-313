#include <iostream> 
#include <string>
#include <math.h>  
#include "Eigen/Dense"


// Moments Params Array:
// 0: gradient axis
// 1: Moment Order
// 2: Time offset (for higher order moments: this defines where is t=0 in relation to the waveform)
// 3: Start index
// 4: Stop index
// 5: Target Moment, currently this is in units of ms,mT,m to match up with Siemens, but maybe we should use SI to
//                      be mroe consistent with the rest of the package units
// 6: tolerance

// We are getting rid of this because it is needlessly confusing.  (It was a byproduct of some old compatibility)  
// Switching to separate arrays for each of these values, and we can make some helpers to adapt the moment_params arrays

#include "op_moments.hpp"
#include "logging.hpp" 

namespace Gropt {

Op_Moments::Op_Moments(int N, int Naxis, double dt, int Nc) 
    : GroptOperator(N, Naxis, dt, Nc, Nc, true)
{
    name = "Moments";

    moment_axis.setZero(Nc);
    moment_order.setZero(Nc);
    moment_ref0.setZero(Nc);
    moment_start.setZero(Nc);
    moment_stop.setZero(Nc);
    moment_target.setZero(Nc);
    moment_tol0.setOnes(Nc);
    moment_tol0 *= 1e-6;

    A.setZero(Nc, Naxis*N);
    mod.setZero(Nc);
    do_rw = true;
    balanced = false;    
}

void Op_Moments::prep_A()
{
    A.setZero();
    spec_norm2.setZero();
    spec_norm.setZero();
    
    for(int i = 0; i < Nc; i++) {

        double axis = moment_axis(i);
        double order = moment_order(i);
        double ref0 = moment_ref0(i);
        double start = moment_start(i);
        double stop = moment_stop(i);

        // Default start and stop is an entire axis
        int i_start = axis*N;
        int i_stop = (axis+1)*N;

        // Defined start and stop indices
        if (start > 0) {
            i_start = (int)(start+0.5) + axis*N;
        }
        if (stop > 0) {
            i_stop = (int)(stop+0.5) + axis*N;
        }

        for(int j = i_start; j < i_stop; j++) {
            double order = moment_order(i);
            double jj = j - axis*N;
            double val = 1000.0 * 1000.0 * dt * pow( (1000.0 * (dt*(jj - ref0))), order);
            
            A(i, j) = val * inv_vec(j);
            spec_norm2(i) += val*val;
        }

        spec_norm2(i) = sqrt(spec_norm2(i));
        spec_norm(i) = sqrt(spec_norm2(i));


        target(i) = moment_target(i);
        tol0(i) = moment_tol0(i);
        tol(i) = (1.0-cushion) * tol0(i);
        
        if (balanced) {
            balance_mod(i) = 1.0 / tol(i);
        } else {
            balance_mod(i) = 1.0;
        }

    }

}


// This is a special case for comparing to some Julia code
// Can probably just delete later
void Op_Moments::prep_A_ones()
{
    A.setZero();
    spec_norm2.setZero();
    spec_norm.setZero();
    
    for(int i = 0; i < Nc; i++) {

        double axis = moment_axis(i);
        double order = moment_order(i);
        double ref0 = moment_ref0(i);
        double start = moment_start(i);
        double stop = moment_stop(i);

        // Default start and stop is an entire axis
        int i_start = axis*N;
        int i_stop = (axis+1)*N;

        // Defined start and stop indices
        if (start > 0) {
            i_start = (int)(start+0.5) + axis*N;
        }
        if (stop > 0) {
            i_stop = (int)(stop+0.5) + axis*N;
        }

        for(int j = i_start; j < i_stop; j++) {
            double order = moment_order(i);
            double jj = j - axis*N;
            double val = pow( (jj - ref0) / (i_stop - i_start) , order);
            
            A(i, j) = val * inv_vec(j);
            spec_norm2(i) += val*val;
        }

        spec_norm2(i) = 1.0;
        spec_norm(i) = 1.0;


        target(i) = moment_target(i);
        tol0(i) = moment_tol0(i);
        tol(i) = (1.0-cushion) * tol0(i);
        
        if (balanced) {
            balance_mod(i) = 1.0 / tol(i);
        } else {
            balance_mod(i) = 1.0;
        }

    }

}

void Op_Moments::set_params(std::vector<double> m_axis,
                            std::vector<double> m_order,
                            std::vector<double> m_ref0,
                            std::vector<double> m_start,
                            std::vector<double> m_stop,
                            std::vector<double> m_target,
                            std::vector<double> m_tol0)
{   
    
    if (m_axis.size() != Nc) {log_print(LOG_ERROR, "ERROR:  Size mismatch with moment_axis");}
    if (m_order.size() != Nc) {log_print(LOG_ERROR, "ERROR:  Size mismatch with moment_order");}
    if (m_ref0.size() != Nc) {log_print(LOG_ERROR, "ERROR:  Size mismatch with moment_ref0");}
    if (m_start.size() != Nc) {log_print(LOG_ERROR, "ERROR:  Size mismatch with moment_start");}
    if (m_stop.size() != Nc) {log_print(LOG_ERROR, "ERROR:  Size mismatch with moment_stop");}
    if (m_target.size() != Nc) {log_print(LOG_ERROR, "ERROR:  Size mismatch with moment_target");}
    if (m_tol0.size() != Nc) {log_print(LOG_ERROR, "ERROR:  Size mismatch with moment_tol0");}

    moment_axis = Eigen::Map<Eigen::VectorXd, Eigen::Unaligned>(m_axis.data(), m_axis.size());
    moment_order = Eigen::Map<Eigen::VectorXd, Eigen::Unaligned>(m_order.data(), m_order.size());
    moment_ref0 = Eigen::Map<Eigen::VectorXd, Eigen::Unaligned>(m_ref0.data(), m_ref0.size());
    moment_start = Eigen::Map<Eigen::VectorXd, Eigen::Unaligned>(m_start.data(), m_start.size());
    moment_stop = Eigen::Map<Eigen::VectorXd, Eigen::Unaligned>(m_stop.data(), m_stop.size());
    moment_target = Eigen::Map<Eigen::VectorXd, Eigen::Unaligned>(m_target.data(), m_target.size());
    moment_tol0 = Eigen::Map<Eigen::VectorXd, Eigen::Unaligned>(m_tol0.data(), m_tol0.size());

    prep_A();
}

void Op_Moments::forward(Eigen::VectorXd &X, Eigen::VectorXd &out, 
                         int apply_weight, int norm, bool no_balance)
{
    out = A*X;

    if (apply_weight == 2) {
        out.array() *= weight.array();
    } else if (apply_weight == 1) {
        out.array() *= weight.array().sqrt();
    }

    if (balanced && !no_balance) {
        out.array() *= balance_mod.array();
    }

    if (norm == 2) {
        out.array() /= spec_norm2.array();
    } else if (norm == 1) {
        out.array() /= spec_norm.array();
    }

}

void Op_Moments::transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, 
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
    out = A.transpose() * mod;
    out.array() *= fixer.array();
}


void Op_Moments::prox(Eigen::VectorXd &X)
{
    for (int i = 0; i < X.size(); i++) {
        double lower_bound = balance_mod(i) / spec_norm(i) * (target(i)-tol(i));
        double upper_bound = balance_mod(i) / spec_norm(i) * (target(i)+tol(i));
        X(i) = X(i) < lower_bound ? lower_bound:X(i);
        X(i) = X(i) > upper_bound ? upper_bound:X(i);
    }
}

// Overload because A needs to be recomputed
void Op_Moments::set_inv_vec(Eigen::VectorXd &inv_vec_in)
{
    inv_vec = inv_vec_in;
    prep_A();
}

}  // end namespace Gropt
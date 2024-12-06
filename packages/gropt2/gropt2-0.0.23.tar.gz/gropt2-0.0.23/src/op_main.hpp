#ifndef OP_MAIN_H
#define OP_MAIN_H

/**
 * This is our main parent class for every constraint and regularization term in GrOpt
 * The main functions that we use here are the reweighting schemes, where most operators will
 * then just need to implement the forward, transpose, and proximal mapping operators.
 */

#include <iostream> 
#include <string>
#include "Eigen/Dense"

namespace Gropt {

class GroptOperator 
{  
    public:   

        int N; // Number of entries on a single axis
        int Naxis; // Number of axis
        int Ntot;

        bool rot_variant; // Some constriants support rotationally variant vs invariant solutions

        double dt;
        std::string name;

        Eigen::VectorXd weight;
        Eigen::VectorXd gamma;
        
        double cushion;
        Eigen::VectorXd tol0;
        Eigen::VectorXd tol;
        Eigen::VectorXd target;

        bool row_constraints; // Are there multiple individual constraints within this operator? (i.e. the moment constraint, or eddy current lambdas)
        int Nc; // Number of constraints within the operator
        int Ax_size; // Vector size of Ax
        Eigen::VectorXd spec_norm2;
        Eigen::VectorXd spec_norm;

        bool balanced;
        Eigen::VectorXd balance_mod;

        // Only used in some operators where we can expliciety write A
        Eigen::MatrixXd A;

        Eigen::VectorXd x_temp;
        Eigen::VectorXd Ax_temp;

        Eigen::VectorXd Y0;
        Eigen::VectorXd Y1;
        Eigen::VectorXd U0;
        Eigen::VectorXd U1;

        Eigen::VectorXd s;
        Eigen::VectorXd xbar;

        Eigen::VectorXd Uhat00;
        Eigen::VectorXd U00;
        Eigen::VectorXd s00;
        Eigen::VectorXd Y00;

        Eigen::VectorXd r_feas;
        Eigen::VectorXd feas_temp;
        Eigen::VectorXd feas_check;
        
        // This should mostly come from gparams, but keep local copies in case we need to change them individually
        double e_corr;
        bool do_rw;
        double rw_eps;
        double rw_scalelim;
        int rw_interval;

        double weight_min;
        double weight_max;

        bool do_gamma;
        bool do_weight;
        bool do_scalelim; 

        double weight_init;
        double gamma_init;

        double solver_lim_min;
        double solver_lim_max;
        double solver_lim_weight;

        // These should maybe be references to gparams avoid unecessary copies,
        // but maybe we will want them to be different in some cases?
        Eigen::VectorXd fixer;
        Eigen::VectorXd inv_vec;
        Eigen::VectorXd set_vals;

        // Vectors to pre-allocate for the reweighting
        Eigen::VectorXd uhat1;
        Eigen::VectorXd duhat;
        Eigen::VectorXd du;
        Eigen::VectorXd dhhat;
        Eigen::VectorXd dghat;

        Eigen::MatrixXd hist_check;
        Eigen::MatrixXd hist_feas;
        Eigen::MatrixXd hist_obj;

        double current_obj;
        
        GroptOperator(int N, int Naxis, double dt, int Nc, int Ax_size, bool row_constraints);
        virtual ~GroptOperator();
        void allocate_rwvecs();    
        void reweight(int iiter);
        void update(Eigen::VectorXd &X, int iiter);
        void add2b(Eigen::VectorXd &b);
        virtual void obj_add2b(Eigen::VectorXd &b);
        virtual Eigen::VectorXd get_AtAx(Eigen::VectorXd &X, int apply_weight);
        void add2AtAx(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight);
        void add2AtAx(Eigen::VectorXd &X, Eigen::VectorXd &out);
        virtual void init_vals(double e_corr_in, double rw_eps_in, 
                                double rw_scalelim_in, int rw_interval_in, 
                                double weight_min_in, double weight_max_in,
                                bool do_gamma_in, bool do_weight_in, bool do_scalelim_in, double weight_init_in, double gamma_init_in,
                                Eigen::VectorXd &set_vals_in,
                                Eigen::VectorXd &inv_vec_in,
                                Eigen::VectorXd &fixer_in);
        virtual void init(Eigen::VectorXd &X, bool do_init); 
        virtual void soft_init(Eigen::VectorXd &X);
        virtual void prep_y(Eigen::VectorXd &X); 
        virtual void forward(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool no_balance);
        virtual void transpose(Eigen::VectorXd &X, Eigen::VectorXd &out, int apply_weight, int norm, bool repeat_balance);
        virtual void prox(Eigen::VectorXd &X);
        virtual void check(Eigen::VectorXd &X, int iiter);
        virtual void get_obj(Eigen::VectorXd &X, int iiter);
        virtual void set_inv_vec(Eigen::VectorXd &inv_vec_in);
        virtual void set_fixer(Eigen::VectorXd &fixer_in);
        virtual void set_set_vals(Eigen::VectorXd &set_vals_in);
        virtual void change_cushion(double cushion_in);
        virtual void get_feas(Eigen::VectorXd &s, int iiter);

        Eigen::VectorXd get_b();
        Eigen::VectorXd get_obj_b();

        
};

}  // close "namespace Gropt"

#endif










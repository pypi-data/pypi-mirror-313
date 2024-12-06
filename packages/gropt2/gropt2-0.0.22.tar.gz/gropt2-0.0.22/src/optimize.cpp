#include "optimize.hpp"
#include "cg_iter.hpp"
#include "lsmr_iter.hpp"
#include "minres_iter.hpp"
#include "minresqlp_iter.hpp"
#include "solver.hpp"
#include "logging.hpp"
#include "debugger.hpp"
#include "linesearch.hpp"

#define N_HIST_TEMP 20

namespace Gropt {

// Reweight the 'worst' constraint, based on the r_feas value from the PAR-SDMM paper
void do_globalreweight(GroptParams &gparams, int iiter)
{
    int grw_interval = gparams.grw_interval;
    int grw_start = gparams.grw_start;

    int max_i = -1;
    int max_j = -1;
    double max_feas = -1.0;
    double feas;
    
    // Find the worst r_feas (search each constraint, and sub-constraints if applicable (such as in moments))
    if ((iiter > grw_start) && (iiter%grw_interval==0)) {
        
        for (int i = 0; i < gparams.all_op.size(); i++) {
            for (int j = 0; j < gparams.all_op[i]->hist_check.col(iiter).size(); j++) {
                if ((gparams.all_op[i]->do_rw) && (gparams.all_op[i]->hist_check(j,iiter) > 0)) {
                    feas = gparams.all_op[i]->hist_feas(j,iiter);
                    if (feas > max_feas) {
                        max_feas = feas;
                        max_i = i; // Constraint index
                        max_j = j; // Sub constraint index
                    }
                }
            }
        }

        // Apply the weight scaling
        if (max_i >= 0) {
            gparams.all_op[max_i]->weight(max_j) *= gparams.grw_scale;
            log_print(LOG_VERBOSE, "do_globalreweight()  max_i = %d  max_j = %d  iiter  = %d", max_i, max_j, iiter);
        }

    }
}

// void reset_weights(GroptParams &gparams, int iiter)
// {
//     for (int i = 0; i < gparams.all_op.size(); i++) {
//         for (int j = 0; j < gparams.all_op[i]->weight.size(); j++) {
//             gparams.all_op[i]->weight(j) = 1.0;
//         }
//     }

//     for (int i = 0; i < gparams.all_obj.size(); i++) {
//         for (int j = 0; j < gparams.all_obj[i]->weight.size(); j++) {
//             gparams.all_obj[i]->weight(j) *= 2;
//         }
//     }
// }


void logger(GroptParams &gparams, int iiter, Eigen::VectorXd &X, Solver &solver, bool force_print)
{  
    
    if (iiter < 0) {
        log_print(LOG_VERBOSE, "Optimization ended without finshing a full iteration . . .");

    } else if ( (((iiter % gparams.verbose_interval) == 0) && (LOG_LEVEL >= LOG_VERBOSE)) || force_print ){

        double current_obj = 0.0;
        double max_diff = 0.0;    

        // Get the current objective value
        if ((gparams.all_obj.size() > 0) && (gparams.all_obj[0]->hist_obj.size() > 0)) {

            current_obj = gparams.all_obj[0]->hist_obj(0,iiter);

            max_diff = 0.0;
            
            // Find the biggest objective value difference from current, in the last N_HIST_TEMP iterations
            for (int i = 0; i < N_HIST_TEMP; i++) {
                if ((iiter - i) < 0) {break;}
                double obj = gparams.all_obj[0]->hist_obj(0,iiter - i);
                double diff = fabs(current_obj - obj);
                if (diff > max_diff) {
                    max_diff = diff;
                }
            }
            // Normalize
            max_diff /= current_obj;
        }

        log_print(LOG_VERBOSE, "\n~~~~~~~~  Update iiter = %d  ~~~~~~~~   solver iter = %d  current_obj = %.2e  max_diff = %.2e  total_n_feval = %.0f",  
                    iiter, solver.hist_n_iter[iiter], current_obj, max_diff, gparams.total_n_feval);
                                

        
        
        
        for (int i = 0; i < gparams.all_op.size(); i++) {
            log_print(LOG_VERBOSE, "   *** %-12s   --  Checks: %s   --  Weights: %s   --  Gamma: %s   --  r_feas: %s ",  
                        gparams.all_op[i]->name.c_str(), 
                        eigen2str(gparams.all_op[i]->hist_check.col(gparams.last_iiter).transpose()).c_str(),
                        eigen2str(gparams.all_op[i]->weight.transpose()).c_str(),
                        eigen2str(gparams.all_op[i]->gamma.transpose()).c_str(),
                        eigen2str(gparams.all_op[i]->hist_feas.col(iiter).transpose()).c_str() );
        }



    }
}


int do_checks(GroptParams &gparams, int iiter, Eigen::VectorXd &X)
{    

    if (X.hasNaN()) {
        log_print(LOG_WARNING, "WARNING: optimize.cpp stopped due to NaN in X");
        return 1;
    }

    double current_obj = 0.0;
    double max_diff = 0.0;    
    // Get the current objective value
    if (gparams.all_obj.size() > 0) {
        current_obj = gparams.all_obj[0]->hist_obj(0,iiter);
        max_diff = 0.0;
        
        // Find the biggest objective value difference from current, in the last N_HIST_TEMP iterations
        for (int i = 0; i < N_HIST_TEMP; i++) {
            if ((iiter - i) < 0) {break;}
            double obj = gparams.all_obj[0]->hist_obj(0,iiter - i);
            double diff = fabs(current_obj - obj);
            if (diff > max_diff) {
                max_diff = diff;
            }
        }
        // Normalize
        max_diff /= current_obj;
    }

    // Sum up all of the check values, (0 is pass so anything greater than 0 does not pass)
    double all_check = 0.0;
    for (int i = 0; i < gparams.all_op.size(); i++) {
        all_check += gparams.all_op[i]->hist_check.col(iiter).sum();
    }
    
    // Start reducing objective weights if we are close to the end and aren't passing checks
    if ((all_check > 0) && (gparams.obj_min > 0) && (iiter > (gparams.N_iter - gparams.obj_min)))
    {
        log_print_nn(LOG_VERBOSE, "Reducing weights: ");
        for (int i = 0; i < gparams.all_obj.size(); i++) {
            gparams.all_obj[i]->weight *= gparams.obj_scale;
            log_print_nn(LOG_VERBOSE, "%s   ", eigen2str(gparams.all_obj[i]->weight).c_str());
        }
        log_print(LOG_VERBOSE, " Done!");
    }



    // -------------- Stopping Condition Checks --------------

    if ((max_diff < gparams.d_obj_thresh) && (all_check < 0.5)  && (iiter > 0)) {
        // The waveform has converged and passed all checks
        log_print(LOG_INFO, "optimize.cpp do_checks() passed!  iiter = %d  obj = %.2e  max_diff = %.2e  all_check = %.1f", iiter, current_obj, max_diff, all_check);
        gparams.final_good = 2; // Converged and passed checks
        return 1;
    } else if ((gparams.total_n_feval > (gparams.N_feval - 1000)) && (all_check < 0.5)  && (iiter > 0)) {
        // Waveforms passed checks, but did not converge (and within 1000 f_eval of f_eval limit)
        log_print(LOG_INFO, "optimize.cpp do_checks() SEMI-passed!  iiter = %d  obj = %.2e  max_diff = %.2e  total_n_feval = %.0f  N_feval = %d  all_check = %.1f", 
                       iiter, current_obj, max_diff, gparams.total_n_feval, gparams.N_feval, all_check);
        gparams.final_good = 1; // Passed checks, didn't converge
        return 1;
    } else if (gparams.total_n_feval > gparams.N_feval) {
        // Did too many f_eval and did not converge or pass checks
        log_print(LOG_INFO, "optimize.cpp do_checks() failed, too many f_eval  iiter = %d  obj = %.2e  max_diff = %.2e  total_n_feval = %.0f  N_feval = %d  all_check = %.1f", 
                       iiter, current_obj, max_diff, gparams.total_n_feval, gparams.N_feval, all_check);
        gparams.final_good = 0;
        return 1;
    } else if ( (iiter == (gparams.N_iter-1)) && (all_check < 0.5) ) {
        // Waveforms passed checks, but did not converge (and on last iteration)
        log_print(LOG_INFO, "optimize.cpp do_checks() SEMI-passed2!  iiter = %d  obj = %.2e  max_diff = %.2e  total_n_feval = %.0f  N_feval = %d  all_check = %.1f", 
                       iiter, current_obj, max_diff, gparams.total_n_feval, gparams.N_feval, all_check);
        gparams.final_good = 1;
        return 1;    
    } else {
        gparams.final_good = 0;
        return 0;
    }


}

void debug_names(GroptParams &gparams) {

    for (int i = 0; i < gparams.all_op.size(); i++) {
        for (int j = 0; j < gparams.all_op[i]->weight.size(); j++) {
            std::stringstream sstm;
            sstm << gparams.all_op[i]->name << "_" << j;
            gparams.debugger.op_names.push_back(sstm.str());
        }
    }

    for (int i = 0; i < gparams.all_obj.size(); i++) {
        for (int j = 0; j < gparams.all_obj[i]->weight.size(); j++) {
            std::stringstream sstm;
            sstm << gparams.all_obj[i]->name << "_" << j;
            gparams.debugger.op_names.push_back(sstm.str());
        }
    }
}

void run_debugger(GroptParams &gparams)
{
    std::vector<double> weights;
    std::vector<double> gammas;
    std::vector<double> feas;

    for (int i = 0; i < gparams.all_op.size(); i++) {
        for (int j = 0; j < gparams.all_op[i]->weight.size(); j++) {
            weights.push_back(gparams.all_op[i]->weight(j));
            gammas.push_back(gparams.all_op[i]->gamma(j));
            feas.push_back(gparams.all_op[i]->r_feas(j));
        }
    }

    for (int i = 0; i < gparams.all_obj.size(); i++) {
        for (int j = 0; j < gparams.all_obj[i]->weight.size(); j++) {
            weights.push_back(gparams.all_obj[i]->weight(j));
            gammas.push_back(gparams.all_obj[i]->gamma(j));
            feas.push_back(gparams.all_obj[i]->r_feas(j));
        }
    }

    gparams.debugger.hist_weight.push_back(weights);
    gparams.debugger.hist_gamma.push_back(gammas);
    gparams.debugger.hist_feas.push_back(feas);

    if (gparams.debugger.op_names.size() == 0) {
        debug_names(gparams);
    }

}   



void run_optimization(GroptParams &gparams, Eigen::VectorXd &out)
{
    gparams.start_time = std::chrono::steady_clock::now();

    // Initialize starting vector
    Eigen::VectorXd X;
    X = gparams.X0;

    // This should also be a vector to automatically resize
    Eigen::MatrixXd Xhist;
    Xhist.setZero(N_HIST_TEMP, gparams.Naxis*gparams.N);

    // Initialize the CG iteration class
    Solver *solver; 
    
    if (gparams.solver_type == "cg") {
        solver = new CG_Iter(gparams.Naxis*gparams.N, gparams.cg_niter);
    } else if (gparams.solver_type == "lsmr") {
        solver = new LSMR_Iter(gparams.Naxis*gparams.N, gparams.all_op, gparams.all_obj, gparams.cg_niter);
    } else if (gparams.solver_type == "minres") {
        solver = new MINRES_Iter(gparams.Naxis*gparams.N, gparams.cg_niter, gparams.cg_rtol, gparams.cg_shift);
    } else if (gparams.solver_type == "minresqlp") {
        solver = new MINRESQLP_Iter(gparams.Naxis*gparams.N, gparams.cg_niter, gparams.cg_rtol, gparams.cg_shift);
    }

    // Solver *solver; 
    // std::vector<Solver*> all_solvers;
    // all_solvers.push_back(new CG_Iter(gparams.Naxis*gparams.N, gparams.cg_niter));
    // all_solvers.push_back(new LSMR_Iter(gparams.Naxis*gparams.N, gparams.all_op, gparams.all_obj, gparams.cg_niter));
    // all_solvers.push_back(new MINRES_Iter(gparams.Naxis*gparams.N, gparams.cg_niter, gparams.cg_rtol, gparams.cg_shift));
    // all_solvers.push_back(new MINRESQLP_Iter(gparams.Naxis*gparams.N, gparams.cg_niter, gparams.cg_rtol, gparams.cg_shift));

    gparams.init_all_vals();

    for (int i = 0; i < gparams.all_op.size(); i++) {
        gparams.all_op[i]->init(X, gparams.do_init);
    }

    // Number of function evaluations (counts CG iterations)
    gparams.total_n_feval = 0;

    // Actual iterations
    int iiter;
    for (iiter = 0; iiter < gparams.N_iter; ++iiter) {

        // Store what iteration we are on for later array indexing
        gparams.last_iiter = iiter;

        // Debugging: comment for release
        if (gparams.debugger.debug_active) {
            gparams.debugger.hist_x0.push_back(X); 
            run_debugger(gparams);
            solver->get_residual(gparams, X, 0);
        }

        std::vector<double> pre_norms = solver->get_stats(gparams, X);
        std::vector<double> pre_norms2 = solver->get_stats_normal(gparams, X);

        X = solver->solve(gparams.all_op, gparams.all_obj, X, iiter);

        std::vector<double> post_norms = solver->get_stats(gparams, X);
        std::vector<double> post_norms2 = solver->get_stats_normal(gparams, X);

        // log_print(LOG_NOTHING, "+++ %-12s Iteration: %05d  rnorm = %.2e -> %.2e (%.2f)  rnorm2 = %.2e -> %.2e (%.2f)   Arnorm = %.2e -> %.2e (%.2f)  Arnorm2 = %.2e -> %.2e (%.2f)  solve time = %.2f", 
        //                 solver->name, iiter, 
        //                 pre_norms[2], post_norms[2], post_norms[2]/pre_norms[2], 
        //                 pre_norms2[2], post_norms2[2], post_norms2[2]/pre_norms2[2],
        //                 pre_norms[1], post_norms[1], post_norms[1]/pre_norms[1], 
        //                 pre_norms2[1], post_norms2[1], post_norms2[1]/pre_norms2[1],
        //                 solver->elapsed_us.count());

        log_print(LOG_DEBUG, "+++ %-12s Iteration: %05d   rnorm = %.2e -> %.2e (%.2f)   rnorm2 = %.2e -> %.2e (%.2f)   solve time = %.2f", 
                solver->name.c_str(), iiter, 
                pre_norms[2], post_norms[2], post_norms[2]/pre_norms[2], 
                pre_norms2[2], post_norms2[2], post_norms2[2]/pre_norms2[2],
                solver->elapsed_us.count());

        // LineSearch *linesearch;
        // linesearch->linesearch(gparams, X);
        

        // Eigen::VectorXd Xtemp;
        // for (int i_solve = 0; i_solve < all_solvers.size(); i_solve++) {
        //     solver = all_solvers[i_solve];

        //     std::vector<double> pre_norms = solver->get_stats(gparams, X);
        //     std::vector<double> pre_norms2 = solver->get_stats_normal(gparams, X);

        //     // Do CG iterations
        //     Xtemp = solver->solve(gparams.all_op, gparams.all_obj, X, iiter);

        //     // Debugging: comment for release
        //     std::vector<double> post_norms = solver->get_stats(gparams, Xtemp);
        //     std::vector<double> post_norms2 = solver->get_stats_normal(gparams, Xtemp);

        //     log_print(LOG_NOTHING, "+++ %-12s Iteration: %05d  rnorm = %.2e -> %.2e (%.2f)  rnorm2 = %.2e -> %.2e (%.2f)   Arnorm = %.2e -> %.2e (%.2f)  Arnorm2 = %.2e -> %.2e (%.2f)  solve time = %.2f", 
        //                 solver->name, iiter, 
        //                 pre_norms[2], post_norms[2], post_norms[2]/pre_norms[2], 
        //                 pre_norms2[2], post_norms2[2], post_norms2[2]/pre_norms2[2],
        //                 pre_norms[1], post_norms[1], post_norms[1]/pre_norms[1], 
        //                 pre_norms2[1], post_norms2[1], post_norms2[1]/pre_norms2[1],
        //                 solver->elapsed_us.count());
        // }
        // X = Xtemp;

        if (gparams.debugger.debug_active) {
            gparams.debugger.hist_x1.push_back(X); 
            solver->get_residual(gparams, X, 1);
            gparams.debugger.hist_cgiter.push_back(solver->hist_n_iter[iiter]);
        }

        gparams.total_n_feval += solver->hist_n_iter[iiter];

        // Update all constraints (do prox operations)        
        for (int i = 0; i < gparams.all_op.size(); i++) {
            gparams.all_op[i]->update(X, iiter);
        }

        if (gparams.debugger.debug_active) {
            gparams.debugger.hist_x2.push_back(X); 
        }

        // Compute objective values if there are some
        for (int i = 0; i < gparams.all_obj.size(); i++) {
            gparams.all_obj[i]->get_obj(X, iiter);
        }

        // Stopping checks
        if (do_checks(gparams, iiter, X) > 0) {
            break;
        }

        // Reweight constraints
        do_globalreweight(gparams, iiter);

        // if (iiter == 1000) {
        //     reset_weights(gparams, iiter);
        // }

        logger(gparams, iiter, X, *solver, false);
    }

    gparams.stop_time = std::chrono::steady_clock::now();
    gparams.elapsed_us = gparams.stop_time - gparams.start_time;

    log_print(LOG_VERBOSE, "\n!!!!!!!!!!! Final Logger: !!!!!!!!!!!");
    logger(gparams, iiter-1, X, *solver, true);
    log_print(LOG_VERBOSE, "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n");
    
    gparams.total_n_iter = iiter;
    
    out = X;

    return;
}


// Interp one vector to another based only on its size
// The first and last points match up exactly, and then everything is linearly interpolated
// I think there is some more insight into how this could be done better in some Pulseq docs, need to look that up
//  (with regard to where you are interpolating in dt, the center of the segment or beginning, etc...)
void interp_vec2vec(Eigen::VectorXd &vec0, Eigen::VectorXd &vec1) {
    int N0 = vec0.size();
    int N1 = vec1.size();
    
    if (N0 == N1) {
        vec1 = vec0;
        return;
    }

    double tt;
    double di0;
    int i0_lo, i0_hi;
    double v_lo, v_hi;
    double d_lo, d_hi;

    for (int i1 = 0; i1 < N1; i1++) {
        
        tt = (double)i1 / (N1-1);
        
        di0 = tt * (N0-1);
        i0_lo = floor(di0);
        if (i0_lo < 0) {i0_lo = 0;}  // This shouldn't happen unless some weird rounding and floor?
        i0_hi = i0_lo + 1;

        if (i0_hi < N0) {
            d_lo = fabs(di0-i0_hi);
            d_hi = 1.0 - d_lo;

            v_lo = d_lo * vec0(i0_lo);
            v_hi = d_hi * vec0(i0_hi);

            vec1(i1) = v_lo + v_hi;
        } else {
            d_lo = fabs(di0-i0_hi);
            v_lo = d_lo * vec0(i0_lo);
            vec1(i1) = v_lo;
        }
    }
}

}  // end namespace Gropt
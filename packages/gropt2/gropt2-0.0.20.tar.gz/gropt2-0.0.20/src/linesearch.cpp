
#include "linesearch.hpp"
#include "logging.hpp"

namespace Gropt {

void LineSearch::linesearch(GroptParams &gparams, Eigen::VectorXd &X) {

    Eigen::VectorXd dX = gparams.all_obj[0]->get_AtAx(X, 0);

    for (double weight = -1; weight < 1 ; weight += 0.1) {
        Eigen::VectorXd XdX = X + (weight * dX);
        double res = get_res(gparams, XdX);
        double res2 = get_res2(gparams, XdX);

        gparams.all_obj[0]->Ax_temp.setZero();
        gparams.all_obj[0]->forward(XdX, gparams.all_obj[0]->Ax_temp, false, 0, true);
        double bval = gparams.all_obj[0]->Ax_temp.squaredNorm();

        log_print(LOG_NOTHING, "    LS weight %.1f   res = %.2e   res2 = %.2e   bval = %.1f", 
                        weight, res, res2, bval); 
    }

    // double final_weight = gparams.all_obj[0]->weight(0);
    // X = (final_weight * dX);
}


double LineSearch::get_res(GroptParams &gparams, Eigen::VectorXd &X) {
    
    double rnorm = 0;

    for (int i = 0; i < gparams.all_op.size(); i++) {
        gparams.all_op[i]->Ax_temp.setZero();
        gparams.all_op[i]->forward(X, gparams.all_op[i]->Ax_temp, 1, 1, false);

        rnorm += (gparams.all_op[i]->Ax_temp - gparams.all_op[i]->get_b()).squaredNorm();
    }

    rnorm = sqrt(rnorm);
    return rnorm;
}


double LineSearch::get_res2(GroptParams &gparams, Eigen::VectorXd &X) {
    
    Eigen::VectorXd temp_Ax;
    Eigen::VectorXd temp_b;

    temp_Ax.setZero(gparams.N);
    temp_b.setZero(gparams.N);

    for (int i = 0; i < gparams.all_op.size(); i++) {
        gparams.all_op[i]->add2AtAx(X, temp_Ax);
        gparams.all_op[i]->add2b(temp_b);
    }

    for (int i = 0; i < gparams.all_obj.size(); i++) {
        gparams.all_obj[i]->add2AtAx(X, temp_Ax);
        gparams.all_obj[i]->obj_add2b(temp_b);
    }

    double rnorm = (temp_Ax - temp_b).norm();
    return rnorm;
}



}

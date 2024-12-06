#include <iostream> 

#include "gropt_params.hpp"
#include "logging.hpp"

using namespace Gropt;

void demo_bipolar_minTE()
{
    double dt = 10e-6;
    
    double T = 2e-3;
    double good_check = 1;

    while (good_check > 0) {
        GroptParams gparams;
        T -= dt; 
        int N = floor(T/dt) + 1;

        gparams.init_N(N, dt);
        gparams.add_gmax(.035);
        gparams.add_smax(100);
        gparams.add_moment(0, 0);
        gparams.add_moment(1, 14);
        gparams.verbose = 0;

        gparams.optimize();

        good_check = gparams.final_good;
        std::cout << "T = " << T;
        std::cout << "  N = " << N;
        std::cout << "  good_check = " << good_check << std::endl;
    }
}

int main(int argc, char* argv[]) 
{
    // LOG_LEVEL = LOG_VERBOSE;
    demo_bipolar_minTE();
    return 0;
}


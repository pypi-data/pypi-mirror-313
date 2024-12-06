#include <fstream>
#include "logging.hpp"
#include "Eigen/Dense"

namespace Gropt {

// This can be changed anywhere you include logging.hpp
log_level_t LOG_LEVEL = LOG_WARNING;

void log_print(log_level_t level, char const* fmt_str, ...) { 
    if (level <= LOG_LEVEL) {
        char dest[1024 * 16];
        va_list argptr;
        va_start(argptr, fmt_str);
        vsprintf(dest, fmt_str, argptr);
        va_end(argptr);
        printf(dest);
        printf("\n");
        fflush(stdout);
    }
}

void log_print_nn(log_level_t level, char const* fmt_str, ...) { 
    if (level <= LOG_LEVEL) {
        char dest[1024 * 16];
        va_list argptr;
        va_start(argptr, fmt_str);
        vsprintf(dest, fmt_str, argptr);
        va_end(argptr);
        printf(dest);
        fflush(stdout);
    }
}

std::string eigen2str(const Eigen::MatrixXd& mat){
    std::stringstream ss;
    ss << mat;
    return ss.str();
}

void write_vector_xd(const std::string &filename, const Eigen::VectorXd &vec) {
    std::ofstream out(filename, std::ios::out | std::ios::binary | std::ios::trunc);
    out.write((char*) vec.data(), vec.size()*sizeof(double));
    out.close();
}

template<class Derived>
void WriteEigen(const Eigen::PlainObjectBase<Derived>& dense, const std::string &fileName) {
    std::ofstream outFile(fileName, std::ios_base::out | std::ios_base::binary);
    const auto& reshaped = dense.reshaped();
    std::copy(reshaped.begin(), reshaped.end(), std::ostream_iterator<typename Derived::Scalar>(outFile));
}

}

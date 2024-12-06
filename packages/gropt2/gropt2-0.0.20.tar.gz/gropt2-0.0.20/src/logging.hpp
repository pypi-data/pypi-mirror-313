#ifndef LOGGING_H
#define LOGGING_H

#include <stdarg.h>
#include <iostream>
#include <string>
#include "Eigen/Dense"

namespace Gropt {

enum log_level_t {
    LOG_NOTHING,
    LOG_CRITICAL,
    LOG_ERROR,
    LOG_WARNING,
    LOG_INFO,
    LOG_VERBOSE,
    LOG_DEBUG
};

extern log_level_t LOG_LEVEL;

void log_print(log_level_t level, char const* fmt_str, ...);
void log_print_nn(log_level_t level, char const* fmt_str, ...);
std::string eigen2str(const Eigen::MatrixXd& mat);
void write_vector_xd(const std::string &filename, const Eigen::VectorXd &vec);

template<class Derived>
void WriteEigen(const Eigen::PlainObjectBase<Derived>& dense, const std::string &fileName);

}  // close "namespace Gropt"

#endif
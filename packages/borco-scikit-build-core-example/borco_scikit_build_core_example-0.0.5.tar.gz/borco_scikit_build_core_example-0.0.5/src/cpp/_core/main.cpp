#include "square.h"

#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(_core, m) {
    m.doc() = "pybind11 example module";
    m.def("square", &square);
}

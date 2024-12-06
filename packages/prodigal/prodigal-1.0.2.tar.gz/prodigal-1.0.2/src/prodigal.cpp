#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <iostream>

namespace py = pybind11;

extern "C" {
    int main(int argc, char* argv[]);
}

void run(const std::vector<std::string>& args) {
    std::vector<char*> c_args;

    c_args.push_back(const_cast<char*>("prodigal"));
    for (const auto& arg : args) {
        c_args.push_back(const_cast<char*>(arg.c_str()));
    }

    // Call the actual main function.
    main(static_cast<int>(c_args.size()), c_args.data());
}


PYBIND11_MODULE(prodigal_py, m) {
    m.doc() = R"pbdoc(
        Pybind11 Prodigal module
        ------------------------

        .. currentmodule:: prodigal

        .. autosummary::
           :toctree: _generate

           run
    )pbdoc";

    m.def(
        "run",
        &run,
        "Run Prodigal tool: https://github.com/hyattpd/Prodigal/wiki/",
        py::arg("args")
    );
}

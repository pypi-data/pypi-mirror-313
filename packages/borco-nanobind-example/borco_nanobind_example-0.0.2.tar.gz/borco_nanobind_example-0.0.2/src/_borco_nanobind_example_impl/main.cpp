#include "add.h"
#include "dog.h"

#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>

namespace nb = nanobind;
using namespace nb::literals;

// the module name must match the name provided to nanobind_add_module in CMakeLists.txt
NB_MODULE(_borco_nanobind_example_impl, m)
{
    // set the module docstring
    m.doc() = "A simple example python extension";

    // export a function
    m.def("add", &add, "a"_a, "b"_a = 1,
          "This function adds two numbers and increments if only one is provided.");

    // export a value
    m.attr("the_answer") = 42;

    // export a class
    nb::class_<Dog>(m, "Dog")
        // define constructors
        .def(nb::init<>(), "Create a dog with no name.")
        .def(nb::init<const std::string &>(), "name"_a, "Create a dog with a name.")
        // export a method
        .def("bark", &Dog::bark, "Make the dog bark.")
        // export a mutable member
        .def_rw("name", &Dog::name, "The name of the dog.")
        // export a lambda - this adds extra functionality, not defined in the Dog class
        .def("__repr__", [](const Dog &p) { return "<my_ext.Dog named '" + p.name + "'>"; });
}

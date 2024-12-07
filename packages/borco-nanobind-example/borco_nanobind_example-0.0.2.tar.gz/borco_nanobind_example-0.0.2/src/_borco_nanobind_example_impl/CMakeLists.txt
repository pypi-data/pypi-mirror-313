# the module name must match the name provided to NB_MODULE in C++
set(MODULE_NAME _borco_nanobind_example_impl)

nanobind_add_module(
    # name of the extension
    ${MODULE_NAME}

    # Target the stable ABI for Python 3.12+, which reduces
    # the number of binary wheels that must be built. This
    # does nothing on older Python versions
    STABLE_ABI

    # source files
    main.cpp
)

target_link_libraries(${MODULE_NAME} PUBLIC _core_lib)

# Install directive for scikit-build-core
install(TARGETS ${MODULE_NAME} LIBRARY DESTINATION ${CMAKE_PROJECT_NAME})

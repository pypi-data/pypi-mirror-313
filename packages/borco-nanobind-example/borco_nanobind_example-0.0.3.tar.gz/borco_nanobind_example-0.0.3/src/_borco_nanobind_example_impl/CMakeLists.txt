# The module name must match the name provided to NB_MODULE in C++
set(MODULE_NAME _borco_nanobind_example_impl)

# Creates the python binding
nanobind_add_module(
    ${MODULE_NAME}

    # Target the stable ABI for Python 3.12+, which reduces
    # the number of binary wheels that must be built. This
    # does nothing on older Python versions
    STABLE_ABI

    # source files
    main.cpp
)

# Creates typing information in *.pyi and a py.typed marker
nanobind_add_stub(
    ${MODULE_MODULE}_stub
    MODULE ${MODULE_NAME}
    OUTPUT ${MODULE_NAME}.pyi
    PYTHON_PATH $<TARGET_FILE_DIR:${MODULE_NAME}>
    DEPENDS ${MODULE_NAME}
    MARKER_FILE py.typed
)

target_link_libraries(${MODULE_NAME} PUBLIC _core_lib)

# Install the *.pyd binding library
install(TARGETS ${MODULE_NAME} LIBRARY DESTINATION ${CMAKE_PROJECT_NAME})

# Install the files with type information
install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/py.typed
    ${CMAKE_CURRENT_BINARY_DIR}/${MODULE_NAME}.pyi
    DESTINATION ${CMAKE_PROJECT_NAME}
)

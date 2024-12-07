cmake_minimum_required(VERSION 3.29)


# --------------------
# project definition
# --------------------
if(NOT SKBUILD)
    message("-- Running CMake directly.")
    set(SKBUILD_PROJECT_NAME borco_nanobind_example)
else()
    message("-- Running from 'scikit-build-core'.")
endif()

project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)


# --------------
# C++ features
# --------------
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


# ------------------
# Check for Python
# ------------------
find_package(Python 3.12
    REQUIRED COMPONENTS Interpreter Development.Module
    OPTIONAL_COMPONENTS Development.SABIModule
)


# --------------------------------------------------------------------
# FetchContent is required to install software from remote git repos
# --------------------------------------------------------------------
include(FetchContent)


# ------------------
# install nanobind
# ------------------
FetchContent_Declare(
    nanobind
    GIT_REPOSITORY https://github.com/wjakob/nanobind.git
    GIT_TAG v2.2.0 # or a later release
)
FetchContent_MakeAvailable(nanobind)


# ----------------------------------
# add subdirectories with C++ code
# ----------------------------------
add_subdirectory(src/_core_lib)
add_subdirectory(src/_borco_nanobind_example_impl)

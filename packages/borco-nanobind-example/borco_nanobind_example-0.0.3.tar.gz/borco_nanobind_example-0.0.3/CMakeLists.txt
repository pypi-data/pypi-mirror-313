cmake_minimum_required(VERSION 3.29)


# --------------------
# Project definition
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


# ---------
# Options
# ---------
include(CMakeDependentOption)

cmake_dependent_option(
    _CPP_DEV_MODE "Enable C++ developer mode." ON "NOT DEFINED SKBUILD" OFF
)

cmake_dependent_option(
    WITH_DEMOS "Build demo applications." ON "_CPP_DEV_MODE" OFF
)

cmake_dependent_option(
    WITH_TESTS "Build tests." ON "_CPP_DEV_MODE" OFF
)

# Catch2: https://github.com/catchorg/Catch2
cmake_dependent_option(
    WITH_CATCH2 "Enable Catch2 tests." ON "WITH_TESTS" OFF
)

# Google Test: https://google.github.io/googletest/
cmake_dependent_option(
    WITH_GTEST "Enable Google Test/Google Mock tests." ON "WITH_TESTS" OFF
)


# --------------------------------------------------------------------
# FetchContent is required to install software from remote git repos
# --------------------------------------------------------------------
include(FetchContent)


# -----------
# c++ tests
# -----------
if(${WITH_TESTS})
    include(CTest)

    if(${WITH_CATCH2})
        FetchContent_Declare(
            Catch2
            GIT_REPOSITORY https://github.com/catchorg/Catch2.git
            GIT_TAG v3.7.1 # or a later release
        )
        FetchContent_MakeAvailable(Catch2)

        # dirs with c++ tests
        add_subdirectory(tests/cpp/catch/_core_lib)
    endif()

    if(${WITH_GTEST})
        FetchContent_Declare(
            GoogleTest
            GIT_REPOSITORY https://github.com/google/googletest
            GIT_TAG v1.15.2
        )
        # For Windows: Prevent overriding the parent project's compiler/linker settings
        set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
        FetchContent_MakeAvailable(GoogleTest)

        # dirs with c++ tests
        add_subdirectory(tests/cpp/google/_core_lib)
    endif()
endif()


# ------------------
# Check for Python
# ------------------
find_package(Python 3.12
    REQUIRED COMPONENTS Interpreter Development.Module
    OPTIONAL_COMPONENTS Development.SABIModule
)


# ------------------
# Install nanobind
# ------------------
FetchContent_Declare(
    nanobind
    GIT_REPOSITORY https://github.com/wjakob/nanobind.git
    GIT_TAG v2.2.0 # or a later release
)
FetchContent_MakeAvailable(nanobind)


# ----------------------------------
# Add subdirectories with C++ code
# ----------------------------------
add_subdirectory(src/_core_lib)
add_subdirectory(src/_borco_nanobind_example_impl)

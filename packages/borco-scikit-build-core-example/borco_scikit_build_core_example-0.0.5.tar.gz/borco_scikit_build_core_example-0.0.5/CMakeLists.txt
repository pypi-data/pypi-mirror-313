cmake_minimum_required(VERSION 3.29)


# ---------
# options
# ---------

include(CMakeDependentOption)

cmake_dependent_option(
    _CPP_DEV_MODE "Enable C++ developer mode." ON "NOT DEFINED SKBUILD_PROJECT_NAME" OFF
)

cmake_dependent_option(
    WITH_DEMOS "Build demo applications." ON "_CPP_DEV_MODE" OFF
)

cmake_dependent_option(
    WITH_TESTS "Build tests." ON "_CPP_DEV_MODE" OFF
)

# Catch2: https://github.com/catchorg/Catch2
cmake_dependent_option(
    WITH_CATCH2 "Enable Catch2 tests." OFF "WITH_TESTS" OFF
)

# Google Test: https://google.github.io/googletest/
cmake_dependent_option(
    WITH_GTEST "Enable Google Test/Google Mock tests." ON "WITH_TESTS" OFF
)


# --------------
# main c++ lib
# --------------

if(NOT DEFINED SKBUILD_PROJECT_NAME)
    set(SKBUILD_PROJECT_NAME borco_scikit_build_core_example)
endif()

project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Core Test)

add_subdirectory(src/cpp/_core_lib)


# -----------------
# python bindings
# -----------------

if(NOT ${_CPP_DEV_MODE})
    set(PYBIND11_NEWPYTHON ON)
    find_package(pybind11 CONFIG)
    if(pybind11_FOUND)
        add_subdirectory(src/cpp/_core)
    endif()
endif()

# ---------------
# c++ demo apps
# ---------------

if(${WITH_DEMOS})
    add_subdirectory(demos/cpp/simple)
endif()


# -----------
# c++ tests
# -----------

if(${WITH_TESTS})
    include(FetchContent)

    include(CTest)

    add_subdirectory(tests/cpp/qtest/square)

    if(${WITH_CATCH2})
        FetchContent_Declare(
            Catch2
            GIT_REPOSITORY https://github.com/catchorg/Catch2.git
            GIT_TAG v3.7.1 # or a later release
        )
        FetchContent_MakeAvailable(Catch2)

        add_subdirectory(tests/cpp/catch/square)
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

        add_subdirectory(tests/cpp/google/square)
    endif()
endif()

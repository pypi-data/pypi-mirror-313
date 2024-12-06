cmake_minimum_required(VERSION 3.29)

if(NOT DEFINED SKBUILD_PROJECT_NAME)
    set(SKBUILD_PROJECT_NAME scikit-build-core-example)
endif()

# Catch2: https://github.com/catchorg/Catch2
option(WITH_CATCH2 "Enable Catch2 tests." OFF)

# Google Test: https://google.github.io/googletest/
option(WITH_GTEST "Enable Google Test/Google Mock tests." OFF)

project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Core Test)

if(${WITH_CATCH2} OR ${WITH_GTEST})
    include(FetchContent)
endif()

# main library
add_subdirectory(src/cpp/_core_lib)

# tests
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

# pybind11
set(PYBIND11_NEWPYTHON ON)
find_package(pybind11 CONFIG)
if(pybind11_FOUND)
    add_subdirectory(src/cpp/_core)
endif()

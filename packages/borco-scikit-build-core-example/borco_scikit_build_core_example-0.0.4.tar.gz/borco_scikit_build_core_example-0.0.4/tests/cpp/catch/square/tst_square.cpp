#include <catch2/catch_test_macros.hpp>
#include <catch2/generators/catch_generators.hpp>

#include "square.h"

unsigned int Factorial(unsigned int number)
{
    return number > 1 ? Factorial(number - 1) * number : 1;
}

TEST_CASE("Catch2 factorial example", "[factorial]")
{
    REQUIRE(Factorial(0) == 1);
    REQUIRE(Factorial(1) == 1);
    REQUIRE(Factorial(2) == 2);
    REQUIRE(Factorial(3) == 6);
    REQUIRE(Factorial(10) == 3628800);
}

TEST_CASE("Catch2 square example")
{
    // Needs C++17 or newer for this format to work
    auto [test_input, expected_output] = GENERATE(
        table<float, float>({
            {1, 1},
            {2, 4},
            {3, 9},
            {-1, 1},
            {-2, 4}
        })
        );

    // capture the input data to go with the outputs.
    CAPTURE(test_input);

    // check it matches the pre-calculated data
    REQUIRE(square(test_input) == expected_output);
}

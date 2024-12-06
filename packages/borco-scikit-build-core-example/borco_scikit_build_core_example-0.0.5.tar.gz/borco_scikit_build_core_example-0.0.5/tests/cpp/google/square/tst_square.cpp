#include <gtest/gtest.h>
#include <tuple>

#include "square.h"


// Demonstrate some basic assertions.
TEST(GoogleExample1, BasicAssertions)
{
    // Expect two strings not to be equal.
    EXPECT_STRNE("hello", "world");
    // Expect equality.
    EXPECT_EQ(7 * 6, 42);
}


using SquareTestFixtureValue = std::tuple<double, double>;

class SquareTestFixture: public testing::TestWithParam<SquareTestFixtureValue> {};


TEST_P(SquareTestFixture, Square)
{
    auto [input_value, expected_result] = GetParam();
    EXPECT_EQ(square(input_value), expected_result);
}

SquareTestFixtureValue square_test_fixture_values[] = {
    {1, 1},
    {2, 4},
    {-1, 1},
    {-2, 4},
};


INSTANTIATE_TEST_SUITE_P(
    GoogleExample2,
    SquareTestFixture,
    ::testing::ValuesIn(square_test_fixture_values)
);

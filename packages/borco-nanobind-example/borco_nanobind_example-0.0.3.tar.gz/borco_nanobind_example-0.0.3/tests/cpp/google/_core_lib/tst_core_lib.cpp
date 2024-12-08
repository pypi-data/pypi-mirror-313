#include <gtest/gtest.h>
#include <tuple>

#include "add.h"

using AddTestFixtureValue = std::tuple<int, int, int>;

AddTestFixtureValue add_test_fixture_values[] = {
    {1, 1, 2},
    {2, 4, 6},
    {-1, 1, 0},
};

class AddTestFixture : public testing::TestWithParam<AddTestFixtureValue>
{
};

TEST_P(AddTestFixture, Add)
{
    auto [a, b, expected_result] = GetParam();
    EXPECT_EQ(add(a, b), expected_result);
}

INSTANTIATE_TEST_SUITE_P(GoogleExample, AddTestFixture,
                         ::testing::ValuesIn(add_test_fixture_values));

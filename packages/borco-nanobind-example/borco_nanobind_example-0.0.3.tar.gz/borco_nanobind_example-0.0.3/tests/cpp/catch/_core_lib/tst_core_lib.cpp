#include <catch2/catch_test_macros.hpp>
#include <catch2/generators/catch_generators.hpp>

#include "add.h"

TEST_CASE("Catch2 _core_lib.add example")
{
    // Needs C++17 or newer for this format to work
    auto [a, b, expected_output] = GENERATE(table<int, int, int>({
        {1, 1, 2},
        {1, 2, 3},
    }));

    // capture the input data to go with the outputs.
    CAPTURE(a, b);

    // check it matches the pre-calculated data
    REQUIRE(add(a, b) == expected_output);
}

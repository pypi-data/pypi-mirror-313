set(TEST_APP tst_google_core_lib)

enable_testing()

add_executable(
    ${TEST_APP}
    tst_core_lib.cpp
)

target_link_libraries(
    ${TEST_APP} PRIVATE
    GTest::gtest_main
    _core_lib
)

include(GoogleTest)
gtest_discover_tests(${TEST_APP})

add_test(NAME ${TEST_APP} COMMAND ${TEST_APP})

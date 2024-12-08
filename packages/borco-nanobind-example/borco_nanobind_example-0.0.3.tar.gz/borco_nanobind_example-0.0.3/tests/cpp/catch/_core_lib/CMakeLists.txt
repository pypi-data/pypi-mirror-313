set(TEST_APP tst_catch_core_lib)

enable_testing()

add_executable(
    ${TEST_APP}
    tst_core_lib.cpp
)

target_link_libraries(
    ${TEST_APP} PRIVATE
    Catch2::Catch2WithMain
    _core_lib
)

add_test(NAME ${TEST_APP} COMMAND ${TEST_APP})

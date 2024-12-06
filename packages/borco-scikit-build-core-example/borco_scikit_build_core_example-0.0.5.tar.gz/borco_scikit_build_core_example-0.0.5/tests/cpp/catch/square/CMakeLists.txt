set(TEST_APP tst_catch_square)
set(TEST_NAME catch_square)

enable_testing()

add_executable(
    ${TEST_APP}
    tst_square.cpp
)

target_link_libraries(
    ${TEST_APP} PRIVATE
    Catch2::Catch2WithMain
    _core_lib
)

add_test(NAME ${TEST_NAME} COMMAND ${TEST_APP})

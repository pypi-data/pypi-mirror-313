set(TEST_APP tst_qtest_square)
set(TEST_NAME qtest_square)

enable_testing()

add_executable(
    ${TEST_APP}
    tst_square.cpp
)

target_link_libraries(
    ${TEST_APP} PRIVATE
    Qt6::Test
    _core_lib
)

add_test(NAME ${TEST_NAME} COMMAND ${TEST_APP})

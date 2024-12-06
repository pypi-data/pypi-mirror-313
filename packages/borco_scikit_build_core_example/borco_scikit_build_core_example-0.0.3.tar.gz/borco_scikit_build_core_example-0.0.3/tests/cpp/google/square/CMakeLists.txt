set(TEST_APP tst_google_square)
set(TEST_NAME google_square)

enable_testing()

add_executable(
    ${TEST_APP}
    tst_square.cpp
)

target_link_libraries(
    ${TEST_APP} PRIVATE
    GTest::gtest_main
    _core_lib
)

include(GoogleTest)
gtest_discover_tests(${TEST_APP})

add_test(NAME ${TEST_NAME} COMMAND ${TEST_APP})

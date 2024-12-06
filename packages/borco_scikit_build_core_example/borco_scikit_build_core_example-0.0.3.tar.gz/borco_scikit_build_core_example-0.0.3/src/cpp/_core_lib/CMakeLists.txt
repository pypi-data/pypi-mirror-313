set(LIB_NAME _core_lib)
set(LIB_DEFINITION _CORE_LIB_LIBRARY)

add_library(${LIB_NAME} STATIC
    square.h
    square.cpp
)

target_link_libraries(${LIB_NAME} PUBLIC
    Qt6::Core
)

target_include_directories(${LIB_NAME} PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

target_compile_definitions(${LIB_NAME} PRIVATE ${LIB_DEFINITION})

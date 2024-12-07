set(LIB_NAME _core_lib)

add_library(${LIB_NAME} STATIC
    add.cpp
    dog.cpp
)

target_include_directories(${LIB_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

cmake_minimum_required(VERSION 3.14)
cmake_policy(SET CMP0128 NEW)
cmake_policy(SET CMP0083 NEW)

project(testing)
set(CMAKE_CXX_STANDARD 17)

set(QT_VERSION Qt5 CACHE STRING "The Qt version framework to use (Qt5 or Qt6).")

include(${CMAKE_CURRENT_SOURCE_DIR}/breeze.cmake)
set(SOURCE_FILES ${CMAKE_CURRENT_SOURCE_DIR}/test_qt.cpp)
add_executable(testing ${SOURCE_FILES})
target_link_libraries(testing PRIVATE Qt${QT_VERSION_MAJOR}::Widgets breeze)

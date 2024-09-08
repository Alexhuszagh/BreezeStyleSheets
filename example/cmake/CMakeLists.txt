cmake_minimum_required(VERSION 3.13)
cmake_policy(SET CMP0128 NEW)

project(testing)
set(CMAKE_CXX_STANDARD 17)

set(QT_VERSION Qt5 CACHE STRING "The Qt version framework to use (Qt5 or Qt6).")
set(BREEZE_EXTENSIONS all CACHE STRING "The extensions to include in our stylesheets.")
set(BREEZE_STYLES all CACHE STRING "The styles to include in our stylesheets.")

include(${CMAKE_CURRENT_SOURCE_DIR}/breeze.cmake)
set(SOURCE_FILES ${CMAKE_CURRENT_SOURCE_DIR}/test_qt.cpp)
add_executable(testing ${SOURCE_FILES})
target_link_libraries(testing PRIVATE Qt${QT_VERSION_MAJOR}::Widgets breeze)

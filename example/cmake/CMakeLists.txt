cmake_minimum_required(VERSION 3.14)
cmake_policy(SET CMP0128 NEW)
cmake_policy(SET CMP0083 NEW)

project(testing)
set(CMAKE_CXX_STANDARD 17)

set(QT_VERSION Qt5 CACHE STRING "The Qt version framework to use (Qt5 or Qt6).")
set(PREFER_PIE OFF CACHE BOOL "If to prefer position-independent code, if the compiler supports it.")
set(BREEZE_EXTENSIONS all CACHE STRING "The extensions to include in our stylesheets.")
set(BREEZE_STYLES all CACHE STRING "The styles to include in our stylesheets.")

include(${CMAKE_CURRENT_SOURCE_DIR}/breeze.cmake)
set(SOURCE_FILES ${CMAKE_CURRENT_SOURCE_DIR}/test_qt.cpp)
add_executable(testing ${SOURCE_FILES})
target_link_libraries(testing PRIVATE Qt${QT_VERSION_MAJOR}::Widgets breeze)

# Prefer position independent code, if the compiler supports it.
if(PREFER_PIE)
  include(CheckPIESupported)
  check_pie_supported(LANGUAGES CXX OUTPUT_VARIABLE pie-supported)
  if(CMAKE_C_LINK_PIE_SUPPORTED)
    set_property(TARGET breeze PROPERTY POSITION_INDEPENDENT_CODE ON)
  endif()
endif()

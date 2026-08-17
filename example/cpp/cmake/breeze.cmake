# Setup Qt: this works with both Qt5 and Qt6
# NOTE: We use cached strings to specify the options for these.
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(
  ${QT_VERSION}
  COMPONENTS Core Gui Widgets Svg
  REQUIRED)
# -------------------

# Get Python to compile the stylesheets.
# Fetch the repository, configure, compile the stylesheets.
find_package(Python COMPONENTS Interpreter)

include(FetchContent)

set(FETCHCONTENT_QUIET OFF CACHE BOOL "Silence fetch content" FORCE)
set(PREFER_PIE OFF CACHE BOOL "If to prefer position-independent code, if the compiler supports it.")
set(BREEZE_EXTENSIONS all CACHE STRING "The extensions to include in our stylesheets.")
set(BREEZE_STYLES all CACHE STRING "The styles to include in our stylesheets.")

FetchContent_Declare(
  breeze_stylesheets
  GIT_REPOSITORY https://github.com/Alexhuszagh/BreezeStyleSheets.git
  GIT_TAG origin/main
  GIT_PROGRESS ON
  GIT_SHALLOW 1
  USES_TERMINAL_DOWNLOAD TRUE)

FetchContent_GetProperties(breeze_stylesheets)
if(NOT breeze_stylesheets_POPULATED)
  FetchContent_Populate(breeze_stylesheets)

  add_library(breeze STATIC "${breeze_stylesheets_SOURCE_DIR}/dist/breeze.qrc")

  add_custom_target(
    run_python_breeze ALL
    COMMAND ${Python_EXECUTABLE} configure.py --extensions=${BREEZE_EXTENSIONS}
            --styles=${BREEZE_STYLES} --resource breeze.qrc
    WORKING_DIRECTORY ${breeze_stylesheets_SOURCE_DIR}
    BYPRODUCTS "${breeze_stylesheets_SOURCE_DIR}/dist/breeze.qrc"
    COMMENT "Generating themes")

  add_dependencies(breeze run_python_breeze)
endif()

# Prefer position independent code, if the compiler supports it.
if(PREFER_PIE)
  include(CheckPIESupported)
  check_pie_supported(LANGUAGES CXX OUTPUT_VARIABLE pie-supported)
  if(CMAKE_C_LINK_PIE_SUPPORTED)
    set_property(TARGET breeze PROPERTY POSITION_INDEPENDENT_CODE ON)
  endif()
endif()

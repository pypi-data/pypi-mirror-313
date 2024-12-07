cmake_minimum_required(VERSION 3.15...3.26)

project(cfpng LANGUAGES CXX)

if (NOT SKBUILD)
  message(WARNING "\
  This CMake file is meant to be executed using 'scikit-build'. Running
  it directly will almost certainly not produce the desired result. If
  you are a user trying to install this package, please use the command
  below, which will install all necessary build dependencies, compile
  the package in an isolated environment, and then install it.
  =====================================================================
   $ pip install .
  =====================================================================
  If you are a software developer, and this is your own package, then
  it is usually much more efficient to install the build dependencies
  in your environment once and use the following command that avoids
  a costly creation of a new virtual environment at every compilation:
  =====================================================================
   $ pip install nanobind scikit-build-core[pyproject]
   $ pip install --no-build-isolation -ve .
  =====================================================================
  You may optionally add -Ceditable.rebuild=true to auto-rebuild when
  the package is imported. Otherwise, you need to re-run the above
  after editing C++ files.")
endif()

# Try to import all Python components potentially needed by nanobind
find_package(Python 3.8
  REQUIRED COMPONENTS Interpreter Development.Module
  OPTIONAL_COMPONENTS Development.SABIModule)

# Import nanobind through CMake's find_package mechanism
find_package(nanobind CONFIG REQUIRED)

# We are now ready to compile the actual extension module
nanobind_add_module(fpng_ext STABLE_ABI NB_STATIC
  src/fpng_ext.cpp
)

# Install directive for scikit-build-core
install(TARGETS fpng_ext LIBRARY DESTINATION fpng)

target_link_libraries(fpng_ext PRIVATE fpng)
target_include_directories(fpng_ext PRIVATE
  src
  fpng/src
)

# Build static fpng
if (NOT MSVC)
  set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
  set(GCC_COMPILE_FLAGS "-fvisibility=hidden -fno-strict-aliasing -D_LARGEFILE64_SOURCE=1 -D_FILE_OFFSET_BITS=64 -Wall -Wextra")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${GCC_COMPILE_FLAGS}")

  if (CMAKE_SYSTEM_PROCESSOR MATCHES "x86_64" OR CMAKE_SYSTEM_PROCESSOR MATCHES "AMD64")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DFPNG_NO_SSE=0 -msse4.1 -mpclmul")
  else()
    set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -DFPNG_NO_SSE=1")
  endif()
endif()

message("${CMAKE_CXX_FLAGS}")

set(CMAKE_POSITION_INDEPENDENT_CODE ON)
add_library(fpng STATIC
  fpng/src/fpng.cpp
)

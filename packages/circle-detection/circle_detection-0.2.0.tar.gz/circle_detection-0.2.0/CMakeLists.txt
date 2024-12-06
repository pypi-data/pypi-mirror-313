cmake_minimum_required(VERSION 3.30...3.35)
project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

set(PYBIND11_NEWPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

if(APPLE)
    execute_process(COMMAND brew --prefix OUTPUT_VARIABLE BREW_PREFIX OUTPUT_STRIP_TRAILING_WHITESPACE)
    set(OpenMP_CXX "${CMAKE_CXX_COMPILER}")
    set(OpenMP_CXX_FLAGS "-Xclang -fopenmp -I${BREW_PREFIX}/opt/libomp/include")
    set(OpenMP_CXX_LIB_NAMES "libomp")
    set(OpenMP_libomp_LIBRARY "omp")
    include_directories("${BREW_PREFIX}/opt/libomp/include")
    link_directories("${BREW_PREFIX}/opt/libomp/lib")
endif()

set(OpenMP_RUNTIME_MSVC llvm)
find_package(OpenMP REQUIRED)

set(EIGEN_URL "https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.zip")
set(EIGEN_SOURCE_DIR "${CMAKE_SOURCE_DIR}/eigen3")
set(EIGEN_INCLUDE_DIR "${CMAKE_SOURCE_DIR}/eigen3/eigen-3.4.0")
set(EIGEN_ZIP_PATH "${EIGEN_SOURCE_DIR}/eigen-3.4.0.zip")
set(EIGEN_CORE_HEADER_PATH "${EIGEN_INCLUDE_DIR}/Eigen/Core")

if (NOT EXISTS ${EIGEN_CORE_HEADER_PATH})
  message(STATUS "Downloading Eigen.")
  file(MAKE_DIRECTORY ${EIGEN_SOURCE_DIR})
  file(DOWNLOAD ${EIGEN_URL} ${EIGEN_ZIP_PATH} SHOW_PROGRESS)
  file(ARCHIVE_EXTRACT INPUT ${EIGEN_ZIP_PATH} DESTINATION ${EIGEN_SOURCE_DIR})
else()
    message(STATUS "Found Eigen source directory. Skipping download.")
endif()

include_directories( ${EIGEN_INCLUDE_DIR} )

pybind11_add_module(_circle_detection_cpp MODULE csrc/circle_detection.cpp)
target_link_libraries(_circle_detection_cpp PUBLIC OpenMP::OpenMP_CXX)

pybind11_add_module(_operations_cpp MODULE csrc/operations/operations.cpp csrc/operations/non_maximum_suppression.cpp)

install(TARGETS _circle_detection_cpp DESTINATION "${SKBUILD_PROJECT_NAME}")
install(TARGETS _operations_cpp DESTINATION "${SKBUILD_PROJECT_NAME}/operations")

cmake_minimum_required(VERSION 3.12)

project(Prodigal)

# Important for Link to succeed.
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(pybind11 REQUIRED)

# Wrapper module.
pybind11_add_module(prodigal_py MODULE prodigal.cpp)

# Static link the actual Prodigal library.
file(GLOB_RECURSE PRODIGAL_SOURCES "Prodigal/*.c")
add_library(prodigal STATIC ${PRODIGAL_SOURCES})

# Build target.
target_link_libraries(prodigal_py PRIVATE pybind11::module prodigal)

set_target_properties(
    prodigal_py PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    OUTPUT_NAME "prodigal_py"
)

# Install the pybind11 library
install(
    TARGETS prodigal_py
    COMPONENT prodigal_py
    LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX}/prodigal
    ARCHIVE DESTINATION ${CMAKE_INSTALL_PREFIX}/prodigal
    RUNTIME DESTINATION ${CMAKE_INSTALL_PREFIX}/prodigal
)

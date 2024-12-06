# SPDX-FileCopyrightText: Contributors to the Power Grid Model project <powergridmodel@lfenergy.org>
#
# SPDX-License-Identifier: MPL-2.0

# C API library
add_library(power_grid_model_io_native_c SHARED
  "src/handle.cpp"
  "src/vnf_pgm_converter.cpp"
)

target_include_directories(power_grid_model_io_native_c PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)

set(PGM_IO_NATIVE_PUBLIC_HEADERS
  "${CMAKE_CURRENT_SOURCE_DIR}/include/power_grid_model_io_native_c/basics.h"
  "${CMAKE_CURRENT_SOURCE_DIR}/include/power_grid_model_io_native_c/handle.h"
  "${CMAKE_CURRENT_SOURCE_DIR}/include/power_grid_model_io_native_c/vnf_pgm_converter.h"
  "${CMAKE_CURRENT_SOURCE_DIR}/include/power_grid_model_io_native_c.h"
)

target_link_libraries(power_grid_model_io_native_c
  PRIVATE power_grid_model_io_native
)

target_sources(power_grid_model_io_native_c PUBLIC 
  FILE_SET pgm_io_native_public_headers 
  TYPE HEADERS 
  BASE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}/include/" 
  FILES "${PGM_IO_NATIVE_PUBLIC_HEADERS}"
)

set_target_properties(power_grid_model_io_native_c PROPERTIES
  VERSION ${PGM_VERSION}
  SOVERSION ${PGM_VERSION}
  INTERPROCEDURAL_OPTIMIZATION_RELEASE TRUE
  INTERPROCEDURAL_OPTIMIZATION_RELWITHDEBINFO TRUE
)

install(TARGETS power_grid_model_io_native_c
  EXPORT power_grid_model_io_nativeTargets
  COMPONENT power_grid_model_io_native
  FILE_SET pgm_io_native_public_headers
)

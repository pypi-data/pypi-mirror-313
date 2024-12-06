# SPDX-FileCopyrightText: Contributors to the Power Grid Model project <powergridmodel@lfenergy.org>
#
# SPDX-License-Identifier: MPL-2.0

add_library(power_grid_model_io_native INTERFACE)

target_include_directories(power_grid_model_io_native INTERFACE "${CMAKE_CURRENT_SOURCE_DIR}/include")

target_link_libraries(power_grid_model_io_native INTERFACE power_grid_model)

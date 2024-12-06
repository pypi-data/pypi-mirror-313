// SPDX-FileCopyrightText: Contributors to the Power Grid Model project <powergridmodel@lfenergy.org>
//
// SPDX-License-Identifier: MPL-2.0

#define PGM_IO_DLL_EXPORTS

#include "power_grid_model_io_native_c/handle.h"

#include "handle.hpp"

#include <algorithm>

namespace {
using namespace power_grid_model_io_native;
} // namespace

// create and destroy handle
PGM_IO_Handle* PGM_IO_create_handle() { return new PGM_IO_Handle{}; }
void PGM_IO_destroy_handle(PGM_IO_Handle* handle) { delete handle; }

// error handling
PGM_IO_Idx PGM_IO_error_code(PGM_IO_Handle const* handle) { return handle->err_code; }
char const* PGM_IO_error_message(PGM_IO_Handle const* handle) { return handle->err_msg.c_str(); }
void PGM_IO_clear_error(PGM_IO_Handle* handle) { *handle = PGM_IO_Handle{}; }

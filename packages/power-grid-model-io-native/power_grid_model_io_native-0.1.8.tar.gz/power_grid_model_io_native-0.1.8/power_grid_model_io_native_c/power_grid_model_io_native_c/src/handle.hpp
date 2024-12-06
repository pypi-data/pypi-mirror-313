// SPDX-FileCopyrightText: Contributors to the Power Grid Model project <powergridmodel@lfenergy.org>
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#ifndef PGM_IO_DLL_EXPORTS
#define PGM_IO_DLL_EXPORTS
#endif

#include "power_grid_model_io_native_c/handle.h"

#include <power_grid_model_io_native/common/common.hpp>

#include <string_view>

// context handle
struct PGM_IO_Handle {
    power_grid_model_io_native::Idx err_code;
    std::string err_msg;
};

template <class Exception = std::exception, class Functor>
auto call_with_catch(PGM_IO_Handle* handle, Functor func, PGM_IO_Idx error_code, std::string_view extra_msg = {})
    -> std::invoke_result_t<Functor> {
    if (handle) {
        PGM_IO_clear_error(handle);
    }
    using ReturnValueType = std::remove_cvref_t<std::invoke_result_t<Functor>>;
    static std::conditional_t<std::is_void_v<ReturnValueType>, int, ReturnValueType> const empty{};
    try {
        return func();
    } catch (Exception const& e) {
        handle->err_code = error_code;
        handle->err_msg = std::string(e.what()) + std::string(extra_msg);
        return static_cast<ReturnValueType>(empty);
    }
}

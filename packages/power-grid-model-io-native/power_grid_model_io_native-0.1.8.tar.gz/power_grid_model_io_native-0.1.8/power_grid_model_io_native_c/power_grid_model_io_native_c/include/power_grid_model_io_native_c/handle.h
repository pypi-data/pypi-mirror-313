// SPDX-FileCopyrightText: Contributors to the Power Grid Model project <powergridmodel@lfenergy.org>
//
// SPDX-License-Identifier: MPL-2.0

/**
 * @brief header file which includes handle functions
 *
 */

#pragma once
#ifndef POWER_GRID_MODEL_IO_NATIVE_C_HANDLE_H
#define POWER_GRID_MODEL_IO_NATIVE_C_HANDLE_H

#include "basics.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Create a new handle.
 *
 * A handle object is needed to store error information.
 * If you run it in multi-threading at user side, each thread should have unique handle.
 * The handle should be destroyed by PGM_IO_destroy_handle().
 *
 * @return A pointer to the created handle.
 */
PGM_IO_API PGM_IO_Handle* PGM_IO_create_handle(void);

/**
 * @brief Destroy the handle.
 *
 * @param handle The pointer to the handle created by PGM_IO_create_handle().
 */
PGM_IO_API void PGM_IO_destroy_handle(PGM_IO_Handle* handle);

/**
 * @brief Get error code of last operation.
 *
 * @param handle The pointer to the handle you just used for an operation.
 * @return The error code, see #PGM_IO_ErrorCode .
 */
PGM_IO_API PGM_IO_Idx PGM_IO_error_code(PGM_IO_Handle const* handle);

/**
 * @brief Get error message of last operation.
 *
 * @param handle The pointer to the handle you just used for an operation.
 * @return A char const* poiner to a zero terminated string.
 * The pointer is not valid if you execute another operation.
 * You need to copy the string in your own data.
 */
PGM_IO_API char const* PGM_IO_error_message(PGM_IO_Handle const* handle);

/**
 * @brief Clear and reset the handle.
 *
 * @param handle The pointer to the handle.
 */
PGM_IO_API void PGM_IO_clear_error(PGM_IO_Handle* handle);

#ifdef __cplusplus
}
#endif

#endif

// SPDX-FileCopyrightText: Contributors to the Power Grid Model project <powergridmodel@lfenergy.org>
//
// SPDX-License-Identifier: MPL-2.0

/**
 * @brief Header file which includes basic type definitions
 *
 */

#pragma once
#ifndef POWER_GRID_MODEL_IO_NATIVE_C_BASICS_H
#define POWER_GRID_MODEL_IO_NATIVE_C_BASICS_H

// Generic helper definitions for shared library support
// API_MACRO_BLOCK
#if defined _WIN32
#define PGM_IO_HELPER_DLL_IMPORT __declspec(dllimport)
#define PGM_IO_HELPER_DLL_EXPORT __declspec(dllexport)
#define PGM_IO_HELPER_DLL_LOCAL
#else
#if __GNUC__ >= 4
#define PGM_IO_HELPER_DLL_IMPORT __attribute__((visibility("default")))
#define PGM_IO_HELPER_DLL_EXPORT __attribute__((visibility("default")))
#define PGM_IO_HELPER_DLL_LOCAL __attribute__((visibility("hidden")))
#else
#define PGM_IO_HELPER_DLL_IMPORT
#define PGM_IO_HELPER_DLL_EXPORT
#define PGM_IO_HELPER_DLL_LOCAL
#endif
#endif
// Now we use the generic helper definitions above to define PGM_IO_API and PGM_IO_LOCAL.
#ifdef PGM_IO_DLL_EXPORTS // defined if we are building the POWER_GRID_MODEL DLL (instead of using it)
#define PGM_IO_API PGM_IO_HELPER_DLL_EXPORT
#else
#define PGM_IO_API PGM_IO_HELPER_DLL_IMPORT
#endif // PGM_IO_DLL_EXPORTS
#define PGM_IO_LOCAL PGM_IO_HELPER_DLL_LOCAL
// API_MACRO_BLOCK

// integers
#ifdef __cplusplus
#include <cstddef>
#include <cstdint>
#else
#include <stddef.h>
#include <stdint.h>
#endif

// C linkage
#ifdef __cplusplus
extern "C" {
#endif

// NOLINTBEGIN(modernize-use-using)

// index type
typedef int64_t PGM_IO_Idx;
typedef int32_t PGM_IO_ID;

// TODO(mgovers): re-add
// /**
//  * @brief Opaque struct for the PowerGridModel class.
//  *
//  */
// typedef struct PGM_IO_VnfConverter PGM_IO_VnfConverter;

/**
 * @brief Opaque struct for the VnfConverter class.
 *
 */
typedef struct PGM_IO_VnfPgmConverter PGM_IO_VnfPgmConverter;

/**
 * @brief Opaque struct for the handle class.
 *
 * The handle class is used to store error and information.
 *
 */
typedef struct PGM_IO_Handle PGM_IO_Handle;

// NOLINTEND(modernize-use-using)

/**
 * @brief Enumeration of error codes.
 *
 */
enum PGM_IO_ErrorCode {
    PGM_IO_no_error = 0,           /**< no error occurred */
    PGM_IO_regular_error = 1,      /**< some error occurred which is not in the batch calculation */
    PGM_IO_batch_error = 2,        /**< some error occurred which is in the batch calculation */
    PGM_IO_serialization_error = 3 /**< some error occurred which is in the (de)serialization process */
};

/**
 * @brief Enumeration of experimental features.
 *
 * [Danger mode]
 *
 * The behavior of experimental features may not be final and no stability guarantees are made to the users.
 * Which features (if any) are enabled in experimental mode may change over time.
 *
 */
enum PGM_IO_ExperimentalFeatures {
    PGM_IO_experimental_features_disabled = 0, /**< disable experimental features */
    PGM_IO_experimental_features_enabled = 1,  /**< enable experimental features */
};

#ifdef __cplusplus
}
#endif

#endif

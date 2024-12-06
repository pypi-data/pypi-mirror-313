// SPDX-FileCopyrightText: Contributors to the Power Grid Model project <powergridmodel@lfenergy.org>
//
// SPDX-License-Identifier: MPL-2.0

#define PGM_IO_DLL_EXPORTS

#include <power_grid_model_io_native/common/enum.hpp>
#include <power_grid_model_io_native/vnf_converter/vnf_pgm_converter.hpp>

#include "handle.hpp"
#include <power_grid_model_io_native_c/basics.h>
#include <power_grid_model_io_native_c/vnf_pgm_converter.h>

#include <power_grid_model/auxiliary/dataset.hpp>
#include <power_grid_model/common/exception.hpp>

namespace pgm_io = power_grid_model_io_native;

struct PGM_IO_VnfPgmConverter : public pgm_io::PgmVnfConverter {
    using PgmVnfConverter::PgmVnfConverter;
};

PGM_IO_VnfPgmConverter* PGM_IO_create_vnf_converter(PGM_IO_Handle* handle, char const* file_buffer,
                                                    PGM_IO_ExperimentalFeatures experimental_features) {
    return call_with_catch(
        handle,
        [file_buffer, experimental_features] {
            using enum pgm_io::ExperimentalFeatures;
            auto experimental_feature = experimental_features_disabled;
            switch (experimental_features) {
            case PGM_IO_experimental_features_disabled:
                experimental_feature = experimental_features_disabled;
                break;
            case PGM_IO_experimental_features_enabled:
                experimental_feature = experimental_features_enabled;
                break;
            default:
                throw power_grid_model::MissingCaseForEnumError{"PGM_IO_create_vnf_converter", experimental_features};
            }
            auto* converter = new PGM_IO_VnfPgmConverter(file_buffer, experimental_feature);
            parse_vnf_file_wrapper(converter);
            return converter;
        },
        PGM_IO_regular_error);
}

char const* PGM_IO_vnf_pgm_converter_get_input_data(PGM_IO_Handle* handle, PGM_IO_VnfPgmConverter* converter_ptr) {
    return call_with_catch(
        handle, [converter_ptr] { return convert_input_wrapper(converter_ptr).c_str(); }, PGM_IO_regular_error);
}

void PGM_IO_destroy_vnf_converter(PGM_IO_VnfPgmConverter* converter_ptr) { delete converter_ptr; }

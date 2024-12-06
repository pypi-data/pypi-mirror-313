// SPDX-FileCopyrightText: Contributors to the Power Grid Model project <powergridmodel@lfenergy.org>
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include <power_grid_model/common/common.hpp>

namespace power_grid_model_io_native {
namespace pgm = power_grid_model;

// id type
using pgm::asymmetric_t;
using pgm::ID;
using pgm::Idx;
using pgm::Idx2D;
using pgm::IdxVector;
using pgm::IntS;
using pgm::is_asymmetric_v;
using pgm::is_symmetric_v;
using pgm::other_symmetry_t;
using pgm::symmetric_t;
using pgm::symmetry_tag;

// math constant
using namespace std::complex_literals;
using pgm::DoubleComplex;

using pgm::inv_sqrt3;
using pgm::pi;
using pgm::sqrt3;

using pgm::a;
using pgm::a2;
using pgm::deg_120;
using pgm::deg_240;
using pgm::deg_30;
using pgm::na_IntID;
using pgm::na_IntS;
using pgm::nan;

// power grid constant
using pgm::base_power_1p;
using pgm::base_power_3p;

// some usual vector
using pgm::ComplexVector;
using pgm::DoubleVector;
using pgm::IntSVector;

} // namespace power_grid_model_io_native

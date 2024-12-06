# SPDX-FileCopyrightText: Contributors to the Power Grid Model project <powergridmodel@lfenergy.org>
#
# SPDX-License-Identifier: MPL-2.0

import pytest
from power_grid_model._core.error_handling import InvalidArguments

from power_grid_model_io_native._core.error_handling import assert_no_error
from power_grid_model_io_native._core.vnf_converter import PgmVnfConverter


def test_pgmvnfconverter_constructor_without_experimental_features():
    """A test case for creating pgmvnfconverter without experimental features"""
    with pytest.raises(InvalidArguments):
        _ = PgmVnfConverter("", 0)


def test_pgmvnfconverter_constructor_with_experimental_features():
    """A test case for creating pgmvnfconverter with experimental features"""
    _ = PgmVnfConverter("", 1)
    assert_no_error()


def test_get_pgm_input_data():
    """A test case for obtaining the data in PGM format from pgmvnfconverter"""
    converter = PgmVnfConverter("", 1)
    result_buffer = converter.get_pgm_input_data()
    json_output = '{"version":"1.0","type":"input","is_batch":false,"attributes":{},"data":{}}'
    assert result_buffer == json_output

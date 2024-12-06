# SPDX-FileCopyrightText: Contributors to the Power Grid Model project <powergridmodel@lfenergy.org>
#
# SPDX-License-Identifier: MPL-2.0

"""
Power grid model io native converter for vnf files
"""

from power_grid_model_io_native._core.error_handling import assert_no_error
from power_grid_model_io_native._core.power_grid_model_io_core import PgmVnfConverterPtr, pgm_io_core as pgmic


class PgmVnfConverter:
    """A converter class which will convert a given string representation of .vnf data to the PowerGridModel format"""

    _pgm_vnf_converter: PgmVnfConverterPtr
    _serialized_data: str

    def __new__(
        cls,
        string_buffer: str,
        experimental_feature: int,
    ):
        instance = super().__new__(cls)

        instance._pgm_vnf_converter = pgmic.create_vnf_converter(string_buffer, experimental_feature)
        assert_no_error()

        return instance

    def __del__(self):
        if hasattr(self, "_pgm_vnf_converter"):
            pgmic.destroy_vnf_converter(self._pgm_vnf_converter)

    def get_pgm_input_data(self):
        """A function of the PgmVnfConverter class which will convert and return the data in PGM format

        Returns:
            str: json data in PGM format
        """
        pgm_data = pgmic.vnf_pgm_converter_get_input_data(self._pgm_vnf_converter)
        assert_no_error()
        self._serialized_data = pgm_data
        return self._serialized_data

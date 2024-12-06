# SPDX-FileCopyrightText: Contributors to the Power Grid Model project <powergridmodel@lfenergy.org>
#
# SPDX-License-Identifier: MPL-2.0

"""
Error handling
"""

from power_grid_model._core.error_handling import (
    PGM_NO_ERROR,
    PGM_REGULAR_ERROR,
    PGM_SERIALIZATION_ERROR,
    VALIDATOR_MSG,
    PowerGridBatchError,
    PowerGridSerializationError,
    _interpret_error,
)

from power_grid_model_io_native._core.power_grid_model_io_core import pgm_io_core as pgmic

# def _interpret_error_pgm_io(message: str, decode_error: bool = True) -> PowerGridError:
#     if decode_error:
#         for pattern, type_ in _ERROR_MESSAGE_PATTERNS.items():
#             if pattern.search(message) is not None:
#                 return type_(message)

#     return PowerGridError(message)


def find_error(batch_size: int = 1, decode_error: bool = True) -> RuntimeError | None:
    """
    Check if there is an error and return it

    Args:
        batch_size: (int, optional): Size of batch. Defaults to 1.
        decode_error (bool, optional): Decode the error message(s) to derived error classes. Defaults to True

    Returns: error object, can be none

    """
    _ = batch_size
    error_code: int = pgmic.error_code()
    if error_code == PGM_NO_ERROR:
        return None
    if error_code == PGM_REGULAR_ERROR:
        error_message = pgmic.error_message()
        error_message += VALIDATOR_MSG
        return _interpret_error(error_message, decode_error=decode_error)
    if error_code == PGM_SERIALIZATION_ERROR:
        return PowerGridSerializationError(pgmic.error_message())
    return RuntimeError("Unknown error!")


def assert_no_error(batch_size: int = 1, decode_error: bool = True):
    """
    Assert there is no error in the last operation
    If there is an error, raise it

    Args:
        batch_size (int, optional): Size of batch. Defaults to 1.
        decode_error (bool, optional): Decode the error message(s) to derived error classes. Defaults to True

    Returns:

    """
    error = find_error(batch_size=batch_size, decode_error=decode_error)
    if error is not None:
        raise error


def handle_errors(
    continue_on_batch_error: bool, batch_size: int = 1, decode_error: bool = True
) -> PowerGridBatchError | None:
    """
    Handle any errors in the way that is specified.

    Args:
        continue_on_batch_error (bool): Return the error when the error type is a batch error instead of reraising it.
        batch_size (int, optional): Size of batch. Defaults to 1.
        decode_error (bool, optional): Decode the error message(s) to derived error classes. Defaults to True

    Raises:
        error: Any errors previously encountered, unless it was a batch error and continue_on_batch_error was True.

    Returns:
        PowerGridBatchError | None: None if there were no errors, or the previously encountered
                                    error if it was a batch error and continue_on_batch_error was True.
    """
    error: RuntimeError | None = find_error(batch_size=batch_size, decode_error=decode_error)
    if error is None:
        return None

    if continue_on_batch_error and isinstance(error, PowerGridBatchError):
        # continue on batch error
        return error

    # raise normal error
    raise error

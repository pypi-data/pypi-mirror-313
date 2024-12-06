# SPDX-FileCopyrightText: Contributors to the Power Grid Model project <powergridmodel@lfenergy.org>
#
# SPDX-License-Identifier: MPL-2.0

"""PGM IO CORE module."""

import platform
from ctypes import CDLL, c_double, c_size_t, c_void_p
from inspect import signature
from itertools import chain
from pathlib import Path
from typing import Callable

from power_grid_model._core.power_grid_core import CharPtr, CStr, IdxC

# functions with size_t return
_FUNC_SIZE_T_RES = {"meta_class_size", "meta_class_alignment", "meta_attribute_offset"}
_ARGS_TYPE_MAPPING = {bytes: CharPtr, str: CStr, int: IdxC, float: c_double}

# The c_void_p is extended only for type hinting and type checking; therefore no public methods are required.
# pylint: disable=too-few-public-methods


class HandlePtr(c_void_p):
    """
    Pointer to handle
    """


class PgmVnfConverterPtr(c_void_p):
    """
    Pointer to PgmVnfConverter
    """


def _load_core() -> CDLL:
    """

    Returns: DLL/SO object

    """
    if platform.system() == "Windows":
        dll_file = "_power_grid_model_io_core.dll"
    else:
        dll_file = "_power_grid_model_io_core.so"
    cdll = CDLL(str(Path(__file__).parent / dll_file))
    # assign return types
    # handle
    cdll.PGM_IO_create_handle.argtypes = []
    cdll.PGM_IO_create_handle.restype = HandlePtr
    cdll.PGM_IO_destroy_handle.argtypes = [HandlePtr]
    cdll.PGM_IO_destroy_handle.restype = None
    return cdll


# load dll once
_CDLL: CDLL = _load_core()


def make_c_binding(func: Callable):
    """
    Descriptor to make the function to bind to C

    Args:
        func: method object from PowerGridModelIoCore

    Returns:
        Binded function

    """
    name = func.__name__
    sig = signature(func)

    # get and convert types, skip first argument, as it is self
    py_argnames = list(sig.parameters.keys())[1:]
    py_argtypes = [v.annotation for v in sig.parameters.values()][1:]
    py_restype = sig.return_annotation
    c_argtypes = [_ARGS_TYPE_MAPPING.get(x, x) for x in py_argtypes]
    c_restype = _ARGS_TYPE_MAPPING.get(py_restype, py_restype)
    if c_restype == IdxC and name in _FUNC_SIZE_T_RES:
        c_restype = c_size_t
    # set argument in dll
    # mostly with handle pointer, except destroy function
    is_destroy_func = "destroy" in name
    if is_destroy_func:
        getattr(_CDLL, f"PGM_IO_{name}").argtypes = c_argtypes
    else:
        getattr(_CDLL, f"PGM_IO_{name}").argtypes = [HandlePtr] + c_argtypes
    getattr(_CDLL, f"PGM_IO_{name}").restype = c_restype

    # binding function
    def cbind_func(self, *args, **kwargs):
        if "destroy" in name:
            c_inputs = []
        else:
            c_inputs = [self._handle]  # pylint: disable=protected-access
        args = chain(args, (kwargs[key] for key in py_argnames[len(args) :]))
        for arg in args:
            if isinstance(arg, str):
                c_inputs.append(arg.encode())
            else:
                c_inputs.append(arg)

        # call
        res = getattr(_CDLL, f"PGM_IO_{name}")(*c_inputs)
        # convert to string for CStr
        if c_restype == CStr:
            res = res.decode() if res is not None else ""
        return res

    return cbind_func


# pylint: disable=missing-function-docstring
class PowerGridModelIoCore:
    """
    DLL caller
    """

    _handle: HandlePtr
    _instance: "PowerGridModelIoCore | None" = None

    # singleton of power grid model io core
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._handle = _CDLL.PGM_IO_create_handle()
        return cls._instance

    def __del__(self):
        _CDLL.PGM_IO_destroy_handle(self._handle)

    # not copyable
    def __copy__(self):
        raise NotImplementedError("Class not copyable")

    def __deepcopy__(self, memodict):
        raise NotImplementedError("Class not copyable")

    @make_c_binding
    def error_code(self) -> int:  # type: ignore[empty-body]
        pass  # pragma: no cover

    @make_c_binding
    def error_message(self) -> str:  # type: ignore[empty-body]
        pass  # pragma: no cover

    @make_c_binding
    def create_vnf_converter(self, data: str, experim_feature: int) -> PgmVnfConverterPtr:  # type: ignore[empty-body]
        pass  # pragma: no cover

    @make_c_binding
    def vnf_pgm_converter_get_input_data(self, pgmvnfconverter: PgmVnfConverterPtr) -> str:  # type: ignore[empty-body]
        pass  # pragma: no cover

    @make_c_binding
    def destroy_vnf_converter(self, pgmvnfconverter: PgmVnfConverterPtr) -> None:  # type: ignore[empty-body]
        pass  # pragma: no cover


# make one instance
pgm_io_core = PowerGridModelIoCore()

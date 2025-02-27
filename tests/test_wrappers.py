import dataclasses
import inspect
import pytest
from unittest import mock
from mpi4py import MPI
import numpy as np

from httomo.wrappers_class import HttomolibWrapper, HttomolibgpuWrapper, TomoPyWrapper


def test_tomopy_wrapper_cpu():
    wrp = TomoPyWrapper("recon", "algorithm", "recon", MPI.COMM_WORLD)
    assert wrp.cupyrun is False
    assert inspect.ismodule(wrp.module)


def test_httomolib_wrapper_max_slices_cpu():
    wrp = HttomolibWrapper("misc", "images", "save_to_images", MPI.COMM_WORLD)
    assert wrp.cupyrun is False
    assert inspect.ismodule(wrp.module)


@pytest.mark.cupy
def test_httomolibgpu_wrapper_max_slices_gpu():
    wrp = HttomolibgpuWrapper("prep", "normalize", "normalize", MPI.COMM_WORLD)
    assert wrp.cupyrun is True
    assert wrp.calc_max_slices(0, (100, 100), np.uint8, 50000)[0] < 100000


@pytest.mark.cupy
def test_httomolibgpu_wrapper_max_slices_passes_kwargs():
    from httomolibgpu.prep.normalize import normalize

    mock_method = mock.Mock()
    mockMeta = dataclasses.replace(normalize.meta, calc_max_slices=mock_method)
    with mock.patch.object(normalize, "meta", mockMeta):
        wrp = HttomolibgpuWrapper("prep", "normalize", "normalize", MPI.COMM_WORLD)
        wrp.dict_params = dict(testarg=1, minus_log=True)
        wrp.calc_max_slices(0, (100, 100), np.uint8(), 50000)

    # make sure the default args are called and the args given above are overriding the defaults
    mock_method.assert_called_once_with(
        0,
        (100, 100),
        np.uint8(),
        50000,
        cutoff=10.0,
        minus_log=True,
        testarg=1,
        nonnegativity=False,
        remove_nans=False,
    )

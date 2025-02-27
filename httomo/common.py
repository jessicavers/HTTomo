import re
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import IntEnum, unique
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from httomo.utils import Pattern


@dataclass
class MethodFunc:
    """
    Class holding information about each tomography pipeline method

    Parameters
    ==========

    module_name : str
        Fully qualified name of the module where the method is. E.g. httomolib.prep.normalize
    method_func : Callable
        The actual method callable
    wrapper_func: Optional[Callable]
        The wrapper function to handle the execution. It may be None,
        for example for loaders.
    calc_max_slices: Optional[Callable]
        A callable with the signature
        (slice_dim: int, other_dims: int, dtype: np.dtype, available_memory: int) -> int
        which determines the maximum number of slices it can fit in the given memory.
        If it is not present (None), the method is assumed to fit any amount of slices.
    parameters : Dict[str, Any]
        The method parameters that are specified in the pipeline yaml file.
        They are used as kwargs when the method is called.
    cpu : bool
        Whether CPU execution is supported.
    gpu : bool
        Whether GPU execution is supported.
    reslice_ahead : bool
        Whether a reslice needs to be done due to a pattern change in the pipeline
    is_last_method : bool
        True if it is the last method in the pipeline
    """

    module_name: str
    method_func: Callable
    wrapper_func: Optional[Callable] = None
    calc_max_slices: Optional[Callable] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    pattern: Pattern = Pattern.projection
    cpu: bool = True
    gpu: bool = False
    reslice_ahead: bool = False
    is_loader: bool = False
    is_last_method: bool = False


@dataclass
class ResliceInfo:
    """
    Class holding information regarding reslicing

    Parameters
    ==========

    count: int
        Counter for how many reslices were done so far
    has_warn_printed : bool
        Whether the reslicing warning has been printed
    reslice_bool_list : List[bool]
        List of booleans to identify when reslicing is needed
    reslice_dir : Optional[Path]
        The directory to use with file-based reslicing. If None,
        reslicing will be done in-memory.
    """

    count: int
    has_warn_printed: bool
    reslice_bool_list: List[bool]
    reslice_dir: Optional[Path] = None


@dataclass
class PlatformSection:
    """
    Data class to represent a section of the pipeline that runs on the same platform.
    That is, all methods contained in this section of the pipeline run either all on CPU
    or all on GPU.

    This is used to iterate through GPU memory in chunks.

    Attributes
    ----------
    gpu : bool
        Whether this section is a GPU section (True) or CPU section (False)
    pattern : Pattern
        To denote the slicing pattern - sinogram, projection
    max_slices : int
        Holds information about how many slices can be fit in one chunk without
        exhausting memory (relevant on GPU only)
    methods : List[MethodFunc]
        List of methods in this section
    """

    gpu: bool
    pattern: Pattern
    max_slices: int
    methods: List[MethodFunc]


@dataclass
class RunMethodInfo:
    """
    Class holding information about each method before/while it runs.

    Parameters
    ==========

    dict_params_method : Dict
        The dict of param names and their values for a given method function.
    data_in : List
        Input datasets in a list
    data_out : List
        Output datasets in a list
    param_sweep_name : str
        The name of the param sweep involved
    param_sweep_vals: Any
        The tuple values of the param sweep
    should_reslice : bool
        To check if the input dataset should be resliced before the task runs
    dict_httomo_params : Dict
        Dict containing extra params unrelated to wrapped packages but related to httomo
    save_result : bool
        Bool to check if we need to save the result (e.g., if it is the last method)
    current_slice_dim : int
        the dimension of the data that the current method requires the data to be sliced in.
    next_slice_dim : int
        the dimension of the data that the next method requires the data to be sliced in
    task_idx: int
        Index of the task in the pipeline being run
    package_name: str
        The name of the package the method is imported from
    method_name: str
        The name of the method being executed
    """

    dict_params_method: Dict[str, Any] = field(default_factory=dict)
    data_in: List[str] = field(default_factory=list)
    data_out: List[str] = field(default_factory=list)
    should_reslice: bool = False
    dict_httomo_params: Dict[str, Any] = field(default_factory=dict)
    save_result: bool = False
    current_slice_dim: int = -1
    next_slice_dim: int = -1
    task_idx: int = -1
    param_sweep_name: str = None
    param_sweep_vals: Tuple = field(default_factory=tuple)
    package_name: str = None
    method_name: str = None

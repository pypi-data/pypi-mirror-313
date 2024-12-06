"""""" # start delvewheel patch
def _delvewheel_patch_1_9_0():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'scikit_primate.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-scikit_primate-0.5.6')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-scikit_primate-0.5.6')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_9_0()
del _delvewheel_patch_1_9_0
# end delvewheel patch

import importlib.metadata

__version__ = importlib.metadata.version("scikit-primate")

## --- For benchmarking import times ---
## > python -m benchmark_imports primate
# from .estimators import hutch
# from .lanczos import OrthogonalPolynomialBasis, lanczos, rayleigh_ritz
# from .operators import MatrixFunction, is_linear_op, normalize_unit
# from .integrate import spectral_density, quadrature
# from .stats import ControlVariableEstimator, ConfidenceEstimator
# from .random import isotropic, symmetric
# from .tridiag import eigh_tridiag, eigvalsh_tridiag


## Based on Numpy's usage: https://github.com/numpy/numpy/blob/v1.25.0/numpy/lib/utils.py#L75-L101
def get_include():
	"""Return the directory that contains the primate's .h header files.

	Extension modules that need to compile against primate should use this
	function to locate the appropriate include directory.

	Notes:
	  When using `distutils`, for example in `setup.py`:
	    ```python
	    import primate
	    ...
	    Extension('extension_name', ..., include_dirs=[primate.get_include()])
	    ...
	    ```
	  Or with `meson-python`, for example in `meson.build`:
	    ```meson
	    ...
	    run_command(py, ['-c', 'import primate; print(primate.get_include())', check : true).stdout().strip()
	    ...
	    ```
	"""
	import os

	d = os.path.join(os.path.dirname(__file__), "include")
	return d

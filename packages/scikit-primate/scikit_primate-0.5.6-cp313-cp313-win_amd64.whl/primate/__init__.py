"""""" # start delvewheel patch
def _delvewheel_patch_1_9_0():
    import os
    if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'scikit_primate.libs'))):
        os.add_dll_directory(libs_dir)


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

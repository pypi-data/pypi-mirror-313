import warnings
import xarray as xr
import numpy as np
from scipy.signal import butter, sosfiltfilt

class DecimationWarning(UserWarning):
    """Custom warning for decimation issues."""
    pass

def decimate(da, q_int, axis='time'):
    """
    Decimate an xarray.DataArray or Dataset along a specified axis by a given interval.

    Parameters:
    da : xarray.DataArray or xarray.Dataset
        The input data to be decimated.
    q_int : int
        The decimation interval. Must be a positive integer.
    axis : str, optional
        The dimension name along which to decimate. Default is 'time'.

    Returns:
    xarray.DataArray or xarray.Dataset
        The decimated data.

    Raises:
    ValueError:
        If q_int is not a positive integer.
    """
    if not isinstance(q_int, int) or q_int <= 0:
        raise ValueError("q_int must be a positive integer.")

    if axis not in da.dims:
        warnings.warn(f"{axis} is not in the dimensions of the DataArray or Dataset.", 
                      DecimationWarning, stacklevel=2)
        return da
    
    # Perform decimation along the specified axis
    return da.isel(**{axis: slice(0, None, q_int)})

def bandpass(da, lowcut, highcut, order=4, axis='time'):
    """
    Apply a bandpass filter to an xarray.DataArray along a specified axis lazily, compatible with Dask.
    
    Parameters:
    da : xarray.DataArray
        Input DataArray to be filtered. Can be Dask-backed for lazy evaluation.
    lowcut : float
        Low cutoff frequency for the bandpass filter.
    highcut : float
        High cutoff frequency for the bandpass filter.
    order : int, optional
        Order of the Butterworth filter. Default is 4.
    axis : str, optional
        The dimension along which to apply the filter. Default is 'time'.

    Returns:
    xarray.DataArray
        The bandpass-filtered DataArray, computed lazily if Dask-backed.
    """
    if axis not in da.dims:
        raise ValueError(f"Axis '{axis}' is not in the dimensions of the DataArray: {list(da.dims)}")

    # Determine sampling frequency
    dT = (da[axis][1] - da[axis][0]).values.astype(float)
    fs = 1 / (dT * 1e-9)  # Convert nanoseconds to seconds for sampling rate

    # Design the Butterworth bandpass filter using SOS (more stable than b/a coefficients)
    sos = butter(order, [lowcut, highcut], fs=fs, btype='bandpass', output='sos')

    # Get the axis index
    axis_index = list(da.dims).index(axis)

    # Apply the filter using xr.apply_ufunc
    def apply_filter(data):
        return sosfiltfilt(sos, data, axis=axis_index)

    da_bp = xr.apply_ufunc(
        apply_filter,                # Function to apply
        da,                          # Input array
        input_core_dims=[[axis]],    # Core dimension to apply the function on
        output_core_dims=[[axis]],   # Core dimension for the output
        vectorize=True,              # Apply the function element-wise across chunks
        dask="parallelized",         # Enable Dask parallelization
        output_dtypes=[da.dtype],    # Specify output data type
        dask_gufunc_kwargs={"allow_rechunk": True},  # Allow rechunking along the core dimension
    )

    return da_bp.T

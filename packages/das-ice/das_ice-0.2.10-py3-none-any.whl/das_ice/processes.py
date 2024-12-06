import xarray as xr

def std_local(da,nt=6,nx=4,ax_t='time',ax_x='distance'):
    '''
    Compute local standard deviation for a DataArray

    :param da: Variable on which compute the local standard deviation
    :type da: xr.DataArray
    :param nt: number of element in ax_t direction (default: 6)
    :type nt: int
    :param nx: number of element in ax_x direction (default: 4)
    :type nx: int
    :param ax_t: ax_t axis (default: 'time')
    :type ax_t: string
    :param ax_x: ax_x axis (default: 'distance')
    :type ax_x: string
    '''

    return da.rolling({ax_t:nt,ax_x:nx}).std(ax_t)

def strain_rate(da,ax_d='distance'):
    '''
    Compute strain rate from velocity mesurement

    :param da: Variable on which compute differentiate
    :type da: xr.DataArray
    :param ax_d: axis for differentiate (default: 'distance')
    :type ax_d: string
    '''

    return da.differentiate(ax_d)
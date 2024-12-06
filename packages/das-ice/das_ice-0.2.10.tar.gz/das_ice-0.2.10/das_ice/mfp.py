from itertools import product
import dask.array as da
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import pylab as plt
import torch
from tqdm import tqdm
from scipy.signal import ricker


def MFP_2D_series(ds,delta_t,stations,zrange=[0,100],freqrange=[100,200],xrange=[0,50],vrange=[2500,3500],dz=1,dx=1,dv=250):
    sampling_rate=(ds.time[1]-ds.time[0]).values.astype(float)*10**-9
    # defined number of sample per time series
    dn=int(delta_t/sampling_rate)
    # build a data cube with a dimention for each time series
    ll=[]
    true_time=[]
    din=int(len(ds.time)/dn)
    for i in range(din):
        tmp=ds[:,i*dn:(i+1)*dn]
        new_time = np.arange(dn) * sampling_rate
        true_time.append(tmp.time[0].values)
        tmp = tmp.assign_coords(time=new_time)
        ll.append(tmp)
    ds_cube=xr.concat(ll,dim='true_time')
    # Fiber signal processing
    multi_waveform_spectra=torch.fft.fft(torch.from_numpy(ds_cube.values),axis=2).to(dtype=torch.complex128)
    freqs = torch.fft.fftfreq(len(ds_cube.time),sampling_rate)
    omega = 2 * torch.pi * freqs
    # frequency sampling
    freq_idx = torch.where((freqs > freqrange[0]) & (freqs < freqrange[1]))[0]
    omega_lim = omega[freq_idx]
    waveform_spectra_lim = multi_waveform_spectra[:,:,freq_idx]
    K = waveform_spectra_lim[:,:, None, :] * waveform_spectra_lim.conj()[:,None, :, :]
    diag_idxs = torch.arange(K.shape[1])
    zero_spectra = torch.zeros(omega_lim.shape, dtype=torch.cdouble)
    K[:,diag_idxs, diag_idxs, :] = zero_spectra
    K = da.from_array(K.numpy())
    # Compute grid
    x_coords = torch.arange(xrange[0], xrange[1] + dx, dx)
    z_coords = torch.arange(zrange[0], zrange[1] + dz, dz)
    v_coords=torch.arange(vrange[0], vrange[1] + dv, dv)
    gridpoints = torch.tensor(list(product(x_coords, z_coords)))

    stations=torch.tensor(stations).to(dtype=torch.complex128)
    distances_to_all_gridpoints = torch.linalg.norm(gridpoints[:, None, :] - stations[None, :, :], axis=2)
    # Compute traveltimes
    traveltimes=distances_to_all_gridpoints[None,:,:]/v_coords[:,None,None]
    greens_functions = torch.exp(-1j * omega_lim[None, None,None, :] * traveltimes[:, :, :, None])
    # move critical part to dask
    greens_functions_dask = da.from_array(greens_functions.numpy(), chunks='auto')
    S = (greens_functions_dask[:, :,:, None,:]*greens_functions_dask.conj()[:,:, None, :,:])
    # Perform the einsum operation
    beampowers_d = da.einsum("vlgijw, ljiw -> vlg", S[:, None , :, :, :, :], K).real
    beampowers = beampowers_d.compute()
    bp = beampowers.reshape(len(v_coords),din, len(x_coords), len(z_coords))

    res=xr.DataArray(bp,dims=['velocity','true_time','x','z'])
    res['velocity']=v_coords
    res['true_time']=true_time
    res['x']=x_coords
    res['z']=z_coords

    res=res.transpose("z","x","velocity","true_time")/((stations.shape[0]-1)*stations.shape[0]*len(omega_lim))
    
    return res



def MFP_2D(ds,stations,zrange=[0,100],freqrange=[100,200],xrange=[0,50],vrange=[2500,3500],dz=1,dx=1,dv=250):
    '''
    Perform Matched Field Processing (MFP) to compute beamforming power over a range of 
    spatial coordinates, velocities, and frequencies.

    :param ds: Input data as an xarray DataArray containing waveform data. 
               Must include 'distance' and 'time' coordinates.
    :type ds: xarray.DataArray

    :param zrange: Range of depths to compute (start and end), default is [0, 100].
    :type zrange: list of float or int

    :param freqrange: Frequency range for processing in Hz (start and end), default is [100, 200].
    :type freqrange: list of float

    :param xrange: Range of horizontal x-coordinates to search (start and end), default is [0, 50].
    :type xrange: list of float or int

    :param vrange: Velocity range to search in m/s (start and end), default is [1000, 6000].
    :type vrange: list of float or int

    :param dz: Spacing between grid points in the depth dimension (z), default is 1.
    :type dz: float or int

    :param dx: Spacing between grid points in the horizontal x dimension, default is 1.
    :type dx: float or int

    :param dv: Spacing between velocities, default is 100.
    :type dv: float or int

    :return: A 3D xarray DataArray containing the computed beampower values. The dimensions are
             'v' (velocity), 'z' (depth), and 'x' (horizontal position).
    :rtype: xarray.DataArray
    '''
    
    # Extract data from dataarray
    sampling_rate=((ds.time[1]-ds.time[0]).values.astype(float)*10**-9)
    # Compute FFT of all the receiver
    waveform_spectra=torch.fft.fft(torch.from_numpy(ds.values),axis=1).to(dtype=torch.complex128)

    freqs = torch.fft.fftfreq(len(ds.time),sampling_rate)
    omega = 2 * torch.pi * freqs
    # Build grid for search
    x_coords = torch.arange(xrange[0], xrange[1] + dx, dx)
    z_coords = torch.arange(zrange[0], zrange[1] + dz, dz)
    v_coords = torch.arange(vrange[0], vrange[1] + dv, dv)
    gridpoints = torch.tensor(list(product(x_coords, z_coords)))
    
    stations=torch.tensor(stations).to(dtype=torch.complex128)


    distances_to_all_gridpoints = torch.linalg.norm(gridpoints[:, None, :] - stations[None, :, :], axis=2)
    # COM: This is matching print(distances_to_all_gridpoints)
    # limit to frequency band of interest for
    # a) speed# limit to frequency band of interest for
    # a) speed-up
    # b) focusing on specific frequencies
    freq_idx = torch.where((freqs > freqrange[0]) & (freqs < freqrange[1]))[0]
    omega_lim = omega[freq_idx]
    waveform_spectra_lim = waveform_spectra[:, freq_idx]

    bp=[]
    for vel in tqdm(v_coords):
        

        traveltimes = distances_to_all_gridpoints / vel
        
        # Green's functions between all stations and all grid points
        # within selected frequency band
        # G = exp(-iωt)
        greens_functions = torch.exp(-1j * omega_lim[None, None, :] * traveltimes[:, :, None])
        
        # move critical part to dask
        greens_functions_dask = da.from_array(greens_functions.numpy(), chunks='auto')

        S = (greens_functions_dask[:, :, None, :]*greens_functions_dask.conj()[:, None, :, :])
        
        

        # this assumes that K can be computed without memory issues.
        # If this is not the case, you can also use dask and chunk K.
        K = waveform_spectra_lim[:, None, :] * waveform_spectra_lim.conj()[None, :, :]

        # exclude autocorrelations by filling diagonal with complex zeros
        diag_idxs = torch.arange(K.shape[0])
        zero_spectra = torch.zeros(omega_lim.shape, dtype=torch.cdouble)
        K[diag_idxs, diag_idxs, :] = zero_spectra

        K = da.from_array(K.numpy())

        beampowers_d = da.einsum("gjiw, ijw -> g", S, K).real

        beampowers = beampowers_d.compute()
        bp.append(beampowers.reshape(len(x_coords),len(z_coords)))

    bp=np.stack(bp)
    # bp /= (len(freq_idx)*(len(ds.distance)**2))

    res=xr.DataArray(np.stack(bp),dims=['v','x','z'])
    res['v']=v_coords
    res['x']=x_coords
    res['z']=z_coords

    res=res.transpose("z","x","v")/((stations.shape[0]-1)*stations.shape[0]*len(omega_lim))

    return res

def artificial_sources(sensors,sources,velocity,sampling_rate=100,window_length=200,scale=1):
    
    tsensors=torch.tensor(sensors).to(dtype=torch.complex128)
    tsources=torch.tensor(sources).to(dtype=torch.complex128)
    distances = torch.linalg.norm(tsensors - tsources, axis=1)

    traveltimes = (distances / velocity)
    
    # define source wavelet
    times = np.arange(0, window_length + 1 / sampling_rate, 1 / sampling_rate)
    
    # compute frequencies
    freqs = torch.fft.fftfreq(len(times), 1 / sampling_rate)
    omega = 2 * np.pi * freqs

    wavelet = torch.fft.fft(torch.from_numpy(ricker(len(times), scale*sampling_rate)))

    waveform_spectra = wavelet * torch.exp(-1j * omega[None, :] * traveltimes[:, None])
    waveforms = torch.fft.ifft(waveform_spectra, axis=1).real

    da=xr.DataArray(waveforms,dims=['distance','time'])
    da['time']=times*10**9
    return da


def artificial_sources_freq(sensors,sources,velocity,sampling_rate=100,window_length=200):
    
    tsensors=torch.tensor(sensors).to(dtype=torch.complex128)
    tsources=torch.tensor(sources).to(dtype=torch.complex128)
    distances = torch.linalg.norm(tsensors - tsources, axis=1)

    traveltimes = (distances / velocity)
    
    # define source wavelet
    times = np.arange(0, window_length + 1 / sampling_rate, 1 / sampling_rate)
    
    # compute frequencies
    freqs = torch.fft.fftfreq(len(times), 1 / sampling_rate)
    omega = 2 * np.pi * freqs

    #wavelet = torch.fft.fft(torch.from_numpy(ricker(len(times), scale*sampling_rate)))

    waveform_spectra = torch.exp(-1j * omega[None, :] * traveltimes[:, None])
    waveforms = torch.fft.ifft(waveform_spectra, axis=1).real

    da=xr.DataArray(waveforms,dims=['distance','time'])
    da['time']=times*10**9
    return da


def MFP_BH(ds,stations_pos,freqrange=[100,200],xrange=[0,50],yrange=[0,50],zrange=[0,100],vrange=[3000,4000],dx=1,dy=1,dz=1,dv=100):
    '''
    Perform Matched Field Processing (MFP) to compute beamforming power over a range of 
    spatial coordinates, velocities, and frequencies.

    :param ds: Input data as an xarray DataArray containing waveform data. 
               Must include 'distance' and 'time' coordinates.
    :type ds: xarray.DataArray

    :param zrange: Range of depths to compute (start and end), default is [0, 100].
    :type zrange: list of float or int

    :param freqrange: Frequency range for processing in Hz (start and end), default is [100, 200].
    :type freqrange: list of float

    :param xrange: Range of horizontal x-coordinates to search (start and end), default is [0, 50].
    :type xrange: list of float or int

    :param vrange: Velocity range to search in m/s (start and end), default is [1000, 6000].
    :type vrange: list of float or int

    :param dz: Spacing between grid points in the depth dimension (z), default is 1.
    :type dz: float or int

    :param dx: Spacing between grid points in the horizontal x dimension, default is 1.
    :type dx: float or int

    :param dv: Spacing between velocities, default is 100.
    :type dv: float or int

    :return: A 3D xarray DataArray containing the computed beampower values. The dimensions are
             'v' (velocity), 'z' (depth), and 'x' (horizontal position).
    :rtype: xarray.DataArray
    '''
    
    # Extract data from dataarray
    sampling_rate=((ds.time[1]-ds.time[0]).values.astype(float)*10**-9)
    # Compute FFT of all the receiver
    waveform_spectra=torch.fft.fft(torch.from_numpy(ds.values.T),axis=1).to(dtype=torch.complex128)
    freqs = torch.fft.fftfreq(len(ds.time),sampling_rate)
    omega = 2 * torch.pi * freqs
    # Build grid for search
    x_coords = torch.arange(xrange[0], xrange[1] + dx, dx)
    y_coords = torch.arange(yrange[0], yrange[1] + dy, dy)
    z_coords = torch.arange(zrange[0], zrange[1] + dz, dz)
    v_coords = torch.arange(vrange[0], vrange[1] + dv, dv)
    gridpoints = torch.tensor(list(product(x_coords,y_coords,z_coords)))
    
    stations=torch.tensor(stations_pos)

    distances_to_all_gridpoints = torch.linalg.norm(gridpoints[:, None, :] - stations[None, :, :], axis=2)
    # limit to frequency band of interest for
    # a) speed# limit to frequency band of interest for
    # a) speed-up
    # b) focusing on specific frequencies
    freq_idx = torch.where((freqs > freqrange[0]) & (freqs < freqrange[1]))[0]
    omega_lim = omega[freq_idx]
    waveform_spectra_lim = waveform_spectra[:, freq_idx]

    bp=[]
    for vel in tqdm(v_coords):
        
        traveltimes = distances_to_all_gridpoints / vel
        
        # Green's functions between all stations and all grid points
        # within selected frequency band
        # G = exp(-iωt)
        greens_functions = torch.exp(-1j * omega_lim[None, None, :] * traveltimes[:, :, None])
        # move critical part to dask
        greens_functions_dask = da.from_array(greens_functions.numpy(), chunks='auto')

        S = (greens_functions_dask[:, :, None, :]*greens_functions_dask.conj()[:, None, :, :])

        # this assumes that K can be computed without memory issues.
        # If this is not the case, you can also use dask and chunk K.
        K = waveform_spectra_lim[:, None, :] * waveform_spectra_lim.conj()[None, :, :]

        # exclude autocorrelations by filling diagonal with complex zeros
        diag_idxs = torch.arange(K.shape[0])
        zero_spectra = torch.zeros(omega_lim.shape, dtype=torch.cdouble)
        K[diag_idxs, diag_idxs, :] = zero_spectra

        K = da.from_array(K.numpy())

        beampowers_d = da.einsum("gjiw, ijw -> g", S, K).real

        beampowers = beampowers_d.compute()
        bp.append(beampowers.reshape(len(x_coords),len(y_coords),len(z_coords)))

    bp=np.stack(bp)
    bp /= (len(freq_idx)*len(ds.distance))

    res=xr.DataArray(np.stack(bp),dims=['v','x','y','z'])
    res['x']=x_coords
    res['y']=y_coords
    res['z']=z_coords
    res['v']=v_coords

    return res
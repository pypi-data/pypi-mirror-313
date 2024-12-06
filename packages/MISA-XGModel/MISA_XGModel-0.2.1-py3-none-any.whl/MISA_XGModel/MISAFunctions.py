import xarray as xr
import pandas as pd
import numpy as np


import os
import glob
import xarray as xr
import h5py
import numpy as np


def load_datasets_with_timestamp_and_range(file_path, group_name):
    with h5py.File(file_path, 'r') as f:
        try:
            group = f[group_name]
        except KeyError:
            # print('key error!')
            return np.nan

        timestamp = group['timestamps'][()]
        range_ = group['range'][()]

        data_dict = {
            'timestamp': ('timestamp', timestamp),
            'range': ('range', range_)
        }

        for dataset_name, dataset in group.items():
            if dataset_name not in ['timestamps', 'range']:
                data = dataset[()]
                if data.ndim == 1 and len(data) == len(timestamp):
                    data_dict[dataset_name] = ('timestamp', data)
                elif data.ndim == 2 and data.shape == (len(timestamp), len(range_)):
                    data_dict[dataset_name] = (('timestamp', 'range'), data)

        dataset = xr.Dataset(data_dict)

        dates = xr.DataArray(timestamp.astype('datetime64[s]').astype('datetime64[ns]'), dims='timestamp', name='dates')
        dataset = dataset.assign_coords(dates=dates)
        # Swap 'timestamp' dimension with 'dates' dimension
        dataset['slt'] = dates.dt.hour + dates.dt.minute / 60.0 + dates.dt.second / 3600.0
        dataset = dataset.swap_dims({'timestamp': 'dates'})
        dataset['doy'] = dataset['dates'].dt.dayofyear

    return dataset


def concatenate_hdf5_files_in_directory(directory_path, group_name):
    datasets = []

    for file_name in sorted(os.listdir(directory_path)):
        if file_name.endswith('.hdf5'):
            file_path = os.path.join(directory_path, file_name)
            ds = load_datasets_with_timestamp_and_range(file_path, group_name)
            if isinstance(ds, (xr.Dataset, xr.DataArray)):
                print(f'appending {file_name}')
                datasets.append(ds)
            else:
                print(f'skipping {file_name}')
                continue

    # Concatenate datasets along the 'timestamp' dimension
    concatenated_dataset = xr.concat(datasets, dim='dates')

    return concatenated_dataset


def convert_YYYYDOY_to_datetime(dates):
    """
    Converts dates from YYYYDOY format to pandas datetime objects.

    Parameters:
    dates: array-like
        An array, list, pandas Series, or xarray DataArray containing dates in YYYYDOY format.

    Returns:
    pandas.DatetimeIndex or pandas.Series
        A DatetimeIndex or Series with the converted dates.
    """
    import pandas as pd
    import numpy as np

    # Ensure dates are in string format
    dates_str = dates.astype(str)

    # Extract the year and day of year from the YYYYDOY format
    years = dates_str.str.slice(0, 4).astype(int)
    doy = dates_str.str.slice(4,).astype(int)

    # Combine year and day of year into datetime objects
    converted_dates = pd.to_datetime(years * 1000 + doy, format='%Y%j')

    # If the input was an xarray DataArray, return an array; otherwise, return a Series or DatetimeIndex
    if isinstance(dates, xr.DataArray):
        return converted_dates.values
    else:
        return converted_dates

def create_geophysical_index_xr(hp_ap_dir, kp_f107_dir, fism2_dir):
    # Load datasets
    fism2_xr = xr.open_dataset(fism2_dir).sel(wavelength=30.4, method='nearest')
    hp_ap_df = pd.read_csv(hp_ap_dir, delim_whitespace=True, skiprows=30, header=None,
                           names=['YYYY', 'MM', 'DD', 'hh.h', 'hh._m', 'days', 'd_m', 'Hp30', 'ap30', 'D'])
    f10_kp_df = pd.read_csv(kp_f107_dir, delim_whitespace=True, skiprows=40, header=None,
                            names=['YYYY', 'MM', 'DD', 'days', 'days_m', 'BSR', 'dB',
                                   'Kp1', 'Kp2', 'Kp3', 'Kp4', 'Kp5', 'Kp6', 'Kp7', 'Kp8',
                                   'ap1', 'ap2', 'ap3', 'ap4', 'ap5', 'ap6', 'ap7', 'ap8',
                                   'Ap', 'SN', 'F10.7obs', 'F10.7adj', 'D'])
    # Replace missing values and parse dates
    f10_kp_df.replace(-1, np.nan, inplace=True)
    hp_ap_df['date'] = pd.to_datetime({'year': hp_ap_df['YYYY'], 'month': hp_ap_df['MM'], 'day': hp_ap_df['DD'], 'hour': hp_ap_df['hh.h']})
    f10_kp_df['date'] = pd.to_datetime({'year': f10_kp_df['YYYY'], 'month': f10_kp_df['MM'], 'day': f10_kp_df['DD']})
    fism2_xr['date'] = convert_YYYYDOY_to_datetime(fism2_xr['date'])
    fism2_df = fism2_xr.to_dataframe()

    # Expand Kp columns to 3-hour intervals
    kp_intervals = pd.to_timedelta([0, 3, 6, 9, 12, 15, 18, 21], unit='h')
    expanded_df = f10_kp_df.loc[f10_kp_df.index.repeat(8)].reset_index(drop=True)
    expanded_df['date'] += np.tile(kp_intervals, len(f10_kp_df))
    kp_columns = ['Kp1', 'Kp2', 'Kp3', 'Kp4', 'Kp5', 'Kp6', 'Kp7', 'Kp8']
    expanded_df['Kp'] = np.array([[f10_kp_df[col][i] for col in kp_columns] for i in range(len(f10_kp_df))]).flatten()

    # Create time series for each index
    hp30_series = pd.Series(hp_ap_df['Hp30'].values, index=hp_ap_df['date'])
    ap30_series = pd.Series(hp_ap_df['ap30'].values, index=hp_ap_df['date'])
    f107_series = pd.Series(f10_kp_df['F10.7adj'].values, index=f10_kp_df['date'])
    kp_series = pd.Series(expanded_df['Kp'].values, index=expanded_df['date'])
    fism2_series = pd.Series(fism2_df['irradiance'].values, index=fism2_df.index)

    # Define date range and forward-fill each series to match target frequency
    start_date = min(hp30_series.index.min(), ap30_series.index.min(), f107_series.index.min(),
                     kp_series.index.min(), fism2_series.index.min())
    end_date = max(hp30_series.index.max(), ap30_series.index.max(), f107_series.index.max(),
                   kp_series.index.max(), fism2_series.index.max())
    dates_full = pd.date_range(start=start_date, end=end_date, freq='30T')

    # Forward-fill to create continuous series
    hp30_series_full = hp30_series.reindex(dates_full, method='ffill')
    ap30_series_full = ap30_series.reindex(dates_full, method='ffill')
    f107_series_full = f107_series.reindex(dates_full, method='ffill')
    kp_series_full = kp_series.reindex(dates_full, method='ffill')
    fism2_series_full = fism2_series.reindex(dates_full, method='ffill')

    # make an slt variable for convenience
    # Convert to decimal hours
    slt_full = [
        date.hour + date.minute / 60 + date.second / 3600 for date in dates_full
    ]

    # Combine into an xarray Dataset
    geo_indices_ds = xr.Dataset({
        'slt': xr.DataArray(slt_full, coords=[dates_full], dims=['dates']),
        'hp30': xr.DataArray(hp30_series_full, coords=[dates_full], dims=['dates']),
        'ap30': xr.DataArray(ap30_series_full, coords=[dates_full], dims=['dates']),
        'f107': xr.DataArray(f107_series_full, coords=[dates_full], dims=['dates']),
        'kp': xr.DataArray(kp_series_full, coords=[dates_full], dims=['dates']),
        'fism2': xr.DataArray(fism2_series_full, coords=[dates_full], dims=['dates']),
    })

    return geo_indices_ds
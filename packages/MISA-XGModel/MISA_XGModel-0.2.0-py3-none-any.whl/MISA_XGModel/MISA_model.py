import requests
import os
import numpy as np
from xgboost import XGBRegressor
import xarray as xr
import pandas as pd
import json
from sklearn.preprocessing import StandardScaler

# Dropbox URLs for required files
MODEL_URL = "https://www.dropbox.com/scl/fi/buerwbp580l98c5egbmvg/xgboost_optimized_model.json?rlkey=0mxboow2r44j7pz3xx199inko&dl=1"
SCALER_URL = "https://www.dropbox.com/scl/fi/6oas604oh4xcupzc8at2b/scaler_large.json?rlkey=6huwm1baf1vc7cf9r4of4xxds&st=2s3wu078&dl=1"
GEO_DS_URL = "https://www.dropbox.com/scl/fi/m6p9h25h2f517ibk1a233/master_geo_ds.nc?rlkey=8tw5idep8mu1prydtbn3vjl87&st=8zo54jno&dl=1"

# Paths to save downloaded files
MODEL_PATH = "data/xgboost_optimized_model.json"
SCALER_PATH = "data/scaler_large.json"
MASTER_GEO_DS_PATH = "data/master_geo_ds.nc"

# Bounds for clamping
input_bounds = {
    'lat': (np.float64(37.5), np.float64(49.9)),
    'lon': (np.float64(-85.7), np.float64(-76.1)),
    'alt': (np.float64(94.6), np.float64(500)),
    'slt': (np.float64(0.0), np.float64(24))
}


# Utility to download files from Dropbox
def download_file(url, save_path):
    """Download a file from a URL if it doesn't exist locally."""
    if not os.path.exists(save_path):
        print(f"Downloading file from {url}...")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):  # 8 KB chunks
                    f.write(chunk)
            print(f"File downloaded and saved to {save_path}.")
        else:
            raise RuntimeError(f"Failed to download file. HTTP Status Code: {response.status_code}")

# Utility to load scaler
def load_scaler(json_path):
    """Load a StandardScaler from a JSON file."""
    with open(json_path, "r") as f:
        scaler_params = json.load(f)

    scaler = StandardScaler()
    scaler.mean_ = np.array(scaler_params["mean"])
    scaler.scale_ = np.array(scaler_params["scale"])
    scaler.var_ = np.array(scaler_params["var"])
    scaler.n_features_in_ = len(scaler.mean_)  # Ensure compatibility with sklearn's expectations
    return scaler

# Download required files
download_file(MODEL_URL, MODEL_PATH)
download_file(SCALER_URL, SCALER_PATH)
download_file(GEO_DS_URL, MASTER_GEO_DS_PATH)


# Load the model, scaler, and geophysical dataset
optimized_xgb = XGBRegressor()
optimized_xgb.load_model(MODEL_PATH)
scaler_large = load_scaler(SCALER_PATH)
master_geo_ds = xr.open_dataset(MASTER_GEO_DS_PATH)

def predict_ne(lat, lon, doy, alt, slt, year, master_geo_ds=master_geo_ds, model=optimized_xgb, scaler=scaler_large):
    """
    Batch predict electron density (Ne) for multiple inputs.

    Parameters:
        lat, lon, doy, alt, slt (array-like): Arrays of input parameters for batch predictions.
        year (int): Year for geophysical indices lookup (applies to all inputs).
        master_geo_ds (xarray.Dataset): Dataset containing geophysical indices.
        model (XGBRegressor): Trained XGBoost model for predictions.
        scaler (StandardScaler): Scaler used for feature normalization.

    Returns:
        ndarray: Array of predicted electron densities (Ne).
    """
    # Convert inputs to NumPy arrays for batch processing
    lat = np.asarray(lat)
    lon = np.asarray(lon)
    doy = np.asarray(doy)
    alt = np.asarray(alt)
    slt = np.asarray(slt)

    # Clamp inputs
    lat = np.clip(lat, *input_bounds["lat"])
    lon = np.clip(lon, *input_bounds["lon"])
    doy = doy % 365  # Wrap DOY
    alt = np.clip(alt, *input_bounds["alt"])
    slt = np.clip(slt, *input_bounds["slt"])

    # Ensure `dates` coordinate is in datetime format
    dates_as_datetime = pd.to_datetime(master_geo_ds["dates"].values)

    # Filter by year
    year_mask = dates_as_datetime.year == year
    if not np.any(year_mask):
        raise ValueError(f"No data available in `master_geo_ds` for year {year}.")

    filtered_data = master_geo_ds.sel(dates=year_mask)
    geo_indices = []
    for day in doy:
        # Match DOY
        dates_doy = pd.to_datetime(filtered_data["dates"].values).dayofyear
        doy_mask = dates_doy == day
        if not np.any(doy_mask):
            raise ValueError(f"No data available in `master_geo_ds` for DOY {day} in year {year}.")
        matched_dates = filtered_data.sel(dates=doy_mask)
        geo_indices.append(matched_dates.isel(dates=0))

    # Extract geophysical indices
    hp30 = np.array([g["hp30"].values.item() for g in geo_indices])
    ap30 = np.array([g["ap30"].values.item() for g in geo_indices])
    f107 = np.array([g["f107"].values.item() for g in geo_indices])
    kp = np.array([g["kp"].values.item() for g in geo_indices])
    fism2 = np.array([g["fism2"].values.item() for g in geo_indices])

    # Predict using query_model
    return query_model(lat, lon, doy, alt, slt, hp30, ap30, f107, kp, fism2, model=model, scaler=scaler)

def query_model(lat, lon, doy, alt, slt, hp30, ap30, f107, kp, fism2, model=optimized_xgb, scaler=scaler_large):
    """
    Predicts Ne using the model and precomputed geophysical indices,
    clamping input values to the range of training data.

    Parameters:
        lat, lon, doy, alt, slt, hp30, ap30, f107, kp, fism2 (array-like): Arrays of input parameters.
        model (XGBRegressor): Pre-trained XGBoost model.
        scaler (StandardScaler): Scaler used for feature normalization.

    Returns:
        ndarray: Array of predicted electron densities (Ne).
    """
    # Convert inputs to NumPy arrays
    lat = np.asarray(lat)
    lon = np.asarray(lon)
    doy = np.asarray(doy)
    alt = np.asarray(alt)
    slt = np.asarray(slt)
    hp30 = np.asarray(hp30)
    ap30 = np.asarray(ap30)
    f107 = np.asarray(f107)
    kp = np.asarray(kp)
    fism2 = np.asarray(fism2)

    # Clamp inputs
    lat = np.clip(lat, *input_bounds["lat"])
    lon = np.clip(lon, *input_bounds["lon"])
    doy = doy % 365  # Wrap DOY
    alt = np.clip(alt, *input_bounds["alt"])
    slt = np.clip(slt, *input_bounds["slt"])

    # Compute engineered features
    doy_sin = np.sin(2 * np.pi * doy / 365)
    doy_cos = np.cos(2 * np.pi * doy / 365)
    slt_sin = np.sin(2 * np.pi * slt / 24)
    slt_cos = np.cos(2 * np.pi * slt / 24)
    alt_f107 = alt * f107
    lat_fism2 = lat * fism2
    hp30_ap30 = hp30 / (ap30 + 1e-6)
    f107_kp = f107 * kp
    alt_squared = alt ** 2
    f107_squared = f107 ** 2
    slt_cubed = slt ** 3
    doy_cubed = doy ** 3
    log_f107 = np.log1p(f107)
    log_ap30 = np.log1p(ap30)

    # Prepare input features for the model
    input_features = np.column_stack((
        lat, lon, alt, slt, doy, hp30, ap30, f107, kp, fism2,
        slt_sin, slt_cos, doy_sin, doy_cos, alt_f107, lat_fism2,
        hp30_ap30, f107_kp, alt_squared, f107_squared,
        slt_cubed, doy_cubed, log_f107, log_ap30
    ))

    # Scale features
    input_features_scaled = scaler.transform(input_features)

    # Predict using the model
    prediction_log = model.predict(input_features_scaled)
    return np.expm1(prediction_log)  # Transform back from log scale
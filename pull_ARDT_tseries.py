######################################################################
# Filename:    pull_ARDT_tseries.py
# Author:      Deanna Nash, dnash@ucsd.edu
# Description: Pull ARDT from CDR dataset at specified point and save as csv
######################################################################

import xarray as xr
import pandas as pd

# =====================================================================
# CONFIG
# =====================================================================
start_date = '2025-08-01'
end_date = '2026-08-31'

# target grid cell - closest to Sitka
x = -135.33
y = 57.05
ext = [x-1, x+1, y-1, y+1]

# =====================================================================
# DATA LOADING FUNCTIONS
# =====================================================================


def read_AR_data(ar_filename, ext, multifile=False):
    """Read AR catalog data."""

    if multifile:
        ds = xr.open_mfdataset(ar_filename)
    else:
        ds = xr.open_dataset(ar_filename)

    ds = ds.assign_coords({
        "longitude": (((ds.longitude + 180) % 360) - 180)
    })

    ds = ds.sortby("longitude")

    da = (
        ds
        .sel(
            latitude=slice(ext[3], ext[2]),
            longitude=slice(ext[0], ext[1]),
        )
        .squeeze()
        .ARs
    )

    return da
    
# =================================================================
# AR DATA
# =================================================================
filenames = []
for date in pd.date_range(start_date, end_date, freq='1M'):
    year = date.year
    month = date.month
    filename = f"/data/projects/AR_Science/CDR/ARScale/data/v2.0/{year}/CDR_ERA5_ARScale_v2.0_{year}{str(month).zfill(2)}.nc"
    filenames.append(filename)

AR = read_AR_data(
    ar_filename=filenames,
    ext=ext,
    multifile=True,
)

# Maximum across spatial dimensions: was an AR detected anywhere?
tmp = AR.max(dim=["latitude", "longitude"])

# Convert to daily dataframe
df_ardt_6hr = tmp.to_dataframe(name="AR_detected").reset_index()

# Save to CSV
outfile = f"data/ARDT/Sitka_ARDT_6hr_timeseries_{start_date}_{end_date}.csv"
df_ardt_6hr.to_csv(outfile, index=False)

print(f"Saved {outfile}")

# Daily maximum: was an AR detected at any time during the day?
daily_da = tmp.resample(time="1D").max()

# Convert to daily dataframe
df_ardt = daily_da.to_dataframe(name="AR_detected").reset_index()

# Save to CSV
outfile = f"data/ARDT/Sitka_ARDT_daily_timeseries_{start_date}_{end_date}.csv"
df_ardt.to_csv(outfile, index=False)

print(f"Saved {outfile}")
######################################################################
# Filename:    pull_IVT_tseries.py
# Author:      Deanna Nash, dnash@ucsd.edu
# Description: Pull IVT at specified point and save as csv
######################################################################

import xarray as xr
import pandas as pd
import numpy as np
from pathlib import Path

path_to_ERA5 = Path("/data/projects/external_datasets/ERA5_IVT/data/processed/")
path_to_out  = Path("/home/dnash/repos/ivt_isotope_analysis/data/IVT/ERA5_IVT_point_timeseries_20250201-20260930_135.25W_57N.csv")

# target grid cell - closest to Sitka
x = -135.33
y = 57.05

start = "2026-02-01"
end   = "2026-09-30"

# create date range
dates = pd.date_range(start, end, freq="D")

def pull_ivt_point_to_csv(dates, x, y, outfile):

    first_write = True

    for d in dates:

        fname = path_to_ERA5 / f"{d.year}/ERA5_IVT_{d.strftime('%Y%m%d')}.nc"

        if not fname.exists():
            print(f"Missing {fname}")
            continue

        print(f"Processing {fname}")

        with xr.open_dataset(fname) as ds:

            # drop unused variables
            ds = ds.drop_vars(["uIVT", "vIVT", "IWV"], errors="ignore")

            # select nearest grid cell
            point = ds.sel(longitude=x, latitude=y, method="nearest")

            # convert to dataframe
            df = point["IVT"].to_dataframe().reset_index()

        # append to CSV
        df.to_csv(
            outfile,
            mode="w" if first_write else "a",
            header=first_write,
            index=False
        )

        first_write = False


# run function
pull_ivt_point_to_csv(dates, x, y, path_to_out)

print(f"Saved to {path_to_out}")
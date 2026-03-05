######################################################################
# Filename:    align_IVT_with_isotope_dates.py
# Author:      Deanna Nash, dnash@ucsd.edu
# Description: Pull IVT at specified time to align with isotope sample dates
######################################################################
import pandas as pd

datadir="/home/dnash/repos/ivt_isotope_analysis/data/"
isotope_dates="sitka_isotope_start_end_dates.csv"
ivt_data="ERA5_IVT_point_timeseries_20250801-20260131_135.25W_57N.csv"

# -----------------------
# Read data
# -----------------------
df = pd.read_csv(datadir + isotope_dates)
ivt = pd.read_csv(datadir + ivt_data)

# -----------------------
# Parse times
# -----------------------
date_fmt = "%m/%d/%y %H:%M"

df["start_local"] = pd.to_datetime(df["Start_Date_Start_Time"], format=date_fmt)
df["end_local"]   = pd.to_datetime(df["Collection_Date_Collection_Time"], format=date_fmt)

# Alaska local timezone
df["start_utc"] = (
    df["start_local"]
    .dt.tz_localize("America/Anchorage")
    .dt.tz_convert("UTC")
)

df["end_utc"] = (
    df["end_local"]
    .dt.tz_localize("America/Anchorage")
    .dt.tz_convert("UTC")
)

# IVT timestamps
ivt["time"] = pd.to_datetime(ivt["time"], utc=True)

# -----------------------
# Loop through samples
# -----------------------
max_ivt = []
ivt_at_collection = []

for _, row in df.iterrows():

    start = row["start_utc"]
    end = row["end_utc"]

    # subset IVT during sample collection
    subset = ivt[(ivt["time"] >= start) & (ivt["time"] <= end)]

    if len(subset) > 0:
        max_ivt.append(subset["IVT"].max())
    else:
        max_ivt.append(None)

    # IVT closest to collection time
    idx = (ivt["time"] - end).abs().idxmin()
    ivt_at_collection.append(ivt.loc[idx, "IVT"])

# -----------------------
# Add to dataframe
# -----------------------
df["IVT_max_during_collection"] = max_ivt
df["IVT_nearest_collection"] = ivt_at_collection

# -----------------------
# Save
# -----------------------
outfile = datadir + "sitka_isotope_ivt_summary.csv"
df.to_csv(outfile, index=False)

print("Saved:", outfile)
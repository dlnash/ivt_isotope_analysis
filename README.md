# Align IVT with Isotope Sample Collection Dates

This repository contains scripts used to extract Integrated Vapor Transport (IVT) from ERA5 reanalysis data and align it with isotope sample collection periods from Sitka, Alaska. 

Additionally, this repository contains scripts that extract a 6-hourly and daily time series of whether or not an Atmospheric River was detected using the Tracking Atmospheric Rivers Globally as Elongated Targets (tARget) algorithm version 4 (Guan and Waliser, 2024) applied to ERA5 every 6-hours. The ARDT was applied to the grid cell closest to Sitka (e.g., 135.33W,  57.05N) +- 1 degree in each direction. If there was an AR detected in any of the 8 gridcells, then an AR was marked for that time step. For the daily time series, if an AR was present at any of the 6-hr time steps within a day, then an AR was marked for that day.

The workflow produces a dataset that includes:

- Maximum IVT during each sample collection period  
- IVT closest to the sample collection time
- 6-hr AR detection tools (ARDTs) time series
- Daily AR detection tools (ARDTs) time series 

These metrics allow comparison between atmospheric river occurrence, intensity and isotope measurements.

---

# Repository Structure

```
.
├── LICENSE.md
├── README.md
├── align_IVT_with_isotope_dates.py
├── data
│   ├── ARDT
│   ├── IVT
│   │   ├── ERA5_IVT_point_timeseries_20250201-20260930_135.25W_57N.csv
│   │   └── ERA5_IVT_point_timeseries_20250801-20260131_135.25W_57N.csv
│   ├── Sitka_ARDT_6hr_timeseries_2025-08-01_2026-08-31.csv
│   ├── Sitka_ARDT_daily_timeseries_2025-08-01_2026-08-31.csv
│   └── archive
│       ├── sitka_isotope_ivt_summary.csv
│       └── sitka_isotope_start_end_dates.csv
├── pull_ARDT_tseries.py
└── pull_IVT_tseries.py
```

---

# Scripts

## `pull_ARDT_tseries.py`

Extracts a 6-hr and daily ARDT time series for the 8 grid cells surrounding Sitka.

### Input

6hr ARDT files with the pattern:

```
/data/projects/AR_Science/CDR/ARScale/data/v2.0/YYYY/CDR_ERA5_ARScale_v2.0_YYYYMM.nc
```

### Process

The script:

1. Opens ARDT files all at once.
2. Selects the 8 nearest grid cells to the specified latitude/longitude  
3. Extracts 6-hr ARDT values  
4. Appends them to a CSV file
5. Resamples to daily maximum
6. Appends them to a daily CSV file  

### Output

```
data/ARDT/Sitka_ARDT_6hr_timeseries_YYYY-MM-DD_YYYY-MM-DD.csv
data/ARDT/Sitka_ARDT_daily_timeseries_YYYY-MM-DD_YYYY-MM-DD.csv
```

Example:

```
Sitka_ARDT_6hr_timeseries_2025-08-01_2026-08-31.csv
```

Columns:

| column | description |
|------|-------------|
| time | timestamp (UTC) |
| AR_detected | AR detected by tARget = 1, no AR = 0 |

---

## `pull_IVT_tseries.py`

Extracts an hourly IVT time series from ERA5 for a single grid cell.

### Input

Daily ERA5 IVT files with the pattern:

```
ERA5_IVT_YYYYMMDD.nc
```

### Process

The script:

1. Opens daily ERA5 files sequentially  
2. Selects the nearest grid cell to the specified latitude/longitude  
3. Extracts hourly IVT values  
4. Appends them to a CSV file  

This approach minimizes memory usage by reading one file at a time.

### Output

```
data/IVT/ERA5_IVT_point_timeseries_YYYYMMDD-YYYYMMDD_lon_lat.csv
```

Example:

```
ERA5_IVT_point_timeseries_20250801-20260131_135.25W_57N.csv
```

Columns:

| column | description |
|------|-------------|
| time | timestamp (UTC) |
| lat | latitude of grid cell |
| lon | longitude of grid cell |
| ivt | integrated vapor transport (kg m⁻¹ s⁻¹) |

---

## `align_IVT_with_isotope_dates.py`

Aligns IVT data with isotope sampling periods.

### Inputs

1. **Isotope sampling times**

```
data/sitka_isotope_start_end_dates.csv
```

Contains:

| column | description |
|------|-------------|
| Start_Date_Start_Time | start of sample collection (Alaska local time) |
| Collection_Date_Collection_Time | end of sample collection (Alaska local time) |
| Sample_ID | sample identifier |

2. **ERA5 IVT time series**

```
data/ERA5_IVT_point_timeseries_20250801-20260131_135.25W_57N.csv
```

### Processing Steps

The script:

1. Converts isotope timestamps from **Alaska local time** (`America/Anchorage`) to **UTC**  
2. For each sample:
   - Calculates the **maximum IVT during the collection period**
   - Finds the **IVT value closest to the collection time**
3. Appends these metrics to the isotope dataset.

### Output

```
data/sitka_isotope_ivt_summary.csv
```

New columns added:

| column | description |
|------|-------------|
| IVT_max_during_collection | maximum IVT between sample start and end |
| IVT_nearest_collection | IVT closest to the collection time |

---

# Data

The `data/` directory contains:

| file | description |
|----|-------------|
| `sitka_isotope_start_end_dates.csv` | sampling start/end times provided by collaborator |
| `ERA5_IVT_point_timeseries_*.csv` | ERA5 IVT extracted for Sitka grid cell |
| `sitka_isotope_ivt_summary.csv` | final merged dataset with IVT metrics |

---

# Dependencies

Required Python packages:

```
pandas
xarray
numpy
```

Install with:

```
pip install pandas xarray numpy
```

---

# Notes

- Isotope timestamps are provided in **Alaska local time** and converted to **UTC** to match ERA5 data.
- ERA5 IVT files are processed **one day at a time** to minimize memory usage.
- The grid cell is selected using **nearest-neighbor selection**.
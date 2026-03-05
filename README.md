# Align IVT with Isotope Sample Collection Dates

This repository contains scripts used to extract Integrated Vapor Transport (IVT) from ERA5 reanalysis data and align it with isotope sample collection periods from Sitka, Alaska.

The workflow produces a dataset that includes:

- Maximum IVT during each sample collection period  
- IVT closest to the sample collection time  

These metrics allow comparison between atmospheric river intensity and isotope measurements.

---

# Repository Structure

```
.
├── align_IVT_with_isotope_dates.py
├── pull_IVT_tseries.py
├── data/
│   ├── ERA5_IVT_point_timeseries_20250801-20260131_135.25W_57N.csv
│   ├── sitka_isotope_start_end_dates.csv
│   └── sitka_isotope_ivt_summary.csv
└── README.md
```

---

# Scripts

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
data/ERA5_IVT_point_timeseries_YYYYMMDD-YYYYMMDD_lon_lat.csv
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
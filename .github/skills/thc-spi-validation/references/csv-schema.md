# CSV Schema — WBIO SIV Measurement File

Reference for all columns present in the CSV exported from WBIO/CloudCDS for SIV electrical validation.

## Identity & Traceability

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| `hostname` | str | `GM03WVAW2676` | Machine where the test ran |
| `username` | str | `gmsvuser` | Test runner |
| `createdat` | datetime | `2026-01-09T19:53:38.221Z` | ISO-8601 timestamp of test execution |
| `lab` | str | `GM` | Lab identifier |
| `team` | str | `wbio` | Team that owns the test |
| `project` | str | `nvlhx` | Project/platform codename |
| `testid` | uuid | `7e8fef8a-…` | Unique test run ID |
| `subtestid` | str | `/4/2/1/1/` | Sub-test path within the test run |

## Product / Platform

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| `product_name` | str | `Nova Lake` | Full product name |
| `product_type` | str | `Discrete PCH` | PCH type |
| `platform_name` | str | `RVP01-NVL Hx_UL DDR5 SODIMM 1DPC T3` | Board/platform name |
| `platform_type` | str | `RVP` | Platform category |
| `product_class` | str | `Hx` | Product class |
| `pch_stepping` | str | `a0` | PCH stepping |
| `pch_ult` | str | `Q515B301_080_+3_+0` | PCH ULT string |
| `pch_vid` | str | `U5KF411700907` | PCH Visual ID (unique unit identifier) |
| `die` | str | `PCD-H` | Die name |
| `cpu_stepping` | str | `a0` | CPU stepping |
| `cpu_ult` | str | `G5238080_079_-22_+7` | CPU ULT string |
| `cpu_vid` | str | `U538G12400977` | CPU Visual ID |
| `ifwi_version` | str | `NVL_HR11_A1A0-…_2025WW48.3.01` | IFWI firmware version |

## Test Configuration

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| `interface_name` | str | `THC_SPI` | Interface under test — **primary pre-filter** |
| `discipline` | str | `SIV` | Measurement discipline — **filter = SIV** |
| `mode` | str | `Quad` | SPI mode — **filter = Quad** |
| `port` | str | `THC0` | Port used |
| `topology` | str | `Single Load` | Board topology |
| `data_rate` | str | `Single` | Data rate mode — **filter = Single** |
| `end_point` | str | `Generic \| Generic` | Endpoint description |
| `frequency` | str | `42 MHz` | Clock frequency used |
| `vt_corner` | str | `Low` / `Typ` / `High` / `Fast` / `Slow` | Voltage-Temperature corner — **X-axis grouping** |
| `buffer_type` | str | `c76pxecfio_io1p8_hsmv` | IO buffer type |

## Measurement Data

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| `Signal` | str | `Clock`, `TXIO0`, `TXIO1`, `TXIO2`, `TXIO3`, `ChipSelect` | Signal group — **used by each script to self-filter** |
| `Measurement` | str | `tF`, `tR`, `DutyCycle`, `HoldF`, `SetupR`, … | Measurement parameter name — **By() panel** |
| `mean` | numeric | `2.46E-09` | Mean value across all waveforms — **Y-axis** |
| `min` | numeric | `1.67E-09` | Minimum measured value |
| `max` | numeric | `3.55E-09` | Maximum measured value |
| `std dev` | numeric | `3.42E-10` | Standard deviation |
| `current` | numeric | `2.38E-09` | Last measured value |
| `# of meas` | int | `1748` | Number of waveforms measured |

## Spec Limits (from EDS — embedded in CSV)

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| `spec_min` | numeric or `n/a` | `9.37E-09` | Minimum spec limit from EDS — **lower ref line** |
| `spec_max` | numeric or `n/a` | `1.41E-08` | Maximum spec limit from EDS — **upper ref line** |
| `spec_id` | int | `646055` | Spec database ID |
| `spec_version` | str | `661` | Spec document version |
| `parameter_name_from_spec` | str | `Frequency` | Parameter name as it appears in the EDS spec |

> **Important:** `spec_min` and `spec_max` can contain the string `"n/a"` when the spec has no limit for that direction. Always use `Num()` in JMP to convert — it returns `.` (missing) for non-numeric strings, and `Is Missing()` to check before drawing the reference line.

## Validity Flags

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| `Valid_Meas` | bool | `TRUE` | Whether this measurement is considered valid |
| `DataValid_by_TestId` | bool | `TRUE` | Data validity per test ID |
| `is_valid_mask` | hex | `0x1ffffffff` | Bitmask for valid waveforms |
| `meas_id` | int | `15` | Measurement ID within the test |

## PCD Configuration (scope images)

| Column | Type | Description |
|--------|------|-------------|
| `PCD_Dts0` … `PCD_Dts7` | numeric | Scope DTS channel configurations |
| `Tc` | numeric | Temperature (°C) during measurement |
| `V1P8A` | numeric | 1.8V rail measured voltage |

## Signals & Measurements Matrix

| Signal | Measurements Available |
|--------|----------------------|
| `Clock` | tF, tR, DutyCycle, LowTime, HighTime, Period, t180a (Frequency) |
| `TXIO0` | tF, tR, HoldF, HoldR, SetupF, SetupR |
| `TXIO1` | tF, tR, HoldF, HoldR, SetupF, SetupR |
| `TXIO2` | tF, tR, HoldF, HoldR, SetupF, SetupR |
| `TXIO3` | tF, tR, HoldF, HoldR, SetupF, SetupR |
| `ChipSelect` | HoldTime, SetupTime |

## Corner Values

| `vt_corner` | Meaning |
|-------------|---------|
| `Low` | Low voltage, nominal temperature |
| `Typ` | Typical voltage, typical temperature |
| `High` | High voltage, nominal temperature |
| `Fast` | Best-case process, high voltage, low temperature |
| `Slow` | Worst-case process, low voltage, high temperature |

# Scripts

Each subfolder is a self-contained analysis script that the Autoreporting tool
can queue and execute. Scripts receive a filtered JMP data table and return a
chart object pointer (used for PPTX export).

## Script Contract

Every script **must** follow this signature:

```jsl
script = Function( { dt, pntr },
    { Default Local },
    // ... analysis ...
    Return( vc );   // chart pointer — required for PPTX export
                    // Return( 0 ) marks the script as a utility (no chart)
);
```

## Folder Contents

Each script folder should contain:

| File | Required | Purpose |
|------|----------|---------|
| `Script.jsl` | Yes | Main script code |
| `Description.txt` | Yes | Shown in GUI preview panel |
| `*.png` / `*.jpg` | Optional | Preview image shown in GUI |

## Available Scripts

### THC_SPI — Nova Lake Hx

| Folder | Signal group | Measurements | Spec limits |
|--------|-------------|--------------|-------------|
| `charVariability_THC_SPI_Clock` | Clock | tF, tR, DutyCycle, LowTime, HighTime, Period, t180a | Dynamic from CSV |
| `charVariability_THC_SPI_DataLines` | TXIO0–TXIO3 | tF, tR, HoldF, HoldR, SetupF, SetupR | Dynamic from CSV |
| `charVariability_THC_SPI_CS` | ChipSelect | HoldTime, SetupTime | Dynamic from CSV |

### Variability — Generic SIV

| Folder | Description |
|--------|-------------|
| `charVariability_WBIO_SIV_3Sigma` | ±3σ variability chart from Mean/StdDev columns |
| `charVariability_WBIO_SIV_3Sigma_CPU` | Same as above, CPU variant |
| `chrVariability_WBIO_SIV_StackData` | Stack-based variability chart |
| `Variability_EH_Safe` | Eye Height variability with fixed ±8 ref lines |
| `Variability_EW_Safe` | Eye Width variability with fixed ref lines |

### Utilities

| Folder | Description |
|--------|-------------|
| `save_as_pptx` | Captures all chart images and assembles a PPTX (always last in pipeline) |
| `save_as_csv` | Saves the filtered data table as CSV |
| `save_as_image` | Saves individual chart captures |

## Design Principles

- **Self-filtering**: each script subsets by its own `Signal` value — no pre-filtering in the GUI needed
- **Dynamic spec limits**: `spec_min`/`spec_max` are read from the CSV columns, never hardcoded
- **Additive pipeline**: scripts run in queue order; each one gets the same `subset` table
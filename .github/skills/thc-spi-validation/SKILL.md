---
name: thc-spi-validation
description: "Electrical validation skill for Intel THC_SPI interface (and any SIV interface). Use when: user wants to validate THC SPI, run electrical validation from a CSV, generate variability charts, create an autoreport for SPI, add a new interface to the Autoreporting tool, or asks about spec limits, signal measurements (tF, tR, DutyCycle, Setup, Hold), or corner analysis (Low/Typ/High/Fast/Slow). Covers: running main_THC_SPI.jsl, creating JMP scripts for new interfaces, profile management, and CSV-to-PPTX automated pipeline."
argument-hint: "interface name or CSV path (optional)"
---

# THC_SPI Electrical Validation — Autoreporting Skill

## What This Skill Does

Guides automated electrical validation of Intel SPI interfaces using the **Autoreporting** JMP-based tool.  
Given a WBIO CSV from the measurement database, it produces:
- Variability Charts per signal group (Clock, Data Lines, ChipSelect)
- Automatic spec limit lines from the CSV itself (no hardcoding)
- A dated PPTX report — zero manual steps after selecting the CSV

## Workspace Layout

```
Autoreporting/Autoreporting/Main/
├── main_THC_SPI.jsl                     ← Fully automated entry point (1-click)
├── main.jsl                             ← Interactive GUI entry point
├── profiles/
│   └── NVL-THC_SPI/profile.json        ← Pre-configured filters + script pipeline
├── scripts/
│   ├── charVariability_THC_SPI_Clock/  ← Clock: tF, tR, DutyCycle, LowTime, HighTime
│   ├── charVariability_THC_SPI_DataLines/ ← TXIO0-3: Setup/Hold times
│   └── charVariability_THC_SPI_CS/     ← ChipSelect: SetupTime, HoldTime
└── config/config.json
```

---

## Procedure: Run THC_SPI Validation (Automated)

**Requirements:** JMP 17+, CSV file from WBIO/CloudCDS with the columns in [CSV Schema](./references/csv-schema.md).

1. Open JMP.
2. `File → Run Script` → select `Autoreporting/Autoreporting/Main/main_THC_SPI.jsl`.
3. When prompted, select the CSV file (e.g., `Data_WBIO_NVL_Hx_THC_SPI.csv`).
4. Script automatically:
   - Filters rows: `interface_name=THC_SPI`, `discipline=SIV`, `mode=Quad`, `data_rate=Single`
   - Runs 3 variability chart scripts
   - Creates `THC_SPI_Report_YYYY-MM-DD/` next to the CSV
   - Exports PPTX

**If something fails:** check the JMP Log window — each step prints its status.

---

## Procedure: Run via GUI (Interactive)

Use when you need to explore data or apply custom filters before running.

1. Open `main.jsl` in JMP.
2. "Search Local Data" → select CSV.
3. Load profile `NVL-THC_SPI` from the Profiles panel.
4. Click Run.

The profile pre-loads all 4 filters and the 3-script pipeline automatically.

---

## Procedure: Add a New Interface

When a user asks to add validation for a new interface (e.g., I2C, USB, PCIe), follow the steps in [New Interface Template](./references/new-interface-template.md).

**Summary of what to create:**
1. `scripts/charVariability_<IFACE>_<SignalGroup>/Script.jsl` (one per signal group)
2. `scripts/charVariability_<IFACE>_<SignalGroup>/Description.txt`
3. `profiles/<PRODUCT>-<IFACE>/profile.json`
4. Optionally a dedicated `main_<IFACE>.jsl`

---

## Key Design Principles (always apply)

| Principle | Implementation |
|-----------|----------------|
| Spec limits are **dynamic** | Read `spec_min`/`spec_max` from CSV columns — never hardcode numbers |
| Filters are **additive** | Each filter restricts the previous selection via `FL:filter_engine()` |
| Scripts are **self-filtering** | Each script subsets by its own `Signal` value — no pre-filtering needed |
| Charts return a **pointer** | `Return( vc )` so `SC:execute_jsl` can accumulate `pntr` for PPTX export |
| Output path is **derived** | From the CSV file path — no `PickDirectory()` needed in automated mode |

---

## CSV Column Reference

See [CSV Schema](./references/csv-schema.md) for all column names, types, and example values.

Key columns used by the scripts:

| Column | Used for |
|--------|----------|
| `Signal` | Filter per script (Clock / TXIO0-3 / ChipSelect) |
| `Measurement` | Panel grouping in By() clause |
| `mean` | Y-axis value (converted to numeric) |
| `pch_vid` | X-axis unit identifier |
| `vt_corner` | X-axis corner (Low/Typ/High/Fast/Slow) |
| `spec_min` / `spec_max` | Reference lines (dynamic) |
| `interface_name` | Pre-filter = "THC_SPI" |
| `discipline` | Pre-filter = "SIV" |
| `mode` | Pre-filter = "Quad" |
| `data_rate` | Pre-filter = "Single" |

---

## Profile JSON Structure

```json
{
    "OBJECT":     { "DSN": "Local", "Obj": "", "Schema": "", "Type": "Local" },
    "PREFILTERS": { "Date": [], "Filter": null, "Interfaces": ["THC_SPI"] },
    "FILTERS": {
        "1": {"interface_name": ["THC_SPI"]},
        "2": {"discipline":     ["SIV"]},
        "3": {"mode":           ["Quad"]},
        "4": {"data_rate":      ["Single"]}
    },
    "SCRIPTS": [
        "charVariability_THC_SPI_Clock",
        "charVariability_THC_SPI_DataLines",
        "charVariability_THC_SPI_CS",
        "save_as_pptx"
    ]
}
```

`FILTERS` keys must be sequential strings `"1"`, `"2"`, etc.  
`SCRIPTS` order defines execution order in the pipeline.

---

## JMP Script Template (per signal group)

Every analysis script must follow this structure so the orchestrator can handle it:

```jsl
script = Function( { dt, pntr },
    { Default Local },

    /* 1. Convert numeric columns */
    CM:col_to_num( dt, "mean"     );
    CM:col_to_num( dt, "spec_min" );
    CM:col_to_num( dt, "spec_max" );

    /* 2. Filter by Signal */
    dt << Select Where( :Signal == "<SIGNAL_VALUE>" );
    sub = dt << Subset( Output Table( "<NAME>" ), Selected Rows(1), Invisible );
    dt << Clear Select;

    If( N Rows( sub ) == 0, Throw( "No rows for Signal = <SIGNAL_VALUE>" ) );

    /* 3. Build Variability Chart with dynamic spec lines */
    vc = sub << Variability Chart(
        Y( :mean ),
        X( :pch_vid, :vt_corner ),
        Std Dev Chart( 0 ),
        By( :Signal, :Measurement ),
        SendToReport(
            Dispatch( {}, "2", ScaleBox, {
                Label Row( { Show Major Grid(1), Show Minor Grid(1) } ),
                Add Ref Line( Num(Column(sub,"spec_min")[1]), "Dashed", "Medium Dark Red",
                    "MinSpec "||Char(Format(Num(Column(sub,"spec_min")[1]),"Engineering SI",3)), 3 ),
                Add Ref Line( Num(Column(sub,"spec_max")[1]), "Dashed", "Medium Dark Red",
                    "MaxSpec "||Char(Format(Num(Column(sub,"spec_max")[1]),"Engineering SI",3)), 3 )
            } ),
            Dispatch( {}, "Variability Chart", FrameBox, {
                Marker Size(5),
                Row Legend( vt_corner, Color(1), Color Theme("JMP Default"),
                    Marker(0), Marker Theme(""), Continuous Scale(0),
                    Reverse Scale(0), Excluded Rows(0) )
            } )
        )
    );

    Return( vc );  /* REQUIRED: enables PPTX export pointer */
);
```

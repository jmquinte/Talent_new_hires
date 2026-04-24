---
name: jmp-csv-analysis
description: 'Analyze CSV data using JMP Pro. Use when: user provides CSV files and needs variability charts, data analysis, statistical plots, exported images (PNG/JPG), or PPTX reports. Use for: generating Variability Charts, Distribution, Oneway, control charts, stacking data, 3-sigma analysis, exporting results as images or PowerPoint, filtering outliers, generating HTML reports with chart interpretation. Triggers: CSV analysis, JMP chart, variability, plot data, generate report, silicon validation data, outlier removal, HTML report.'
argument-hint: 'Describe what analysis you need and provide the CSV file path'
---

# JMP CSV Data Analysis

Skill for loading CSV data into JMP Pro, generating analysis/charts (primarily Variability Charts), and exporting results as images (JPG/PNG) or PPTX reports. Runs headless via command line.

## Environment

- **JMP Pro 17**: `C:\Program Files\SAS\JMPPRO\17\jmp.exe`
- **Execution**: `& "C:\Program Files\SAS\JMPPRO\17\jmp.exe" script.jsl`
- **Workspace**: See [CONTEXT.md](../../../CONTEXT.md) for full repo context

## When to Use

- User provides a CSV file and asks for charts or analysis
- User needs Variability Charts (dynamic column selection, grouping)
- User needs data stacking, 3-sigma calculations, or spec limit overlays
- User needs results exported as JPG images or PPTX presentations
- User needs statistical summaries from silicon validation data

## Procedure

### Step 1: Understand the Request

Clarify with the user:
1. **CSV file path** — Where is the data?
2. **Analysis type** — What chart/analysis is needed?
   - `Variability Chart` (most common — Y, X grouping, By variables, legends)
   - `Distribution` / `Histogram`
   - `Oneway` / `Fit`
   - `Control Chart`
   - Custom JSL analysis
3. **Column mapping** — Which columns map to Y (response), X (grouping), By (panels)?
4. **Output** — Images (JPG/PNG), PPTX, or both?
5. **Output folder** — Where to save results?

### Step 2: Inspect the CSV

Before generating the script, read the first rows of the CSV to understand:
- Column names and data types
- Number of rows
- Potential grouping columns vs. numeric response columns

Use terminal: `Get-Content "path\to\file.csv" -First 10`

### Step 3: Generate the JSL Script

Create a temporary `.jsl` script following these patterns:

#### Base Template (headless, no GUI)
```jsl
//! Headless JMP Script — Auto-generated
Names Default To Here(1);

/* Open CSV */
dt = Open(
    "$CSVPATH$",
    Columns(
        /* Column definitions auto-detected from CSV header */
    ),
    Import Settings(
        End Of Line( CRLF ),
        End Of Field( Comma ),
        Column Names Start( 1 ),
        Data Starts( 2 ),
        Lines To Read( "All" )
    )
);

/* Analysis */
$ANALYSIS_BLOCK$

/* Export */
$EXPORT_BLOCK$

/* Cleanup */
Close All( Data Tables, No Save );
Close All( Reports, No Save );
```

#### Variability Chart Block
```jsl
vc = Variability Chart(
    Y( $Y_COLUMNS$ ),
    X( $X_COLUMNS$ ),
    By( $BY_COLUMNS$ ),
    Std Dev Chart( 0 ),
    SendToReport(
        Dispatch( {}, "2", ScaleBox, {
            Label Row( {Show Major Grid(1), Show Minor Grid(1)} )
        }),
        Dispatch( {}, "Variability Chart", FrameBox, {
            Row Legend(
                $LEGEND_COLUMN$,
                Color(1),
                Color Theme("JMP Default"),
                Marker(0)
            )
        })
    )
);
```

#### Variability Chart with Spec Limits
```jsl
/* Add reference lines for min/max spec */
Dispatch( {}, "2", ScaleBox, {
    Add Ref Line( $MIN_SPEC$, Dotted, "Medium Dark Red", "MinSpec", 3 ),
    Add Ref Line( $MAX_SPEC$, Dotted, "Medium Dark Red", "MaxSpec", 3 )
})
```

#### 3-Sigma Mode (Stack Mean ± 3*StdDev)
```jsl
dt:Mean << Data Type(Numeric) << Format("Best", 12) << Modeling Type(Continuous);
dt:StdDev << Data Type(Numeric) << Format("Best", 12) << Modeling Type(Continuous);
dt << New Column("MinimumSTD", Formula(:Mean - (:StdDev * 3)));
dt << New Column("MaximumSTD", Formula(:Mean + (:StdDev * 3)));
stkTable = dt << Stack(
    Columns(:MinimumSTD, :Mean, :MaximumSTD),
    Source Label Column("Label"),
    Stacked Data Column("Data")
);
stkTable << Set Name("Data Stacked");
```

#### Stack Mode (Multiple columns into one)
```jsl
stkTable = dt << Stack(
    Columns( $STACK_COLUMNS$ ),
    Source Label Column("Label"),
    Stacked Data Column("Data")
);
```

#### Outlier Removal (IQR × 1.5 Method)
Apply per-group before charting. This removes data points beyond Q1 - 1.5·IQR and Q3 + 1.5·IQR:
```jsl
/* Remove outliers using IQR method */
mean_col = Column( sub, "mean" );
vals = mean_col << Get Values;
q1 = Quantile( 0.25, vals );
q3 = Quantile( 0.75, vals );
iqr = q3 - q1;
lower_bound = q1 - 1.5 * iqr;
upper_bound = q3 + 1.5 * iqr;
sub << Select Where( :mean < lower_bound | :mean > upper_bound );
sub << Delete Rows;
sub << Clear Select;
```
**When to apply:** Always filter outliers per subset (e.g., per Measurement) rather than on the full dataset, so that each group's distribution is respected.

#### Export as Images
```jsl
/* Save each report frame as JPG */
output_path = "$OUTPUT_PATH$";
report = vc << Report;
pic_list = report << Get Pictures;
For(i = 1, i <= N Items(pic_list), i++,
    pic_list[i] << Save Picture(
        output_path || "chart_" || Char(i) || ".jpg",
        JPEG
    );
);
```

#### Export using Journal (alternative, more reliable)
```jsl
output_path = "$OUTPUT_PATH$";
jrnl = New Window("Export", << Journal);
vc << Journal;
jrnl << Save Picture(output_path || "variability_chart.jpg", JPEG);
Close(jrnl, No Save);
```

### Step 4: Execute the Script

Run JMP headless from terminal:
```powershell
& "C:\Program Files\SAS\JMPPRO\17\jmp.exe" "path\to\generated_script.jsl"
```

**Important notes:**
- JMP will open briefly even in script mode — it auto-closes when script ends if you add `Exit()` at the end
- Add `Exit();` as the last line for truly headless execution
- Check output folder for generated images after execution

### Step 5: Verify and Deliver

1. Check that output files were created: `Get-ChildItem "$OUTPUT_PATH$"`
2. Report file names and sizes to the user
3. If PPTX was requested, verify the .pptx file was generated

### Step 6: Generate HTML Report (Optional but Recommended)

After exporting chart images, generate an HTML report that embeds the images with interpretation. This provides a self-contained, shareable document.

**HTML Report Structure:**
1. **Header** — Platform, interface, date, test conditions
2. **Navigation bar** — Sticky nav with links to each measurement
3. **How to Read section** — Explains axes, dots, colors, VT corner legend
4. **Signal reference table** — What each signal is (Clock, TXIO0–3, ChipSelect, etc.)
5. **Measurement cards** organized by category:
   - Clock Timing (Period, DutyCycle, HighTime, LowTime, t180a)
   - Edge Rate (tR, tF)
   - Setup & Hold (SetupTime, HoldTime, SetupR/F, HoldR/F)
   - Voltage / Signal Quality (Vmax, Vmin, Overshoot, Undershoot)
6. **Each card contains:**
   - Measurement name + badge (Timing/Voltage/Quality)
   - "What it measures" — plain-language description
   - "Why it matters" — engineering significance
   - Embedded chart image (`<img src="charts/Variability_NAME.jpg">`)
   - "What to look for" — interpretation guidance (worst-case corners, thresholds, red flags)
7. **Footer** — Source file, tool version, outlier method used

**Key principles:**
- Images use relative paths (`charts/filename.jpg`) so the HTML is portable alongside the charts folder
- Style with Intel blue theme (`#0071c5`, `#00285a`)
- Cards are collapsible-friendly (use `<div class="card">` pattern)
- Include VT corner color legend matching JMP's color theme
- Adapt measurement descriptions to the specific interface being tested (SPI, I2C, etc.)
- Open in browser after creation: `Start-Process "path\to\report.html"`

## Script Patterns from This Repo

Reference existing scripts in [Autoreporting/Main/scripts/](../../../Autoreporting/Autoreporting/Main/scripts/):

| Script | Purpose |
|--------|---------|
| `CharVariabilityDinamyc` | Dynamic variability chart with modes: Normal, Stack, 3Sigma |
| `charVariability_WBIO_SIV_3Sigma` | Variability chart with ±3σ and spec limits |
| `save_as_image` | Export report frames as JPG |
| `save_as_pptx` | Export as PPTX via VBS + XML template |
| `EQMAP` | EQ Map analysis (MinEH, AsymEH, MinEW, AsymEW) |
| `Variability_EH` / `Variability_EW` | Eye Height/Width variability |

## Column Type Conversion

JMP may import CSV columns as character. Force numeric when needed:
```jsl
Column(dt, "colname") << Data Type(Numeric, Format(Best, 12)) << Modeling Type(Continuous);
```

## Error Handling

- If JMP fails silently, check `%TEMP%\jmp.log` or JMP log window
- If CSV columns have special characters, quote them: `Column(dt, "My Column Name")`
- If images are blank, ensure the report was fully rendered before saving

## Anti-patterns

- Do NOT use `Current Data Table()` in headless mode — always reference `dt` explicitly
- Do NOT forget `Exit();` at the end — JMP will stay open
- Do NOT hardcode column names — inspect CSV first and parameterize

# Adding a New Interface to Autoreporting

Follow this checklist when a user asks to create validation for an interface other than THC_SPI (e.g., I2C, USB SBU, PCIe CLKREQ, GPIO, etc.).

---

## Step 1 — Understand the interface

Before creating any files, ask the user (or read from the CSV):

| Question | Where to find it |
|----------|-----------------|
| What is the `interface_name` value in the CSV? | Column `interface_name` |
| What `Signal` values exist? | `SELECT DISTINCT Signal` mentally or `Column(dt,"Signal") << GetValues` |
| What `Measurement` values per Signal? | Column `Measurement` |
| What are the filter values? (`discipline`, `mode`, `data_rate`) | Same columns in CSV |
| What product/platform is this for? | `product_name`, `pch_stepping` |

**Naming convention:**
- Script folder: `charVariability_<IFACE>_<SignalGroup>` — e.g., `charVariability_I2C_SDA`, `charVariability_USB_SBU`
- Profile folder: `<PRODUCT>-<IFACE>` — e.g., `NVL-I2C`, `MTL-USB`

---

## Step 2 — Create one script per signal group

**File:** `Autoreporting/Autoreporting/Main/scripts/charVariability_<IFACE>_<SignalGroup>/Script.jsl`

Replace the placeholders:
- `<SIGNAL_FILTER_EXPR>` — JMP expression to match rows, e.g.:
  - Exact match: `:Signal == "SDA"`
  - Prefix match: `Contains( Char(:Signal), "IO" ) > 0`
- `<SUBSET_NAME>` — short descriptive name for the subset table
- `<IFACE>_<SignalGroup>` — for the Throw error message

```jsl
script = Function( { dt, pntr },
    { Default Local },

    CM:col_to_num( dt, "mean"     );
    CM:col_to_num( dt, "spec_min" );
    CM:col_to_num( dt, "spec_max" );

    dt << Select Where( <SIGNAL_FILTER_EXPR> );
    sub = dt << Subset(
        Output Table( "<SUBSET_NAME>" ),
        Selected Rows( 1 ),
        Invisible
    );
    dt << Clear Select;

    If( N Rows( sub ) == 0,
        Throw( "[charVariability_<IFACE>_<SignalGroup>] No rows found — check Signal filter" )
    );

    vc = sub << Variability Chart(
        Y( :mean ),
        X( :pch_vid, :vt_corner ),
        Std Dev Chart( 0 ),
        By( :Signal, :Measurement ),
        SendToReport(
            Dispatch( {}, "2", ScaleBox, {
                Label Row( { Show Major Grid(1), Show Minor Grid(1) } ),
                Add Ref Line(
                    Num( Column( sub, "spec_min" )[1] ),
                    "Dashed", "Medium Dark Red",
                    "MinSpec " || Char( Format( Num( Column(sub,"spec_min")[1] ), "Engineering SI", 3 ) ),
                    3
                ),
                Add Ref Line(
                    Num( Column( sub, "spec_max" )[1] ),
                    "Dashed", "Medium Dark Red",
                    "MaxSpec " || Char( Format( Num( Column(sub,"spec_max")[1] ), "Engineering SI", 3 ) ),
                    3
                )
            } ),
            Dispatch( {}, "Variability Chart", FrameBox, {
                Marker Size( 5 ),
                Row Legend(
                    vt_corner,
                    Color( 1 ), Color Theme( "JMP Default" ),
                    Marker( 0 ), Marker Theme( "" ),
                    Continuous Scale( 0 ), Reverse Scale( 0 ), Excluded Rows( 0 )
                )
            } )
        )
    );

    Return( vc );
);
```

**Critical:** `Return( vc )` must be present — the orchestrator uses this pointer for PPTX export. Scripts that return `0` or nothing are treated as utility steps (like `save_as_pptx`).

---

## Step 3 — Create Description.txt for each script

**File:** `Autoreporting/Autoreporting/Main/scripts/charVariability_<IFACE>_<SignalGroup>/Description.txt`

```
Variability chart for <IFACE> <SignalGroup> measurements (<PRODUCT> / SIV).

Signals covered : <comma-separated Signal values>
Measurements    : <comma-separated Measurement values>

Data columns used from CSV:
  Y-axis  -> :mean  (converted to numeric)
  X-axis  -> :pch_vid, :vt_corner
  By      -> :Signal, :Measurement
  Limits  -> :spec_min / :spec_max (read dynamically per measurement group)

Requirements:
  - CSV must contain: Signal, Measurement, pch_vid, vt_corner, mean, spec_min, spec_max
  - Script auto-filters by Signal.
```

---

## Step 4 — Create the profile

**File:** `Autoreporting/Autoreporting/Main/profiles/<PRODUCT>-<IFACE>/profile.json`

```json
{
    "OBJECT": {
        "DSN": "Local",
        "Obj": "",
        "Schema": "",
        "Type": "Local"
    },
    "PREFILTERS": {
        "Date": [],
        "Filter": null,
        "Interfaces": ["<IFACE>"]
    },
    "FILTERS": {
        "1": {"interface_name": ["<IFACE>"]},
        "2": {"discipline":     ["SIV"]},
        "3": {"mode":           ["<MODE>"]},
        "4": {"data_rate":      ["<DATA_RATE>"]}
    },
    "SCRIPTS": [
        "charVariability_<IFACE>_<SignalGroup1>",
        "charVariability_<IFACE>_<SignalGroup2>",
        "save_as_pptx"
    ]
}
```

Rules:
- `FILTERS` keys MUST be sequential strings: `"1"`, `"2"`, `"3"`, `"4"`
- Only include filter keys that exist as columns in the CSV
- `SCRIPTS` list defines execution order
- `save_as_pptx` should always be last if PPTX export is desired

---

## Step 5 — Create the automated main script (optional but recommended)

**File:** `Autoreporting/Autoreporting/Main/main_<IFACE>.jsl`

Copy `main_THC_SPI.jsl` and replace:
1. All occurrences of `"THC_SPI"` → `"<IFACE>"`
2. The `filters` associative array — match the new interface's filter columns and values
3. The `analysis_scripts` list — use the new script folder names
4. The output folder name: `"THC_SPI_Report_"` → `"<IFACE>_Report_"`
5. The slide title string

---

## Step 6 — Validate

Run through this checklist before delivering:

- [ ] Each `Script.jsl` has `Return( vc )` as last line
- [ ] `spec_min`/`spec_max` are read via `Column(sub,"spec_min")[1]` — NOT hardcoded
- [ ] `N Rows( sub ) == 0` guard is present in every script
- [ ] Profile `FILTERS` keys are `"1"`, `"2"`, `"3"` (strings, not integers)
- [ ] Profile `SCRIPTS` list matches the exact folder names created in `scripts/`
- [ ] `Description.txt` exists in every script folder (required for GUI preview)
- [ ] `main_<IFACE>.jsl` lives in `Main/` folder (so `$MAIN_PATH` resolves correctly)

---

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| `Return( 0 )` instead of `Return( vc )` | Chart not exported to PPTX | Change to `Return( vc )` |
| Hardcoded spec values | Wrong limits when CSV changes | Use `Column(sub,"spec_min")[1]` |
| Script in wrong folder | Not visible in GUI dropdown | Must be direct child of `scripts/` |
| Profile FILTERS key as integer | Profile load silently skips filters | Keys must be strings: `"1"`, not `1` |
| `main_<IFACE>.jsl` outside `Main/` | `$MAIN_PATH` resolves to wrong dir | File must be in same folder as `main.jsl` |
| Missing `CM:col_to_num` call | `spec_min`/`spec_max` stay as Character | Call `CM:col_to_num` for all 3 columns |

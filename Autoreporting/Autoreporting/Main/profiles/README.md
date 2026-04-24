# Profiles

Each subfolder is a saved analysis configuration that can be loaded from the GUI
(`main.jsl` → Profiles panel → Load) or used automatically by a dedicated launcher.

## Profile JSON Structure

```json
{
    "OBJECT":     { "DSN": "Local", "Obj": "", "Schema": "", "Type": "Local" },
    "PREFILTERS": { "Date": [], "Filter": null, "Interfaces": ["<IFACE>"] },
    "FILTERS": {
        "1": {"<column>": ["<value>"]},
        "2": {"<column>": ["<value>"]}
    },
    "SCRIPTS": [
        "<script_folder_name_1>",
        "<script_folder_name_2>",
        "save_as_pptx"
    ]
}
```

- `FILTERS` keys **must be sequential strings**: `"1"`, `"2"`, `"3"` …
- `SCRIPTS` list defines execution order; each entry must match a folder name in `../scripts/`
- Use `"DSN": "Local"` and `"Type": "Local"` for CSV-based workflows

## Available Profiles

| Profile folder | Interface | Product | Filters applied |
|----------------|-----------|---------|----------------|
| `NVL-THC_SPI`  | THC_SPI   | Nova Lake Hx (A0) | interface_name, discipline=SIV, mode=Quad, data_rate=Single |
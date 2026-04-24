# Repo Github Copilot - Workspace Context

## Overview
Intel Data Analysis repository. Contains tools for semiconductor validation data analysis, automated reporting, and hardware register testing (THC/SPI).

## Main Projects

### 1. Autoreporting (JMP/JSL - JMP Scripting Language)
**Purpose:** GUI-based tool for querying databases, filtering data, running analysis scripts, and generating reports for silicon validation data.

**Architecture:** Modular MVC-like pattern with Namespaces:
- **main.jsl** — Entry point for CCDS (CloudCDS) DB mode. Creates "Autoreporting-GUI" window with sections: DB, Search, Filters, Scripts, Profile.
- **main_UDM.jsl** — Entry point for UDM (Unified Data Management) mode. Similar GUI but uses Python-based UDM puller instead of ODBC.
- **Namespace pattern:** Each section has its own Namespace (DB, SE, FL, SC, PR) with `_class.jsl` (UI components), `_methods.jsl` (logic/callbacks), `_helpers.jsl` (utilities).

**Key Sections:**
- **DB (Section_DB):** Database connection via ODBC DSN (cloudcds, cloudcds_ts, cloudcds_dev) or local file import.
- **UDM_DB (Section_UDM_DB):** UDM-based data pulling with filters (Lab, Team, Project, TestId, PlatformName, etc.). Uses Python helper.
- **SE (Section_Search):** Search by date range, interface, result objects (Views/Procedures/Tables).
- **FL (Section_Filters):** Dynamic column-based data filtering UI.
- **SC (Section_Scripts):** Script orchestrator — select, add, and run analysis scripts sequentially on loaded data.
- **PR (Section_Profile):** Save/load configuration profiles.

**Config (config.json):** DSN list, UDM configs (labs: VL/GM, teams: SIO/WBIO, projects: MTL/PTL_H), object types, prefilter keys.

**Common (common.jsl):** Utility functions — Python script import, data stacking, valid data filtering, threshold prompts, column type conversion, XML/PPTX slide generation.

**Scripts folder:** Analysis scripts (each has Script.jsl + Description.txt):
- charVariability_WBIO_SIV_3Sigma — Variability charts with ±3σ limits
- EQMAP — EQ Map analysis (MinEH, AsymEH, MinEW, AsymEW)
- DTR_EH, DTR_EW — Design Target Reports
- Variability_EH/EW — Eye Height/Width variability
- save_as_csv/image/pptx — Export utilities
- StackAndGetSkew — Data stacking and skew analysis

**UDM Python helper (udm_puller_helper.py):** CParamType class for typed filter parameters. FILTERDICT defines all possible filters with types (str, int, date, bool, list). getOptionsDict() converts JSL params to Python dict.

### 2. THC_SPI (Python - Post-Silicon HW Validation)
**Purpose:** THC (Touch Host Controller) SPI register read/write for post-silicon validation.
- **PIO_ReadWrite_PostSi_THC0.py:** Uses Intel `namednodes`/`sv` for register access. Functions: Init_DataRegisters, pollSTSAndPrint, PIO_Read, PIO_Write. Supports Single/Dual/Quad/QuadParallel modes. SPI frequencies: 42/30/24/20/17 MHz.
- **GPIO_Config_SPI_1.json:** Oscilloscope/signal analyzer config for eSPI clock/data channels. Measurement thresholds, trigger settings, sample rates.
- Results folders contain JMP data tables (.jmp), CSV files, and variability chart reports (.jrp).
- **Results2/variability_chart.jsl** — Headless JSL script that generates per-measurement variability charts with IQR×1.5 outlier filtering.
- **Results2/charts/** — 17 exported JPG variability charts (one per measurement: Period, DutyCycle, tR, tF, SetupTime, HoldTime, Vmax, Vmin, Overshoot, Undershoot, etc.).
- **Results2/report.html** — Interactive HTML report with chart interpretation, signal reference table, and VT corner legend.

### 3. UtilitiesTools
- **ResultTable_Editer.jsl:** GUI tool to update isValid and Comment columns in database records. Uses EV_User environment variable for access control.

### 4. Talent_new_hires
- Empty project (only .git folder).

## Tech Stack
- **JMP/JSL** (JMP Scripting Language) — primary language for data analysis GUI
- **Python** — UDM data pulling, hardware register access
- **ODBC/SQL** — database connectivity (CloudCDS)
- **JSON** — configuration files
- **Intel internal tools:** namednodes, sv (silicon validation), UDM API

## Key Patterns
- Namespace-based modularity in JSL (DB, SE, FL, SC, PR, CM)
- Class/Methods/Helpers separation per section
- Scripts are pluggable functions with signature `Function({dt, pntr}, ...)`
- Config-driven (config.json for DSN, labs, teams, projects)
- Python-JSL interop via PythonInit/PythonSend/PythonSubmit

## Skills
- **jmp-csv-analysis** (`.github/skills/jmp-csv-analysis/SKILL.md`) — Copilot skill for analyzing CSV data with JMP Pro. Covers: CSV inspection, JSL script generation, variability charts, 3-sigma, outlier removal (IQR×1.5), image export (JPG), and HTML report generation with chart interpretation.

## Environment
- **JMP Pro 17** — `C:\Program Files\SAS\JMPPRO\17\jmp.exe`
- **JMP Pro 14** — `C:\Program Files\SAS\JMPPRO\14\` (legacy)
- Para ejecutar scripts JSL desde terminal: `& "C:\Program Files\SAS\JMPPRO\17\jmp.exe" script.jsl`

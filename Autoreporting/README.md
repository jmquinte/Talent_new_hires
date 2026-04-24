# Autoreporting — Electrical Validation Data Analysis

JMP-based semi-automatic tool for electrical validation of Intel SPI/IO interfaces.
Given a WBIO CSV from the measurement database (CloudCDS / UDM), it produces
Variability Charts with spec limits and exports a dated PPTX report.

## Quick Start

| Mode | Entry point | Interaction required |
|------|-------------|----------------------|
| Fully automatic | `Autoreporting/Main/main_THC_SPI.jsl` | Select CSV once |
| Interactive GUI | `Autoreporting/Main/main.jsl` | Select data, filters, scripts, then Run |

## Supported Interfaces

| Interface | Product | Entry point | Profile |
|-----------|---------|-------------|--------|
| THC_SPI (42 MHz Quad) | Nova Lake Hx (NVL-Hx) | `main_THC_SPI.jsl` | `NVL-THC_SPI` |

## Repository Structure

```
Autoreporting/
├── README.md                        ← this file
└── Autoreporting/
    ├── Main/
    │   ├── main.jsl                 ← Interactive GUI launcher
    │   ├── main_THC_SPI.jsl         ← Automated THC_SPI launcher (1-click)
    │   ├── common/                  ← Shared utilities (CM namespace)
    │   ├── components/              ← GUI section classes
    │   ├── config/config.json       ← Tool-wide settings
    │   ├── helpers/                 ← Section helper functions
    │   ├── methods/                 ← Section method functions
    │   ├── profiles/                ← Saved analysis configurations
    │   └── scripts/                 ← Analysis script library
    └── UtilitiesTools/
```

## How It Works

1. **Load data** — CSV from WBIO/CloudCDS or direct DB connection via ODBC
2. **Apply filters** — select column/value pairs to subset the data
3. **Run scripts** — each script in the queue receives the filtered table and returns a chart pointer
4. **Export** — `save_as_pptx` captures all chart images and assembles the PPTX via VBScript

## Adding a New Interface

See `.github/skills/thc-spi-validation/references/new-interface-template.md` for the
step-by-step checklist to add validation for any new SIV interface.
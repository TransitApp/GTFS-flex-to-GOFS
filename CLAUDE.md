# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python tool that converts GTFS-Flex (General Transit Feed Specification - Flexible services) data to the GOFS-lite (General On-demand Feed Specification - lite) format. It processes on-demand/flexible transit services data and outputs standardized GOFS files.

## Core Architecture

The conversion process follows this flow:
1. Load GTFS data using `gtfs_loader` 
2. Extract relevant data through `operation_rules.py` which analyzes trip types and creates `GofsData`
3. Generate individual GOFS files via modules in `gtfs_flex_to_gofs_lite/files/`
4. Output structured GOFS-lite format files

### Key Components

- **`gofs_lite_converter.py`**: Main conversion orchestrator that coordinates all file generation
- **`gofs_data.py`**: Contains `GofsData` class that tracks extracted IDs and transfers from GTFS-Flex
- **`files/operation_rules.py`**: Core logic for classifying trip types (regular_service, deviated_service, pure_microtransit, other) and extracting zone-to-zone transfers
- **`files/` directory**: Individual modules for generating each GOFS file type (zones, calendars, fares, etc.)
- **`gofs_file.py`**: Base class for GOFS file objects with save functionality

### Trip Classification Logic

The system classifies GTFS trips into four types:
- `PURE_MICROTRANSIT`: Flexible zone-to-zone services
- `DEVIATED_SERVICE`: Routes with some flexible elements  
- `REGULAR_SERVICE`: Fixed route services
- `OTHER`: Unclassified trips

Only `PURE_MICROTRANSIT` trips are converted to GOFS format.

## Development Commands

### Installation
```bash
uv sync
```

### Running Tests
```bash
python -m pytest .
```

### Running the Tool
```bash
python -m gtfs_flex_to_gofs_lite --gtfs-dir <input_dir> --gofs-lite-dir <output_dir> --url <base_url>
```

### Test Regeneration
```bash
./createTests.sh
```

This script regenerates expected test outputs for all test cases.

### Single Test Execution
```bash
python -m pytest tests/test_runner.py::test_default[test_simple_conversion]
```

Replace `test_simple_conversion` with any test case name from the `tests/` directory.

## Dependencies

- `py-gtfs-loader`: Custom GTFS loading library from TransitApp
- `shapely>=2.0.4`: Geometric operations
- `pytest`: Testing framework

## File Structure Notes

- Test cases are in `tests/test_*/` with `input/` and `expected_default/` subdirectories
- The `locations.geojson` file in GTFS input is required for conversion - without it, conversion is skipped
- GOFS files are generated with specific headers including TTL, version, and timestamps
- Split-by-route functionality creates separate GOFS folders per route when enabled
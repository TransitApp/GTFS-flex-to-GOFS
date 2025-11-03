# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python tool that converts GTFS-Flex (General Transit Feed Specification - Flexible services) data to the GOFS (General On-demand Feed Specification) format. It processes on-demand/flexible transit services data and outputs standardized GOFS files.

## Core Architecture

The conversion process follows this flow:
1. Load GTFS data using `gtfs_loader`
2. Extract relevant data through `operation_rules.py` which analyzes trip types and creates `GofsData`
3. Generate individual GOFS files via modules in `gtfs_flex_to_gofs/files/`
4. Output structured GOFS format files

### Key Components

- **`gofs_converter.py`**: Main conversion orchestrator that coordinates all file generation
- **`gofs_data.py`**: Contains `GofsData` class that tracks extracted IDs and transfers from GTFS-Flex
- **`files/operation_rules.py`**: Core logic for classifying trip types (regular_service, deviated_service, pure_microtransit, other) and extracting zone-to-zone transfers
- **`files/` directory**: Individual modules for generating each GOFS file type (zones, calendars, fares, etc.)
- **`gofs_file.py`**: Base class for GOFS file objects with save functionality

### Trip Classification Logic

The system classifies GTFS trips into four types based on stop time patterns in `operation_rules.py:get_type_of_trip()`:
- `PURE_MICROTRANSIT`: All stop times are flexible zones (have pickup/dropoff windows)
- `DEVIATED_SERVICE`: Mix of regular stops and flexible zones (3+ stop times required)
- `REGULAR_SERVICE`: All stop times are regular fixed stops
- `OTHER`: Invalid or unclassifiable trips (e.g., <2 stops)

Only `PURE_MICROTRANSIT` trips are converted to GOFS format.

### Conversion Workflow

1. **Trip Analysis** (`operation_rules.py:create()`):
   - Iterates through all GTFS trips and their stop times
   - Classifies each trip using `get_type_of_trip()`
   - For `PURE_MICROTRANSIT` trips, extracts zone-to-zone transfers
   - Populates `GofsData` with extracted IDs (routes, calendars, zones, booking rules)

2. **File Generation** (`gofs_converter.py:convert_to_gofs()`):
   - Creates individual GOFS files using `GofsData` to filter relevant GTFS entities
   - Files generated in order: operation_rules, zones, system_information, service_brands, vehicle_types, calendars, fares, wait_times, wait_time, booking_rules, gofs_versions, gofs
   - Each file module has a `create()` function that returns a `GofsFile` object

3. **Output** (`gofs_converter.py:save_files()`):
   - Single folder mode: All GOFS files in one directory
   - Split-by-route mode: Creates one folder per route_id, with filtered operation_rules per folder

## Development Commands

### Installation
```bash
uv sync --extra dev
```

### Running Tests
```bash
python -m pytest .                    # All tests
python -m pytest tests/ -v            # Verbose output
```

### Running the Tool
```bash
python -m gtfs_flex_to_gofs --gtfs-dir <input_dir> --gofs-dir <output_dir> --url <base_url>

# With optional parameters:
--ttl <seconds>              # Time-to-live for GOFS files (default: 86400)
--timestamp <unix_time>      # Fixed timestamp for deterministic output
--split-by-route             # Create separate GOFS folders per route
--out-gtfs-dir <dir>         # Output directory for patched GTFS
--no-warning                 # Silence warnings
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

### Linting
```bash
uv run flake8
```

### Deployment

Deployment to PyPI is automated via GitHub Actions when the version in `pyproject.toml` is updated on the `main` branch. See `.github/workflows/release.yml` for details.

## Dependencies

- `py-gtfs-loader`: Custom GTFS loading library from TransitApp
- `shapely>=2.0.4`: Geometric operations
- `pytest`: Testing framework

## Testing Structure

Test cases use a snapshot-based approach:
- Each test case lives in `tests/test_*/` directory
- `input/`: Contains GTFS files (including required `locations.geojson`)
- `expected_default/`: Contains expected GOFS output files
- `test_runner.py` uses pytest parametrization to automatically discover all test cases
- Tests compare generated output against expected files using `gtfs_loader.test_support`
- `createTests.sh` regenerates all expected output files (run after intentional changes)

### Important Testing Notes

- Tests use `timestamp=0` for deterministic output
- The `locations.geojson` file in GTFS input is required for conversion - without it, conversion is skipped
- Test isolation: each test gets its own work directory created by `test_support.create_test_data()`
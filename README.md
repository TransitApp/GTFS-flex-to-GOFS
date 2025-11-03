# GTFS-flex-to-GOFS-lite

[![Build Status](https://github.com/TransitApp/GTFS-flex-to-GOFS-lite/actions/workflows/pull-request.yml/badge.svg)](https://github.com/TransitApp/GTFS-flex-to-GOFS-lite/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A Python tool to convert [GTFS-Flex](https://github.com/MobilityData/gtfs-flex) (General Transit Feed Specification - Flexible services) data to the [GOFS-lite](https://github.com/NABSA/micromobility/blob/main/general-on-demand-feed-specification.md) (General On-demand Feed Specification - lite) format.

This tool processes on-demand and flexible transit services data from GTFS-Flex feeds and outputs standardized GOFS-lite files for consumption by trip planning applications and mobility platforms.

## Installation

Install from PyPI:
```bash
pip install GTFS-flex-to-GOFS-lite
```

Or install from source:
```bash
git clone https://github.com/TransitApp/GTFS-flex-to-GOFS-lite.git
cd GTFS-flex-to-GOFS-lite
uv sync --extra dev
```

## Usage

```bash
gtfs-flex-to-gofs-lite --gtfs-dir <input_dir> --gofs-lite-dir <output_dir> --url <base_url>
```

### Command Line Options

```
optional arguments:
  -h, --help           show this help message and exit
  --gtfs-dir Dir       input gtfs directory
  --gofs-lite-dir Dir  output gofs directory
  --url URL            auto-discovery url. Base URL indicate for where each files will be uploaded (and downloadable)
  --ttl TTL            time to live of the generated gofs files in seconds (default: 86400)
  --no-warning         Silence warnings
```

## Development

### Running Tests

```bash
python -m pytest .
```

### Regenerating Test Fixtures

```bash
./createTests.sh
```

## Features

- Converts GTFS-Flex pure microtransit services to GOFS-lite format
- Supports zone-based on-demand transit operations
- Generates all required GOFS-lite files (zones, calendars, fares, booking rules, etc.)
- Optional split-by-route output for multi-service feeds
- Automated CI/CD with GitHub Actions

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Related Projects

- [GTFS-Flex Specification](https://github.com/MobilityData/gtfs-flex)
- [GOFS-lite Specification](https://github.com/NABSA/micromobility/blob/main/general-on-demand-feed-specification.md)
- [py-gtfs-loader](https://github.com/TransitApp/py-gtfs-loader)

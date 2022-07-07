Tool to convert GTFS-Flex data to the GOFS-lite format

### man
```
Convert GTFS-flex on-demand format to GOFS-lite

optional arguments:
  -h, --help           show this help message and exit
  --gtfs-dir Dir       input gtfs directory
  --gofs-lite-dir Dir  output gofs directory
  --url URL            auto-discovery url. Base URL indicate for where each files will be uploaded (and downloadable)
  --ttl TTL            time to live of the generated gofs files in seconds (default: 86400)
  --no-warning         Silence warnings
```
Tool to convert GTFS-Flex data to the GOFS-lite format

To install:
* `python -m pip install -e .`

To run test:
* `python -m pytest .`

You can use `createTests.sh` to regenerate the test.

To deploy a new version, run:
```
rm -r dist/
python setup.py sdist bdist_wheel
TWINE_USERNAME=transit TWINE_REPOSITORY_URL=https://pypi.transitapp.com:443 TWINE_PASSWORD=[PASSWORD] twine upload dist/*
```

The twine password can be found in 1Password under the same `PyPI password`. 

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

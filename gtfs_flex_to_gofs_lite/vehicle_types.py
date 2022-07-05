from copy import deepcopy

from .save_file import *
from .utils import GofsFile

FILENAME = 'vehicle_types.json'


def create_vehicle_types_file(gtfs, gofs_dir, default_headers_template):
    # Uncomment to support this file
    # file = deepcopy(default_headers_template)
    # save_file(gofs_dir / FILENAME, file)

    return GofsFile(FILENAME, False)

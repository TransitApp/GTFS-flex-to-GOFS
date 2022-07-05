from copy import deepcopy

from .utils import GofsFile
from .save_file import *

FILENAME = 'fares.json'


def create_fares_file(gtfs, gofs_dir, default_headers_template):
    # Uncomment to support this file
    # file = deepcopy(default_headers_template)
    # save_file(gofs_dir / FILENAME, file)

    return GofsFile(FILENAME, False)

from copy import deepcopy

from .save_file import *

FILENAME = 'wait_time.json'


def create_wait_time_file(gtfs, gofs_dir, default_headers_template):
    file = deepcopy(default_headers_template)

    save_file(gofs_dir / FILENAME, file)
    return FILENAME

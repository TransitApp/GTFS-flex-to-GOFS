from copy import deepcopy

from .default_headers import get_default_headers
from .save_file import *


def create_gofs_file(gtfs, gofs_dir, default_headers_template):
    file = deepcopy(default_headers_template)

    save_file(gofs_dir / "gofs.json", file)

from .default_headers import get_default_headers
from .save_file import *

def create_gofs_file(gtfs, gofs_dir):
    file = get_default_headers(gtfs)

    save_file(gofs_dir / "gofs.json", file)

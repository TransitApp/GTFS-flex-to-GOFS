from copy import deepcopy
import re

from .save_file import *
from .utils import concat_url

FILENAME = 'gofs.json'


def create_gofs_file(gtfs, gofs_dir, default_headers_template, base_url, created_files):
    if base_url is None:
        return None

    file = deepcopy(default_headers_template)

    agency = list(gtfs.agency.values())[0]
    lang = agency.agency_lang

    urls = []

    for created_file in created_files:
        urls.append(
            {
                'name': created_file,
                'url': concat_url(base_url, lang, created_file)
            }
        )

    file['data'][lang] = {}
    file['data'][lang]['feeds'] = urls

    save_file(gofs_dir / FILENAME, file)
    return FILENAME

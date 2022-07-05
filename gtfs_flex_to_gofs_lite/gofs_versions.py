from copy import deepcopy

from .save_file import *
from .utils import concat_url

FILENAME = 'gofs_versions.json'


def create_gofs_versions_file(gtfs, gofs_dir, default_headers_template, base_url):
    if base_url is None:
        return 
        
    file = deepcopy(default_headers_template)

    versions = []
    versions.append(
        {
            'version': file['version'],
            'url': concat_url(base_url, 'gofs')
        }
    )

    file['data']['versions'] = versions

    save_file(gofs_dir / FILENAME, file)
    return FILENAME

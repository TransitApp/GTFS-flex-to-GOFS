from copy import deepcopy

from .gofs_file import GofsFile
from .utils import concat_url

FILENAME = 'gofs_versions'


def create_gofs_versions_file(default_headers_template, base_url):
    if base_url is None:
        return GofsFile(FILENAME, False)

    versions = []
    versions.append(
        {
            'version': default_headers_template['version'],
            'url': concat_url(base_url, 'gofs')
        }
    )

    return GofsFile(FILENAME, True, versions)

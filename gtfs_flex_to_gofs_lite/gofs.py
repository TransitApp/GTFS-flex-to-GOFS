from dataclasses import dataclass
from typing import List

from .gofs_file import GofsFile
from .utils import concat_url

FILENAME = 'gofs'


@dataclass
class URL:
    name: str
    url: str


@dataclass
class URLS:
    urls: List[URL]


def create_gofs_file(gtfs, base_url, created_files):
    if base_url is None:
        return GofsFile(FILENAME, False)

    agency = list(gtfs.agency.values())[0]
    lang = agency.agency_lang
    urls = []

    for created_file in created_files:
        urls.append(URL(name=created_file.filename, url=concat_url(
            base_url, lang, created_file.filename)))

    data = {lang: urls}
    return GofsFile(FILENAME, created=True, data=URLS(urls))

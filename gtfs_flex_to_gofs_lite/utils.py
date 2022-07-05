import re


class GofsFile:
    def __init__(self, filename, created):
        self.filename = filename
        self.created = created


def concat_url(*args):
    url = '/'.join([*args])
    url = re.sub(r'(?<!:)//', r'/', url)
    return url

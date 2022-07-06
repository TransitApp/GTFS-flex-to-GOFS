import re

RED_STRING = '\033[91m{}\033[00m'
GREEN_STRING = '\033[92m{}\033[00m'
YELLOW_STRING = '\033[93m{}\033[00m'


def concat_url(*args):
    url = '/'.join([*args])
    url = re.sub(r'(?<!:)//', r'/', url)
    return url

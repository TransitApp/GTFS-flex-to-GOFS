import os
import re

__RED_STRING = '\033[91m{}\033[00m' if os.isatty(0) else '{}'
__GREEN_STRING = '\033[92m{}\033[00m' if os.isatty(0) else '{}'
__YELLOW_STRING = '\033[93m{}\033[00m' if os.isatty(0) else '{}'


def red_text(text):
    return __RED_STRING.format(text)


def green_text(text):
    return __GREEN_STRING.format(text)


def yellow_text(text):
    return __YELLOW_STRING.format(text)


def concat_url(*args):
    url = '/'.join([*args])
    url = re.sub(r'(?<!:)//', r'/', url)
    return url

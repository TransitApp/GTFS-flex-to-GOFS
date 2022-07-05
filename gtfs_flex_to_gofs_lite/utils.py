import re

def concat_url(*args):
        url = '/'.join([*args])
        url = re.sub(r'(?<!:)//', r'/', url)
        return url
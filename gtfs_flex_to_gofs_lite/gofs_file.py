import json

from .default_headers import get_default_headers


class GofsFile:
    def __init__(self, filename, created, data=None, nest_data_under_filename=True):
        self.filename = filename
        self.created = created
        self.data = data
        self.nest_data_under_filename = nest_data_under_filename

        self.extension = '.json'

    def get_filename_with_ext(self):
        return self.filename + self.extension

    def save(self, filepath, ttl, version, creation_timestamp):
        file = get_default_headers(ttl, version, creation_timestamp)
        if self.nest_data_under_filename:
            file['data'][self.filename] = self.data
        else:
            file['data'] = self.data

        full_filepath = filepath / (self.filename + self.extension)

        print('Saving {}'.format(full_filepath))
        with open(filepath / (self.filename + self.extension), 'w', encoding='utf-8') as f:
            f.write(json.dumps(file, indent=4, default=vars))

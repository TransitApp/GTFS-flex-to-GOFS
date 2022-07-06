import json
from copy import deepcopy


class GofsFile:
    def __init__(self, filename, created, data=None):
        self.filename = filename
        self.created = created
        self.data = data

        self.extension = '.json'

    def get_full_filename(self):
        return self.filename + self.extension

    def save(self, filepath, headers):
        file = deepcopy(headers)
        file['data'][self.filename] = self.data

        full_filepath = filepath / (self.filename + self.extension)

        print('Saving {}'.format(full_filepath))
        with open(filepath / (self.filename + self.extension), 'w', encoding='utf-8') as f:
            f.write(json.dumps(file, indent=4, default=vars))

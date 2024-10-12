import json

class config():
    def __init__(self, path):
        buffer = self.import_from_file(path)
        self.path_tesseract = buffer['path_tesseract']
        self.language_mode = buffer['lang_tesseract']

    def import_from_file(self, path):
        with open(path, 'r', encoding='utf8') as config_file:
            config = json.load(config_file)
        return config
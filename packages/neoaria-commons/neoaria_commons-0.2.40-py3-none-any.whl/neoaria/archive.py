import zipfile, os

class Zip(object):
    
    def __init__(self, path):
        self.path = path
        self.zip = zipfile.ZipFile(path, 'w')

    def add(self, path):
        self.zip.write(path, os.path.basename(path))

    def close(self):
        self.zip.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    @staticmethod
    def extract(path, dest):
        with zipfile.ZipFile(path, 'r') as z:
            z.extractall(dest)

    @staticmethod
    def list(path):
        with zipfile.ZipFile(path, 'r') as z:
            return z.namelist()
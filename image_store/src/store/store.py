import os
import uuid


class StoreBase(object):
    def __init__(self, root):
        assert root.endswith('/')
        self.root = root

    def _gen_path(self, ext):
        file_name = str(uuid.uuid4())
        return self.root + file_name + f'.{ext}'


class FileSystemStore(StoreBase):
    def __init__(self, root):
        super().__init__(root)
        if not os.path.exists(self.root):
            os.makedirs(self.root)

    def new(self, data, ext):
        path = self._gen_path(ext)
        with open(path, 'wb') as f:
            f.write(data)

        return path

    def read(self, path):
        try:
            with open(path, 'rb') as f:
                return f.read()
        except:
            return None


class MemoryStore(StoreBase):
    def __init__(self, root):
        super().__init__(root)
        self.data = {}

    def new(self, data, ext):
        path = self._gen_path(ext)
        self.data[path] = data

    def read(self, path):
        return self.data[path]

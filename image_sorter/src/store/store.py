import requests

class RemoteImageResolver(object):
    def __init__(self, domain, port):
        self.url = f'http://{domain}:{port}'

    def get_img_data_by_id(self, id):
        r = requests.get(f'{self.url}/images/{id}')
        if r.status_code == 200:
            return r.content
        return None



class MemoryStore(object):
    def __init__(self, root):
        self.data = {}

    def add_img(self, id, data):
        self.data[id] = data

    def get_img_data_by_id(self, id):
        if id in self.data:
            return self.data[id]
        return None

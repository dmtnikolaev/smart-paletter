import io
import requests

from flask import Blueprint, request, current_app, send_file
from flask_restx import Api, Resource

gateway_blueprint = Blueprint('gateway', __name__)
api = Api(gateway_blueprint)

def config():
    return current_app.config

class Store(Resource):
    def get(self):
        r = requests.get(config()['IMAGE_STORE_URL'] + 'images')
        if r.status_code >= 500:
            return {
                'message': f'Internal image_store service error \
                    (code={r.status_code})'
            }
        return r.json(), r.status_code

    def post(self):
        mimetype = request.mimetype
        headers = {
                'Content-Type': mimetype
        }
        data = request.get_data()
        r = requests.post(config()['IMAGE_STORE_URL'] + 'images', headers=headers,
                          data=data)
        if r.status_code >= 500:
            return {
                'message': f'Internal image_store service error \
                    (code={r.status_code})'
            }
        return r.json(), r.status_code


class StoreDownload(Resource):
    def get(self, img_id):
        r = requests.get(config()['IMAGE_STORE_URL'] + f'images/{img_id}')
        if r.status_code >= 500:
            return {
                'message': f'Internal image_store service error \
                    (code={r.status_code})'
            }

        if r.status_code != 200:
            return r.json(), r.status_code

        return send_file(
            io.BytesIO(r.content),
            mimetype=request.mimetype,
            download_name=r.headers['Content-Disposition'].split('filename="')[-1][:-1],
            as_attachment=True)



class StoreDelete(Resource):
    def delete(self, img_id):
        r = requests.delete(config()['IMAGE_STORE_URL'] + f'images/{img_id}')
        if r.status_code >= 500:
            return {
                'message': f'Internal image_store service error \
                    (code={r.status_code})'
            }
        return r.json(), r.status_code


class Sort(Resource):
    def post(self):
        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.post(config()['IMAGE_SORTER_URL'] + 'sort',
                          data=request.get_data(), headers=headers)
        if r.status_code >= 500:
            return {
                'message': f'Internal image_sorter service error \
                    (code={r.status_code})'
            }
        return r.json(), r.status_code


api.add_resource(Store, '/image')
api.add_resource(StoreDownload, '/image/<int:img_id>')
api.add_resource(StoreDelete, '/image/<int:img_id>')
api.add_resource(Sort, '/image/sort')

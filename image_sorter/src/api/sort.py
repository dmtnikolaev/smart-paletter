from flask import Blueprint, request, send_file
from flask_restx import Api, Resource, fields

from src import dependencies as deps
from src.api.models import Image
from src.sorter import sort_images

sort_blueprint = Blueprint('sort', __name__)
api = Api(sort_blueprint)

image = api.model('Image', {
    'id': fields.Integer(readOnly=True),
    'data': fields.String(readOnly=True),
})


class Sort(Resource):
    def post(self):
        ids = request.get_json()
        imgs = self._download_all(ids)
        none_img_ids = \
            list(map(
                lambda x: x.id, filter(lambda x: x.data is None, imgs)))
        if len(none_img_ids) > 0:
            return {'message': f'Images with id={none_img_ids} does not exists'}, 404

        imgs = sort_images(imgs)

        res = []
        for i in imgs:
            res.append(i.id)
        return res, 200

    def _download_all(self, ids):
        imgs = []
        for id in ids:
            data = deps.img_store.get_img_data_by_id(id)
            imgs.append(Image(id, data))
        return imgs


api.add_resource(Sort, '/sort')

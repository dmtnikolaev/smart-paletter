from flask import Blueprint, request, send_file
from flask_restx import Api, Resource, fields

from src import dependencies as deps
from src.api.models import Image


images_blueprint = Blueprint('images', __name__)
api = Api(images_blueprint)

image = api.model('Image', {
    'id': fields.Integer(readOnly=True),
    'path': fields.String(readOnly=True),
    'uploaded_date': fields.DateTime,
})


class Images(Resource):
    def post(self):
        res = {}

        mimetype = request.mimetype
        extension = self._get_ext_from_mimetype(mimetype)
        if extension is None:
            res['message'] = f'Unsupported mimetype "{mimetype}"'
            return res, 400

        path = deps.img_store.new(request.get_data(), extension)
        img = Image(path=path)
        deps.db.session.add(img)
        deps.db.session.commit()

        return img.id, 201

    @api.marshal_with(image, as_list=True)
    def get(self):
        return Image.query.all(), 200

    def _get_ext_from_mimetype(self, mt):
        if not mt.startswith('image/'):
            return None
        return mt.split('/')[-1]


class ImagesDownload(Resource):
    def get(self, img_id):
        print(f'Download {img_id}')
        img = Image.query.filter_by(id=img_id).first()
        if not img:
            print(f'Image id={img_id} was not found')
            return {'message': 'Image id={img_id} was not found'}, 404

        extension = img.path.split('.')[-1]

        return send_file(img.path, as_attachment=True)


class ImagesDelete(Resource):
    def delete(self, img_id):
        Image.query.filter_by(id=img_id).delete()
        deps.db.session.commit()
        return img_id, 200


api.add_resource(Images, '/images')
api.add_resource(ImagesDownload, '/images/<int:img_id>')
api.add_resource(ImagesDelete, '/images/<int:img_id>')

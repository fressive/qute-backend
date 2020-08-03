import config
from app.helpers import imagesource, response
from app.models.model import ImageQuery
from app.resources import limiter, images_blueprint
from flask import make_response, jsonify

"""
Params: 
    ID              The ID of image source.
    
"""
@images_blueprint.route("/page")
@limiter.limit(lambda : config.get_page_limit)
def page():
    return jsonify(response.make(200, {
        imagesource.RECOMMENDED: ImageQuery.count(),
        imagesource.KONACHAN: ImageQuery.count_by_source(imagesource.KONACHAN),
        imagesource.YANDERE: ImageQuery.count_by_source(imagesource.YANDERE),
        imagesource.DANBOORU: ImageQuery.count_by_source(imagesource.DANBOORU),
        imagesource.PIXIV: ImageQuery.count_by_source(imagesource.PIXIV)
    }))
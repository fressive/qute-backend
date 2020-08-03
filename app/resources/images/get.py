import config
from app.models.model import ImageQuery
from app.helpers import imagesource, response, dbhelper
from app.resources import limiter, images_blueprint
from flask import make_response, jsonify

"""
Params: 
    ID      The ID of image source.
    
"""
@images_blueprint.route("/get/<int:sid>/<int:page>")
@limiter.limit(lambda : config.get_images_limit)
def get(sid, page):
    results = list(map(lambda x: dbhelper.serialize(x), ImageQuery.query_by_source(sid, page)))
    
    return jsonify(response.make(200, results))
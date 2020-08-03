import config
import requests
from app.helpers import imagesource, response, dbhelper
from app.resources import limiter, images_blueprint
from flask import make_response, jsonify, request, stream_with_context, Response

@images_blueprint.route("/view/<int:sid>")
@limiter.limit(lambda : config.view_images_limit)
def view(sid):
    if (sid == imagesource.PIXIV):
        req = requests.get(request.args["url"], headers={"Referer": "https://app-api.pixiv.net/"})

    return Response(req.content, content_type=req.headers['content-type'])
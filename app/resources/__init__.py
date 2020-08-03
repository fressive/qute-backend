from flask import Blueprint

images_blueprint = Blueprint("images", __name__)


from run import limiter
from app.resources.images import get, page, view

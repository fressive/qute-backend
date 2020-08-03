from app.helpers.imagesource import login
from app.models.model import Artist, ImageQuery


login()
ImageQuery.add_from_pixiv(74078476)
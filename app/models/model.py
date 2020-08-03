import config
import json
from app.helpers import dbhelper, imagesource
from sqlalchemy import CheckConstraint, Column, ForeignKey, Text, text, func
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, TEXT, TINYINT, TINYTEXT, MEDIUMTEXT, DOUBLE
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Artist(Base):
    __tablename__ = 'artist'
    __table_args__ = (
        CheckConstraint('json_valid(`social_links`)'),
    )

    artist_id = Column(INTEGER(11), primary_key=True)
    avatar_url = Column(MEDIUMTEXT)
    name = Column(MEDIUMTEXT, unique=True)
    social_links = Column(LONGTEXT)
    description = Column(Text)
    favorites = Column(INTEGER(11), server_default=text("0"))

    def __repr__(self):
        return "<Artist(ID={}, name={})>".format(self.artist_id, self.name)

class ArtistQuery:
    
    @staticmethod
    def get_by_pixiv_id(uid):
        if not isinstance(uid, int):
            return None

        session = dbhelper.get_session()
        result = session.query(Artist).filter(text("JSON_EXTRACT(social_links, '$.pixiv') = {}".format(uid))).first()
        return result

    @staticmethod
    def create_by_pixiv_id(uid):
        if not isinstance(uid, int):
            return None
        
        detail = imagesource.pixivApi.user_detail(uid)

        sl = {
            "twitter": detail["profile"]["twitter_account"],
            "pixiv": detail["user"]["id"]
        }

        artist = Artist(
            avatar_url = detail["user"]["profile_image_urls"]["medium"], 
            name = detail["user"]["name"], 
            social_links = json.dumps(sl), 
            description = detail["user"]["comment"]
        )

        session = dbhelper.get_session()
        session.add(artist)
        session.commit()

        return artist

class Image(Base):
    __tablename__ = 'image'

    image_id = Column(INTEGER(11), primary_key=True)
    image_url = Column(Text)
    artist_id = Column(ForeignKey('artist.artist_id'), index=True)
    favorites = Column(INTEGER(11))
    source_url = Column(Text)
    tags = Column(Text)
    title = Column(Text)
    description = Column(Text)
    width = Column(INTEGER(11))
    height = Column(INTEGER(11))
    r18 = Column(TINYINT(1))
    source_id = Column(TINYINT(2), index=True)

    artist = relationship('Artist')

    def __repr__(self):
        return "<Image(ID={}, artistID={}, title={})>".format(self.artist_id, self.artist_id, self.title)

class ImageQuery:

    @staticmethod
    def count():
        session = dbhelper.get_session()
        return session.query(func.count(Image.image_id)).scalar()

    @staticmethod
    def count_by_source(source_id):
        session = dbhelper.get_session()
        return session.query(func.count(Image.image_id)).filter(Image.source_id == source_id).scalar()

    @staticmethod
    def add_from_moebooru(source_id, post_id):
        """
            Get image from moebooru posts.
        """
        pass

    @staticmethod
    def add_from_pixiv(illust_id):
        detail = imagesource.pixivApi.illust_detail(illust_id)["illust"]
        
        artist_uid = detail["user"]["id"]
        artist = ArtistQuery.get_by_pixiv_id(artist_uid)
        if not artist:
            artist = ArtistQuery.create_by_pixiv_id(artist_uid)

        r18 = len(list(filter(lambda x: x["name"].lower() in config.r18_tags, detail["tags"]))) > 0

        if r18 and not config.allow_r18:
            return None

        image = Image(
            image_url = detail["image_urls"]["large"],
            artist_id = artist.artist_id, favorites = 0, 
            source_url = "https://www.pixiv.net/artworks/{}".format(illust_id), 
            tags = ','.join(map(lambda x: x["name"], detail["tags"])),
            title = detail["title"],
            description = detail["caption"],
            width = detail["width"],
            height = detail["height"],
            r18 = r18,
            source_id = imagesource.PIXIV
        )

        session = dbhelper.get_session()
        session.add(image)
        session.commit()

        return image

    @staticmethod
    def query_by_source(source_id, page, limit=20):
        session = dbhelper.get_session()
        return session.query(Image).filter(Image.source_id == source_id).limit(limit).offset(limit * (page - 1))
        
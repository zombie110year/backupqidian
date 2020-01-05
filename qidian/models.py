from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base()


class Book(Model):
    __tablename__ = "t_book"


class Volume(Model):
    __tablename__ = "t_volume"


class Chapter(Model):
    __tablename__ = "t_chapter"


class SpiderStatus(Model):
    __tablename__ = "t_spiderstatus"

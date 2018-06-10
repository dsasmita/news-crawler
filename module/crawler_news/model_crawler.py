import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, BigInteger, Text, Integer, String, Boolean

db_crawler = SQLAlchemy()


class NewsPost(db_crawler.Model):
    __tablename__ = 'news_post'
    id = Column(BigInteger, primary_key=True)
    id_portal = Column(Integer)
    link_news = Column(Text)
    kanal_index = Column(Text)
    scrap_status = Column(Boolean, default=False)
    title = Column(Text)
    content = Column(Text)
    tags = Column(Text)
    category = Column(Text)
    category_sub = Column(Text)
    date_publish = Column(DateTime)
    image_link = Column(Text)
    image_link_alt = Column(Text)
    author = Column(Text)
    editor = Column(Text)
    source = Column(Text)
    meta_description = Column(Text)
    meta_keyword = Column(Text)
    meta_content_category = Column(Text)
    meta_content_category_sub = Column(Text)
    meta_content_location = Column(Text)
    meta_content_author = Column(Text)
    meta_content_editor = Column(Text)
    meta_content_lipsus = Column(Text)
    meta_content_type = Column(Text)
    meta_content_publish_date = Column(DateTime)
    meta_content_source = Column(Text)
    meta_content_tag = Column(Text)
    meta_content_total_words = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class Kanal(db_crawler.Model):
    __tablename__ = 'news_kanal'
    id = Column(BigInteger, primary_key=True)
    id_portal = Column(Integer)
    title = Column(String(255))
    slug = Column(String(255))
    type = Column(String(255))
    description = Column(Text)


class Portal(db_crawler.Model):
    __tablename__ = 'portal'
    id = Column(BigInteger, primary_key=True)
    title = Column(String(255))
    home_page = Column(String(255))
    link_index = Column(String(255))

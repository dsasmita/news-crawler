import sys, os
sys.path.append(os.getcwd()) # sesuai dengan mark directory

from module.crawler_news.model_crawler import Portal, db_crawler
from app import create_app


app = create_app()

with app.app_context():
    # portal feed
    # kompas
    portal = Portal()
    portal.title = 'kompas.com'
    portal.home_page = 'https://www.kompas.com'
    portal.link_index = 'https://indeks.kompas.com/'

    db_crawler.session.add(portal)
    db_crawler.session.commit()

    # detik
    portal = Portal()
    portal.title = 'detik.com'
    portal.home_page = 'https://www.detik.com/'
    portal.link_index = 'https://news.detik.com/indeks'

    db_crawler.session.add(portal)
    db_crawler.session.commit()


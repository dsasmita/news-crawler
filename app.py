from flask import Flask

from module.crawler_news.model_crawler import db_crawler
from module.crawler_news.view import module_crawler_news
from module.home.view import module_home


def create_app():
    app = Flask(__name__)
    # setup config
    app.config.from_pyfile('settings.py')

    # register all module
    app.register_blueprint(module_home, url_prefix="/")
    app.register_blueprint(module_crawler_news, url_prefix="/crawler")

    # register model
    db_crawler.init_app(app)

    return app

from flask import Blueprint

module_crawler_news = Blueprint(
        'module_scrap_news',
        __name__,
        template_folder='templates'
)


@module_crawler_news.route('/')
def index():
    return 'This is landing for crawler'
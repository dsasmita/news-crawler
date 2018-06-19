import datetime

from flask import Blueprint, request, jsonify
from sqlalchemy.sql.elements import Null

from module.crawler_news.detikcom.DetikCrawler import DetikCrawler
from module.crawler_news.kompascom.KompasCrawler import KompasCrawler
from module.crawler_news.model_crawler import Portal, Kanal, NewsPost, db_crawler

module_crawler_news = Blueprint('module_scrap_news', __name__, template_folder='templates')


@module_crawler_news.route('/')
def index():
    data = {'page': 'crawler', 'title': 'home crawler'}
    return jsonify(data)


# kompas
@module_crawler_news.route('/kompas/list')
def kompas_list():
    date_scrap = request.args.get('date', datetime.datetime.now().strftime('%Y-%m-%d'))

    print('start ....')
    start_time = datetime.datetime.now()
    print(start_time)
    print('......')
    print('......')
    print('......')

    check_kompas = Portal.query.filter_by(title='kompas.com').count()
    if check_kompas == 0:
        return 'news portal kompas not added yet'

    portal = Portal.query.filter_by(title='kompas.com').first()
    kanals = Kanal.query.filter_by(id_portal=portal.id).all()

    kanal_list = []
    for kn in kanals:
        tmp = {}
        tmp['link'] = 'https://indeks.kompas.com/' + kn.title + '/' + date_scrap
        tmp['link_ori'] = 'https://indeks.kompas.com/' + kn.title
        tmp['kanal'] = kn.title
        kanal_list.append(tmp)

    kompas = KompasCrawler()
    link_news = kompas.generate_link(kanal_list)

    for link in link_news:
        check = NewsPost.query.filter_by(link_news=link['href']).count()
        if check == 0:
            news = NewsPost()
            news.link_news = link['href']
            news.id_portal = portal.id
            news.title = link['title']
            news.kanal_index = link['kanal']
            news.date_publish = link['date']

            db_crawler.session.add(news)
            db_crawler.session.commit()
        else:
            news = NewsPost.query.filter_by(link_news=link['href']).first()
            if link['kanal'] not in news.kanal_index:
                news.kanal_index = news.kanal_index + ', ' + link['kanal']
                db_crawler.session.add(news)
                db_crawler.session.commit()

    print('Done')
    end_time = datetime.datetime.now()
    print(end_time)

    data = {
            'page' : 'crawler.kompas.list',
            'title' : 'crawl kompas list',
            'count' : len(link_news),
            'start' : start_time,
            'end' : end_time
    }
    return jsonify(data)

@module_crawler_news.route('/kompas/category-insert')
def kompas_category():
    check_kompas = Portal.query.filter_by(title='kompas.com').count()
    if check_kompas == 0:
        return 'news portal kompas not added yet'

    portal = Portal.query.filter_by(title='kompas.com').first()

    kompas = KompasCrawler()
    kompas.id_news = portal.id
    kompas.link_index = portal.link_index
    kanals = kompas.get_kanal();

    for kn in kanals:
        check_category = Kanal.query.filter_by(slug=kn).count()
        if check_category == 0:
            kanal = Kanal()
            kanal.id_portal = portal.id
            kanal.title = kn
            kanal.slug = kn
            kanal.description = kn

            db_crawler.session.add(kanal)
            db_crawler.session.commit()

    return 'Kompas: category inserted'

@module_crawler_news.route('kompas/detail')
def kompas_detail():
    check_kompas = Portal.query.filter_by(title='kompas.com').count()
    if check_kompas == 0:
        return 'news portal kompas not added yet'

    portal = Portal.query.filter_by(title='kompas.com').first()

    limit = request.args.get('limit', 20)

    print('start ....')
    start_time = datetime.datetime.now()
    print(start_time)
    print('......')
    print('......')
    print('......')

    news_posts = NewsPost.query.filter_by(scrap_status=False, id_portal=portal.id ).\
                    order_by(NewsPost.date_publish.desc()).limit(limit).all()

    kompas = KompasCrawler()

    i = 0
    for news in news_posts:
        print(str(i + 1) + ': ' + str(datetime.datetime.now()))
        print(news.link_news)
        content = kompas.scarp_detail_news(news.link_news)
        news.scrap_status = True

        if content == False:
            db_crawler.session.add(news)
            db_crawler.session.commit()
        else:
            if content['title'] != '':
                news.title = content['title']

            news.content = content['content']
            news.tags = content['tags']
            news.category = content['category']
            news.category_sub = content['category_sub']

            if content['date_publish'] != '':
                news.date_publish = content['date_publish']

            news.image_link = content['image_link']
            news.image_link_alt = content['image_link_alt']
            news.author = content['author']
            news.editor = content['editor']
            news.source = content['meta_content_source']
            news.meta_description = content['meta_description']
            news.meta_keyword = content['meta_keyword']
            news.meta_content_category = content['meta_content_category']
            news.meta_content_category_sub = content['meta_content_category_sub']
            news.meta_content_location = content['meta_content_location']
            news.meta_content_author = content['meta_content_author']
            news.meta_content_editor = content['meta_content_editor']
            news.meta_content_lipsus = content['meta_content_lipsus']
            news.meta_content_type = content['meta_content_type']

            if content['meta_content_publish_date'] != '':
                news.meta_content_publish_date = content['meta_content_publish_date']

            news.meta_content_source = content['meta_content_source']
            news.meta_content_total_words = content['meta_content_total_words']
            news.meta_content_total_words = content['meta_content_total_words']

            db_crawler.session.add(news)
            db_crawler.session.commit()

            i = i + 1

    end_time = datetime.datetime.now()
    print(end_time)
    print(str(i) + ' news scarp')
    print('done ....')

    data = {
            'page': 'crawler.kompas.detail',
            'title': 'crawl kompas detail',
            'count': i,
            'start': start_time,
            'end': end_time
    }
    return jsonify(data)

# Detik
@module_crawler_news.route('/detik/list')
def detik_scrap_list():
    date_scrap = request.args.get('date', datetime.datetime.now().strftime('%m/%d/%Y'))

    print('start ....')
    start_time = datetime.datetime.now()
    print(start_time)
    print('......')
    print('......')
    print('......')

    check_kompas = Portal.query.filter_by(title='detik.com').count()
    if check_kompas == 0:
        return 'news portal detik not added yet'

    portal = Portal.query.filter_by(title='detik.com').first()
    kanals = Kanal.query.filter_by(id_portal=portal.id).all()

    kanal_list = []
    for kn in kanals:
        link = kn.slug
        link_array = link.split('?')
        link = link_array[0]
        tmp = {}
        tmp['link'] = 'https://' + link + '?date=' + date_scrap
        tmp['link_ori'] = 'https://' + link
        tmp['kanal'] = kn.title
        tmp['type'] = kn.type
        tmp['date'] = date_scrap
        kanal_list.append(tmp)

    detik = DetikCrawler()
    link_news = detik.generate_link(kanal_list)

    for link in link_news:
        check = NewsPost.query.filter_by(link_news=link['href']).count()
        if check == 0:
            news = NewsPost()
            news.link_news = link['href']
            news.id_portal = portal.id
            news.title = '%s' %link['title']
            news.title_sub = '%s' %link['title_sub']
            news.kanal_index = link['kanal']
            news.date_publish = link['date']

            db_crawler.session.add(news)
            db_crawler.session.commit()
        else:
            news = NewsPost.query.filter_by(link_news=link['href']).first()
            if link['kanal'] not in news.kanal_index:
                news.kanal_index = news.kanal_index + ', ' + link['kanal']
                db_crawler.session.add(news)
                db_crawler.session.commit()

    print('Done')
    end_time = datetime.datetime.now()
    print(end_time)

    data = {'page': 'crawler.detik.list', 'title': 'crawl detik list', 'count': len(link_news), 'start': start_time,
        'end': end_time}
    return jsonify(data)

@module_crawler_news.route('/detik/category-insert')
def detik_category_insert():
    check_kompas = Portal.query.filter_by(title='detik.com').count()
    if check_kompas == 0:
        return 'news portal detik not added yet'

    portal = Portal.query.filter_by(title='detik.com').first()

    detik = DetikCrawler()
    detik.id_news = portal.id
    detik.link_index = portal.link_index
    kanals = detik.get_kanal()

    for kn in kanals:
        check_category = Kanal.query.filter_by(slug=kn['slug']).count()
        if check_category == 0:
            kanal = Kanal()
            kanal.id_portal = portal.id
            kanal.title = kn['title']
            kanal.slug = kn['slug']
            kanal.description = kn['slug']

            db_crawler.session.add(kanal)
            db_crawler.session.commit()

    return 'Detik: category inserted'

@module_crawler_news.route('/detik/detail/singlepagenews')
def detik_detail_singlepagenews():
    check = Portal.query.filter_by(title='detik.com').count()
    if check == 0:
        return 'news portal detik not added yet'

    print('start ....')
    start_time = datetime.datetime.now()
    print(start_time)
    print('......')
    print('......')
    print('......')

    portal = Portal.query.filter_by(title='detik.com').first()

    limit = request.args.get('limit', 20)

    news_posts = NewsPost.query.filter_by(scrap_status=False, meta_content_type='singlepagenews', id_portal=portal.id). \
        order_by(NewsPost.date_publish.desc()).limit(limit).all()

    detik = DetikCrawler()

    i = 0
    for news in news_posts:
        content = detik.scarp_detail_news(news.link_news)

        print(str(i + 1) + ': ' + str(datetime.datetime.now()))
        print(news.link_news)

        news.scrap_status = True

        if content['title'] != '':
            news.title = content['title']

        news.content = '%s' %content['content']
        news.tags = '%s' %content['tags']
        news.category = '%s' %content['category']
        news.category_sub = '%s' %content['category_sub']

        news.image_link = '%s' %content['image_link']
        news.image_link_alt = '%s' %content['image_link_alt']
        news.author = '%s' %content['author']
        news.meta_description = '%s' %content['meta_description']
        news.meta_keyword = '%s' %content['meta_keyword']
        news.meta_content_author = '%s' %content['meta_content_author']
        news.meta_content_type = '%s' %content['meta_content_type']

        db_crawler.session.add(news)
        db_crawler.session.commit()

        i = i + 1


    end_time = datetime.datetime.now()
    print(end_time)
    print(str(i) + ' news scarp')
    print('done ....')

    data = {'page': 'crawler.detik.detail', 'title': 'crawl detik detail', 'count': i, 'start': start_time,
        'end': end_time}
    return jsonify(data)

@module_crawler_news.route('/detik/news-type')
def detik_news_type():
    check = Portal.query.filter_by(title='detik.com').count()
    if check == 0:
        return 'news portal detik not added yet'

    print('start ....')
    start_time = datetime.datetime.now()
    print(start_time)
    print('......')
    print('......')
    print('......')

    portal = Portal.query.filter_by(title='detik.com').first()

    limit = request.args.get('limit', 20)

    news_posts = NewsPost.query.filter_by(meta_content_type=None, id_portal=portal.id). \
        order_by(NewsPost.date_publish.desc()).limit(limit).all()

    detik = DetikCrawler()

    i = 0
    for news in news_posts:
        content = detik.scarp_news_type(news.link_news)

        news.meta_description = '%s' %content['meta_description']
        news.meta_keyword = '%s' %content['meta_keyword']
        news.meta_content_author = '%s' %content['meta_content_author']
        news.meta_content_type = '%s' %content['meta_content_type']

        db_crawler.session.add(news)
        db_crawler.session.commit()

        i = i + 1


    end_time = datetime.datetime.now()
    print(end_time)
    print(str(i) + ' news scarp')
    print('done ....')

    data = {'page': 'crawler.detik.news.type', 'title': 'crawl detik news type', 'count': i, 'start': start_time,
        'end': end_time}
    return jsonify(data)
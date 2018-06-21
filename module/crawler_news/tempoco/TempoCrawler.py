import datetime
import bs4
import requests

class TempoCrawler:
    HEADERS = {
        'Accept-Encoding': 'gzip, '
        'deflate, sdch', 'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive'
    }

    def __init__(self):
        self.id_news = 0 # id news
        self.link_index = '' # indeks link
        self.link_list = '' # indeks want to scarp

    def generate_index(self, link_list):
        return 'generate_index'

    def generate_link(self, link_list):
        return 'generate_link'

    def generate_content_all_news(self):
        return 'news'

    def get_kanal(self):
        return 'gent_kanal'

    def scarp_detail_news(self, news_link):
        return 'scrap_detail_news'

    def date_format_id(self, date):
        date_time_array = date.split(',')
        time = date_time_array[1].replace('WIB', '').strip()
        date_array = date_time_array[0].split('/')

        return '%s-%s-%s %s' %(date_array[2], date_array[1], date_array[0], time)

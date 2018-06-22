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
        link_index = self.link_index
        categories = []
        if link_index == '':
            return categories

        content = requests.get(link_index, timeout=10, headers=TempoCrawler.HEADERS)
        response = bs4.BeautifulSoup(content.text, "html.parser")

        categories_container = response.find('div', {'id': 'pilih-kanal'})
        for cat_option in categories_container.select('option'):
            if(cat_option['value'] != ''):
                tmp = {}
                tmp['slug'] = cat_option['value']
                tmp['title'] = cat_option.get_text()
                categories.append(tmp)

        content.close()
        response.decompose()

        return categories

    def scarp_detail_news(self, news_link):
        return 'scrap_detail_news'

    def date_format_id(self, date):
        date_time_array = date.split(',')
        time = date_time_array[1].replace('WIB', '').strip()
        date_array = date_time_array[0].split('/')

        return '%s-%s-%s %s' %(date_array[2], date_array[1], date_array[0], time)

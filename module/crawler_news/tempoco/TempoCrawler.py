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
        news_link = []
        for lk in link_list:
            link_request = lk['link']

            try:
                print(link_request)
                content = requests.get(link_request, timeout=10, headers=TempoCrawler.HEADERS)
                response = bs4.BeautifulSoup(content.text, "html.parser")
                list_link = response.find('section', 'list-type-1')

                for link in list_link.select('li'):
                    tmp = {}
                    tmp['href'] = link.find('a')['href']
                    tmp['title'] = link.find('h2', 'title').get_text().strip()
                    tmp['kanal'] = lk['kanal_slug']
                    date = link.find('span', 'col').get_text().strip()
                    tmp['date'] = self.date_format_id(date)
                    news_link.append(tmp)

                content.close()
                response.decompose()
            except:
                print('error: ' + link_request)

        return news_link

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
        date = date.replace('WIB', '').strip()
        date_array = date.split(' ')

        months = [
            'bulan',
            'Januari',
            'Februari',
            'Maret',
            'April',
            'Mei',
            'Juni',
            'Juli',
            'Agustus',
            'September',
            'Oktober',
            'November',
            'Desember'
        ]

        month = 0
        for m in months:
            if date_array[1] == m:
                month = months.index(m)

        return '%s-%s-%s %s' %(date_array[2], month, date_array[0], date_array[3])

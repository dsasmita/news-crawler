# -*- coding: utf-8 -*-
import bs4
import requests


class DetikCrawler:
    def __init__(self):
        self.id_news = 0  # id news
        self.link_index = ''  # indeks link
        self.link_list = ''  # indeks want to scarp

    def generate_index(self, link_list):
        if link_list['link'] == '':
            return 'link_list not specified'

        url_pagination = []

        if (link_list['type'] == 'GET'):
            content = requests.get(link_list['link'], timeout=10)
            bs = bs4.BeautifulSoup(content.text, "html.parser")

            pagination = bs.find('div', 'paging')
            last_page = 1
            if (pagination != None):
                for page in pagination.select('a'):
                    number = page.get_text().replace('Â»', '')
                    number = number.strip()
                    if (self.is_number(number)):
                        last_page = self.cast_to_int(number)

                for i in range(0, last_page):
                    tmp = {}
                    tmp['link'] = "%s/all/%s?date=%s" % (link_list['link_ori'], i, link_list['date'])
                    tmp['date'] = link_list['date']
                    tmp['type'] = link_list['type']
                    url_pagination.append(tmp)
            else:
                tmp = {}
                tmp['link'] = link_list['link']
                tmp['date'] = link_list['date']
                tmp['type'] = link_list['type']
                url_pagination.append(tmp)

            content.close()
            bs.decompose()
        else:
            tmp = {}
            tmp['link'] = link_list['link_ori']
            tmp['date'] = link_list['date']
            tmp['type'] = link_list['type']
            url_pagination.append(tmp)

        return url_pagination;

    def generate_link(self, link_list):
        news_link = []
        for lk in link_list:
            if lk['kanal'] == 'detikNews':
                url_pagination = self.generate_index(lk)
                for url in url_pagination:
                    content = requests.get(url['link'], timeout=10)
                    bs = bs4.BeautifulSoup(content.text, "html.parser")
                    list_array = bs.find("ul", {"id": "indeks-container"})

                    if len(list_array) > 0:
                        for link in list_array.select('article'):
                            tmp = {}
                            tmp['href'] = link.find('a')['href']
                            tmp['title'] = link.find('h2').get_text().strip()
                            tmp['kanal'] = lk['kanal']
                            tmp['title_sub'] = ''
                            title_sub = link.find('span', 'sub_judul')
                            if title_sub != None:
                                tmp['title_sub'] = title_sub.get_text().strip()

                            # date
                            date = link.find('span', 'labdate').get_text().strip()
                            date = self.date_format_id(date)

                            tmp['date'] = date
                            news_link.append(tmp)

                    content.close()
                    bs.decompose()

            if lk['kanal'] == 'detikFinance':
                content = requests.get(lk['link'], timeout=10)
                bs = bs4.BeautifulSoup(content.text, "html.parser")

                list_array = bs.find('div', 'lf_content')

                if list_array != None:
                    for link in list_array.select('article'):
                        tmp = {}
                        tmp['href'] = link.find('a')['href']
                        tmp['title'] = link.find('h2').get_text().strip()
                        tmp['kanal'] = lk['kanal']
                        tmp['title_sub'] = ''
                        title_sub = link.find('span', 'sub_judul')
                        if title_sub != None:
                            tmp['title_sub'] = title_sub.get_text().strip()

                        # date
                        date = link.find('span', 'labdate').get_text().strip()
                        date = self.date_format_en(date)

                        tmp['date'] = date
                        news_link.append(tmp)

                content.close()
                bs.decompose()

            if lk['kanal'] == 'detiki-Net':
                content = requests.get(lk['link'], timeout=10)
                bs = bs4.BeautifulSoup(content.text, "html.parser")

                list_array = bs.find('ul', 'feed')

                if list_array != None:
                    for link in list_array.select('article'):
                        tmp = {}
                        tmp['href'] = link.find('a')['href']
                        tmp['title'] = link.find('h2').get_text().strip()
                        tmp['kanal'] = lk['kanal']
                        tmp['title_sub'] = ''
                        title_sub = link.find('span', 'sub_judul')
                        if title_sub != None:
                            tmp['title_sub'] = title_sub.get_text().strip()

                        # date
                        date = link.find('span', 'date').get_text().strip()
                        date = self.date_format_en(date)

                        tmp['date'] = date
                        news_link.append(tmp)

                content.close()
                bs.decompose()

            if lk['kanal'] == 'detikTravel':
                content = requests.get(lk['link'], timeout=10)
                bs = bs4.BeautifulSoup(content.text, "html.parser")

                list_array = bs.find('section', 'list__news')

                if list_array != None:
                    for link in list_array.select('article'):
                        tmp = {}
                        tmp['href'] = link.find('a')['href']
                        tmp['title'] = link.find('h3').get_text().strip()
                        tmp['kanal'] = lk['kanal']
                        tmp['title_sub'] = ''
                        title_sub = link.find('div', 'list__news__sub')
                        if title_sub != None:
                            tmp['title_sub'] = title_sub.get_text().strip()

                        # date
                        date = link.find('div', 'date').get_text().strip()
                        date = self.date_format_en(date)

                        tmp['date'] = date
                        news_link.append(tmp)

                content.close()
                bs.decompose()

            if lk['kanal'] == 'detikFood':
                content = requests.get(lk['link'], timeout=10)
                bs = bs4.BeautifulSoup(content.text, "html.parser")

                list_array = bs.find('ul', 'feed')

                if list_array != None:
                    for link in list_array.select('article'):
                        tmp = {}
                        tmp['href'] = link.find('a')['href']
                        tmp['title'] = link.find('h2').get_text().strip()
                        tmp['kanal'] = lk['kanal']
                        tmp['title_sub'] = ''
                        title_sub = link.find('span', 'sub_judul')
                        if title_sub != None:
                            tmp['title_sub'] = title_sub.get_text().strip()

                        # date
                        date = link.find('span', 'date').get_text().strip()
                        date = self.date_format_en(date)

                        tmp['date'] = date
                        news_link.append(tmp)

                content.close()
                bs.decompose()

            if lk['kanal'] == 'detikHealth':
                content = requests.get(lk['link'], timeout=10)
                bs = bs4.BeautifulSoup(content.text, "html.parser")

                list_array = bs.find('ul', 'list')

                if list_array != None:
                    for link in list_array.select('article'):
                        tmp = {}
                        tmp['href'] = link.find('a')['href']
                        tmp['title'] = link.find('h2').get_text().strip()
                        tmp['kanal'] = lk['kanal']
                        tmp['title_sub'] = ''
                        title_sub = link.find('span', 'sub_judul')
                        if title_sub != None:
                            tmp['title_sub'] = title_sub.get_text().strip()

                        # date
                        date = link.find('span', 'date').get_text().strip()
                        date = self.date_format_en(date)

                        tmp['date'] = date
                        news_link.append(tmp)

                content.close()
                bs.decompose()

            if lk['kanal'] == 'detikOto':
                content = requests.get(lk['link'], timeout=10)
                bs = bs4.BeautifulSoup(content.text, "html.parser")

                list_array = bs.find('div', 'lf_content')

                if list_array != None:
                    for link in list_array.select('article'):
                        tmp = {}
                        tmp['href'] = link.find('a')['href']
                        tmp['title'] = link.find('h2').get_text().strip()
                        tmp['kanal'] = lk['kanal']
                        tmp['title_sub'] = ''
                        title_sub = link.find('span', 'sub_judul')
                        if title_sub != None:
                            tmp['title_sub'] = title_sub.get_text().strip()

                        # date
                        date = link.find('span', 'labdate').get_text().strip()
                        date = self.date_format_en(date)

                        tmp['date'] = date
                        news_link.append(tmp)

                content.close()
                bs.decompose()

        return news_link

    def generate_content_all_news(self):
        return 'list'

    def get_kanal(self):
        link_index = self.link_index
        categories = []
        if link_index == '':
            return categories

        content = requests.get(link_index, timeout=10)
        response = bs4.BeautifulSoup(content.text, "html.parser")

        categories_container = response.find('div', 'menu_idx')
        for cat_option in categories_container.select('a'):
            title = cat_option.get_text()
            title = title.replace("» ", "")
            slug = cat_option['href']
            slug = slug.replace("https://", '')
            slug = slug.replace("//", "")
            slug_array = slug.split('?')

            tmp = {}
            tmp['title'] = title
            tmp['slug'] = slug_array[0]
            categories.append(tmp)

        return categories

    def scarp_detail_news(self, news_link):
        return 'detail'

    def is_number(self, s):
        try:
            return float(s)
        except ValueError:
            return False

    def cast_to_int(self, s):
        try:
            return int(s)
        except ValueError:
            return False

    def date_format_id(self, date):
        date_time_array = date.split(',')
        time = date_time_array[1].replace('WIB', '').strip()
        date_array = date_time_array[0].split(' ')

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
            if date_array[2] == m:
                month = months.index(m)

        return '%s-%s-%s %s' %(date_array[3], month, date_array[1], time)

    def date_format_en(self, date):
        d = date.split(',')
        date_time = d[1].replace('WIB', '').strip()

        date_time_array = date_time.split(' ')

        months = [
            'bulan',
            'Jan',
            'Feb',
            'Mar',
            'Apr',
            'Mei',
            'Jun',
            'Jul',
            'Agu',
            'Sep',
            'Okt',
            'Nov',
            'Des'
        ]

        month = 0
        for m in months:
            if date_time_array[1] == m:
                month = months.index(m)

        return '%s-%s-%s %s' % (date_time_array[2], month, date_time_array[0], date_time_array[3])
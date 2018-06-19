# -*- coding: utf-8 -*-
import datetime

import bs4
import requests
from bs4 import Comment


class DetikCrawler:
    HEADERS = {
        'Accept-Encoding': 'gzip, '
        'deflate, sdch', 'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0', 'Connection': 'keep-alive'}

    def __init__(self):
        self.id_news = 0  # id news
        self.link_index = ''  # indeks link
        self.link_list = ''  # indeks want to scarp

    def generate_index(self, link_list):
        if link_list['link'] == '':
            return 'link_list not specified'

        url_pagination = []

        if (link_list['type'] == 'GET'):
            content = requests.get(link_list['link'], timeout=10, headers=DetikCrawler.HEADERS)
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
                    print(url['link'])
                    content = requests.get(url['link'], timeout=10, headers=DetikCrawler.HEADERS)
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
                print(lk['link'])
                content = requests.get(lk['link'], timeout=10, headers=DetikCrawler.HEADERS)
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
                print(lk['link'])
                content = requests.get(lk['link'], timeout=10, headers=DetikCrawler.HEADERS)
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
                print(lk['link'])
                content = requests.get(lk['link'], timeout=10, headers=DetikCrawler.HEADERS)
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
                print(lk['link'])
                content = requests.get(lk['link'], timeout=10, headers=DetikCrawler.HEADERS)
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
                print(lk['link'])
                content = requests.get(lk['link'], timeout=10, headers=DetikCrawler.HEADERS)
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
                print(lk['link'])
                content = requests.get(lk['link'], timeout=10, headers=DetikCrawler.HEADERS)
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

    def scarp_detail_news(self, news_link):
        content = requests.get(news_link, timeout=10, headers=DetikCrawler.HEADERS)
        response = bs4.BeautifulSoup(content.text, "html.parser")

        news = {}

        # meta data
        metas = response.find_all('meta')
        news['meta_description'] = ''
        news['meta_keyword'] = ''
        news['meta_content_author'] = ''
        news['meta_content_type'] = ''

        for meta in metas:
            if 'name' in meta.attrs:
                if meta.attrs['name'] == 'description':
                    news['meta_description'] = meta.attrs['content']
                elif meta.attrs['name'] == 'keywords':
                    news['meta_keyword'] = meta.attrs['content']
                elif meta.attrs['name'] == 'author':
                    news['meta_content_author'] = meta.attrs['content']
                elif meta.attrs['name'] == 'contenttype':
                    news['meta_content_type'] = meta.attrs['content']

        if news['meta_content_type'] == 'singlepagenews':
            # title
            try:
                title_container = response.find('div', 'jdl')
                news["title"] = title_container.select_one('h1').get_text()
                news["title_sub"] = title_container.select_one('h2').get_text()
            except:
                news["title"] = ''
                news["title_sub"] = ''

            author_container = response.find('div', 'author')
            try:
                author_array = author_container.get_text().split('-')
                news['author'] = author_array[0].strip()
            except:
                news['author'] = 'empty'

            # tags
            try:
                tags = response.find('div', 'detail_tag')
                tmp_tags_array = []
                for tag in tags.select('a'):
                    tmp_tags_array.append(tag.get_text().strip())

                news['tags'] = ', '.join(tmp_tags_array)
            except:
                news['tags'] = ''

            # image_link
            try:
                photos = response.find('div','pic_artikel')
                news['image_link'] = photos.img['src']
                news['image_link_alt'] = photos.img['alt']
            except:
                news['image_link'] = ''
                news['image_link_alt'] = ''

            # content
            try:
                contents_container = response.find('div', {"id": "detikdetailtext"})

                for script_tag in contents_container.find_all('script'):
                    script_tag.extract()

                for comment_tag in contents_container.find_all(text=lambda text:isinstance(text, Comment)):
                    comment_tag.extract()

                for table_tag in contents_container.find_all('table'):
                    table_tag.extract()

                for center_tag in contents_container.find_all('center'):
                    center_tag.extract()

                for div_tag in contents_container.find_all('div'):
                    div_tag.extract()

                news["content"] = contents_container
            except:
                news["content"] = ''

            # category
            try:
                categories = response.find('div', 'breadcrumb')
                tmp_category_array = []
                for category in categories.select("a"):
                    if category.get_text().strip() != 'Detail Berita':
                        tmp_category_array.append(category.get_text().strip())
            except:
                tmp_category_array = []

            try:
                news['category'] = tmp_category_array[0]
            except:
                news['category'] = 'empty'

            try:
                news['category_sub'] = tmp_category_array[1]
            except:
                news['category_sub'] = 'empty'

            news['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            news['updated_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        content.close()
        response.decompose()

        return news

    def scarp_news_type(self, news_link):
        content = requests.get(news_link, timeout=10, headers=DetikCrawler.HEADERS)
        response = bs4.BeautifulSoup(content.text, "html.parser")

        news = {}

        # meta data
        metas = response.find_all('meta')
        news['meta_description'] = ''
        news['meta_keyword'] = ''
        news['meta_content_author'] = ''
        news['meta_content_type'] = ''

        for meta in metas:
            if 'name' in meta.attrs:
                if meta.attrs['name'] == 'description':
                    news['meta_description'] = meta.attrs['content']
                elif meta.attrs['name'] == 'keywords':
                    news['meta_keyword'] = meta.attrs['content']
                elif meta.attrs['name'] == 'author':
                    news['meta_content_author'] = meta.attrs['content']
                elif meta.attrs['name'] == 'contenttype':
                    news['meta_content_type'] = meta.attrs['content']

        content.close()
        response.decompose()

        return news

    def get_kanal(self):
        link_index = self.link_index
        categories = []
        if link_index == '':
            return categories

        content = requests.get(link_index, timeout=10, headers=DetikCrawler.HEADERS)
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
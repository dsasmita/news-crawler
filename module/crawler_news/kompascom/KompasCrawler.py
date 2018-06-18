import datetime
import bs4
import requests

class KompasCrawler:
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
        if link_list == '':
            return 'link_list not specified'

        content = requests.get(link_list, timeout=10, headers=KompasCrawler.HEADERS)
        bs = bs4.BeautifulSoup(content.text, "html.parser")

        index = [item['data-ci-pagination-page']
                 for item in bs.find_all('a', attrs={'data-ci-pagination-page': True})]
        last_page = 0;
        if len(index) > 0:
            last_page = int(index[len(index) - 1]) + 1

        url_pagination = []
        for i in range(1, last_page):
            url_pagination.append("%s/%s" % (link_list, i))

        return url_pagination;

    def generate_link(self, link_list):
        news_link = []
        for lk in link_list:
            url_pagination = self.generate_index(lk['link'])

            if len(url_pagination) > 0:
                for url in url_pagination:
                    content = requests.get(url, timeout=10, headers=KompasCrawler.HEADERS)
                    response = bs4.BeautifulSoup(content.text, "html.parser")
                    list_link = response.find_all('div', 'article__list')

                    for link in list_link:
                        tmp = {}
                        tmp['href'] = link.find('a')['href']
                        tmp['title'] = link.find('a','article__link').get_text().strip()
                        tmp['kanal'] = lk['kanal']

                        date = link.find('div','article__date').get_text().strip()
                        tmp['date'] = self.date_format_id(date)
                        news_link.append(tmp)

                    content.close()
                    response.decompose()
            else:
                if lk['kanal'] == 'headline':
                    link_request = lk['link_ori']
                else:
                    link_request = lk['link']

                content = requests.get(link_request, timeout=10, headers=KompasCrawler.HEADERS)
                response = bs4.BeautifulSoup(content.text, "html.parser")
                list_link = response.find_all('div', 'article__list')

                for link in list_link:
                    tmp = {}
                    tmp['href'] = link.find('a')['href']
                    tmp['title'] = link.find('a', 'article__link').get_text().strip()
                    tmp['kanal'] = lk['kanal']

                    date = link.find('div', 'article__date').get_text().strip()
                    tmp['date'] = self.date_format_id(date)
                    news_link.append(tmp)

                content.close()
                response.decompose()

        return news_link

    def generate_content_all_news(self):
        news_list_link = self.generate_link()
        news = []
        for link in news_list_link:
            news.append(self.scarp_detail_news(link))

        return news

    def get_kanal(self):
        link_index = self.link_index
        categories = []
        if link_index == '':
            return categories

        content = requests.get(link_index, timeout=10, headers=KompasCrawler.HEADERS)
        response = bs4.BeautifulSoup(content.text, "html.parser")

        categories_container = response.find('div','form__select__wrap')
        for cat_option in categories_container.select('option'):
            if(cat_option['value'] != 'topik-pilihan'):
                categories.append(cat_option['value'])

        content.close()
        response.decompose()

        return categories

    def scarp_detail_news(self, news_link):
        try:
            content = requests.get(news_link, timeout=10, headers=KompasCrawler.HEADERS)
            response = bs4.BeautifulSoup(content.text, "html.parser")

            news = {}
            # title
            try:
                news["title"] = response.find('h1','read__title').get_text()
            except:
                news["title"] = ''

            # content
            try:
                contens = response.find('div', 'read__content')
                tmp_paragraf_news = []
                for paragraf in contens.select('p'):
                    check = True
                    if paragraf.get_text().find('Baca juga') != -1:
                        check = False

                    if check and paragraf.get_text().strip() != "":
                        tmp_paragraf_news.append('<p>%s</p>' %(paragraf.get_text().strip()))

                news["content"] = ' '.join(tmp_paragraf_news)
            except:
                news["content"] = ''

            # tags
            try:
                tags = response.find('ul', 'tag__article__wrap')
                tmp_tags_array = []
                for tag in tags.select('li'):
                    tmp_tags_array.append(tag.get_text().strip())

                news['tags'] = ', '.join(tmp_tags_array)
            except:
                news['tags'] = ''

            # category
            try:
                categories = response.find('ul', 'breadcrumb__wrap')
                tmp_category_array = []
                for category in categories.select("li"):
                    if category.get_text().strip() != 'Home':
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

            # date_publish
            try:
                date_time = response.find('div', 'read__time').get_text()
                date_before_format = date_time.replace('Kompas.com - ', '')
                date_time_array = date_before_format.split(',')
                date_array = date_time_array[0].split('/')
                time_array = date_time_array[1].split(' ')
                news['date_publish'] =  '%s-%s-%s %s' % (date_array[2], date_array[1], date_array[0], time_array[1])
            except:
                news['date_publish'] = ''

            # image_link
            try:
                photos = response.find('div','photo')
                news['image_link'] = photos.img['src']
                news['image_link_alt'] = photos.img['alt']
            except:
                news['image_link'] = ''
                news['image_link_alt'] = ''

            # author
            author = response.find('div', {'id' : 'penulis'})
            try:
                news['author'] = author.a.get_text()
            except:
                news['author'] = 'empty'

            # editor
            try:
                editor = response.find('div', {'id': 'editor'})
                news['editor'] = editor.a.get_text()
            except:
                news['editor'] = ''

            # meta data
            metas = response.find_all('meta')
            news['meta_description'] = ''
            news['meta_keyword'] = ''
            news['meta_content_category'] = ''
            news['meta_content_category_sub'] = ''
            news['meta_content_location'] = ''
            news['meta_content_author'] = ''
            news['meta_content_editor'] = ''
            news['meta_content_lipsus'] = ''
            news['meta_content_type'] = ''
            news['meta_content_publish_date'] = ''
            news['meta_content_source'] = ''
            news['meta_content_tag'] = ''
            news['meta_content_total_words'] = ''
            news['meta_content_publish_date'] = ''

            for meta in metas:
                if 'name' in meta.attrs:
                    if meta.attrs['name'] == 'description':
                        news['meta_description'] = meta.attrs['content']
                    elif meta.attrs['name'] == 'keywords':
                        news['meta_keyword'] = meta.attrs['content']
                    elif meta.attrs['name'] == 'content_category':
                        news['meta_content_category'] = meta.attrs['content']
                    elif meta.attrs['name'] == 'content_subcategory':
                        news['meta_content_category_sub'] = meta.attrs['content']
                    elif meta.attrs['name'] == 'content_location':
                        news['meta_content_location'] = meta.attrs['content']
                    elif meta.attrs['name'] == 'content_author':
                        news['meta_content_author'] = meta.attrs['content']
                    elif meta.attrs['name'] == 'content_editor':
                        news['meta_content_editor'] = meta.attrs['content']
                    elif meta.attrs['name'] == 'content_lipsus':
                        news['meta_content_lipsus'] = meta.attrs['content']
                    elif meta.attrs['name'] == 'content_type':
                        news['meta_content_type'] = meta.attrs['content']
                    elif meta.attrs['name'] == 'content_publish_date':
                        news['meta_content_publish_date'] = meta.attrs['content']
                    elif meta.attrs['name'] == 'content_source':
                        news['meta_content_source'] = meta.attrs['content']
                    elif meta.attrs['name'] == 'content_tag':
                        news['meta_content_tag'] = meta.attrs['content']
                    elif meta.attrs['name'] == 'content_total_words':
                        news['meta_content_total_words'] = meta.attrs['content']
                    elif meta.attrs['name'] == 'content_PublishedDate':
                        news['meta_content_publish_date'] = meta.attrs['content']

            news['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            news['updated_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

            content.close()
            response.decompose()

            return news
        except:
            return False

    def date_format_id(self, date):
        date_time_array = date.split(',')
        time = date_time_array[1].replace('WIB', '').strip()
        date_array = date_time_array[0].split('/')

        return '%s-%s-%s %s' %(date_array[2], date_array[1], date_array[0], time)

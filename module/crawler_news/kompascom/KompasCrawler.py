import datetime
import bs4
import requests

class KompasCrawler:
    def __init__(self):
        self.id_news = 0 # id news
        self.link_index = '' # indeks link
        self.link_list = '' # indeks want to scarp

    def generate_index(self, link_list):
        if link_list == '':
            return 'link_list not specified'

        content = requests.get(link_list, timeout=10)
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
                    content = requests.get(url, timeout=10)
                    response = bs4.BeautifulSoup(content.text, "html.parser")
                    list_link = response.find_all('a', 'article__link')

                    for link in list_link:
                        tmp = {}
                        tmp['href'] = link['href']
                        tmp['title'] = link.get_text()
                        tmp['kanal'] = lk['kanal']
                        news_link.append(tmp)
            else:
                content = requests.get(lk['link'], timeout=10)
                response = bs4.BeautifulSoup(content.text, "html.parser")
                list_link = response.find_all('a', 'article__link')

                for link in list_link:
                    tmp = {}
                    tmp['href'] = link['href']
                    tmp['title'] = link.get_text()
                    tmp['kanal'] = lk['kanal']
                    news_link.append(tmp)
        return news_link

    def generate_content_all_news(self):
        news_list_link = self.generate_link()
        news = []
        for link in news_list_link:
            print(link)
            news.append(self.scarp_detail_news(link))

        return news

    def get_kanal(self):
        link_index = self.link_index
        categories = []
        if link_index == '':
            return categories

        content = requests.get(link_index, timeout=10)
        response = bs4.BeautifulSoup(content.text, "html.parser")

        categories_container = response.find('div','form__select__wrap')
        for cat_option in categories_container.select('option'):
            if(cat_option['value'] != 'topik-pilihan'):
                categories.append(cat_option['value'])

        return categories

    def scarp_detail_news(self, news_link):
        content = requests.get(news_link, timeout=10)
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
        tmp_category_array = []
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

        return news

import scrapy
import re
from DouBanMovieSpider.items import Moive,Director,Scenarist,Actor
from scrapy.loader import ItemLoader

class QuotesSpider(scrapy.Spider):
    name = "movie"

# 'https://movie.douban.com/subject/1440347/' 修罗雪姬 少演员

# 'https://movie.douban.com/subject/1292052/' 肖申克的救赎 两编剧

    def start_requests(self):
        urls = [
            'https://movie.douban.com/subject/1292052/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 获取导演信息
        director_list = []
        director_names = ""
        dire_info_html = response.xpath('//div[@id="info"]/span')[0].css('a')
        for dire_html in dire_info_html:
            dire_name = dire_html.css('a::text').get()
            dire_path = dire_html.css('a::attr(href)').get()
            if 'celebrity/' in dire_path:
                dire_id = dire_path.split('/')[2]
                if director_names:
                    director_names = director_names + ", " + dire_name
                else:
                    director_names = dire_name
                director_list.append({"id": dire_id, "name": dire_name, "path": dire_path})
                print(f'Before yield director follow: {dire_path}')
                # yield response.follow(dire_path, callback=self.parseCelebrity)

        # 编剧
        scen_list = []
        scen_names = ""
        scen_info_html = response.xpath('//div[@id="info"]/span')[1].css('a')
        for scen_html in scen_info_html:
            scen_name = scen_html.css('a::text').get()
            scen_path = scen_html.css('a::attr(href)').get()
            if 'celebrity/' in scen_path:
                scen_id = scen_path.split('/')[2]
                if scen_names:
                    scen_names = scen_names + ", " + scen_name
                else:
                    scen_names = scen_name
                scen_list.append({"id": dire_id, "name": dire_name, "path": scen_path})
                print(f'Before yield scen_list follow: {scen_path}')
                # yield response.follow(scen_path, callback=self.parseCelebrity)

        # # 演员
        acotor_list = []
        acotor_names = ""
        actor_info_html = response.xpath('//div[@id="info"]/span')[2].css('a')
        for actor_html in actor_info_html:
            actor_name = actor_html.css('a::text').get()
            actor_path = actor_html.css('a::attr(href)').get()
            if 'celebrity/' in actor_path:
                actor_id = actor_path.split('/')[2]
                if acotor_names:
                    acotor_names = acotor_names + ", " + actor_name
                else:
                    acotor_names = actor_name
                acotor_list.append({"id": dire_id, "name": dire_name, "path": actor_path})
                print(f'Before yield acotor_list follow: {actor_path}')
                # yield response.follow(actor_path, callback=self.parseCelebrity)


        # 解析电影信息
        movie_id = response.url.split('/')[4]
        movie_name = response.xpath('//span[@property="v:itemreviewed"]/text()').get()
        year_String = response.xpath('//span[@class="year"]/text()').get()
        year_int = int(re.sub('[()]', '', year_String)) # 移除（）并转成Int
        types = response.xpath('//span[@property="v:genre"]/text()').getall()
        release_dates = response.xpath('//span[@property="v:initialReleaseDate"]/text()').getall()
        info_br_sibling_html = response.xpath('//div[@id="info"]/br/following-sibling::text()').getall()
        area = info_br_sibling_html[6]
        languages = info_br_sibling_html[8]
        otherNames = info_br_sibling_html[15]
        score = response.xpath('//strong[@class="ll rating_num"]/text()').get()
        score_float = float(score)
        synopsis = response.xpath('//span[@property="v:summary"]/text()').get()
        imdb = info_br_sibling_html[17]
        doubanUrl = response.url
        iconUrl = response.xpath('//img[@rel="v:image"]').xpath('@src').get()
        posterUrl = "https://img9.doubanio.com/view/photo/l/public/" + iconUrl.split('/')[-1]

        movie = Moive(m_id=movie_id, name=movie_name, year=year_int, directors=director_names,scenarists=scen_names,actors=acotor_names)
        movie['style'] = " / ".join(types)
        movie['releaseDate'] = " / ".join(release_dates)
        movie['area'] = area[1:] # 移除最前面的空格
        movie['language'] = languages[1:] # 移除最前面的空格
        movie['length'] = " / ".join(types)
        movie['otherNames'] = otherNames[1:] # 移除最前面的空格
        movie['score'] = score_float
        movie['synopsis'] = synopsis
        movie['imdb'] = imdb[1:] # 移除最前面的空格
        movie['doubanUrl'] = doubanUrl
        movie['posterUrl'] = posterUrl
        movie['iconUrl'] = iconUrl


        # https://docs.scrapy.org/en/latest/topics/request-response.html
        print(f'Before yield movie 对象: {movie}')
        yield {
          movie
        }

    def parseCelebrity(self, response):
        director_id = response.url.split('/')[4]
        director_name = response.xpath('//div[@id="content"]/h1/text()').get()

        l = ItemLoader(item=Director(), response=response)
        l.add_value('d_id', director_id)
        l.add_value('name_cn', director_name)

        all_info_li_html = response.xpath('//div[@class="info"]/ul/li')
        for li in all_info_li_html:
            li_name = li.css('span::text').get()
            li_value_str = li.css('li::text').getall()[1]
            li_value = re.sub(r"[\n\t\s:]*", "", li_value_str)
            print(f'parseCelebrity name: {li_name} li value: {li_value}')
            if li_name == "性别":
                l.add_value('gender', li_value)
            elif li_name == "星座":
                l.add_value('name_cn', li_value)
            elif li_name == "出生日期":
                l.add_value('birthday', li_value)
            elif li_name == "出生地":
                l.add_value('birthplace', li_value)
            elif li_name == "职业":
                l.add_value('name_cn', li_value)
            elif li_name == "imdb编号":
                l.add_value('imdb', li_value)

        # l.add_xpath('name', '//div[@class="product_name"]')
        # l.add_xpath('name', '//div[@class="product_title"]')
        # l.add_xpath('price', '//p[@id="price"]')
        # l.add_css('stock', 'p#stock]')

        print(f'xxxxxxx {l.load_item()}')
        yield l.load_item()
    def parseActor(self, response):
        pass





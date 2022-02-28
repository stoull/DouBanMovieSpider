import scrapy
import re
from DouBanMovieSpider.items import Director
from scrapy.loader import ItemLoader

class QuotesSpider(scrapy.Spider):
    name = "movie"

    def start_requests(self):
        urls = [
            'https://movie.douban.com/subject/34447553/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        movie_name = response.xpath('//span[@property="v:itemreviewed"]/text()').get()
        create_date = response.xpath('//span[@class="year"]/text()').get()
        types = response.xpath('//span[@property="v:genre"]/text()').getall()

        # directors = response.xpath('//div[@id="info"]/span')[0].css('a::text').getall()
        # scenarist = response.xpath('//div[@id="info"]/span')[1].css('a::text').getall()
        # actors = response.xpath('//span[@class="actor"]//span[@class="attrs"]/a/text()').getall()

        # 获取导演信息
        director_list = []
        dire_info_html = response.xpath('//div[@id="info"]/span')[0].css('a')
        for dire_html in dire_info_html:
            dire_name = dire_html.css('a::text').get()
            dire_path = dire_html.css('a::attr(href)').get()
            dire_id = dire_path.split('/')[2]
            director_list.append({"id": dire_id, "name": dire_name, "path": dire_path})
            print('Before yield director follow')
            yield response.follow(dire_path, callback=self.parseCelebrity)

        # 编剧
        scen_list = []
        scen_info_html = response.xpath('//div[@id="info"]/span')[1].css('a')
        for scen_html in scen_info_html:
            scen_name = scen_info_html.css('a::text').get()
            scen_path = scen_info_html.css('a::attr(href)').get()
            scen_id = scen_path.split('/')[2]
            scen_list.append({"id": dire_id, "name": dire_name, "path": scen_path})
            print('Before yield scen_list follow')
            yield response.follow(scen_path, callback=self.parseCelebrity)

        # # 演员
        acotor_list = []
        actor_info_html = response.xpath('//div[@id="info"]/span')[2].css('a')
        for actor_info in actor_info_html:
            actor_name = actor_info_html.css('a::text').get()
            actor_path = actor_info_html.css('a::attr(href)').get()
            actor_id = actor_path.split('/')[2]
            acotor_list.append({"id": dire_id, "name": dire_name, "path": actor_path})
            print('Before yield acotor_list follow')
            yield response.follow(actor_path, callback=self.parseCelebrity)


        # https://docs.scrapy.org/en/latest/topics/request-response.html
        print('Before yield movie 对象')
        yield {
          "movie_name": movie_name,
          "create_date": create_date,
          "directors": director_list,
          "scenarist": scen_list,
          "actors": acotor_list,
          "actors": types
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





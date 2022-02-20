import scrapy

class Director(scrapy.Item):
    d_id = Field()
    name_cn = Field()
    name_en = Field()
    gender = Field()
    birthday = Field(serializer=str)
    leaveday = Field(serializer=str)
    birthplace = Field()
    imdb = Field()
    intro = Field()
    photoUrl = Field()


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

        # 导演
        director_list = []
        dire_info_html = response.xpath('//div[@id="info"]/span')[0].css('a')
        print(f'xxxxxxxxxxxx1 {len(dire_info_html)}')
        for dire_html in dire_info_html:
            dire_name = dire_html.css('a::text').get()
            dire_path = dire_html.css('a::attr(href)').get()
            dire_id = dire_path.split('/')[2]
            director = Director(d_id=dire_id, name_cn=dire_name)
            # director_list.append({"id": dire_id, "name": dire_name, "path": dire_path})
            director_list.append(director)
            print(f'xxxxxxxxxxxx2 {director_list}')
            yield response.follow(dire_path, callback=self.parseDirector)

        # 编剧
        scen_list = []
        # scen_info_html = response.xpath('//div[@id="info"]/span')[1]
        # for scen_html in scen_info_html:
        #     scen_name = scen_html.css('a::text').get()
        #     scen_path = scen_html.css('a::attr(href)').get()
        #     scen_id = scen_path.split('/')
        #     scen_list.append({"id": scen_id, "name": scen_name, "path": scen_path})

        # # 演员
        acotor_list = []
        # actor_info_html = response.css('span.actor span.attrs a').getall()
        # for actor_info in actor_info_html:
        #     actor_name = actor_info.css('a::text').get()
        #     actor_path = actor_info.css('a::attr(href)').get()
        #     actor_id = actor_info.split('/')
        #     acotor_list.append({"id": actor_id, "name": actor_name, "path": actor_path})


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

    def parseDirector(self, response):
        director_name = response.xpath('//div[@id="content"]/h1/text()').get()
        print(f'xxxxxxx {director_name}')
        yield {"director_name": director_name}

    def parseActor(self, response):
        pass





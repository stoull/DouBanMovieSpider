import scrapy

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
        directors = response.xpath('//div[@id="info"]/span')[0].css('a::text').getall()
        scenarist = response.xpath('//div[@id="info"]/span')[1].css('a::text').getall()
        actors = response.xpath('//span[@class="actor"]//span[@class="attrs"]/a/text()').getall()
        types = response.xpath('//span[@property="v:genre"]/text()').getall()

        # https://docs.scrapy.org/en/latest/topics/request-response.html
        yield {
          "movie_name": movie_name,
          "create_date": create_date,
          "directors": directors,
          "scenarist": scenarist,
          "actors": actors,
          "actors": types
        }
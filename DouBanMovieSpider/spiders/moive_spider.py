import scrapy

class QuotesSpider(scrapy.Spider):
    name = "movie"

    def start_requests(self):
        urls = [
            'https://movie.douban.com/subject/1291843/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'movie-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
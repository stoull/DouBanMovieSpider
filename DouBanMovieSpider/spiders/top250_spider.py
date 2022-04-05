
import scrapy

# for log
import logging
from scrapy.utils.log import configure_logging

from DouBanMovieSpider.items import Doubantop250Item


class MovieSpider(scrapy.Spider):
	name = 'top_250'
	configure_logging(install_root_handler=False)
	logging.basicConfig(
		filename='scrapy_top_log.txt',
		format='%(levelname)s: %(message)s',
		level=logging.ERROR
	)

	def start_requests(self):
		urls = [
		'https://movie.douban.com/top250?start=0&filter=',
    	'https://movie.douban.com/top250?start=25&filter=',
    	'https://movie.douban.com/top250?start=50&filter=',
    	'https://movie.douban.com/top250?start=75&filter=',
    	'https://movie.douban.com/top250?start=100&filter=',
    	'https://movie.douban.com/top250?start=125&filter=',
    	'https://movie.douban.com/top250?start=150&filter=',
    	'https://movie.douban.com/top250?start=175&filter=',
    	'https://movie.douban.com/top250?start=200&filter=',
    	'https://movie.douban.com/top250?start=225&filter=',
    	'https://movie.douban.com/top250?start=250&filter=',
		]
		
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parseTopPage)

	def parseTopPage(self, response):
		movie_itmes_html = response.xpath('//ol[@class="grid_view"]/li')
		for item_html in movie_itmes_html:
			movie_name = item_html.xpath('div/div/div/a/span')[0].xpath('text()').get()
			movie_url = item_html.xpath('div/div/div/a/@href').get()
			moive_item = Doubantop250Item(name=movie_name, url=movie_url)
			yield moive_item
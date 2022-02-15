# DouBanMovieSpider


电影名：
response.xpath('//span[@property="v:itemreviewed"]/text()').get()
年份：
response.xpath('//span[@class="year"]/text()').get()

导演们：
response.xpath('//div[@id="info"]/span')[0].css('a::text').getall()


编剧们：
response.xpath('//div[@id="info"]/span')[1].css('a::text').getall()

主演们：
response.xpath('//span[@class="actor"]//span[@class="attrs"]/a/text()').getall()


response.xpath('//span[@class="actor"]//span[@class="attrs"]/a/text()').getall()

类型：
response.xpath('//span[@property="v:genre"]/text()').getall()

国家：
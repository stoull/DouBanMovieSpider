# DouBanMovieSpider


scrapy shell -s USER_AGENT='Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko' 'https://movie.douban.com/subject/34447553/'


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

国家,语言，别名，IMDb (需要处理)：
response.xpath('//div[@id="info"]/span/text()').getall()


小海报（大海报需处理）：
response.xpath('//img[@alt="Verdens verste menneske"]').xpath('@src').get()


小图：
https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2669034145.jpg
大图：
https://img9.doubanio.com/view/photo/l/public/p2668815075.jpg

评分：
response.xpath('//strong[@class="ll rating_num"]/text()').get()

简介(需处理换行符)：
response.xpath('//span[@property="v:summary"]/text()').get()
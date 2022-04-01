# DouBanMovieSpider

## 电影页

### xpath html 取值

电影ID：
response.url.split('/')[4]

电影名：
response.xpath('//span[@property="v:itemreviewed"]/text()').get()


年份：
response.xpath('//span[@class="year"]/text()').get()

导演们：
response.xpath('//div[@id="info"]/span')[0].css('a::text').getall()


编剧们：
response.xpath('//div[@id="info"]/span')[1].css('a::text').getall()

主演们：

response.css('span.actor span.attrs a::text').getall()

response.xpath('//span[@class="actor"]//span[@class="attrs"]/a/text()').getall()


response.xpath('//span[@class="actor"]//span[@class="attrs"]/a/text()').getall()

类型：
response.xpath('//span[@property="v:genre"]/text()').getall()

上映时间：
response.xpath('//span[@property="v:initialReleaseDate"]/text()').getall()


国家,语言，别名，IMDb (需要处理)：
response.xpath('//div[@id="info"]/span/text()').getall()

制片国家/地区：
response.xpath('//div[@id="info"]/br/following-sibling::text()').getall()[6]

小海报（大海报需处理）：
response.xpath('//img[@alt="Verdens verste menneske"]').xpath('@src').get()

response.xpath('//img[@alt="The Shawshank Redemption"]').xpath('@src').get()

response.xpath('//img[@rel="v:image"]').xpath('@src').get()

片长:
response.xpath('//span[@property="v:runtime"]/text()').get()
response.xpath('//span[@property="v:runtime"]').xpath('@content').get()

电影url:
https://movie.douban.com/subject/2669034145/

小图：
https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2669034145.jpg

大图：
https://img9.doubanio.com/view/photo/l/public/p2668815075.jpg

评分：
response.xpath('//strong[@class="ll rating_num"]/text()').get()

简介(需处理换行符)：
response.xpath('//span[@property="v:summary"]/text()').get()

#### 喜欢这部电影的人也喜欢
id:
response.xpath('//div[@id="recommendations"]/div/dl')[0].xpath('dt/a/@href').get()
response.xpath('//div[@id="recommendations"]/div/dl')[0].xpath('dt/a/text()').get()
response.xpath('//div[@id="recommendations"]/div/dl')[0].xpath('dt/a').attrib['href']

img:
response.xpath('//div[@id="recommendations"]/div/dl')[0].xpath('dt/a/img/@src').get()

name:
response.xpath('//div[@id="recommendations"]/div/dl')[0].xpath('dt/a/img/@alt').get()

海报：
response.xpath('//div[@id="recommendations"]/div/dl')[0].xpath('dt/a/img').attrib['src']

名字：
response.xpath('//div[@id="recommendations"]/div/dl')[0].xpath('dt/a/img').attrib['alt']

#### 热门短评：

短评id:
response.xpath('//div[@id="hot-comments"]/div')[0].attrib['data-cid']

短评人url：
url:  https://www.douban.com/people/57810485/

response.xpath('//div[@id="hot-comments"]/div')[0].xpath('div/h3').xpath('span[@class="comment-info"]/a/@href').get()

name:
response.xpath('//div[@id="hot-comments"]/div')[0].xpath('div/h3').xpath('span[@class="comment-info"]/a/text()').get()

内容：
response.xpath('//div[@id="hot-comments"]/div')[0].xpath('div/p/span/text()').get()

#### 影评：
影评人URL：
response.xpath('//div[@class="main review-item"]')[0].xpath('header/a/@href').get()

影评人名字：
response.xpath('//div[@class="main review-item"]')[0].xpath('header/a/text()').getall()[-1]

影评url:
response.xpath('//div[@class="main review-item"]')[0].xpath('div/h2/a/@href').get()

影评id:
从影评url截取

影评titel:
response.xpath('//div[@class="main review-item"]')[0].xpath('div/h2/a/text()').get()

影评short-content:
response.xpath('//div[@class="main review-item"]')[0].xpath('div/div/div/text()').getall()


`scrapy shell -s USER_AGENT='Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko' 'https://movie.douban.com/celebrity/1322354/'`

`scrapy shell -s USER_AGENT='Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko' 'https://movie.douban.com/subject/3017916/'`

response.xpath('//div[@class="comment-item"]')[0].xpath('div/div')


## 人物页

scrapy shell -s USER_AGENT='Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko' 'https://movie.douban.com/celebrity/1036727/'

小津安二郎 Yasujirô Ozu： 已故
https://movie.douban.com/celebrity/1036727/

詹姆斯·卡梅隆 James Cameron：健在
https://movie.douban.com/celebrity/1022571/


https://img9.doubanio.com/view/celebrity/raw/public/p33715.jpg

名字：
response.xpath('//div[@id="content"]/h1/text()').get()

最受好评的5部作品

url
response.xpath('//div[@id="best_movies"]').xpath('div[@class="bd"]/ul/li')[0].xpath('div[@class="info"]/a/@href').get()

poster url:
response.xpath('//div[@id="best_movies"]').xpath('div[@class="bd"]/ul/li')[0].xpath('div[@class="pic"]/a/img/@src').get()

name:
response.xpath('//div[@id="best_movies"]').xpath('div[@class="bd"]/ul/li')[0].xpath('div[@class="info"]/a/text()').get()

评分：

response.xpath('//div[@id="best_movies"]').xpath('div[@class="bd"]/ul/li')[0].xpath('div[@class="info"]/em/text()').get()

年份：
response.xpath('//div[@id="best_movies"]').xpath('div[@class="bd"]/ul/li')[0].xpath('div[@class="info"]/div/text()').get()

## 数据表页

### 数据表

电影(movie)：
>
|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER | 电影id, 对应豆瓣上的id，对应的url: https://movie.douban.com/subject/1291543/ |
| name | VARCHAR(200) | 电影名 |
| directors | VARCHAR(200) | 导演 |
| scenarists | VARCHAR(200) | 编剧 |
| actors | VARCHAR(400) | 演员 |
| style | VARCHAR(60) | 类型 |
| year | INTEGER | 电影年份 |
| release_date | VARCHAR(200) | 电影日期 |
| area | VARCHAR(200) | 制片国家/地区 |
| language | VARCHAR(60) | 语言 |
| length | INTEGER | 时长 |
| other_names | VARCHAR(100) | 别名 |
| score | NUMERIC | 评分 |
| rating_number | NUMERIC | 评价人数 |
| synopsis | TEXT | 简介 |
| imdb | VARCHAR(20) | IMDb |
| poster_name | VARCHAR(80) | 海报文件名字含.jpg, 对应的地址为：https://img9.doubanio.com/view/photo/l/public/p2219011938.jpg，小图片为：https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2219011938.jpg|
| filePath | VARCHAR(250) | 电影文件路径 |
| fileUrl | VARCHAR(250) | 电影文件路径 |
| is_downloaded | BLOB | 是否已下载 |
| download_link | VARCHAR(250) | 下载地址 |
| create_date | DATETIME | 数据创建时间 |
| lastWatch_date | DATETIME | 最近观看时间 |
| lastWatch_user | VARCHAR(40) | 最近观看人 |
|`unique (id)`|

导演,编剧, 演员(celebrity: director, scenarist, actor)：
>
|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER |  |
| name | VARCHAR(100) | 名字 |
| gender | BOOLEAN | 性别 |
| zodiac | VARCHAR(10) | 星座 |
| living_time | VARCHAR(100) | 出生及离世时间String |
| birthday | INTEGER | 出生日期 Unix Time, the number of seconds since 1970-01-01 00:00:00 UTC.|
| left_day | INTEGER | 离世日期 Unix Time, the number of seconds since 1970-01-01 00:00:00 UTC.|
| birthplace | VARCHAR(100) | 出生地 |
| occupation | VARCHAR(100) | 职业 |
| is_director | BLOB | 是否是导演 |
| is_scenarist | BLOB | 是否是编剧 |
| is_actor | BLOB | 是否是演员 |
| names_cn | VARCHAR(250) | 更多中文名 |
| names_en | VARCHAR(250) | 更多英文名 |
| family | VARCHAR(200) | 家庭成员 |
| imdb | VARCHAR(20) | IMDB编号 |
| intro | TEXT | 影人简介 |
| portrait_name | VARCHAR(80) | 头像文件名字.jpg, 对应的地址为：https://img9.doubanio.com/view/celebrity/raw/public/p1391831466.59.jpg |
| create_date | DATETIME | 数据创建时间 |
|`unique (id)`|

最受好评的5部作品(best_movies):
>
|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER | best_movies  id |
| celebrity_id | INTEGER | 对应的人物id |
| movie_brief_id | INTEGER | 简略信息电影（movie_brief）的id |
| FK_celebrity_id | FOREIGN KEY (celebrity_id) REFERENCES celebrity(id)|  |
| FK_movie_brief_id | FOREIGN KEY (movie_brief_id) REFERENCES movie_brief(id)|  |
|`unique (id)`|

喜欢这部电影的人也喜欢(recommendations)：
>
|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER | recommendation  id |
| reference_movie_id | INTEGER | 对应主电影的id |
| movie_brief_id | INTEGER | 简略信息电影（movie_brief）的id |
| FK_reference_movie_id | FOREIGN KEY (reference_movie_id) REFERENCES movie(id)|  |
| FK_movie_brief_id | FOREIGN KEY (movie_brief_id) REFERENCES movie_brief(id)|  |
|`unique (id)`|

电影的简略信息(movie_brief):
>
|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER | 电影id |
| name | VARCHAR(200) | 电影名 |
| score | NUMERIC | 评分 |
| year | INTEGER | 电影年份 |
| poster_name | VARCHAR(80) | 海报文件名字含.jpg, 对应的地址为：https://img9.doubanio.com/view/photo/l/public/p2219011938.jpg，小图片为：https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2219011938.jpg|
|`unique (id)`|

短评(hot_comment)：
>
|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER | 短评id |
| movie_id | INTEGER | 对应电影的id |
| content | TEXT | 短评内容 |
| reviewer_name | VARCHAR(40) | 此条短评的作者的名称 |
| reviewer_id | VARCHAR(20) | 对应的url: https://www.douban.com/people/57810485/ |
|`unique (id)`|


影评(review)：
>
|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER | 影评id, 对应的url:https://movie.douban.com/review/13985361/ |
| movie_id | INTEGER | 对应电影的id |
| title | VARCHAR(150) | 影评标题 |
| content_short | TEXT | 影评的缩略内容 |
| content | TEXT | 影评的全部内容 |
| reviewer_name | VARCHAR(40) | 此条短评的作者的名称 |
| reviewer_id | VARCHAR(20) | 此条短评的作者，对应的url: https://www.douban.com/people/57810485/ |
|`unique (id)`|

地区(area)：
>
|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER |  |
| name | VARCHAR(20) |  |
|`unique (name)`|

电影类型(type)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER |  |
| name | VARCHAR(40) |  |
|`unique (name)`|

电影标签(tag)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER |  |
| name | VARCHAR(40) |  |
|`unique (name)`|

电影语言(language)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER |  |
| name | VARCHAR(30) |  |
|`unique (name)`|

### 关系表

电影_导演(movie_director)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| movie_id | INTEGER |  |
| celebrity_id | INTEGER |  |
| FK_movie_id | FOREIGN KEY (movie_id) REFERENCES movie(id)|  |
| FK_celebrity_id | FOREIGN KEY (celebrity_id) REFERENCES celebrity(id)|  |

电影_演员(movie_actor)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| movie_id | INTEGER |  |
| celebrity_id | INTEGER |  |
| FK_movie_id | FOREIGN KEY (movie_id) REFERENCES movie(id)|  |
| FK_celebrity_id | FOREIGN KEY (celebrity_id) REFERENCES celebrity(id)|  |


电影_编剧(movie_scenarist)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| movie_id | INTEGER |  |
| celebrity_id | INTEGER |  |
| FK_movie_id | FOREIGN KEY (movie_id) REFERENCES movie(id)|  |
| FK_celebrity_id | FOREIGN KEY (celebrity_id) REFERENCES celebrity(id)|  |


电影_地区(movie_area)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| movie_id | INTEGER |  |
| area_id | INTEGER |  |
| FK_movie_id | FOREIGN KEY (movie_id) REFERENCES movie(id)|  |
| FK_area_id | FOREIGN KEY (area_id) REFERENCES area(id)|  |


电影_类型(movie_type)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| movie_id | INTEGER |  |
| type_id | INTEGER |  |
| FK_movie_id | FOREIGN KEY (movie_id) REFERENCES movie(id)|  |
| FK_type_id | FOREIGN KEY (type_id) REFERENCES type(id)|  |


电影_标签(movie_tag)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| movie_id | INTEGER |  |
| tag_id | INTEGER |  |
| FK_movie_id | FOREIGN KEY (movie_id) REFERENCES movie(id)|  |
| FK_tag_id | FOREIGN KEY (tag_id) REFERENCES tag(id)|  |


电影_语言(movie_language)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| movie_id | INTEGER |  |
| language_id | INTEGER |  |
| FK_movie_id | FOREIGN KEY (movie_id) REFERENCES movie(id)|  |
| FK_language_id | FOREIGN KEY (language_id) REFERENCES language(id)|  |

人物_地区(celebrity_area)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| celebrity_id | INTEGER |  |
| area_id | INTEGER |  |
| FK_celebrity_id | FOREIGN KEY (celebrity_id) REFERENCES celebrity(id)|  |
| FK_area_id | FOREIGN KEY (area_id) REFERENCES area(id)|  |

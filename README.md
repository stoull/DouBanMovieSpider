# DouBanMovieSpider

## 电影页
scrapy shell -s USER_AGENT='Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko' 'https://movie.douban.com/subject/34447553/'


scrapy shell -s USER_AGENT='Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko' 'https://movie.douban.com/subject/27203644/?from=showing'

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



## 人物页

小津安二郎 Yasujirô Ozu：
https://movie.douban.com/celebrity/1036727/

scrapy shell -s USER_AGENT='Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko' 'https://movie.douban.com/celebrity/1036727/'

名字：
response.xpath('//div[@id="content"]/h1/text()').get()


电影(movie)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER | 电影id, 对应豆瓣上的id |
| name | VARCHAR(40) | 电影名 |
| releaseDate | DATE | 电影日期 |
| language | VARCHAR(20) | 语言 |
| length | REAL | 时长 |
| otherNames | VARCHAR(100) | 别名 |
| score | INT | 评分 |
| synopsis | TEXT | 简介 |
| doubanUrl | VARCHAR(200) | 对应豆瓣的url |
| filePath | VARCHAR(200) | 电影文件路径 |
| fileUrl | VARCHAR(200) | 电影文件路径 |
| posterUrl | VARCHAR(200) | 电影海报路径 |
| iconUrl | VARCHAR(200) | 电影图标路径 |
| createDate | DATETIME | 电影数据创建 |
| lastWatchDate | DATETIME | 最近观看时间 |
| lastWatchUser | VARCHAR(40) | 最近观看人 |

导演(director)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER |  |
| name_cn | VARCHAR(100) | 中文名 |
| name_en | VARCHAR(100) | 英文名 |
| gender | BOOLEAN | 性别 |
| birthday | DATE | 出生日期 |
| leaveday | DATE | 离世日期 |
| birthplace | VARCHAR(100) | 出生地 |
| imdb | VARCHAR(20) | IMDB编号 |
| intro | TEXT | 影人简介 |
| photoUrl | VARCHAR(200) | 头像 |


编剧(scenarist)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER |  |
| name_cn | VARCHAR(40) | 中文名 |
| name_en | VARCHAR(40) | 英文名 |
| gender | BOOLEAN | 性别 |
| birthday | DATETIME | 出生日期 |
| leaveday | DATE | 离世日期 |
| birthplace | VARCHAR(20) | 出生地 |

演员(actor)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER |  |
| name_cn | VARCHAR(40) | 中文名 |
| name_en | VARCHAR(40) | 英文名 |
| gender | BOOLEAN | 性别 |
| birthday | DATE | 出生日期 |
| leaveday | DATE | 离世日期 |
| birthplace | VARCHAR(20) | 出生地 |

地区(area)：
>
|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER |  |
| name | VARCHAR(20) |  |

电影类型(type)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER |  |
| name | VARCHAR(40) |  |

电影标签(tag)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER |  |
| name | VARCHAR(40) |  |

用户(user)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER |  |
| name | VARCHAR(20) | 名字 |
| alias | VARCHAR(20) | 别名 |
| email | VARCHAR(20) | 邮箱 |
| gender | INT | 性别 |
| phoneNumber | VARCHAR(20) | 电话号码 |
| introduction | TEXT | 绍介 |
| createDate | DATETIME | 创建日期 |
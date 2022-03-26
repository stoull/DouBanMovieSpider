import scrapy
import re
import time
import json
from datetime import datetime

# for log
import logging
from scrapy.utils.log import configure_logging

from DouBanMovieSpider.items import Moive, Celebrity, ImageItem
from DouBanMovieSpider.database import DBManager


class QuotesSpider(scrapy.Spider):
    #  Logging https://docs.scrapy.org/en/latest/topics/logging.html
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='scrapy_log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.ERROR
    )

    name = "movie"
    db = DBManager()

    def start_requests(self):
        urls = [
            'https://movie.douban.com/subject/1291543/',
            'https://movie.douban.com/subject/27079318/',
            'https://movie.douban.com/subject/4719384/',
            'https://movie.douban.com/subject/27172891/',
            'https://movie.douban.com/subject/26752088/',
            'https://movie.douban.com/subject/27110296/',
            'https://movie.douban.com/subject/1296436/',
            'https://movie.douban.com/subject/1303173/',
            'https://movie.douban.com/subject/3036997/',
            'https://movie.douban.com/subject/1299661/',
            'https://movie.douban.com/subject/1461403/',
            'https://movie.douban.com/subject/4876722/',
            'https://movie.douban.com/subject/3734112/',
            'https://movie.douban.com/subject/25921812/',
            'https://movie.douban.com/subject/1306490/',
            'https://movie.douban.com/subject/1301136/',
            'https://movie.douban.com/subject/1292330/',
            'https://movie.douban.com/subject/1294194/',
            'https://movie.douban.com/subject/3629230/',
            'https://movie.douban.com/subject/2136171/',
            'https://movie.douban.com/subject/5343752/',
            'https://movie.douban.com/subject/1761854/',
            'https://movie.douban.com/subject/3724118/',
            'https://movie.douban.com/subject/1292365/',
            'https://movie.douban.com/subject/1306505/',
            'https://movie.douban.com/subject/1303037/',
            'https://movie.douban.com/subject/1292434/',
            'https://movie.douban.com/subject/1292329/',
            'https://movie.douban.com/subject/1291557/',
            'https://movie.douban.com/subject/1291999/',
            'https://movie.douban.com/subject/1309087/',
            'https://movie.douban.com/subject/26872545/',
            'https://movie.douban.com/subject/1301897/',
            'https://movie.douban.com/subject/1296177/',
            'https://movie.douban.com/subject/1303465/',
            'https://movie.douban.com/subject/1303471/',
            'https://movie.douban.com/subject/1307745/',
            'https://movie.douban.com/subject/1303444/',
            'https://movie.douban.com/subject/1303521/',
            'https://movie.douban.com/subject/24525283/',
            'https://movie.douban.com/subject/1303525/',
            'https://movie.douban.com/subject/1291556/',
            'https://movie.douban.com/subject/1298248/',
            'https://movie.douban.com/subject/1295656/',
            'https://movie.douban.com/subject/1294531/',
            'https://movie.douban.com/subject/1299248/',
            'https://movie.douban.com/subject/6518638/',
            'https://movie.douban.com/subject/1408101/',
            'https://movie.douban.com/subject/26766869/',
            'https://movie.douban.com/subject/1296147/',
            'https://movie.douban.com/subject/1297268/',
            'https://movie.douban.com/subject/1422088/',
            'https://movie.douban.com/subject/3285632/',
            'https://movie.douban.com/subject/1416898/',
            'https://movie.douban.com/subject/1292218/',
            'https://movie.douban.com/subject/24750126/',
            'https://movie.douban.com/subject/1782378/',
            'https://movie.douban.com/subject/1306019/',
            'https://movie.douban.com/subject/1306559/',
            'https://movie.douban.com/subject/1295720/',
            'https://movie.douban.com/subject/4221335/',
            'https://movie.douban.com/subject/30391726/',
            'https://movie.douban.com/subject/10535568/',
            'https://movie.douban.com/subject/30310218/',
            'https://movie.douban.com/subject/1769507/',
            'https://movie.douban.com/subject/30257175/',
            'https://movie.douban.com/subject/2009392/',
            'https://movie.douban.com/subject/2935729/',
            'https://movie.douban.com/subject/1305092/',
            'https://movie.douban.com/subject/25958717/',
            'https://movie.douban.com/subject/1300956/',
            'https://movie.douban.com/subject/2078398/',
            'https://movie.douban.com/subject/26614893/',
            'https://movie.douban.com/subject/1291831/',
            'https://movie.douban.com/subject/34447553/',
            'https://movie.douban.com/subject/35293160/',
            'https://movie.douban.com/subject/1291877/',
            'https://movie.douban.com/subject/1293388/',
            'https://movie.douban.com/subject/1302675/',
            'https://movie.douban.com/subject/1293632/',
            'https://movie.douban.com/subject/1294140/',
            'https://movie.douban.com/subject/1296976/',
            'https://movie.douban.com/subject/1294782/',
            'https://movie.douban.com/subject/1302413/',
            'https://movie.douban.com/subject/2342769/',
            'https://movie.douban.com/subject/1303536/',
            'https://movie.douban.com/subject/1401619/',
            'https://movie.douban.com/subject/1292048/',
            'https://movie.douban.com/subject/1292047/',
            'https://movie.douban.com/subject/1292049/',
            'https://movie.douban.com/subject/1293350/',
        ]

        for url in urls:
            # yield  scrapy.Request(url=url, callback=self.parseIpLocation)
            m_id = int(url.split('/')[4])
            if not self.db.isMovieExist(m_id):
                yield scrapy.Request(url=url, callback=self.parseCelebrity)
            else:
                print("Movie Does Exist")

        #  test the proxy with ip
        # yield scrapy.Request(url='https://httpbin.org/ip', callback=self.parseIpLocation)

    #  用于测试代理时的ip地址， https://httpbin.org/ip
    def parseIpLocation(self, response):
        jsonresponse = json.loads(response.text)
        print(jsonresponse)

        # imageItem = ImageItem()
        # imageItem['image_urls'] = ['https://img9.doubanio.com/view/photo/l/public/p1374588202.jpg',]
        # yield imageItem

    def parseMovie(self, response):
        movie_id = response.url.split('/')[4]

        director_names = ""
        dire_info_html = response.xpath('//div[@id="info"]/span')[0].css('a')
        for dire_html in dire_info_html:
            dire_name = dire_html.css('a::text').get()
            dire_path = dire_html.css('a::attr(href)').get()
            if 'celebrity/' in dire_path:
                dire_id = int(dire_path.split('/')[2])
                if director_names:
                    director_names = director_names + ", " + dire_name
                else:
                    director_names = dire_name
                if not self.db.isDirectorExist(dire_id):
                    yield response.follow(dire_path, callback=self.parseCelebrity,
                                          meta={'movie_id': movie_id, 'type': 'Director'}, dont_filter=True)
                else:
                    print("Director Does Exist")
            else:
                if director_names:
                    director_names = director_names + ", " + dire_name
                else:
                    director_names = dire_name

        # 编剧
        scen_names = ""
        scen_info_html = response.xpath('//div[@id="info"]/span')[1].css('a')
        for scen_html in scen_info_html:
            scen_name = scen_html.css('a::text').get()
            scen_path = scen_html.css('a::attr(href)').get()
            if 'celebrity/' in scen_path:
                scen_id = int(scen_path.split('/')[2])
                if scen_names:
                    scen_names = scen_names + ", " + scen_name
                else:
                    scen_names = scen_name
                if not self.db.isScenaristExist(scen_id):
                    yield response.follow(scen_path, callback=self.parseCelebrity,
                                          meta={'movie_id': movie_id, 'type': 'Scenarist'}, dont_filter=True)
                else:
                    print("Scenarist Does Exist")
            else:
                if scen_names:
                    scen_names = scen_names + ", " + scen_name
                else:
                    scen_names = scen_name


        # # 演员
        actor_names = ""
        actor_info_html = response.xpath('//div[@id="info"]/span')[2].css('a')
        maximum_count = 0  # The maximum acotors to crawl
        for actor_html in actor_info_html:
            if maximum_count < 6:
                actor_name = actor_html.css('a::text').get()
                actor_path = actor_html.css('a::attr(href)').get()
                if 'celebrity/' in actor_path:
                    actor_id = int(actor_path.split('/')[2])
                    if actor_names:
                        actor_names = actor_names + ", " + actor_name
                    else:
                        actor_names = actor_name
                    if not self.db.isActorExist(actor_id):
                        yield response.follow(actor_path, callback=self.parseCelebrity,
                                          meta={'movie_id': movie_id, 'type': 'Actor'})
                    else:
                        print("Actor Does Exist")
                else:
                    if actor_names:
                        actor_names = actor_names + ", " + actor_name
                    else:
                        actor_names = actor_name
            else:
                break
            maximum_count += 1

        # 解析电影信息
        movie_name = response.xpath('//span[@property="v:itemreviewed"]/text()').get()
        year_String = response.xpath('//span[@class="year"]/text()').get()
        year_int = int(re.sub('[()]', '', year_String))  # 移除（）并转成Int
        types = response.xpath('//span[@property="v:genre"]/text()').getall()
        release_dates = response.xpath('//span[@property="v:initialReleaseDate"]/text()').getall()
        info_br_sibling_html = response.xpath('//div[@id="info"]/br/following-sibling::text()').getall()

        all_title_string = response.xpath('//span[@class="pl"]/text()').getall()
        all_title_string = "".join(all_title_string)
        all_title_string = re.sub(r"[\n\t()| ·]*", "", all_title_string)

        area_index = 4+len(types)
        if "主演" not in all_title_string:
            area_index = area_index-1
        if "编剧" not in all_title_string:
            area_index = area_index-1
        
        area = info_br_sibling_html[area_index]
        languages = info_br_sibling_html[area_index+2]  # 8

        otherNames = " "
        if "又名" in all_title_string:
            if "IMDb" in all_title_string:
                otherNames = info_br_sibling_html[-4]
            else:
                otherNames = info_br_sibling_html[-2]
        
        lenght = response.xpath('//span[@property="v:runtime"]').xpath('@content').get()
        score = response.xpath('//strong[@class="ll rating_num"]/text()').get()
        ratingPeople = response.xpath('//span[@property="v:votes"]/text()').get()
        if score is None:
            score = 0
        else:
            score_float = float(score)
        ratingPeople_int = int(ratingPeople)
        synopsis = response.xpath('//span[@property="v:summary"]/text()').getall()
        synopsisStr = "".join(synopsis)
        if synopsisStr is not None:
            synopsisStr = synopsisStr.strip()  # 移除说明中的多有的空格及换行
            synopsisStr = re.sub(r"[\n\t]*", "", synopsisStr)   # 移除说明中的多有的空格及换行
        if "IMDb" in all_title_string:
            imdb = info_br_sibling_html[-2]  # 17
            if otherNames == imdb:
                otherNames = ""

        doubanUrl = response.url
        iconUrl = response.xpath('//img[@rel="v:image"]').xpath('@src').get()
        posterUrl = "https://img9.doubanio.com/view/photo/l/public/" + iconUrl.split('/')[-1]


        movie = Moive(m_id=movie_id, name=movie_name, year=year_int, directors=director_names, scenarists=scen_names, actors=actor_names)
        movie['style'] = " / ".join(types)
        movie['releaseDate'] = " / ".join(release_dates)
        movie['area'] = area[1:]  # 移除最前面的空格
        movie['language'] = languages[1:]  # 移除最前面的空格
        movie['length'] = int(lenght)
        movie['otherNames'] = otherNames[1:]  # 移除最前面的空格
        movie['score'] = score_float
        movie['ratingPeople'] = ratingPeople_int
        movie['synopsis'] = synopsisStr
        movie['imdb'] = imdb[1:]  # 移除最前面的空格
        movie['doubanUrl'] = doubanUrl
        movie['posterUrl'] = posterUrl
        movie['iconUrl'] = iconUrl

        imageItem = ImageItem()
        imageItem['image_urls'] = [posterUrl, ]
        yield imageItem

        # https://docs.scrapy.org/en/latest/topics/request-response.html
        print(f'movie 对象: {movie}')
        yield movie

    # 解析导演信息
    def parseCelebrity(self, response):
        director_id = response.url.split('/')[4]
        director_name = response.xpath('//div[@id="content"]/h1/text()').get()
        photoUrl = response.xpath('//div[@class="nbg"]/img').xpath('@src').get()

        introArray = response.xpath('//span[@class="all hidden"]/text()').getall()
        if len(introArray) == 0:
            introArray = response.xpath('//span[@class="short"]/text()').getall()
        intro = "".join(introArray)
        if len(introArray) == 0:
            bdContent = response.xpath('//div[@class="bd"]/text()').getall()
            if len(bdContent) > 4:
                intro = bdContent[4]
            else:
                intro = None

        intro = intro.strip()  # 移除说明中的多有的空格及换行
        intro = re.sub(r"[\n\t]*", "", intro)  # 移除说明中的多有的空格及换行

        movie_id = response.meta.get('movie_id')
        # movie_id = 3629230
        res_Type = response.meta.get('type')
        # res_Type = 'Actor' #  response.meta.get('type')

        director = Celebrity(type=res_Type, movie_id=movie_id, d_id=director_id, name=director_name)
        # if res_Type == 'Director':
        #     director = Celebrity(d_id=director_id, name=director_name)
        # elif res_Type == 'Actor':
        #     director = Actor(d_id=director_id, name=director_name)
        # elif res_Type == 'Scenarist':
        #     director = Scenarist(d_id=director_id, name=director_name)
        # else:
        #     return
        
        all_info_li_html = response.xpath('//div[@class="info"]/ul/li')
        for li in all_info_li_html:
            li_name = li.css('span::text').get()
            li_value_str = li.css('li::text').getall()[1]
            li_value = re.sub(r"[\n\t\s:]*", "", li_value_str)  # 移除值中的所有空格及换行
            if li_name == "性别":
                director['gender'] = li_value
            elif li_name == "星座":
                director['zodiac'] = li_value
            elif li_name == "出生日期":
                director['livingTime'] = li_value
                li_value = re.sub(r"[+]", "", li_value)
                # 1925年08月29日 形式
                dateString = re.sub(r"[^0-9]", "-", li_value)
                dateString = dateString[:-1]
                if len(dateString) == 4:
                    # 1925年 形式
                    datetime_obj = datetime.strptime(dateString, '%Y')
                elif len(dateString) == 7:
                    # 1963年04月 形式
                    datetime_obj = datetime.strptime(dateString, '%Y-%m')
                else:
                    datetime_obj = datetime.strptime(dateString, '%Y-%m-%d')
                director['birthday'] = time.mktime(datetime_obj.timetuple())
            elif li_name == "生卒日期":
                director['livingTime'] = li_value
                li_value = re.sub(r"[ +]", "", li_value)
                # +1903年12月12日 至 +1963年12月12日 及 1956年09月12日 至 2003年04月01日 形式 1890年09月30日 至 1980年05月08日
                dateStrArray = li_value.split('至')
                dateRawString1 = dateStrArray[0]
                dateRawString2 = dateStrArray[1]
                dateString1 = re.sub(r"[^0-9]", "-", dateRawString1)
                dateString2 = re.sub(r"[^0-9]", "-", dateRawString2)
                dateString1 = dateString1[0:-1]
                dateString2 = dateString2[0:-1]
                if len(dateString1) == 7:
                    datetime_object1 = datetime.strptime(dateString1, '%Y-%m')
                    datetime_object2 = datetime.strptime(dateString2, '%Y-%m')
                else:
                    datetime_object1 = datetime.strptime(dateString1, '%Y-%m-%d')
                    datetime_object2 = datetime.strptime(dateString2, '%Y-%m-%d')
                min_day = datetime(1900, 1, 1)
                if datetime_object1 < min_day:
                    epoch = datetime(1970, 1, 1)
                    birthday_diff = datetime_object1-epoch
                    leaveday_diff = datetime_object2-epoch
                    birthday = birthday_diff.total_seconds()
                    leaveday = leaveday_diff.total_seconds()
                else:
                    birthday = time.mktime(datetime_object1.timetuple())
                    leaveday = time.mktime(datetime_object2.timetuple())
                director['birthday'] = birthday
                director['leaveday'] = leaveday

            elif li_name == "出生地":
                director['birthplace'] = li_value
            elif li_name == "职业":
                director['occupation'] = li_value
            elif li_name == "更多外文名":
                director['names_en'] = li_value
            elif li_name == "更多中文名":
                director['names_cn'] = li_value
            elif li_name == "家庭成员":
                director['family'] = li_value
            elif li_name == "imdb编号":
                director['imdb'] = li.css('a::text').get()
        director['photoUrl'] = photoUrl
        imageItem = ImageItem()
        imageItem['image_urls'] = [photoUrl, ]
        yield imageItem
        director['intro'] = intro
        yield director
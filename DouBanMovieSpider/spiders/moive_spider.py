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
            'https://movie.douban.com/celebrity/1337634/',
        ]

        for url in urls:
            # yield  scrapy.Request(url=url, callback=self.parseIpLocation)
            m_id = int(url.split('/')[4])
            if not self.db.isMovieExist(m_id):
                yield scrapy.Request(url=url, callback=self.parseMovie)
            else:
                print(f"Movie Does Exist: {url}")

        #  test the proxy with ip
        # yield scrapy.Request(url='https://httpbin.org/ip', callback=self.parseIpLocation)

    #  用于测试代理时的ip地址， https://httpbin.org/ip
    def parseIpLocation(self, response):
        jsonresponse = json.loads(response.text)
        print(jsonresponse)

        # imageItem = ImageItem()
        # imageItem['image_urls'] = ['https://img9.doubanio.com/view/photo/l/public/p2219011938.jpg',]
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
                    print(f"Director Does Exist:{dire_name}: {dire_id}")
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
                    print(f"Scenarist Does Exist: {scen_name}: {scen_id}")
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
                        print(f"Actor Does Exist: {actor_name}: {actor_id}")
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

        area_index = 4 + len(types)
        if "主演" not in all_title_string:
            area_index = area_index - 1
        if "编剧" not in all_title_string:
            area_index = area_index - 1

        area = info_br_sibling_html[area_index]
        languages = info_br_sibling_html[area_index + 2]  # 8

        otherNames = " "
        if "又名" in all_title_string:
            if "IMDb" in all_title_string:
                otherNames = info_br_sibling_html[-4]
            else:
                otherNames = info_br_sibling_html[-2]

        # 片长解析
        lenght = response.xpath('//span[@property="v:runtime"]').xpath('@content').get()
        if lenght is None:
            if "片长" in all_title_string:
                lenght = info_br_sibling_html[-6]
                print(f"xxxxxxx : {lenght}")
                if lenght is not None:
                    lenght = re.findall(r'\d+', lenght)[0]
                else:
                    lenght = '0'
            else:
                lenght = '0'

        score = response.xpath('//strong[@class="ll rating_num"]/text()').get()
        ratingPeople = response.xpath('//span[@property="v:votes"]/text()').get()
        if score is None:
            score_float = 0
        else:
            score_float = float(score)
        if ratingPeople is None:
            ratingPeople_int = 0
        else:
            ratingPeople_int = int(ratingPeople)
        synopsis = response.xpath('//span[@property="v:summary"]/text()').getall()
        synopsisStr = "".join(synopsis)
        if synopsisStr is not None:
            synopsisStr = synopsisStr.strip()  # 移除说明中的多有的空格及换行
            synopsisStr = re.sub(r"[\n\t]*", "", synopsisStr)  # 移除说明中的多有的空格及换行
        if "IMDb" in all_title_string:
            imdb = info_br_sibling_html[-2]  # 17
            if otherNames == imdb:
                otherNames = ""
        else:
            imdb = ""

        doubanUrl = response.url
        iconUrl = response.xpath('//img[@rel="v:image"]').xpath('@src').get()
        posterUrl = "https://img9.doubanio.com/view/photo/l/public/" + iconUrl.split('/')[-1]

        movie = Moive(m_id=movie_id, name=movie_name, year=year_int, directors=director_names, scenarists=scen_names,
                      actors=actor_names)
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
        # print(f'movie 对象: {movie}')
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
                if li_value is not None:
                    director['livingTime'] = li_value
                    li_value = re.sub(r"[+]", "", li_value)  # 移除值中的所有+号
                    # 1925年08月29日 形式
                    dateString = re.sub(r"[^0-9]", "-", li_value)  # 将所有的非数字转为-
                    if dateString[0] is '-':
                        dateString = dateString[1:]
                    if dateString[-1] is '-':
                        dateString = dateString[:-1]

                    datetime_obj = None
                    try:
                        datetime_obj = datetime.strptime(dateString, '%Y-%m-%d')
                    except ValueError as e:
                        try:
                            datetime_obj = datetime.strptime(dateString, '%Y-%m')
                        except ValueError:
                            try:
                                datetime_obj = datetime.strptime(dateString, '%Y')
                            except ValueError:
                                print("Not found correct format for datetime")
                    if datetime_obj is not None:
                        director['birthday'] = time.mktime(datetime_obj.timetuple())
            elif li_name == "生卒日期":
                director['livingTime'] = li_value
                li_value = re.sub(r"[+]", "", li_value)
                # +1903年12月12日 至 +1963年12月12日 及 1956年09月12日 至 2003年04月01日 形式 1890年09月30日 至 1980年05月08日
                dateStrArray = li_value.split('至')
                bornRawString = dateStrArray[0]
                leaveRawString = dateStrArray[1]
                bornDateString = re.sub(r"[^0-9]", "-", bornRawString)
                leaveDateString = re.sub(r"[^0-9]", "-", leaveRawString)

                if bornDateString[0] is '-':
                    bornDateString = bornDateString[1:]
                if bornDateString[-1] is '-':
                    bornDateString = bornDateString[:-1]

                if leaveDateString[0] is '-':
                    leaveDateString = leaveDateString[1:]
                if leaveDateString[-1] is '-':
                    leaveDateString = leaveDateString[:-1]

                bornDatetime = None
                leaveDatetime = None
                try:
                    bornDatetime = datetime.strptime(bornDateString, '%Y-%m-%d')
                except ValueError as e:
                    try:
                        bornDatetime = datetime.strptime(bornDateString, '%Y-%m')
                    except ValueError:
                        try:
                            bornDatetime = datetime.strptime(bornDateString, '%Y')
                        except ValueError:
                            print("Not found correct format for datetime")

                try:
                    leaveDatetime = datetime.strptime(leaveDateString, '%Y-%m-%d')
                except ValueError as e:
                    try:
                        leaveDatetime = datetime.strptime(leaveDateString, '%Y-%m')
                    except ValueError:
                        try:
                            leaveDatetime = datetime.strptime(leaveDateString, '%Y')
                        except ValueError:
                            print("Not found correct format for datetime")

                min_day = datetime(1900, 1, 1)
                if bornDatetime is not None:
                    if bornDatetime < min_day:
                        epoch = datetime(1970, 1, 1)
                        bornday_diff = bornDatetime - epoch
                        birthday = bornday_diff.total_seconds()
                    else:
                        birthday = time.mktime(bornDatetime.timetuple())
                    director['birthday'] = birthday

                if leaveDatetime is not None:
                    if leaveDatetime < min_day:
                        epoch = datetime(1970, 1, 1)
                        leaveday_diff = leaveDatetime - epoch
                        leaveday = leaveday_diff.total_seconds()
                    else:
                        leaveday = time.mktime(leaveDatetime.timetuple())
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

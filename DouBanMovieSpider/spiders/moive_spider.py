import scrapy
import re
import time
from datetime import datetime

from DouBanMovieSpider.items import Moive,Director,Scenarist,Actor
from scrapy.loader import ItemLoader

class QuotesSpider(scrapy.Spider):
    name = "movie"

# 'https://movie.douban.com/subject/1440347/' 修罗雪姬 少演员

# 'https://movie.douban.com/subject/1292052/' 肖申克的救赎 两编剧

# 'https://movie.douban.com/subject/1291546/' 霸王别姬

# 'https://movie.douban.com/subject/1292722/' 泰坦尼克号

# ‘https://movie.douban.com/subject/1293764/’ 与狼共舞  无又名

# 小津安二郎 Yasujirô Ozu： 已故
# https://movie.douban.com/celebrity/1036727/

# 詹姆斯·卡梅隆 James Cameron：健在
# https://movie.douban.com/celebrity/1022571/


    def start_requests(self):
        urls = [
            'https://movie.douban.com/subject/1293764/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 获取导演信息
        director_list = []
        director_names = ""
        dire_info_html = response.xpath('//div[@id="info"]/span')[0].css('a')
        for dire_html in dire_info_html:
            dire_name = dire_html.css('a::text').get()
            dire_path = dire_html.css('a::attr(href)').get()
            if 'celebrity/' in dire_path:
                dire_id = dire_path.split('/')[2]
                if director_names:
                    director_names = director_names + ", " + dire_name
                else:
                    director_names = dire_name
                director_list.append({"id": dire_id, "name": dire_name, "path": dire_path})
                print(f'Before yield director follow: {dire_path}')
                # yield response.follow(dire_path, callback=self.parseCelebrity)

        # 编剧
        scen_list = []
        scen_names = ""
        scen_info_html = response.xpath('//div[@id="info"]/span')[1].css('a')
        for scen_html in scen_info_html:
            scen_name = scen_html.css('a::text').get()
            scen_path = scen_html.css('a::attr(href)').get()
            if 'celebrity/' in scen_path:
                scen_id = scen_path.split('/')[2]
                if scen_names:
                    scen_names = scen_names + ", " + scen_name
                else:
                    scen_names = scen_name
                scen_list.append({"id": dire_id, "name": dire_name, "path": scen_path})
                print(f'Before yield scen_list follow: {scen_path}')
                # yield response.follow(scen_path, callback=self.parseCelebrity)

        # # 演员
        acotor_list = []
        acotor_names = ""
        actor_info_html = response.xpath('//div[@id="info"]/span')[2].css('a')
        for actor_html in actor_info_html:
            actor_name = actor_html.css('a::text').get()
            actor_path = actor_html.css('a::attr(href)').get()
            if 'celebrity/' in actor_path:
                actor_id = actor_path.split('/')[2]
                if acotor_names:
                    acotor_names = acotor_names + ", " + actor_name
                else:
                    acotor_names = actor_name
                acotor_list.append({"id": dire_id, "name": dire_name, "path": actor_path})
                print(f'Before yield acotor_list follow: {actor_path}')
                # yield response.follow(actor_path, callback=self.parseCelebrity)


        # 解析电影信息
        movie_id = response.url.split('/')[4]
        movie_name = response.xpath('//span[@property="v:itemreviewed"]/text()').get()
        year_String = response.xpath('//span[@class="year"]/text()').get()
        year_int = int(re.sub('[()]', '', year_String)) # 移除（）并转成Int
        types = response.xpath('//span[@property="v:genre"]/text()').getall()
        release_dates = response.xpath('//span[@property="v:initialReleaseDate"]/text()').getall()
        info_br_sibling_html = response.xpath('//div[@id="info"]/br/following-sibling::text()').getall()

        area_index = 4+len(types)
        area = info_br_sibling_html[area_index]
        languages = info_br_sibling_html[area_index+2] # 8
        otherNames = info_br_sibling_html[area_index+9] # 15
        score = response.xpath('//strong[@class="ll rating_num"]/text()').get()
        lenght = response.xpath('//span[@property="v:runtime"]').xpath('@content').get()
        score_float = float(score)
        synopsis = response.xpath('//span[@property="v:summary"]/text()').getall()
        imdb = info_br_sibling_html[-2] #17
        if otherNames == imdb:
            otherNames=""
        doubanUrl = response.url
        iconUrl = response.xpath('//img[@rel="v:image"]').xpath('@src').get()
        posterUrl = "https://img9.doubanio.com/view/photo/l/public/" + iconUrl.split('/')[-1]

        movie = Moive(m_id=movie_id, name=movie_name, year=year_int, directors=director_names, scenarists=scen_names, actors=acotor_names)
        movie['style'] = " / ".join(types)
        movie['releaseDate'] = " / ".join(release_dates)
        movie['area'] = area[1:] # 移除最前面的空格
        movie['language'] = languages[1:] # 移除最前面的空格
        movie['length'] = int(lenght)
        movie['otherNames'] = otherNames[1:] # 移除最前面的空格
        movie['score'] = score_float
        movie['synopsis'] = "".join(synopsis)
        movie['imdb'] = imdb[1:] # 移除最前面的空格
        movie['doubanUrl'] = doubanUrl
        movie['posterUrl'] = posterUrl
        movie['iconUrl'] = iconUrl


        # https://docs.scrapy.org/en/latest/topics/request-response.html
        print(f'movie 对象: {movie}')
        yield movie

    def parseCelebrity(self, response):
        director_id = response.url.split('/')[4]
        director_name = response.xpath('//div[@id="content"]/h1/text()').get()
        photoUrl = response.xpath('//div[@class="nbg"]/img').xpath('@src').get()

        introArray = response.xpath('//span[@class="short"]/text()').getall()
        intro = "".join(introArray)
        if intro is None:
            intro = response.xpath('//div[@class="bd"]/text()').getall()[4]

        director = Director(d_id=director_id, name=director_name)
        
        all_info_li_html = response.xpath('//div[@class="info"]/ul/li')
        for li in all_info_li_html:
            li_name = li.css('span::text').get()
            li_value_str = li.css('li::text').getall()[1]
            li_value = re.sub(r"[\n\t\s:]*", "", li_value_str) # 移除值中的所有空格及换行
            print(f'xxxLi: {li_name} : {li_value}')
            if li_name == "性别":
                director['gender'] = li_value
            elif li_name == "星座":
                director['zodiac'] = li_value
            elif li_name == "出生日期":
                director['livingTime'] = li_value

                dateString = re.sub(r"[^0-9]", "-", li_value)
                dateString = dateString[:-1]
                datetime_obj = datetime.strptime(dateString, '%Y-%m-%d')
                director['birthday'] = time.mktime(datetime_obj.timetuple())

            elif li_name == "生卒日期":
                director['livingTime'] = li_value
                dateStrArray = li_value.split('至')
                dateRawString1 = dateStrArray[0]
                dateRawString2 = dateStrArray[1]
                dateString1 = re.sub(r"[^0-9]", "-", dateRawString1)
                dateString2 = re.sub(r"[^0-9]", "-", dateRawString2)
                dateString1 = dateString1[1:-1]
                dateString2 = dateString2[1:-1]
                datetime_object1 = datetime.strptime(dateString1, '%Y-%m-%d')
                datetime_object2 = datetime.strptime(dateString2, '%Y-%m-%d')
                birthday = time.mktime(datetime_object1.timetuple())
                leaveday = time.mktime(datetime_object2.timetuple())
                director['birthday'] = li_value
                director['leaveday'] = li_value
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
        director['intro'] = intro


        print(f'xxxxxxx {director}')
        yield director
    def parseActor(self, response):
        pass





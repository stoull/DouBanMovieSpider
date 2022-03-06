# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3, os, hashlib, time, sys, json
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from DouBanMovieSpider.items import Moive, Celebrity

class DoubanmoviespiderPipeline:

    def __init__(self):
        thisfile = os.path.abspath(__file__)
        programs = os.path.dirname(thisfile)
        projectDir = os.path.dirname(programs)
        self.db_file = os.path.join(projectDir, 'movie.db')
        self.initialDataBase()

    def open_spider(self, spider):
        self.file = open('items.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        for field in item.fields:
            item.setdefault(field, None)

        if isinstance(item, Moive):
            self.handleMoiveItem(item)
        elif isinstance(item, Celebrity):
            self.handleCelerbrityItem(item)
        return item

    def handleMoiveItem(self, mItem):
        # Add a movie item to database
        con = sqlite3.connect(self.db_file)
        cur = con.cursor()

        # Save the information of movie
        cur.execute('''INSERT OR IGNORE INTO movie(id,name,directors,scenarists,actors,
        style,year,releaseDate,area,language,length,otherNames,score,synopsis,
        imdb,doubanUrl,posterUrl,iconUrl)
         values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(
            mItem['m_id'],
            mItem['name'],
            mItem['directors'],
            mItem['scenarists'],
            mItem['actors'],
            mItem['style'],
            mItem['year'],
            mItem['releaseDate'],
            mItem['area'],
            mItem['language'],
            mItem['length'],
            mItem['otherNames'],
            mItem['score'],
            mItem['synopsis'],
            mItem['imdb'],
            mItem['doubanUrl'],
            mItem['posterUrl'],
            mItem['iconUrl']
        ))

        movie_id = int(mItem['m_id'])

        # save the infomation of area, tag, type
        styleStr = mItem['style']
        if styleStr is not None:
            styleStr = styleStr.replace(" ", "")  # 移除空格
            styles = styleStr.split('/')
            for str in styles:
                cur.execute('''INSERT OR IGNORE INTO type(name) values(?)''', (str,))
                con.commit()
                cur.execute('''SELECT id FROM type WHERE name=?;''', (str,))
                style_id = cur.fetchone()[0]
                if style_id is not None:
                    cur.execute('''INSERT OR IGNORE INTO movie_type(movie_id,type_id) values(?,?)''', (movie_id, style_id))

        areaStr = mItem['area']
        if areaStr is not None:
            areaStr = areaStr.replace(" ", "")  # 移除空格
            areas = areaStr.split('/')
            for str in areas:
                cur.execute('''INSERT OR IGNORE INTO area(name) values(?)''', (str,))
                con.commit()
                cur.execute('''SELECT id FROM area WHERE name=?;''', (str,))
                area_id = cur.fetchone()[0]
                if area_id is not None:
                    cur.execute('''INSERT OR IGNORE INTO movie_area(movie_id,area_id) values(?,?)''', (movie_id, area_id))

        languageStr = mItem['language']
        if languageStr is not None:
            languageStr = languageStr.replace(" ", "")  # 移除空格
            languages = languageStr.split('/')
            for str in languages:
                cur.execute('''INSERT OR IGNORE INTO language(name) values(?)''', (str,))
                con.commit()
                cur.execute('''SELECT id FROM language WHERE name=?;''', (str,))
                language_id = cur.fetchone()[0]
                if language_id is not None:
                    cur.execute('''INSERT OR IGNORE INTO movie_language(movie_id,language_id) values(?,?)''', (movie_id, language_id))

        con.commit()
        cur.close()

    def handleCelerbrityItem(self, dItem):
        # Add a director item to database
        con = sqlite3.connect(self.db_file)
        cur = con.cursor()

        obj_type = dItem['type']

        # save the infomation of area
        briPlaStr = dItem['birthplace']
        if briPlaStr is not None:
            briPlaStr = briPlaStr.replace(" ", "")  # 移除空格
            if "，" in briPlaStr:
                areaStr = briPlaStr.split('，')
            else:
                areaStr = briPlaStr.split(',')
            celebrity_id = int(dItem['d_id'])
            for str in areaStr:
                cur.execute('''INSERT OR IGNORE INTO area(name) values(?)''', (str,))
                con.commit()
                cur.execute('''SELECT id FROM area WHERE name=?;''', (str,))
                area_id = cur.fetchone()[0]
                if area_id is not None:
                    if obj_type == 'Director':
                        cur.execute('''INSERT OR IGNORE INTO diector_area(diector_id,area_id) values(?,?)''',
                                    (celebrity_id, area_id))
                    elif obj_type == 'Actor':
                        cur.execute('''INSERT OR IGNORE INTO actor_area(actor_id,area_id) values(?,?)''',
                                    (celebrity_id, area_id))
                    elif obj_type == 'actor_id':
                        cur.execute('''INSERT OR IGNORE INTO scenarist_area(scenarist_id,area_id) values(?,?)''',
                                    (celebrity_id, area_id))

        if obj_type == 'Director':
            cur.execute('''INSERT OR IGNORE INTO director(id, name, gender, zodiac, livingTime, birthday, 
            leaveday, birthplace, occupation, names_cn, names_en, family, imdb, intro, photoUrl)
             values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?)''', (
                dItem['d_id'],
                dItem['name'],
                dItem['gender'],
                dItem['zodiac'],
                dItem['livingTime'],
                dItem['birthday'],
                dItem['leaveday'],
                dItem['birthplace'],
                dItem['occupation'],
                dItem['names_cn'],
                dItem['names_en'],
                dItem['family'],
                dItem['imdb'],
                dItem['intro'],
                dItem['photoUrl']
            ))
        elif obj_type == 'Actor':
            cur.execute('''INSERT OR IGNORE INTO actor(id, name, gender, zodiac, livingTime, birthday, 
            leaveday, birthplace, occupation, names_cn, names_en, family, imdb, intro, photoUrl)
             values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?)''', (
                dItem['d_id'],
                dItem['name'],
                dItem['gender'],
                dItem['zodiac'],
                dItem['livingTime'],
                dItem['birthday'],
                dItem['leaveday'],
                dItem['birthplace'],
                dItem['occupation'],
                dItem['names_cn'],
                dItem['names_en'],
                dItem['family'],
                dItem['imdb'],
                dItem['intro'],
                dItem['photoUrl']
            ))
        elif obj_type == 'Scenarist':
            cur.execute('''INSERT OR IGNORE INTO scenarist(id, name, gender, zodiac, livingTime, birthday, 
            leaveday, birthplace, occupation, names_cn, names_en, family, imdb, intro, photoUrl)
             values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?)''', (
                dItem['d_id'],
                dItem['name'],
                dItem['gender'],
                dItem['zodiac'],
                dItem['livingTime'],
                dItem['birthday'],
                dItem['leaveday'],
                dItem['birthplace'],
                dItem['occupation'],
                dItem['names_cn'],
                dItem['names_en'],
                dItem['family'],
                dItem['imdb'],
                dItem['intro'],
                dItem['photoUrl']
            ))

        con.commit()
        cur.close()

    def handleActorItem(self, dItem):
        # Add a director item to database
        con = sqlite3.connect(self.db_file)
        cur = con.cursor()
        cur.execute('''INSERT OR IGNORE INTO actor(id, name, gender, zodiac, livingTime, birthday, 
         leaveday, birthplace, occupation, names_cn, names_en, family, imdb, intro, photoUrl)
          values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?)''', (
            dItem['d_id'],
            dItem['name'],
            dItem['gender'],
            dItem['zodiac'],
            dItem['livingTime'],
            dItem['birthday'],
            dItem['leaveday'],
            dItem['birthplace'],
            dItem['occupation'],
            dItem['names_cn'],
            dItem['names_en'],
            dItem['family'],
            dItem['imdb'],
            dItem['intro'],
            dItem['photoUrl']
        ))
        con.commit()
        cur.close()

    def handleScenaristItem(self, dItem):
        # Add a Scenarist item to database
        con = sqlite3.connect(self.db_file)
        cur = con.cursor()
        cur.execute('''INSERT OR IGNORE INTO scenarist(id, name, gender, zodiac, livingTime, birthday, 
         leaveday, birthplace, occupation, names_cn, names_en, family, imdb, intro, photoUrl)
          values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?)''', (
            dItem['d_id'],
            dItem['name'],
            dItem['gender'],
            dItem['zodiac'],
            dItem['livingTime'],
            dItem['birthday'],
            dItem['leaveday'],
            dItem['birthplace'],
            dItem['occupation'],
            dItem['names_cn'],
            dItem['names_en'],
            dItem['family'],
            dItem['imdb'],
            dItem['intro'],
            dItem['photoUrl']
        ))
        con.commit()
        cur.close()

    # 判断一个文件是否是SQLite3文件
    def isSQLite3File(self, filePath):
        if os.path.isfile(filePath):
            if os.path.getsize(filePath) > 100:
                with open(filePath, 'r', encoding="ISO-8859-1") as f:
                    header = f.read(100)
                    if header.startswith('SQLite format 3'):
                        # SQlite3 database has been detected
                        return True
        return False


    # 建表及其关系
    def initialDataBase(self):
        if self.isSQLite3File(self.db_file) == False:
            con = sqlite3.connect(self.db_file)
            cur = con.cursor()

            # create movie table
            cur.execute('''CREATE TABLE movie(
            id INTEGER PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            directors VARCHAR(200),
            scenarists VARCHAR(200),
            actors VARCHAR(400),
            style VARCHAR(60),
            year INTEGER,
            releaseDate VARCHAR(200),
            area VARCHAR(120),
            language VARCHAR(60),
            length INTEGER,
            otherNames VARCHAR(100),
            score NUMERIC,
            synopsis TEXT,
            imdb VARCHAR(20),
            doubanUrl VARCHAR(250),
            posterUrl VARCHAR(250),
            iconUrl VARCHAR(250),
            filePath VARCHAR(250),
            fileUrl VARCHAR(250),
            createDate DATETIME DEFAULT CURRENT_TIMESTAMP,
            lastWatchDate DATETIME,
            lastWatchUser VARCHAR(40))''')

            cur.execute('''CREATE TABLE director(
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            gender BOOLEAN,
            zodiac VARCHAR(10),
            livingTime VARCHAR(100),
            birthday INTEGER,
            leaveday INTEGER,
            birthplace VARCHAR(100),
            occupation VARCHAR(100),
            names_cn VARCHAR(300),
            names_en VARCHAR(300),
            family VARCHAR(200),
            imdb VARCHAR(20),
            intro TEXT,
            photoUrl VARCHAR(250)
            )''')

            cur.execute('''CREATE TABLE actor(
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            gender BOOLEAN,
            zodiac VARCHAR(10),
            livingTime VARCHAR(100),
            birthday INTEGER,
            leaveday INTEGER,
            birthplace VARCHAR(100),
            occupation VARCHAR(100),
            names_cn VARCHAR(300),
            names_en VARCHAR(300),
            family VARCHAR(200),
            imdb VARCHAR(20),
            intro TEXT,
            photoUrl VARCHAR(250)
            )''')

            cur.execute('''CREATE TABLE scenarist(
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            gender BOOLEAN,
            zodiac VARCHAR(10),
            livingTime VARCHAR(100),
            birthday INTEGER,
            leaveday INTEGER,
            birthplace VARCHAR(100),
            occupation VARCHAR(100),
            names_cn VARCHAR(300),
            names_en VARCHAR(300),
            family VARCHAR(200),
            imdb VARCHAR(20),
            intro TEXT,
            photoUrl VARCHAR(250)
            )''')

            cur.execute('''CREATE TABLE area(
            id INTEGER PRIMARY KEY,
            name VARCHAR(20) NOT NULL,
            unique (name)
            )''')

            cur.execute('''CREATE TABLE type(
            id INTEGER PRIMARY KEY,
            name VARCHAR(40) NOT NULL,
            unique (name)
            )''')

            cur.execute('''CREATE TABLE tag(
            id INTEGER PRIMARY KEY,
            name VARCHAR(40) NOT NULL,
            unique (name)
            )''')

            cur.execute('''CREATE TABLE language(
            id INTEGER PRIMARY KEY,
            name VARCHAR(30) NOT NULL,
            unique (name)
            )''')

            cur.execute('''CREATE TABLE movie_director(
            movie_id INTEGER ,
            director_id INTEGER,
            CONSTRAINT FK_movie_id FOREIGN KEY (movie_id) REFERENCES movie(id),
            CONSTRAINT FK_director_id FOREIGN KEY (director_id) REFERENCES director(id)
            )''')

            cur.execute('''CREATE TABLE movie_actor(
            movie_id INTEGER,
            actor_id INTEGER,
            CONSTRAINT FK_movie_id FOREIGN KEY (movie_id) REFERENCES movie(id),
            CONSTRAINT FK_actor_id FOREIGN KEY (actor_id) REFERENCES actor(id)
            )''')

            cur.execute('''CREATE TABLE movie_scenarist(
            movie_id INTEGER,
            scenarist_id INTEGER,
            CONSTRAINT FK_movie_id FOREIGN KEY (movie_id) REFERENCES movie(id),
            CONSTRAINT FK_scenarist_id FOREIGN KEY (scenarist_id) REFERENCES scenarist(id)
            )''')

            cur.execute('''CREATE TABLE movie_area(
            movie_id INTEGER,
            area_id INTEGER,
            CONSTRAINT FK_movie_id FOREIGN KEY (movie_id) REFERENCES movie(id),
            CONSTRAINT FK_area_id FOREIGN KEY (area_id) REFERENCES area(id)
            )''')

            cur.execute('''CREATE TABLE movie_type(
            movie_id INTEGER,
            type_id INTEGER,
            CONSTRAINT FK_movie_id FOREIGN KEY (movie_id) REFERENCES movie(id),
            CONSTRAINT FK_type_id FOREIGN KEY (type_id) REFERENCES type(id)
            )''')

            cur.execute('''CREATE TABLE movie_tag(
            movie_id INTEGER,
            tag_id INTEGER,
            CONSTRAINT FK_movie_id FOREIGN KEY (movie_id) REFERENCES movie(id),
            CONSTRAINT FK_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id)
            )''')

            cur.execute('''CREATE TABLE movie_language(
            movie_id INTEGER,
            language_id INTEGER,
            CONSTRAINT FK_movie_id FOREIGN KEY (movie_id) REFERENCES movie(id),
            CONSTRAINT FK_language_id FOREIGN KEY (language_id) REFERENCES language(id)
            )''')

            cur.execute('''CREATE TABLE diector_area(
            diector_id INTEGER,
            area_id INTEGER,
            CONSTRAINT FK_diector_id FOREIGN KEY (diector_id) REFERENCES diector(id),
            CONSTRAINT FK_type_id FOREIGN KEY (area_id) REFERENCES area(id)
            )''')

            cur.execute('''CREATE TABLE scenarist_area(
            scenarist_id INTEGER,
            area_id INTEGER,
            CONSTRAINT FK_diector_id FOREIGN KEY (scenarist_id) REFERENCES scenarist(id),
            CONSTRAINT FK_type_id FOREIGN KEY (area_id) REFERENCES area(id)
            )''')

            cur.execute('''CREATE TABLE actor_area(
            actor_id INTEGER,
            area_id INTEGER,
            CONSTRAINT FK_diector_id FOREIGN KEY (actor_id) REFERENCES actor(id),
            CONSTRAINT FK_type_id FOREIGN KEY (area_id) REFERENCES area(id)
            )''')

            con.commit()
            cur.close()
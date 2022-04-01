
import sqlite3
import os


class DBManager(object):

    def __init__(self):
        thisfile = os.path.abspath(__file__)
        programs = os.path.dirname(thisfile)
        projectDir = os.path.dirname(programs)
        self.db_file = os.path.join(projectDir, 'movie_db')
        self.initialDataBase()

    def isMovieExist(self, movieId):
        con = sqlite3.connect(self.db_file)
        cur = con.cursor()
        cur.execute('''SELECT EXISTS(SELECT 1 FROM movie WHERE id=? LIMIT 1)''', (movieId,))
        is_exit = cur.fetchone()
        if is_exit[0] == 1:
            return True
        else:
            return False

    def isCelebrityExist(self, i_id):
        con = sqlite3.connect(self.db_file)
        cur = con.cursor()
        cur.execute('''SELECT EXISTS(SELECT 1 FROM celebrity WHERE id=? LIMIT 1)''', (i_id,))
        is_exit = cur.fetchone()
        if is_exit[0] == 1:
            return True
        else:
            return False

    def isBriefMovieExist(self, i_id):
        con = sqlite3.connect(self.db_file)
        cur = con.cursor()
        cur.execute('''SELECT EXISTS(SELECT 1 FROM movie_brief WHERE id=? LIMIT 1)''', (i_id,))
        is_exit = cur.fetchone()
        if is_exit[0] == 1:
            return True
        else:
            return False

    def insertMovieItem(self, mItem):
        # Add a movie item to database
        con = sqlite3.connect(self.db_file)
        cur = con.cursor()

        # Save the information of movie
        cur.execute('''INSERT OR IGNORE INTO movie(id,name,directors,scenarists,actors,
        style,year,release_date,area,language,length,other_names,score,rating_number,synopsis,
        imdb,poster_name)
         values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
            mItem['m_id'],
            mItem['name'],
            mItem['directors'],
            mItem['scenarists'],
            mItem['actors'],
            mItem['style'],
            mItem['year'],
            mItem['release_date'],
            mItem['area'],
            mItem['language'],
            mItem['length'],
            mItem['other_names'],
            mItem['score'],
            mItem['rating_number'],
            mItem['synopsis'],
            mItem['imdb'],
            mItem['poster_name']
        ))

        movie_id = int(mItem['m_id'])

        # save the infomation of area, tag, type
        styleStr = mItem['style']
        if styleStr is not None:
            styleStr = styleStr.replace(" ", "")  # 移除空格
            styles = styleStr.split('/')
            for s_tr in styles:
                cur.execute('''INSERT OR IGNORE INTO type(name) values(?)''', (s_tr,))
                con.commit()
                cur.execute('''SELECT id FROM type WHERE name=?;''', (s_tr,))
                style_id = cur.fetchone()[0]
                if style_id is not None:
                    cur.execute('''INSERT OR IGNORE INTO movie_type(movie_id,type_id) values(?,?)''',
                                (movie_id, style_id))

        areaStr = mItem['area']
        if areaStr is not None:
            areaStr = areaStr.replace(" ", "")  # 移除空格
            areas = areaStr.split('/')
            for s_tr in areas:
                cur.execute('''INSERT OR IGNORE INTO area(name) values(?)''', (s_tr,))
                con.commit()
                cur.execute('''SELECT id FROM area WHERE name=?;''', (s_tr,))
                area_id = cur.fetchone()[0]
                if area_id is not None:
                    cur.execute('''INSERT OR IGNORE INTO movie_area(movie_id,area_id) values(?,?)''',
                                (movie_id, area_id))

        languageStr = mItem['language']
        if languageStr is not None:
            languageStr = languageStr.replace(" ", "")  # 移除空格
            languages = languageStr.split('/')
            for s_tr in languages:
                cur.execute('''INSERT OR IGNORE INTO language(name) values(?)''', (s_tr,))
                con.commit()
                cur.execute('''SELECT id FROM language WHERE name=?;''', (s_tr,))
                language_id = cur.fetchone()[0]
                if language_id is not None:
                    cur.execute('''INSERT OR IGNORE INTO movie_language(movie_id,language_id) values(?,?)''',
                                (movie_id, language_id))

        con.commit()
        cur.close()

    def insertCelerbrityItem(self, dItem):
        # Add a director item to database
        con = sqlite3.connect(self.db_file)
        cur = con.cursor()

        obj_type = dItem['type']
        movie_id = dItem['movie_id']
        celebrity_id = int(dItem['d_id'])

        # save the infomation of area
        briPlaStr = dItem['birthplace']
        if briPlaStr is not None:
            briPlaStr = briPlaStr.replace(" ", "")  # 移除空格
            if "，" in briPlaStr:
                areaStr = briPlaStr.split('，')
            else:
                areaStr = briPlaStr.split(',')
            for str in areaStr:
                cur.execute('''INSERT OR IGNORE INTO area(name) values(?)''', (str,))
                con.commit()
                cur.execute('''SELECT id FROM area WHERE name=?;''', (str,))
                area_id = cur.fetchone()[0]
                if area_id is not None:
                    cur.execute('''INSERT OR IGNORE INTO celebrity_area(celebrity_id,area_id) values(?,?)''',
                                (celebrity_id, area_id))

        # The relationships between movie and celebrity
        if obj_type == 'Director':
            cur.execute('''INSERT OR IGNORE INTO movie_director(movie_id,director_id) values(?,?)''',
                        (movie_id, celebrity_id))
        elif obj_type == 'Actor':
            cur.execute('''INSERT OR IGNORE INTO movie_actor(movie_id,actor_id) values(?,?)''',
                        (movie_id, celebrity_id))
        elif obj_type == 'Scenarist':
            cur.execute('''INSERT OR IGNORE INTO movie_scenarist(movie_id,scenarist_id) values(?,?)''',
                        (movie_id, celebrity_id))

        # insert celebrity
        cur.execute('''INSERT OR IGNORE INTO celebrity(id, name, gender, zodiac, living_time, birthday, 
            left_day, birthplace, occupation, is_director, is_scenarist, is_actor, names_cn, names_en, family, imdb, intro, portrait_name)
             values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?, ?, ?, ?)''', (
                dItem['d_id'],
                dItem['name'],
                dItem['gender'],
                dItem['zodiac'],
                dItem['living_time'],
                dItem['birthday'],
                dItem['left_day'],
                dItem['birthplace'],
                dItem['occupation'],
                dItem['is_director'],
                dItem['is_scenarist'],
                dItem['is_actor'],
                dItem['names_cn'],
                dItem['names_en'],
                dItem['family'],
                dItem['imdb'],
                dItem['intro'],
                dItem['portrait_name']
            ))

        con.commit()
        cur.close()

    def insertHotCommentItem(self, dItem):
        con = sqlite3.connect(self.db_file)
        cur = con.cursor()
        cur.execute('''INSERT OR IGNORE INTO hot_comment(id, movie_id, content, reviewer_name, reviewer_id)
          values(?, ?, ?, ?, ?)''', (
            dItem['d_id'],
            dItem['movie_id'],
            dItem['content'],
            dItem['reviewer_name'],
            dItem['reviewer_id']
        ))
        con.commit()
        cur.close()

    def insertReviewItem(self, dItem):
        con = sqlite3.connect(self.db_file)
        cur = con.cursor()
        cur.execute('''INSERT OR IGNORE INTO review(id, movie_id, title, content_short, content, reviewer_name, reviewer_id)
          values(?, ?, ?, ?, ?, ?, ?)''', (
            dItem['d_id'],
            dItem['movie_id'],
            dItem['title'],
            dItem['content_short'],
            dItem['content'],
            dItem['reviewer_name'],
            dItem['reviewer_id']
        ))
        con.commit()
        cur.close()

    def insertBriefMovieItem(self, dItem):
        con = sqlite3.connect(self.db_file)
        cur = con.cursor()
        brief_movie_id = dItem['d_id']
        cur.execute('''INSERT OR IGNORE INTO movie_brief(id, name, score, year, poster_name)
          values(?, ?, ?, ?, ?)''', (
            brief_movie_id,
            dItem['name'],
            dItem['score'],
            dItem['year'],
            dItem['poster_name']
        ))

        if dItem['location_type'] == 'movie':
            if dItem['movie_id'] is not None:
                cur.execute('''INSERT OR IGNORE INTO recommendations(reference_movie_id, movie_brief_id)
                          values(?, ?)''', (
                    dItem['movie_id'],
                    brief_movie_id
                ))
        elif dItem['location_type'] == 'celebrity':
            if dItem['celebrity_id'] is not None:
                cur.execute('''INSERT OR IGNORE INTO best_movies(celebrity_id, movie_brief_id)
                                          values(?, ?)''', (
                    dItem['celebrity_id'],
                    brief_movie_id
                ))
        con.commit()
        cur.close()

    def forceInsertBriefMovieItem(self, dItem):
        con = sqlite3.connect(self.db_file)
        cur = con.cursor()
        brief_movie_id = dItem['d_id']

        cur.execute('''SELECT name,score FROM movie_brief WHERE id=? LIMIT 1''', (brief_movie_id,))
        brie_result = cur.fetchone()
        if brie_result is not None:
            if brie_result[1] is None:
                cur.execute('''DELETE FROM movie_brief WHERE id=?''', (brief_movie_id,))
                con.commit()
                cur.close()
                self.insertBriefMovieItem(dItem)
            else:
                pass
        else:
            self.insertBriefMovieItem(dItem)

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
        if not self.isSQLite3File(self.db_file):
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
            release_date VARCHAR(200),
            area VARCHAR(120),
            language VARCHAR(60),
            length INTEGER,
            other_names VARCHAR(100),
            score NUMERIC,
            rating_number NUMERIC,
            synopsis TEXT,
            imdb VARCHAR(20),
            poster_name VARCHAR(80),
            filePath VARCHAR(250),
            fileUrl VARCHAR(250),
            is_downloaded BLOB DEFAULT 0,
            download_link VARCHAR(250),
            create_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            lastWatch_date DATETIME,
            lastWatch_user VARCHAR(40))''')

            # 导演,编剧, 演员
            cur.execute('''CREATE TABLE celebrity(
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            gender BOOLEAN,
            zodiac VARCHAR(10),
            living_time VARCHAR(100),
            birthday INTEGER,
            left_day INTEGER,
            birthplace VARCHAR(100),
            occupation VARCHAR(100),
            is_director BLOB DEFAULT 0,
            is_scenarist BLOB DEFAULT 0,
            is_actor BLOB DEFAULT 0,
            names_cn VARCHAR(250),
            names_en VARCHAR(250),
            family VARCHAR(200),
            imdb VARCHAR(20),
            intro TEXT,
            portrait_name VARCHAR(80),
            create_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )''')

            # 最受好评的5部作品
            cur.execute('''CREATE TABLE best_movies(
            id INTEGER PRIMARY KEY,
            celebrity_id INTEGER,
            movie_brief_id INTEGER,
            CONSTRAINT FK_celebrity_id FOREIGN KEY (celebrity_id) REFERENCES celebrity(id),
            CONSTRAINT FK_movie_brief_id FOREIGN KEY (movie_brief_id) REFERENCES movie_brief(id)
            )''')

            # 喜欢这部电影的人也喜欢
            cur.execute('''CREATE TABLE recommendations(
            id INTEGER PRIMARY KEY,
            reference_movie_id INTEGER,
            movie_brief_id INTEGER,
            CONSTRAINT FK_reference_movie_id FOREIGN KEY (reference_movie_id) REFERENCES movie(id),
            CONSTRAINT FK_movie_brief_id FOREIGN KEY (movie_brief_id) REFERENCES movie_brief(id)
            )''')

            # 电影的简略信息
            cur.execute('''CREATE TABLE movie_brief(
            id INTEGER PRIMARY KEY,
            name VARCHAR(200),
            score NUMERIC,
            year INTEGER,
            poster_name VARCHAR(80)
            )''')

            # 短评
            cur.execute('''CREATE TABLE hot_comment(
            id INTEGER PRIMARY KEY,
            movie_id INTEGER,
            content TEXT,
            reviewer_name VARCHAR(60),
            reviewer_id VARCHAR(20)
            )''')

            # 影评
            cur.execute('''CREATE TABLE review(
            id INTEGER PRIMARY KEY,
            movie_id INTEGER,
            title VARCHAR(150),
            content_short TEXT,
            content TEXT,
            reviewer_name VARCHAR(40),
            reviewer_id VARCHAR(20)
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

            cur.execute('''CREATE TABLE celebrity_area(
            celebrity_id INTEGER,
            area_id INTEGER,
            CONSTRAINT FK_celebrity_id FOREIGN KEY (celebrity_id) REFERENCES celebrity(id),
            CONSTRAINT FK_area_id FOREIGN KEY (area_id) REFERENCES area(id)
            )''')

            con.commit()
            cur.close()

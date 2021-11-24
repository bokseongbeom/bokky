#`idnew_table` int unsigned NOT NULL AUTO_INCREMENT,
import string
import requests
import pymysql
import json
import pandas as pd
from pandas import json_normalize


class KakaoLocalAPI:
    """Kakao Local API 컨트롤러"""

    def __init__(self):
        """
        Rest API키 초기화 및 URL 설정
        MariaDB 연결 및 종목코드 딕셔너리 생성
        """
        # MARIA DB CON 설정
        self.conn = pymysql.connect(host="database-1.coyhhlfg38do.ap-northeast-2.rds.amazonaws.com",
                                    port=3306, user="admin", password="noobokmizz",
                                    db='mydb3', charset='utf8')

        with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE IF NOT EXISTS category_info (
                category VARCHAR(40),
                category_id int NOT NULL AUTO_INCREMENT,
                cl_activity VARCHAR(40), 
                cm_activity VARCHAR(40), 
                cs_activity VARCHAR(40),
                UNIQUE KEY `category` (category),
                PRIMARY KEY (category_id, category)
                );
            """
            curs.execute(sql)

            sql = """
            CREATE TABLE IF NOT EXISTS location (
                lc_id varchar(16),
                lc_name varchar(40) ,
                lc_addr varchar(45) ,
                lc_addr_road varchar(45) ,
                lc_x varchar(45) ,
                lc_y varchar(45) ,
                lc_call_number varchar(45) ,
                lc_url varchar(80) ,
                lc_category int NOT NULL,
                PRIMARY KEY (lc_id, lc_category),
                UNIQUE KEY `lc_name` (`lc_id`),
                FOREIGN KEY (lc_category) REFERENCES category_info (category_id) ON UPDATE CASCADE ON DELETE CASCADE);
            """
            curs.execute(sql)

            sql = """
            CREATE TABLE IF NOT EXISTS search (
                search_id int NOT NULL AUTO_INCREMENT,
                search VARCHAR(10),
                UNIQUE KEY `search` (`search`),
                PRIMARY KEY (search_id, search));
            """
            curs.execute(sql)

        self.conn.commit()

        # REST API 키 설정
        self.rest_api_key = "fdc883fda0ab9f3e7a2bec429fc989ae"
        self.headers = {"Authorization": "KakaoAK {}".format("fdc883fda0ab9f3e7a2bec429fc989ae")}

        # 05 키워드 검색
        self.URL = "https://dapi.kakao.com/v2/local/search/keyword.json"

        # self 값 설정

    def search_keyword(self, query, x, y, offset=None, page=None, category_group_code=None,
                       radius=None, size=None, sort=None):

        params = {"query": f"{query}",
                  'rect': f'{x},{y},{x + offset},{y + offset}'
                  }

        if category_group_code != None:
            params['category_group_code'] = f"{category_group_code}"
        if radius != None:
            params['radius'] = f"{radius}"
        if page != None:
            params['page'] = f"{page}"
        if size != None:
            params['size'] = f"{params}"
        if sort != None:
            params['sort'] = f"{sort}"

        res = requests.get(self.URL, headers=self.headers, params=params)
        document = json.loads(res.text)

        return document

    def get_keyword_list(self, query, x, y, offset=0.01):
        """전체 지역 검색"""
        page = 1
        df = pd.DataFrame()
        abc = offset

        while True:
            search_count = self.search_keyword(query, x, y, offset=abc)['meta']['total_count']

            if search_count > 45:
                abc = abc / 2
                x_end = x + abc
                y_end = y + abc
                a = self.get_keyword_list(query, x, y, offset=abc)
                b = self.get_keyword_list(query, x_end, y, offset=abc)
                c = self.get_keyword_list(query, x, y_end, offset=abc)
                d = self.get_keyword_list(query, x_end, y_end, offset=abc)
                df = df.append(a)
                df = df.append(b)
                df = df.append(c)
                df = df.append(d)

                return df

            else:
                if self.search_keyword(query, x, y, offset=abc, page=page)['meta']['is_end']:
                    df = df.append(
                        pd.json_normalize(self.search_keyword(query, x, y, offset=abc, page=page)['documents']))
                    return df
                # 아니면 다음 페이지로 넘어가서 데이터 저장
                else:
                    df = df.append(
                        pd.json_normalize(self.search_keyword(query, x, y, offset=abc, page=page)['documents']))
                    page += 1

    def search_all(self, query):
        # 126 - 128 36.5 - 38.5 경기 지역
        x = 126
        df = pd.DataFrame()
        dfa = pd.DataFrame()
        dfb = pd.DataFrame()

        for j in range(0,4):
            y = 36.5
            for k in range(0,4):  # 바로바꿔용 3 으로 둘다!!!
                print(x, y)
                df = df.append(self.get_keyword_list(query, x, y, offset=0.5))
                y += 0.5
            x += 0.5

        '''전처리'''
        s = df['category_name'].str.split(">")
        df["place_name"] = df["place_name"].str.replace(pat=r'[^\w]', repl=r'', regex=True)
        cl_activity = s.str[0]
        cm_activity = s.str[1]
        cs_activity = s.str[2]
        category = s.str[2].str.strip()
        df['category'] = category
        if s.str[1] is None:
            cm_activity = cl_activity
            df['category'] = cl_activity
        elif s.str[2] is None:
            df['category'] = cm_activity
            cs_activity = None

        df['cs_activity'] = cs_activity.str.strip()
        df['cm_activity'] = cm_activity.str.strip()
        df['cl_activity'] = cl_activity.str.strip()


        df.drop(columns=['category_group_name', 'distance'], axis=1, inplace=True)
        df = df.rename(columns={'address_name': 'lc_addr', 'category_group_name': 'cs_activity',
                                'id': 'lc_id', 'phone': 'lc_call_number', 'place_name': 'lc_name',
                                'place_url': 'lc_url', 'road_address_name': 'lc_addr_road',
                                'x': 'lc_x', 'y': 'lc_y'})

        dfa = df.reindex(columns=['category_group_code', 'cl_activity', 'cm_activity', 'cs_activity', 'category'])
        dfb = df.reindex(columns=['lc_id', 'lc_name', 'lc_addr', 'lc_addr_road', 'lc_x', 'lc_y', 'lc_call_number',
                                  'lc_url', 'category'])
        dfa = dfa.drop_duplicates()
        dfb = dfb.drop_duplicates()




        return dfa, dfb

    def replace_into_db(self, df):
        """검색된 activity db에 REPLACE"""
        with self.conn.cursor() as curs:
            for idx in range(len(df)):
                #category_group_code = df.category_group_code.valeus[idx]
                category = df.category.values[idx]
                cl_activity = df.cl_activity.values[idx]
                cm_activity = df.cm_activity.values[idx]
                cs_activity = df.cs_activity.values[idx]
                sql = f"INSERT IGNORE INTO category_info (category,cl_activity,cm_activity, " \
                      f"cs_activity)VALUES ('{category}','{cl_activity}'," \
                      f"'{cm_activity}','{cs_activity}')"
                curs.execute(sql)
            self.conn.commit()

    def replace_into_db2(self, df):
        """검색된 activity db에 REPLACE"""
        with self.conn.cursor() as curs:


            for idx in range(len(df)):
                category = df.category.values[idx]

                sql = f"SELECT * FROM category_info WHERE category = '{category}'"
                searchlist = pd.read_sql(sql, self.conn)
                search = searchlist.category_id.values[0]

                lc_id = df.lc_id.values[idx]
                lc_name = df.lc_name.values[idx]
                lc_addr = df.lc_addr.values[idx]
                lc_addr_road = df.lc_addr_road.values[idx]
                lc_x = df.lc_x.values[idx]
                lc_y = df.lc_y.values[idx]
                lc_call_number = df.lc_call_number.values[idx]
                lc_url = df.lc_url.values[idx]
                lc_category = search #### 여기 어칼까용

                sql = f"REPLACE INTO location (lc_id, lc_name, lc_addr, lc_addr_road, lc_x, lc_y, lc_call_number," \
                      f" lc_url, lc_category)VALUES ('{lc_id}','{lc_name}','{lc_addr}','{lc_addr_road}','{lc_x}'," \
                      f"'{lc_y}','{lc_call_number}','{lc_url}','{lc_category}')"
                curs.execute(sql)
            self.conn.commit()

    def read_search_info(self):
        """DB의 search table에서 검색어 불러들이기"""
        with self.conn.cursor() as curs:
            sql = "SELECT * FROM search"
            search = pd.read_sql(sql, self.conn)

        return search

    def search_info(self):
        """search table 검색어를 토대로 프로그램 시작"""
        with self.conn.cursor() as curs:
            searchlist = ['여행','음식점']
            for idx in searchlist:
                search = idx
                sql = f"INSERT IGNORE INTO search (search)VALUES ('{search}')"
                curs.execute(sql)
            self.conn.commit()

            search = self.read_search_info()
            for idx in range(len(search)):
                print(range(len(search)))
                query = f'{search.search.values[idx]}'
                print(query)
                dfa, dfb = self.search_all(query)
                print(idx)
                self.replace_into_db(dfa)
                self.replace_into_db2(dfb)


if __name__ == '__main__':
    dbu = KakaoLocalAPI()
    dbu.search_info()
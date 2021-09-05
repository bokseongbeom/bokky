import requests
from datetime import datetime
import pymysql, calendar, time, json
import json
import pandas as pd
from pandas import json_normalize

import collections
import folium
import openpyxl

#sql = f"REPLACE INTO company_info (code, company, last_update) VALUES ('{code}','{company}','{today}')"

'''
dataframe 출력 옵션
'''

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


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
                                    db='mydb', charset='utf8')

        with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE IF NOT EXISTS category_info (
                category VARCHAR(50),
                last_update DATE,
                PRIMARY KEY (category))
            """
            curs.execute(sql)
            '''
            sql = """
            CREATE TABLE IF NOT EXISTS daily_price (
                code VARCHAR(20),
                date DATE,
                open BIGINT(20),
                high BIGINT(20),
                low BIGINT(20),
                close BIGINT(20),
                diff BIGINT(20),
                volume BIGINT(20),
                PRIMARY KEY (code, date))
            """
            curs.execute(sql)
            '''
        self.conn.commit()
        self.codes = dict()

        # REST API 키 설정
        self.rest_api_key = "fdc883fda0ab9f3e7a2bec429fc989ae"
        self.headers = {"Authorization": "KakaoAK {}".format("fdc883fda0ab9f3e7a2bec429fc989ae")}

        # 05 키워드 검색
        self.URL_05 = "https://dapi.kakao.com/v2/local/search/keyword.json"

        # self 값 설정


    def search_keyword(self, query, x, y, offset=None, page=None, category_group_code=None,
                       radius=None, size=None, sort=None):

        params = {"query": f"{query}",
                  'rect': f'{x},{y},{x+offset},{y+offset}'
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

        res = requests.get(self.URL_05, headers=self.headers, params=params)
        document = json.loads(res.text)

        return document

    def get_keyword_list(self, query, x, y, offset = 0.01):
        '''
        전체 검색
        '''
        page = 1
        df = pd.DataFrame()
        abc = offset

        while True:
            search_count = self.search_keyword(query, x, y, offset=abc)['meta']['total_count'] #####
            #print(self.search_keyword(query, x, y, offset= offset, page=page))
            #print(search_count, abc, x, y)

            if search_count > 45:
                abc = abc/2
                x_end = x+abc
                y_end = y+abc
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
                if self.search_keyword(query, x, y, offset= abc, page=page)['meta']['is_end']:
                    df = df.append(pd.json_normalize(self.search_keyword(query, x, y, offset= abc, page=page)))
                    return df
                # 아니면 다음 페이지로 넘어가서 데이터 저장
                else:
                    df = df.append(pd.json_normalize(self.search_keyword(query, x, y, offset=abc, page=page)['documents']))
                    page += 1

    def search_all(self, query):
        # 126 - 128 36.5 - 38.5 경기 지역
        x = 126
        df = pd.DataFrame()

        for j in range(1, 3):
            y = 36.5
            for k in range(1, 2): # 바로바꿔용 3 으로
                print(x, y)
                every_list_one = self.get_keyword_list(query, x, y, offset=0.5)
                df = df.append(every_list_one)

                y += 0.5
            x += 0.5

        '''전처리'''

        s = df['category_name'].str.split(">")
        cs_activity = s.str[2]
        cm_activity = s.str[1]
        cl_activity = s.str[0]

        df['cs_activity'] = cs_activity
        df['cm_activity'] = cm_activity
        df['cl_activity'] = cl_activity

        df.drop(columns=['category_group_code', 'category_group_name', 'distance'], axis=1, inplace=True)
        df = df.rename(columns={'address_name': 'lc_addr', 'category_group_name': 'cs_activity'
            , 'id': 'lc_id', 'phone': 'lc_call_number', 'place_name': 'lc_name',
                                'place_url': 'lc_url', 'road_address_name': 'lc_addr_road', 'x': 'lc_x', 'y': 'lc_y'})

        df = df.reindex(
            columns=['lc_id', 'lc_name', 'lc_addr', 'lc_addr_road', 'lc_x', 'lc_y', 'lc_call_number', 'lc_url',
                     'cl_activity', 'cm_activity' , 'cs_activity'])

        return df

    def replace_into_db(self, df, num, code, company):
        """검색된 activity db에 REPLACE"""
        with self.conn.cursor() as curs:
            for r in df.itertuples():
                sql = f"REPLACE INTO daily_price VALUES ('{r.lc_id}', " \
                      f"'{r.lc_name}', {r.lc_addr}, {r.lc_addr_road}, {r.lc_x}, {r.lc_y}, " \
                      f"{r.lc_call_number}, {r.lc_url}, {r.cl_activity}, {r.cm_activity}, {r.cs_activity})"
                curs.execute(sql)
            self.conn.commit()
            print('[{}] #{:04d} {} ({}) : {} rows > REPLACE INTO daily_' \
                  'price [OK]'.format(datetime.now().strftime('%Y-%m-%d' \
                                                              ' %H:%M'), num + 1, company, code, len(df)))


# 함수 실행
query = '스타벅스'
kakao = KakaoLocalAPI()
df = kakao.search_all(query)
print(df.head(3))


'''
df = pd.json_normalize(kakao.search_keyword(query, x = 127, y = 37.5, page = 1, offset = 0.5 )['documents'])
df1 = pd.json_normalize(kakao.search_keyword(query, x = 127, y = 36.5, page = 1, offset = 0.5 )['documents'])
df = df.append(df1, ignore_index=True)



dataframe 전처리

df.drop(columns=['category_group_code', 'category_group_name', 'distance'], axis=1, inplace=True)
df = df.rename(columns={'address_name': 'lc_addr',  'category_group_name': 'cs_activity'
                , 'category_name': 'cs_activity', 'id': 'lc_id', 'phone': 'lc_call_number', 'place_name': 'lc_name',
                   'place_url': 'lc_url', 'road_address_name': 'lc_addr_road', 'x': 'lc_x', 'y': 'lc_y'})

df = df.reindex(columns=['lc_id','lc_name','lc_addr','lc_addr_road','lc_x', 'lc_y', 'lc_call_number', 'lc_url', 'cs_activity'])
print(df)
'''

#df.append(pd.read_json(self.search_keyword(query, x, y, offset= abc, page=page)))

'''
def search_keyword(self, query, x, y, offset=None, page=None, category_group_code=None,
                       radius=None, size=None, sort=None):
'''

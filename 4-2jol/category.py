import requests
from datetime import datetime
import pymysql, calendar, time, json
import json
import pandas as pd
from pandas import json_normalize

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
                category VARCHAR(40),
                cl_activity VARCHAR(40), 
                cm_activity VARCHAR(40), 
                cs_activity VARCHAR(40),
                PRIMARY KEY (category))
            """
            curs.execute(sql)

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
        """전체 지역 검색"""
        page = 1
        df = pd.DataFrame()
        abc = offset

        while True:
            search_count = self.search_keyword(query, x, y, offset=abc)['meta']['total_count']

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
                    df = df.append(pd.json_normalize(self.search_keyword(query, x, y, offset=abc, page=page)['documents']))
                    return df
                # 아니면 다음 페이지로 넘어가서 데이터 저장
                else:
                    df = df.append(pd.json_normalize(self.search_keyword(query, x, y, offset=abc, page=page)['documents']))
                    page += 1

    def search_all(self, query):
        # 126 - 128 36.5 - 38.5 경기 지역
        x = 126
        df = pd.DataFrame()

        for j in range(1, 2):
            y = 36.5
            for k in range(1, 2): # 바로바꿔용 3 으로 둘다!!!
                print(x, y)
                df = df.append(self.get_keyword_list(query, x, y, offset=0.5))
                y += 0.5
            x += 0.5

        '''전처리'''
        s = df['category_name'].str.split(">")
        cs_activity = s.str[2]
        cm_activity = s.str[1]
        cl_activity = s.str[0]
        category = s.str[-1]

        df['cs_activity'] = cs_activity
        df['cm_activity'] = cm_activity
        df['cl_activity'] = cl_activity
        df['category'] = category

        df.drop(columns=['category_group_code', 'category_group_name', 'distance'], axis=1, inplace=True)

        df = df.reindex(columns=['cl_activity', 'cm_activity', 'cs_activity', 'category'])
        df = df.drop_duplicates()

        return df

    def replace_into_db(self, df):
        """검색된 activity db에 REPLACE"""
        with self.conn.cursor() as curs:
            for idx in range(len(df)):
                category = df.category.values[idx]
                cl_activity = df.cl_activity.values[idx]
                cm_activity = df.cm_activity.values[idx]
                cs_activity = df.cs_activity.values[idx]
                sql = f"REPLACE INTO category_info (category, cl_activity, cm_activity, " \
                      f"cs_activity)VALUES ('{category}', '{cl_activity}', " \
                      f"'{cm_activity}', '{cs_activity}')"
                curs.execute(sql)
            self.conn.commit()



            # 함수 실행
query = '관광명소'
kakao = KakaoLocalAPI()
df = kakao.search_all(query)
print(df)
kakao.replace_into_db(df)

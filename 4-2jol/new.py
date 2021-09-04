import requests
import json
import pandas as pd
from pandas import json_normalize

import collections
import folium
import openpyxl


'''
dataframe 출력 옵션
'''

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class KakaoLocalAPI:
    """
    Kakao Local API 컨트롤러
    """

    def __init__(self):
        """
        Rest API키 초기화 및 기능 별 URL 설정
        """

        # REST API 키 설정
        self.rest_api_key = "fdc883fda0ab9f3e7a2bec429fc989ae"
        self.headers = {"Authorization": "KakaoAK {}".format("fdc883fda0ab9f3e7a2bec429fc989ae")}

        # 서비스 별 URL 설정

        # 05 키워드 검색
        self.URL_05 = "https://dapi.kakao.com/v2/local/search/keyword.json"
        # self 값 설정

    def search_keyword(self, query, x, y, offset=None, page=None, category_group_code=None,
                       radius=None, size=None, sort=None):
        """
        05 키워드 검색
        """

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

# 함수 실행
query = '순두부'
kakao = KakaoLocalAPI()
df = pd.json_normalize(kakao.search_keyword(query, x = 127, y = 37.5, page = 1, offset = 0.5 )['documents'])
df1 = pd.json_normalize(kakao.search_keyword(query, x = 127, y = 36.5, page = 1, offset = 0.5 )['documents'])
df = df.append(df1, ignore_index=True)

'''
dataframe 전처리
'''
df.drop(columns=['category_group_code', 'category_group_name', 'distance'], axis=1, inplace=True)


df = df.rename(columns={'address_name': 'lc_addr',  'category_group_name': 'cs_activity'
                , 'category_name': 'cs_activity', 'id': 'lc_id', 'phone': 'lc_call_number', 'place_name': 'lc_name',
                   'place_url': 'lc_url', 'road_address_name': 'lc_addr_road', 'x': 'lc_x', 'y': 'lc_y'})

df = df.reindex(columns=['lc_id','lc_name','lc_addr','lc_addr_road','lc_x', 'lc_y', 'lc_call_number', 'lc_url', 'cs_activity'])
print(df)


#df.append(pd.read_json(self.search_keyword(query, x, y, offset= abc, page=page)))

'''
def search_keyword(self, query, x, y, offset=None, page=None, category_group_code=None,
                       radius=None, size=None, sort=None):
'''

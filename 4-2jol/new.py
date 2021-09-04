import requests
import json
import pandas as pd
from pandas import json_normalize

import collections
import folium
import openpyxl

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
MergedDF = df.append(df1, ignore_index=True)
print(MergedDF)


#df.append(pd.read_json(self.search_keyword(query, x, y, offset= abc, page=page)))

'''
def search_keyword(self, query, x, y, offset=None, page=None, category_group_code=None,
                       radius=None, size=None, sort=None):
'''

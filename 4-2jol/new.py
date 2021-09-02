import requests
import json
import openpyxl
import pandas as pd
import collections
import folium

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

    def get_keyword_list(self, query, x, y, offset = 0.01):
        '''
        계산부분
        '''
        page = 1
        res_list = []
        abc = offset

        while True:
            search_count = self.search_keyword(query, x, y, offset=abc)['meta']['total_count']
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
                res_list.extend(a)
                res_list.extend(b)
                res_list.extend(c)
                res_list.extend(d)

                return res_list

            else:
                if self.search_keyword(query, x, y, offset= abc, page=page)['meta']['is_end']:
                    res_list.extend(self.search_keyword(query, x, y, offset= abc, page=page)['documents'])
                    return res_list
                # 아니면 다음 페이지로 넘어가서 데이터 저장
                else:
                    res_list.extend(self.search_keyword(query, x, y, offset= abc, page=page)['documents'])
                    page += 1

    def search_all(self, query):
        # 126 - 128 36.5 - 38.5
        x = 126
        df = pd.DataFrame()

        for j in range(1, 3):
            y = 36.5
            for k in range(1, 3):
                print(x, y)
                every_list_one = self.get_keyword_list(query, x, y, offset=0.5)
                df.append(every_list_one)
                
                y += 0.5
            x += 0.5

        return every_list

# 함수 실행
query = '순두부'
kakao = KakaoLocalAPI()
df = kakao.search_all(query)
print(df)


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

    def __init__(self, rest_api_key):
        """
        Rest API키 초기화 및 기능 별 URL 설정
        """

        # REST API 키 설정
        self.rest_api_key = rest_api_key
        self.headers = {"Authorization": "KakaoAK {}".format(rest_api_key)}

        # 서비스 별 URL 설정

        # 01 주소 검색
        self.URL_01 = "https://dapi.kakao.com/v2/local/search/address.json"
        # 02 좌표-행정구역정보 변환
        self.URL_02 = "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json"
        # 03 좌표-주소 변환
        self.URL_03 = "https://dapi.kakao.com/v2/local/geo/coord2address.json"
        # 04 좌표계 변환
        self.URL_04 = "https://dapi.kakao.com/v2/local/geo/transcoord.json"
        # 05 키워드 검색
        self.URL_05 = "https://dapi.kakao.com/v2/local/search/keyword.json"
        # 06 카테고리 검색
        self.URL_06 = "https://dapi.kakao.com/v2/local/search/category.json"

    def search_address(self, query, analyze_type=None, page=None, size=None):
        """
        01 주소 검색
        """
        params = {"query": f"{query}"}

        if analyze_type != None:
            params["analyze_type"] = f"{analyze_type}"

        if page != None:
            params['page'] = f"{page}"

        if size != None:
            params['size'] = f"{size}"

        res = requests.get(self.URL_01, headers=self.headers, params=params)
        document = json.loads(res.text)

        return document


    def geo_coord2regioncode(self, x, y, input_coord=None, output_coord=None):
        """
        02 좌표-행정구역정보 변환
        """
        params = {"x": f"{x}",
                  "y": f"{y}"}

        if input_coord != None:
            params['input_coord'] = f"{input_coord}"

        if output_coord != None:
            params['output_coord'] = f"{output_coord}"

        res = requests.get(self.URL_02, headers=self.headers, params=params)
        document = json.loads(res.text)

        return document

    def geo_coord2address(self, x, y, input_coord=None):
        """
        03 좌표-주소 변환
        """
        params = {"x": f"{x}",
                  "y": f"{y}"}

        if input_coord != None:
            params['input_coord'] = f"{input_coord}"

        res = requests.get(self.URL_03, headers=self.headers, params=params)
        document = json.loads(res.text)

        return document

    def geo_transcoord(self, x, y, output_coord, input_coord=None):
        """
        04 좌표계 변환
        """
        params = {"x": f"{x}",
                  "y": f"{y}",
                  "output_coord": f"{output_coord}"}

        if input_coord != None:
            params['input_coord'] = f"{input_coord}"

        res = requests.get(self.URL_04, headers=self.headers, params=params)
        document = json.loads(res.text)

        return document

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
#        print(params)

        res = requests.get(self.URL_05, headers=self.headers, params=params)
        document = json.loads(res.text)

        return document

    def get_keyword_list(self, query, x, y, offset = 0.01):
        page = 1
        res_list = []
        abc = offset

        while True:
            search_count = self.search_keyword(query, x, y, offset=abc)['meta']['total_count']
            #print(self.search_keyword(query, x, y, offset= offset, page=page))
            print(search_count, abc, x, y)

            if search_count > 45:
                print('dividing')
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
                    #print(page)
                    res_list.extend(self.search_keyword(query, x, y, offset= abc, page=page)['documents'])
                    print(res_list)
                    return res_list
                # 아니면 다음 페이지로 넘어가서 데이터 저장
                else:
                    #print(page)
                    res_list.extend(self.search_keyword(query, x, y, offset= abc, page=page)['documents'])
                    print(res_list)
                    page += 1



# REST API 키
rest_api_key = "fdc883fda0ab9f3e7a2bec429fc989ae"
kakao = KakaoLocalAPI(rest_api_key)


every_list = []

query_list = ['칼국수','닭요리','냉면','돈까스','우동','패스트푸드','곱창','막창','커피전문점',
              '중화요리','국수','순대','육류','고기','족발','보쌈','갈비','해장국','한식','일식',
              '실내포장마차','갈비','회','중식','일본식주점','아이스크림','샌드위치','장어','떡볶이',
              '순대','양꼬치','참치회','제과','베이커리','술집','국밥','호프','요리주점']
query = '국밥'
x = 126
#for i in range(0, len(query_list)-1):
#query = query_list[i]
for j in range(1, 10): #10
    y = 33
    print('y바뀜')
    for k in range(1, 13): #13
        every_list_one = kakao.get_keyword_list(query, x, y, offset=0.5)
        every_list.extend(every_list_one)
        print(x, y)
        y += 0.5
    x += 0.5

#every

# list를 dataframe 으로 변환 후 excel 에 저장
df = pd.DataFrame(every_list)
print(df)
df.to_excel('test.xlsx', sheet_name = query)



#최종결과 저장 리스트선언


#for i in result_5['documents']:
 #   address_name = i['address_name']
  #  category_name = i['category_name']
   # road_address_name = i['road_address_name']
    #id = i['id']
#    phone = i['phone']
#    place_name = i['place_name']
#    place_url = i['place_url']
#    x_list = float(i['y'])
#    y_list = float(i['x'])
#    newave_list.append({'address_name':address_name, 'category_name':category_name,
#                         'road_address_name':road_address_name, 'id':id, 'phone':phone,
#                         'place_name': place_name, 'place_url': place_url,
#                         'x':x_list, 'y':y_list})


#print(len(newave_list))



# list를 dataframe 으로 변환 후 excel 에 저장
#df = pd.DataFrame(newave_list)
#print(df)
#df.to_excel('test.xlsx', sheet_name = 'ada')

import urllib.request
import xml.dom.minidom

encodingKey = "{인코딩 인증키}"
decodingKey = "{디코딩 인증키}"

print("[START]")

# request url정의
url = "	http://211.237.50.150:7080/openapi/sample/xml/Grid_20150827000000000228_1/1/5"
request = urllib.request.Request(url)

# request보내기
response = urllib.request.urlopen(request)

# 결과 코드 정의
rescode = response.getcode()

if(rescode==200):
    response_body = response.read()
    dom = xml.dom.minidom.parseString(response_body.decode('utf-8'))
    pretty_xml_as_string = dom.toprettyxml()
    find
    print(pretty_xml_as_string)
else:
    print("Error Code:" + rescode)

print("[END]")

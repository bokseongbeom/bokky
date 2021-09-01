import pymysql
import csv
import scipy.io
from haversine import haversine


# pymysql 세팅
conn = pymysql.connect(host="database-1.coyhhlfg38do.ap-northeast-2.rds.amazonaws.com", port=3306, user="admin", password="noobokmizz",
					  db='mydb', charset='utf8')
curs = conn.cursor()

#csv파일 불러오기
conn.commit()
f = open('adam.csv', 'rt', encoding='UTF8')
csvReader = csv.reader(f)


sql
# 거리 계산
haversine(T_NODE, F_NODE, unit = 'm')


for row in csvReader:
	user_no = (row[0])
	user_pred = (row[1])
	print(user_pred)
	print(user_no)
	sql = """insert into sabjill (title, content) values (%s, %s)"""
	curs.execute(sql, (user_no, user_pred))

# db의 변화 저장
conn.commit()
f.close()
conn.close()
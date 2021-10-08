import pymysql, calendar, time, json
import json
import pandas as pd
import random


class apdo:

    def __init__(self):
        # MARIA DB CON 설정
        self.conn = pymysql.connect(host="database-1.coyhhlfg38do.ap-northeast-2.rds.amazonaws.com",
                                    port=3306, user="admin", password="noobokmizz",
                                    db='mydb', charset='utf8')
        self.conn.commit()

    def read_search_info(self):
        """DB의 search table에서 검색어 불러들이기"""
        with self.conn.cursor() as curs:
            sql = "SELECT * FROM search"
            search = pd.read_sql(sql, self.conn)

        return search

    def search_info(self):
        """search table 검색어를 토대로 프로그램 시작"""
        search = self.read_search_info()
        for idx in range(len(search)):
            code = search.search_id.values[random.randint(0, int(len(search)))]
            print(code)

    def search_info(self):
        """search table 검색어를 토대로 프로그램 시작"""
        search = self.read_search_info()
        for idx in range(len(search)):
            code = search.search_id.values[random.randint(0, int(len(search)))]
            print(code)

    def replace_into_db(self, df):
        """members TABLE에 REPLACE"""
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

if __name__ == '__main__':
    dbu = apdo()
    dbu.search_info()
import pymysql
import pandas as pd
import random
import RandomString as RS

class gogo:

    def __init__(self):
        # MARIA DB CON 설정
        self.conn = pymysql.connect(host="database-1.coyhhlfg38do.ap-northeast-2.rds.amazonaws.com",
                                    port=3306, user="admin", password="noobokmizz",
                                    db='mydb', charset='utf8')

    def read_search_info(self):
        """DB의 search table에서 검색어 불러들이기"""
        with self.conn.cursor() as curs:
            sql = "SELECT MAX(mem_idnum) as MAX FROM members"
            search = pd.read_sql(sql, self.conn)
            MAX = search.MAX.values[0]
            if MAX == None:
                print(1)
            print(MAX)

        return search


if __name__ == '__main__':
    dbu = gogo()
    dbu.read_search_info()
import pymysql
import pandas as pd
import random
import RandomString as RS

class recommend:
    def __init__(self):
        # MARIA DB CON 설정
        self.conn = pymysql.connect(host="database-1.coyhhlfg38do.ap-northeast-2.rds.amazonaws.com",
                                    port=3306, user="admin", password="noobokmizz",
                                    db='mydb2', charset='utf8')

    def selectbk_contents(self):
        with self.conn.cursor():
            sql = "SELECT * FROM members"
            members = pd.read_sql(sql, self.conn)
            print(members)
        return members

    def slect

recommend = recommend()
last = recommend.selectbk_contents()
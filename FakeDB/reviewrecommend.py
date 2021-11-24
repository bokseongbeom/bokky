import pymysql
import pandas as pd
import random


class NEWbkcontents:

    def __init__(self):
        # MARIA DB CON 설정
        self.conn = pymysql.connect(host="database-1.coyhhlfg38do.ap-northeast-2.rds.amazonaws.com",
                                    port=3306, user="admin", password="noobokmizz",
                                    db='mydb3', charset='utf8')
        with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE IF NOT EXISTS `review` (
              `rv_comment` text,
              `rv_starrate` int DEFAULT NULL,
              `rv_time` datetime DEFAULT NULL,
              `mem_idnum` int NOT NULL,
              `mem_userid` varchar(20) DEFAULT NULL,
              `lc_id` varchar(16) NOT NULL,
              PRIMARY KEY (`mem_idnum`,`lc_id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                        """
            curs.execute(sql)

        self.conn.commit()

    def read_members(self):
        """DB의 members table에서 pk 불러들이기"""

        with self.conn.cursor() as curs:
            sql = f"SELECT * FROM members"
            members = pd.read_sql(sql, self.conn)

        return members

    def read_location(self):
        """DB의 location table에서 pk 불러들이기"""
        with self.conn.cursor() as curs:
            sql = f"SELECT * FROM location"
            location = pd.read_sql(sql, self.conn)

        return location

    def replace_into_db(self):
        """members TABLE에 REPLACE"""
        with self.conn.cursor() as curs:
            members = self.read_members()
            location = self.read_location()

            p = 1000000
            for idx in range(p):
                print("304")
                x = random.randint(0, len(members)-1)
                y = random.randint(0, len(location)-1)
                mem_idnum = members['mem_idnum'][x]
                mem_userid = members['mem_userid'][x]
                lc_id = location['lc_id'][y]
                rv_comment = "좋아요"
                rv_starrate = random.randint(0,10) * 5
                # sql = f"SELECT * FROM category_info WHERE category_id = {lc_category}"

                sql = f"REPLACE INTO `review` (rv_comment,rv_starrate,mem_idnum,mem_userid,lc_id)" \
                      f"VALUES ('{rv_comment}','{rv_starrate}','{mem_idnum}','{mem_userid}','{lc_id}')"
                curs.execute(sql)
                self.conn.commit()




if __name__ == '__main__':
    dbu = NEWbkcontents()
    dbu.replace_into_db()
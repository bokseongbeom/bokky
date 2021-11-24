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
            CREATE TABLE IF NOT EXISTS `keywordstolc` (
              `lc_id` int NOT NULL,
              `kID` varchar(45) NOT NULL,
              `keyword` varchar(45) NOT NULL,
              `ID` varchar(45) NOT NULL,
              PRIMARY KEY (`ID`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

            """
            curs.execute(sql)

        self.conn.commit()

    def read_keywords(self):
        """DB의 members table에서 pk 불러들이기"""
        with self.conn.cursor() as curs:
            sql = "SELECT * FROM keywords"
            members = pd.read_sql(sql, self.conn)

        return members

    def read_location(self):
        """DB의 location table에서 pk 불러들이기"""
        with self.conn.cursor() as curs:
            sql = "SELECT * FROM location"
            location = pd.read_sql(sql, self.conn)

        return location

    def replace_into_db(self):
        """members TABLE에 REPLACE"""
        with self.conn.cursor() as curs:
            keywords = self.read_keywords()
            location = self.read_location()

            p = 500000
            for idx in range(p):
                x = random.randint(0,len(location)-1)
                qstu = random.randint(3,7)
                for op in range(qstu):
                    y = random.randint(0,len(keywords)-1)
                    kID = keywords['kID'][y]
                    keyword = keywords['keyword'][y]
                    lc_id = location['lc_id'][x]
                    ID = f"{lc_id}and{kID}"

                    sql = f"INSERT IGNORE INTO `keywordstolc` (lc_id,kID,keyword,ID)" \
                          f"VALUES ('{lc_id}','{kID}','{keyword}','{ID}')"
                    curs.execute(sql)
                self.conn.commit()




if __name__ == '__main__':
    dbu = NEWbkcontents()
    dbu.replace_into_db()
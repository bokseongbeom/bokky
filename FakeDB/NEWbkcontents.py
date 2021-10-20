import pymysql
import pandas as pd
import random



class NEWbkcontents:

    def __init__(self):
        # MARIA DB CON 설정
        self.conn = pymysql.connect(host="database-1.coyhhlfg38do.ap-northeast-2.rds.amazonaws.com",
                                    port=3306, user="admin", password="noobokmizz",
                                    db='mydb', charset='utf8')
        with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE IF NOT EXISTS `bkcontents` (
              `mem_idnum` int NOT NULL,
              `bk_id` int NOT NULL,
              `lc_id` varchar(16) DEFAULT NULL,
              `category_id` int DEFAULT NULL,
              PRIMARY KEY (`mem_idnum`,`bk_id`),
              KEY `fk_bkcontents_category_info_idx` (`category_id`),
              KEY `fk_bkcontents_location_idx` (`lc_id`),
              CONSTRAINT `loc` FOREIGN KEY (`lc_id`, `category_id`) REFERENCES `location` (`lc_id`, `lc_category`),
              CONSTRAINT `mem` FOREIGN KEY (`mem_idnum`, `bk_id`) REFERENCES `members` (`mem_idnum`, `bk_id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """

            curs.execute(sql)

        self.conn.commit()

    def read_members(self):
        """DB의 members table에서 pk 불러들이기"""
        with self.conn.cursor() as curs:
            sql = "SELECT * FROM members"
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
            members = self.read_members()
            location = self.read_location()
            p = 5000
            for idx in range(p):
                x = random.randint(0,len(members)-1)
                y = random.randint(0,len(location)-1)
                mem_idnum = members['mem_idnum'][x]
                bk_id = members['bk_id'][x]
                lc_id = location['lc_id'][y]
                lc_category = location['lc_category'][y]

                if idx % 1000 == 0:
                    print(f"{(idx/p) * 100}% uploading")


                sql = f"REPLACE INTO `bkcontents` (mem_idnum, bk_id, lc_id,  category_id)" \
                      f"VALUES ('{mem_idnum}','{bk_id}','{lc_id}','{lc_category}')"
                curs.execute(sql)
            self.conn.commit()




if __name__ == '__main__':
    dbu = NEWbkcontents()
    dbu.replace_into_db()
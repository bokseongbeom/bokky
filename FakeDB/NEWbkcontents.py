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
              `mem_userid` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
              `bk_id` int NOT NULL,
              `lc_id` varchar(45) DEFAULT NULL,
              `lc_name` varchar(45) DEFAULT NULL,
              `category` varchar(45) DEFAULT NULL,
              PRIMARY KEY (`mem_idnum`,`mem_userid`,`bk_id`),
              KEY `ff_idx` (`lc_id`,`category`),
              KEY `fk_bkcontents_category_info_idx` (`category`),
              KEY `fk_bkcontents_location_idx` (`lc_id`,`lc_name`),
              CONSTRAINT `fk_bkcontents_location` FOREIGN KEY (`lc_id`, `lc_name`) REFERENCES `location` (`lc_id`, `lc_name`),
              CONSTRAINT `fk_bkcontents_members1` FOREIGN KEY (`mem_idnum`, `mem_userid`, `bk_id`) REFERENCES `members` (`mem_idnum`, `mem_userid`, `bk_id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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

    def read_category_info(self):
        """DB의 category_info에서 category 불러들이기"""
        with self.conn.cursor() as curs:
            sql = "SELECT * FROM category_info"
            category = pd.read_sql(sql, self.conn)

        return category


    def replace_into_db(self):
        """members TABLE에 REPLACE"""
        with self.conn.cursor() as curs:
            members = self.read_members()
            location = self.read_location()
            category_info = self.read_category_info()
            for idx in range(0,5):
                x = random.randint(0,len(members)-1)
                y = random.randint(0,len(location)-1)
                z = random.randint(0,len(category_info)-1)
                mem_idnum = members['mem_idnum'][x]
                mem_userid = members['mem_userid'][x]
                bk_id = members['bk_id'][x]
                lc_id = location['lc_id'][y]
                lc_name = location['lc_name'][y]
                lc_category = location['lc_category'][y]


                print(f"'{mem_idnum}', " \
                      f"'{mem_userid}', '{bk_id}' ,'{lc_id}' " \
                      f",'{lc_name}','{lc_category}'")
                sql = f"REPLACE INTO `bkcontents` " \
                      f"(mem_idnum, mem_userid ,bk_id ,lc_id," \
                      f"lc_name,category)VALUES ('{mem_idnum}', " \
                      f"'{mem_userid}', '{bk_id}' ,'{lc_id}' " \
                      f",'{lc_name}','{lc_category}')"
                curs.execute(sql)
            self.conn.commit()




if __name__ == '__main__':
    dbu = NEWbkcontents()
    dbu.replace_into_db()
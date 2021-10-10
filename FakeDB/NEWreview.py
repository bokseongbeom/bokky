import pymysql
import pandas as pd
import random
import RandomString as RS

class NEWreview:

    def __init__(self):
        # MARIA DB CON 설정
        self.conn = pymysql.connect(host="database-1.coyhhlfg38do.ap-northeast-2.rds.amazonaws.com",
                                    port=3306, user="admin", password="noobokmizz",
                                    db='mydb', charset='utf8')
        with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE IF NOT EXISTS `review` (
              `location_lc_id` varchar(16) NOT NULL,
              `location_lc_name` varchar(40) NOT NULL,
              `sex` tinyint DEFAULT NULL,
              `review_text` varchar(45) DEFAULT NULL,
              `reveiw_rate` int NOT NULL,
              `age` date DEFAULT NULL,
              PRIMARY KEY (`location_lc_id`,`location_lc_name`),
              CONSTRAINT `fk_review_location1` FOREIGN KEY (`location_lc_id`, `location_lc_name`) REFERENCES `location` (`lc_id`, `lc_name`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

            """
            curs.execute(sql)

        self.conn.commit()


    def read_location(self):
        """DB의 location table에서 pk 불러들이기"""
        with self.conn.cursor() as curs:
            sql = "SELECT * FROM location"
            location = pd.read_sql(sql, self.conn)

        return location

    def replace_into_db(self):
        """members TABLE에 REPLACE"""
        with self.conn.cursor() as curs:

            location = self.read_location()

            for idx in range(0,5):

                x = random.randint(0,len(location)-1)

                location_lc_id = location['lc_id'][x]
                location_lc_name = location['lc_name'][x]
                sex = random.randint(0,1)
                reveiw_rate = random.randint(0,10)
                age = RS.makeDate()


                print(f"'{location_lc_id}', " \
                      f"'{location_lc_name}', '{sex}' ,'{reveiw_rate}' " \
                      f",'{age}'")
                sql = f"REPLACE INTO `review` " \
                      f"(location_lc_id, location_lc_name ,sex ,reveiw_rate," \
                      f"age)VALUES ('{location_lc_id}', " \
                      f"'{location_lc_name}', '{sex}' ,'{reveiw_rate}' " \
                      f",'{age}')"
                curs.execute(sql)
            self.conn.commit()




if __name__ == '__main__':
    dbu = NEWreview()
    dbu.replace_into_db()
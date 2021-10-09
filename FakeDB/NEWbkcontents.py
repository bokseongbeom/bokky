import pymysql, calendar, time, json
import json
import pandas as pd
import random
import RandomString as RS
from datetime import datetime


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
              CONSTRAINT `fk_bkcontents_category_info` FOREIGN KEY (`category`) REFERENCES `category_info` (`category`),
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
            category = self.read_category_info()
            for idx in range(1,100):
                mem_idnum = random.randint(0, 100)
                mem_userid = f"user{mem_idnum}"


                sql = f"REPLACE INTO `members` (mem_idnum, " \
                      f"mem_userid,bk_id ,mem_email ,mem_nickname," \
                      f"mem_phone,mem_sex ,mem_birthday,mem_register_datetime," \
                      f"mem_is_admin ,mem_following,mem_followed ,mem_password," \
                      f"mem_profile_content,mem_username,mem_autologin," \
                      f"mem_birthday_open,mem_sex_open,mem_receive_email," \
                      f"mem_receive_sns,mem_open_profile,mem_noti_allow," \
                      f"mem_denied,mem_email_cert,mem_lastlogin_datetime," \
                      f"mem_adminmemo,mem_photo,bk_name,bk_open_bucketlist," \
                      f"bk_share)VALUES ('{mem_idnum}', '{mem_userid}', '{bk_id}' ,'{mem_email}' " \
                      f",'{mem_nickname}','{mem_phone}','{mem_sex}' ,'{mem_birthday}','{mem_register_datetime}' " \
                      f",'{mem_is_admin}' ,'{mem_following}' ,'{mem_followed}' ,'{mem_password}' " \
                      f",'{mem_profile_content}','{mem_username}','{mem_autologin}' ,'{mem_birthday_open}'" \
                      f",'{mem_sex_open}' ,'{mem_receive_email}' ,'{mem_receive_sns}' ,'{mem_open_profile}' " \
                      f",'{mem_noti_allow}' ,'{mem_denied}' ,'{mem_email_cert}' ,'{mem_lastlogin_datetime}' " \
                      f",'{mem_adminmemo}' ,'{mem_photo}' ,'{bk_name}' ,'{bk_open_bucketlist}' ,'{bk_share}')"
                curs.execute(sql)
            self.conn.commit()




if __name__ == '__main__':
    dbu = NEWbkcontents()
    dbu.replace_into_db()
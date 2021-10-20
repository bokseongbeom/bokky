import pymysql
import pandas as pd
import random
import RandomString as RS
from datetime import datetime


class NEWmem:

    def __init__(self):
        # MARIA DB CON 설정
        self.conn = pymysql.connect(host="database-1.coyhhlfg38do.ap-northeast-2.rds.amazonaws.com",
                                    port=3306, user="admin", password="noobokmizz",
                                    db='mydb', charset='utf8')
        with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE IF NOT EXISTS `members` (
              `mem_idnum` int NOT NULL,
              `mem_userid` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
              `bk_id` int NOT NULL,
              `mem_email` varchar(30) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
              `mem_nickname` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
              `mem_phone` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
              `mem_sex` tinyint NOT NULL,
              `mem_birthday` date NOT NULL,
              `mem_register_datetime` datetime NOT NULL,
              `mem_is_admin` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
              `mem_following` int DEFAULT NULL,
              `mem_followed` int DEFAULT NULL,
              `mem_password` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
              `mem_profile_content` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
              `mem_username` varchar(32) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
              `mem_autologin` tinyint(1) DEFAULT NULL,
              `mem_birthday_open` tinyint(1) DEFAULT NULL,
              `mem_sex_open` tinyint(1) DEFAULT NULL,
              `mem_receive_email` tinyint(1) DEFAULT NULL,
              `mem_receive_sns` tinyint(1) DEFAULT NULL,
              `mem_open_profile` tinyint(1) DEFAULT NULL,
              `mem_noti_allow` tinyint(1) DEFAULT NULL,
              `mem_denied` tinyint(1) DEFAULT NULL,
              `mem_email_cert` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
              `mem_lastlogin_datetime` datetime DEFAULT NULL,
              `mem_adminmemo` mediumtext CHARACTER SET utf8 COLLATE utf8_bin,
              `mem_photo` mediumtext CHARACTER SET utf8 COLLATE utf8_bin,
              `bk_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
              `bk_open_bucketlist` tinyint DEFAULT NULL,
              `bk_share` tinyint DEFAULT NULL,
              PRIMARY KEY (`mem_idnum`,`bk_id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
            """
            curs.execute(sql)

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
            code = search.search_id.values[random.randint(0, int(len(search))) - 1]
            print(code)


    def search_info(self):
        """search table 검색어를 토대로 프로그램 시작"""
        search = self.read_search_info()
        for idx in range(len(search)):
            code = search.search_id.values[random.randint(0, int(len(search)))]
            print(code)

    def replace_into_db(self):
        """members TABLE에 REPLACE"""
        with self.conn.cursor() as curs:

            sql = "SELECT MAX(mem_idnum) as MAX FROM members"
            memnum = pd.read_sql(sql, self.conn)
            MAX = memnum.MAX.values[0]

            if MAX == None:
                start = 0
            else:
                start = MAX + 1
            end = start + 100

            sql = "SELECT MAX(bk_id) as MAX FROM members"
            bkid = pd.read_sql(sql, self.conn)
            bkMAX = bkid.MAX.values[0]

            if bkMAX == None:
                count = 0
            else:
                count = bkMAX+1

            #bk_id_list = list(range(1000, 1100))

            for idx in range(start, end):
                mem_idnum = idx
                mem_userid = f"user{mem_idnum}"
                mem_nickname = RS.makeString() #
                mem_email = RS.makeEmail(mem_nickname) #
                mem_phone = RS.makePhonenum() #
                mem_sex = random.randint(0,1) #
                mem_birthday = RS.makeDate() #
                mem_register_datetime = datetime.today().strftime('%Y-%m-%d')
                mem_is_admin = 0 #
                mem_following = 0 #
                mem_followed = 0 #
                mem_password = "0123" #
                mem_profile_content = 'NOPE' #
                mem_username = mem_nickname #
                mem_autologin = random.randint(0,1) #
                mem_birthday_open = random.randint(0,1) #
                mem_sex_open = random.randint(0,1) #
                mem_receive_email = random.randint(0,1) #
                mem_receive_sns = random.randint(0,1) #
                mem_open_profile = random.randint(0,1) #
                mem_noti_allow = random.randint(0,1) #
                mem_denied = 0 #
                mem_email_cert = random.randint(0,1) #
                mem_lastlogin_datetime = datetime.today().strftime('%Y-%m-%d') #
                mem_adminmemo = 'NOPE' #
                mem_photo = 'NOPE' #

                bk_name = f"{mem_nickname}의 버킷리스트"
                bk_open_bucketlist = 1
                bk_share = 0



                for ivx in range(0,2):
                    print(ivx)

                    if ivx != 0:

                        while True:
                            bk_share = 1
                            bk_id = random.randint(0, count)

                            sql = f"SELECT * FROM members WHERE bk_id = {bk_id}"
                            DB_bkshare = pd.read_sql(sql, self.conn)

                            if DB_bkshare.empty:
                                break

                            check_bk_share = DB_bkshare.bk_share.values[0]

                            if check_bk_share == 1:
                                if bk_id == count:
                                    count = count + 1
                                break

                    elif ivx == 0:
                        bk_share = 0
                        bk_id = count
                        count = count + 1

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
    dbu = NEWmem()
    dbu.replace_into_db()
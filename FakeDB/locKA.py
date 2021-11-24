import pymysql
import pandas as pd

class FillCategory:
    """ category 다채우기 """

    def __init__(self):

        # MARIA DB CON 설정
        self.conn = pymysql.connect(host="database-1.coyhhlfg38do.ap-northeast-2.rds.amazonaws.com",
                                    port=3306, user="admin", password="noobokmizz",
                                    db='mydb', charset='utf8')
        self.conn.commit()

    def Fillcategory(self):
        with self.conn.cursor() as curs:

            sql = f"SELECT * FROM category_info"
            category_list = pd.read_sql(sql, self.conn)

            category_list = category_list.drop_duplicates()

            for idx in range(len(category_list)):
                categor

                y = category_list.choice.values[idx]


                sql = f"REPLACE INTO category_info ( category, category_id )VALUES ('{category}' , '{cl_activity}' , '{cm_activity}' , '{cs_activity}')"
                print(sql)
                curs.execute(sql)

            sql = f"SELECT * FROM category_info"
            category_info = pd.read_sql(sql, self.conn)

            for idx in range(len(category_info)):
                lc_category = category_info.category_id.values[idx]
                lc_id = '-' + f"{idx}"
                lc_name = category_info.category.values[idx]

                sql = f"REPLACE INTO location (lc_id, lc_name, lc_category)VALUES ('{lc_id}', '{lc_name}', '{lc_category}')"
                print(sql)
                curs.execute(sql)
            self.conn.commit()



if __name__ == '__main__':
    dbu = FillCategory()
    dbu.Fillcategory()
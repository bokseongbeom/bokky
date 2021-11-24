import pymysql
import pandas as pd

print("pandas version: ", pd.__version__)
pd.set_option('display.max_row', 500)
pd.set_option('display.max_columns', 100)

class FillCategory:
    """ category 다채우기 """

    def __init__(self):

        # MARIA DB CON 설정
        self.conn = pymysql.connect(host="database-1.coyhhlfg38do.ap-northeast-2.rds.amazonaws.com",
                                    port=3306, user="admin", password="noobokmizz",
                                    db='mydb3', charset='utf8')
        self.conn.commit()
    def Fillcategory(self):
        with self.conn.cursor() as curs:
            sql = f"SELECT * FROM category_info"
            category_list = pd.read_sql(sql, self.conn)

            category_list = category_list.drop_duplicates()

            df = category_list
            df.drop(columns=['category_id'], axis=1, inplace=True)
            for x in range(0,3):
                print(x)
                for idx in range(len(category_list)):
                    if x == 0:
                        category = category_list.cs_activity.values[idx]
                        cl_activity = category_list.cl_activity.values[idx]
                        cm_activity = category_list.cm_activity.values[idx]
                        cs_activity = category_list.cs_activity.values[idx]
                    elif x == 1:
                        category = category_list.cm_activity.values[idx]
                        cl_activity = category_list.cl_activity.values[idx]
                        cm_activity = category_list.cm_activity.values[idx]
                        cs_activity = category_list.cm_activity.values[idx]
                    elif x == 2:
                        category = category_list.cl_activity.values[idx]
                        cl_activity = category_list.cl_activity.values[idx]
                        cm_activity = category_list.cl_activity.values[idx]
                        cs_activity = category_list.cl_activity.values[idx]
                    new_data = {
                        'category': category,
                        'cl_activity': cl_activity,
                        'cm_activity': cm_activity,
                        'cs_activity': cs_activity
                    }
                    df = df.append(new_data, ignore_index=True)

                    # sql = f"REPLACE INTO category_info ( category, category_id )VALUES ('{category}' , '{cl_activity}' , '{cm_activity}' , '{cs_activity}')"
            df = df.drop_duplicates()

            print(df)
            for idx in range(len(df)):

                category = df.category.values[idx]
                cl_activity = df.cl_activity.values[idx]
                cm_activity = df.cm_activity.values[idx]
                cs_activity = df.cs_activity.values[idx]

                sql = f"INSERT IGNORE INTO category_info (category,cl_activity,cm_activity,cs_activity)VALUES ('{category}','{cl_activity}','{cm_activity}','{cs_activity}')"


                curs.execute(sql)
                self.conn.commit()

            sql = f"SELECT * FROM category_info"
            loc_list = pd.read_sql(sql, self.conn)
            loc_list = loc_list.drop_duplicates()

            df = loc_list

            for idx in range(len(df)):
                lc_category = df.category_id.values[idx]
                lc_id = '-' + f"{idx}"
                lc_name = df.category.values[idx]

                sql = f"INSERT IGNORE INTO location (lc_id,lc_name,lc_category)VALUES ('{lc_id}','{lc_name}','{lc_category}')"
                print(sql)
                curs.execute(sql)
            self.conn.commit()


if __name__ == '__main__':
    dbu = FillCategory()
    dbu.Fillcategory()
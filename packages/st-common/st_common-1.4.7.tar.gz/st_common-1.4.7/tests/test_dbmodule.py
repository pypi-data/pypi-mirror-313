import unittest
from parameterized import parameterized

from st_common import SQLDatabase,RedisPriorityQueue,MongoDBClient
from st_common import CommonBase
from st_common import Secure

import pandas as pd
from table_strcture import TableSellersCompetitor, TableCommonSess,TableVideoIcRaw,TableSellersCompetitor,ALL_ACCOUNT_SQL
from sqlalchemy import text
import pandas as pd
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
load_dotenv()

class MongoDBDatabaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # print("在每个类之前执行，如创建一个类，创建数据库链接，初始化日志对象")
        # 使用 quote_plus 来进行URL编码
        username = "spider_user"
        password = "Syz2022"
        # 构造数据库连接字符串
        # db_string = f"mongodb://{username}:{password}@host:port/database"
        cls.my_mongodb = MongoDBClient(db_string=f"mongodb://{username}:{password}@192.168.6.243:27017/spider_data")
        ### mongodb://[username:password@]host1[:
    @classmethod
    def tearDownClass(cls) -> None:
        # print("在每个类之后执行，如销毁一个类，销毁数据库链接，销毁日志对象")
        pass

    @unittest.skip(reason="test_push pass")
    def test_insert(self,):
        status = self.my_mongodb.insert_document(database_name="spider_data",collection_name="cache_tiktok_api_search",document={"a":1})
        print(status)
        pass
class RedisDatabaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # print("在每个类之前执行，如创建一个类，创建数据库链接，初始化日志对象")
        cls.my_redis = RedisPriorityQueue(name="seller_priority_queue", host="192.168.6.247", port=6379, db=0)
    @classmethod
    def tearDownClass(cls) -> None:
        # print("在每个类之后执行，如销毁一个类，销毁数据库链接，销毁日志对象")
        pass

    @unittest.skip(reason="test_push pass")
    def test_push(self,):
        # self.my_redis.push({'name':'low_priority_task'}, 100) # 更高的分数表示更低的优先级
        # self.my_redis.push({'name':'high_priority_task'}, 10) # 更低的分数表示更高的优先级
        # 使用示例
        items_with_priorities = [
            {'id': 'task1', 'priority': 5},
            {'id': 'task2', 'priority': 1},
            {'id': 'task3', 'priority': 10}
        ]
        priority_queue = self.my_redis
        for item in items_with_priorities:
            priority_queue.push(item, item['priority'])
    @unittest.skip(reason="test_pop pass")
    def test_pop(self): 
        # 弹出元素
        # 示例
        # priority_queue = self.my_redis
        # while True:
        #     item = priority_queue.pop()
        #     print(item)
        #     if item is None:
        #         break
        #     else:
        #         print(item)
        # 测试用例
        priority_queue = self.my_redis
        item = priority_queue.pop()
        print(item)
    @unittest.skip(reason="test_pop pass")
    def test_peek(self):
        # 获取队列头部元素
        # 示例
        # priority_queue = self.my_redis
        # while True:
        #     item = priority_queue.peek()
        #     print(item)
        #     if item is None:
        #         break
        #     else:
        #         print(item)
        # 测试用例
        priority_queue = self.my_redis
        item = priority_queue.peek()
        print(item)

class SQLDatabaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # init self.sqldatabase
        mode = "dev"
        commonbase =  CommonBase(log_file="test.log")
        if mode == "pro":
            dsn=os.getenv("PRO_MYSQL_DB_STRING")
        else:
            dsn = os.getenv('DEV_MYSQL_DB_STRING')
        cls.sqldatabase = SQLDatabase(db_string = dsn)
    @classmethod
    def tearDownClass(cls) -> None:
        cls.sqldatabase.close()

    def test_create_table(self):
        result = self.sqldatabase.session.execute(text(ALL_ACCOUNT_SQL))
        self.assertEqual(result.rowcount, 0)
    
    
    @parameterized.expand(
            [
                ("all_account", {"station_name":"test","username":"test01","password":"testpw","status":"0"},True),
                ]
    )
    def test_insert_data(self,table_name,item,result):
        self.assertEqual(first=self.sqldatabase.insert_data(table_name=table_name, data_dict=item),second=result)
    @parameterized.expand(
            [
                ("all_account", {"id":"1","station_name":"test","username":"test01","password":"testpw","status":"3"},True),
                ("all_account", {"id":"1","station_name":"test01","username":"test01","password":"testpw","status":"3"},True),
                ("all_account", {"id":"1","station_na":"test01","username":"test01","password":"testpw","status":"3"},False)
            ]
    )
    def test_insert_or_update(self,table_name,data_dict,result):
        self.assertEqual(first=self.sqldatabase.update_or_insert_data(table_name=table_name, data_dict=data_dict), second=result)


    @unittest.skip(reason="table structure with base pass")
    def test_create_table_01(self):
        self.assertTrue(expr=self.sqldatabase.create_table(table_name=TableSellersCompetitor.__tablename__,declarative_base_table=TableSellersCompetitor))

    @unittest.skip(reason="table structure with base pass")
    def test_create_table_03(self):
        self.assertTrue(expr=self.sqldatabase.create_table(table_name=TableVideoIcRaw.__tablename__,declarative_base_table=TableVideoIcRaw))

    @unittest.skip(reason="table structure with base pass")
    def test_create_table_04(self):
        self.assertTrue(expr=self.sqldatabase.create_table(table_name=TableSellersCompetitor.__tablename__,declarative_base_table=TableSellersCompetitor))
   
    @parameterized.expand(
            [
                ("all_account", {"station_name":"test","username":"test01","password":"testpw","status":"0"}),
                # ("all_account_orm", {"station_name":"test","username":"test01","password":"testpw","status":"0"})
                ]
    )
    @unittest.skip(reason="test_insert_data_01 pass")
    def test_insert_data_01(self,table_name,item):
        self.sqldatabase.insert_data(table_name=table_name, data_dict=item)


    @parameterized.expand(
        [
            ("sellers_competitor_asin", r"C:\Users\Administrator\Downloads\ut市场数据.csv"),
        ]
    )
    @unittest.skip(reason="test_insert_or_update_from_csv_to_database pass")
    def test_insert_or_update_from_csv_to_database(self,table_name,file_path):
        df = pd.read_csv(file_path)
        for data_dict in df.to_dict("records"):
            self.sqldatabase.update_or_insert_data(table_name=table_name, data_dict=data_dict)
            # self.assertEqual(first=self.sqldatabase.update_or_insert_data(table_name=table_name, data_dict=data_dict), second=True)
        pass

    @parameterized.expand(
            [
                ("all_account", {"station_name":"test","username":"test01"},{"station_name":"test","username":"test01","password":"testpw","status":"-1"}),
                # ("all_account_orm", {"id":"1","station_name":"test","username":"test01","password":"testpw","status":"3"})
                ]
    )
    @unittest.skip(reason="test_update_or_insert_data_in_log pass")
    def test_update_or_insert_data_in_log(self,table_name, condition_dict, title_dict):
        if self.sqldatabase.fetch(table_name=table_name,filt_dict=condition_dict):
            self.sqldatabase.update_data(table_name=table_name,condition_dict=condition_dict,new_data_dict=title_dict)
        else:
            self.sqldatabase.insert_data(table_name=table_name,data_dict=title_dict)




    @parameterized.expand([
        ("test",93)
        ])
    @unittest.skip(reason="fetch pass")
    def test_fetch_data(self,table_name, data_num):
        self.assertEqual(first=len(self.sqldatabase.fetch(table_name=table_name)), second=data_num)
        pass

    @parameterized.expand([
        ({"platform": "ins"},"mundownloa"),
        ({"platform": "is"},None)
        ])
    @unittest.skip(reason="test_fetch_data_filter pass")
    def test_fetch_data_filter(self,filt_dict,want_result):
        result = self.sqldatabase.fetch(table_name="common_sess",filt_dict=filt_dict)
        if not result:
            print("result is tmp list")
            return 0
        self.assertEqual(first=result[0]._asdict().get("username",None),second=want_result)

    @parameterized.expand([
        ("video_ic_raw")
    ])
    @unittest.skip(reason="test_get_columns_comment pass")
    def test_get_columns_comment(self, table_name):
        result_data_dict = self.sqldatabase._get_columns_comment_dict(table_name=table_name)
        print(result_data_dict)
        # self.assertDictEqual(d1=data_dict,d2=result_data_dict )

    @parameterized.expand([
            ("sellers_competitor_url")
        ])
    @unittest.skip(reason="test_get_columns_name pass")
    def test_get_columns_name(self, table_name):
        result_data_dict = self.sqldatabase._get_columns_name(table_name=table_name)
        print(result_data_dict)

    @unittest.skip(reason="test_export_data pass")
    def test_export_data(self):
        # 从数据库导出数据
        fetch_all = self.sqldatabase.fetch(table_name="video_ic_raw")
        data_csv = pd.DataFrame(fetch_all)
        rename_dict =  self.sqldatabase._get_columns_comment_dict(table_name="video_ic_raw")
        data_csv.rename(columns=rename_dict,inplace=True)
        # pass
    @unittest.skip(reason="test_inport_xls_2 pass")
    def test_import_xls_2(self):
        # python, 指定文件夹A，遍历文件夹，并将文件夹名称赋值给B，读取文件夹下面的.xlsx文件格式，赋值给C，追加两列数据B和C，并合并所有xlsx文件，
        original_dict = self.sqldatabase._get_columns_comment_dict(table_name="sellers_competitor_url")
        swapped_dict = {v: k for k, v in original_dict.items()}
        error_file = "new_file.xlsx"
        error_list = []
        items = pd.read_excel(error_file)
        for item in items.to_dict("records"):
            file_name = item["test"]
            # 判断是否为.xlsx文件
            if file_name.endswith('.xlsx'):
                cate_id = file_name.split("\\")[-2]
                station_name = "com"
                month = file_name.split("-")[-2].replace(".","-")
                df = pd.read_excel(file_name)
                # ### prime价格, 卖家首页, 品牌链接 ## 商品详情链接 # 近30天评论数
                if "商品详情链接" in df.columns:
                    df.drop("商品详情链接", axis=1, inplace=True)
                if "近30天新增评论数" in df.columns:
                    df.drop("近30天新增评论数", axis=1, inplace=True)
                if "类目" in df.columns:
                    df.rename(columns={"类目":"类目路径"},inplace=True)
                    df.drop("BSR排名", axis=1, inplace=True)
                if "prime价格($)" in df.columns:
                    df.rename(columns={"prime价格($)":"价格"},inplace=True)
                if "BuyBox卖家国籍" in df.columns:
                    df.rename(columns={"BuyBox卖家国籍":"卖家所属地"},inplace=True)
                if "卖家首页" in df.columns:
                    df.drop("卖家首页", axis=1, inplace=True)
                if "品牌链接" in df.columns:
                    df.drop("品牌链接", axis=1, inplace=True)
                df.fillna("None",inplace=True)
                for col in df.columns:
                    if "$" in col:
                        col_new = col.replace("($)","") 
                        df.rename(columns={col:col_new},inplace=True)
                df['序号'] = range(1, len(df) + 1)
                df['station_name'] = station_name  # 追加文件夹名称列
                df['cate_id'] = cate_id  # 追加文件名列
                df["month"] = month
            
                df.rename(columns=swapped_dict,inplace=True)
                # df.to_sql(name="sellers_competitor_url", con=self.sqldatabase.engine)
                for item in df.to_dict("records"):
                    if not self.sqldatabase.insert_data(table_name="sellers_competitor_url",data_dict=item):
                        error_list.append(file_name)
        pd.DataFrame(error_list).to_excel("error_list.xlsx")
    @unittest.skip(reason="test_inport_xls pass") 
    def test_inport_xls(self):
        # python, 指定文件夹A，遍历文件夹，并将文件夹名称赋值给B，读取文件夹下面的.xlsx文件格式，赋值给C，追加两列数据B和C，并合并所有xlsx文件，
        import os
        import pandas as pd
        original_dict = self.sqldatabase._get_columns_comment_dict(table_name="sellers_competitor_url")
        swapped_dict = {v: k for k, v in original_dict.items()}
        # 指定文件夹A
        folder_A = r'C:\Users\Administrator\Desktop\市场数据-类目编号-20230911'
        # 遍历文件夹
        error_list = []
        for dir_path, dir_names, file_names in os.walk(folder_A):
            for cate_id in dir_names:
                print(cate_id)
                for dir_path_i , dir_names_i, file_names_i in os.walk(os.path.join(dir_path,cate_id)):
                    for file_name in file_names_i:
                        print(file_name)
                        # 判断是否为.xlsx文件
                        if file_name.endswith('.xlsx'):
                            station_name = "com"
                            # station_name = file_name.split("-")[1]
                            # station_name = "com" if station_name == "US" else station_name
                            month = file_name.split("-")[-2].replace(".","-")
                            file_path = os.path.join(dir_path_i, file_name)
                            df = pd.read_excel(file_path)   
                            # ### prime价格, 卖家首页, 品牌链接 ## 商品详情链接 # 近30天评论数
                            if "商品详情链接" in df.columns:
                                df.drop("商品详情链接", axis=1, inplace=True)
                            if "近30天新增评论数" in df.columns:
                                df.drop("近30天新增评论数", axis=1, inplace=True)
                            if "类目" in df.columns:
                                df.rename(columns={"类目":"类目路径"},inplace=True)
                                df.drop("BSR排名", axis=1, inplace=True)
                            if "BuyBox卖家国籍" in df.columns:
                                df.rename(columns={"BuyBox卖家国籍":"卖家所属地"},inplace=True)
                            if "prime价格($)" in df.columns:
                                df.rename(columns={"prime价格($)":"价格"},inplace=True)
                            if "卖家首页" in df.columns:
                                df.drop("卖家首页", axis=1, inplace=True)
                            if "品牌链接" in df.columns:
                                df.drop("品牌链接", axis=1, inplace=True)
                            df.fillna("None",inplace=True)
                            for col in df.columns:
                                if "$" in col:
                                    col_new = col.replace("($)","") 
                                    df.rename(columns={col:col_new},inplace=True)
                            df['序号'] = range(1, len(df) + 1)
                            df['station_name'] = station_name  # 追加文件夹名称列
                            df['cate_id'] = cate_id  # 追加文件名列
                            df["month"] = month
                            df.rename(columns=swapped_dict,inplace=True)
                            for item in df.to_dict("records"):
                                if not self.sqldatabase.insert_data(table_name="sellers_competitor_url",data_dict=item):
                                    # pass
                                    error_list.append(file_path)
                                # self.sqldatabase.insert_data(table_name="sellers_competitor_url",data_dict=item)
                            pass
        pd.DataFrame(error_list).to_excel("error_list.xlsx")

    @unittest.skip(reason="test_drop_duplicates pass") 
    def test_drop_duplicates(self):
        # 读取Excel文件，'file_name.xlsx'是你的源文件名，记得替换为实际的文件名
        df = pd.read_excel('error_list.xlsx')
        # 'column_name' 是你想要读取的列的名称，记得替换为实际的列名
        column_data = df['test']
        # 去除列中的重复值
        unique_data = column_data.drop_duplicates()
        # 将去重后的数据写入新的Excel文件，'new_file.xlsx'是新的文件名，你可以替换为你喜欢的文件名
        unique_data.to_excel('new_file.xlsx', index=False)



    @unittest.skip(reason="not in prod pass") 
    def test_update_input_resultcache_from_result(self):
        sql = text("SELECT cate_id, count( 1 ) AS result_num , month,station_name FROM `sellers_competitor_url` GROUP BY cate_id, month,station_name")
        results = pd.DataFrame(self.sqldatabase.session.execute(sql))
        results.rename(columns={"cate_id":"node_id"},inplace=True)
        results["status"] = "1"
        results["type"] = "1"
        for item in results.to_dict("records"):
            self.assertEqual(first=self.sqldatabase.update_or_insert_data(table_name="sellers_competitor_input",data_dict=item),second=True)
            pass

    @unittest.skip(reason="not in prod pass") 
    def test_chaneg_station_name_top(self):
        error_results = self.sqldatabase.fetch(table_name="sellers_competitor_url", filt_dict={
            "station_name":"Top3000"
        })
        error_results = pd.DataFrame(error_results)
        error_results["station_name"] = "com"
        for error_result in error_results.to_dict("records"):
            self.assertEqual(first=self.sqldatabase.update_or_insert_data(table_name="sellers_competitor_url",data_dict=error_result),second=True)
        pass
    @parameterized.expand([
        ("all_account", {"station_name":"test01","username":"test01"}, True),
        # ("all_account", {"station_name":"test99","username":"test01"}, False),
        ])
    def test_delete_data(self,table_name, condition_dict,result):
        self.assertEqual(first=self.sqldatabase.delete_data(table_name=table_name, condition_dict=condition_dict),second=result)

if __name__ == '__main__':
    unittest.main()

import unittest
import os
from st_common.commonbase import load_and_persist_env
from dotenv import load_dotenv




class TestYourModule(unittest.TestCase):

    def test_env(self):
        load_dotenv()
        db_username = os.getenv("DB_USERNAME")
        db_password = os.getenv("DB_PASSWORD")
        self.assertEqual(db_username, "your_username")  
        self.assertEqual(db_password, "your_password")

    @unittest.skip(reason="避免环境变量污染")
    def test_load_and_persist_env(self):
        # # 加载环境变量
        load_and_persist_env()
        db_username = os.getenv("DB_USERNAME")
        db_password = os.getenv("DB_PASSWORD")
        self.assertEqual(db_username, "your_username")  
        self.assertEqual(db_password, "your_password")

if __name__ == '__main__':
    unittest.main()
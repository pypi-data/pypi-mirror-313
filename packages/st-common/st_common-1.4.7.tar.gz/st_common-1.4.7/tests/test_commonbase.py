import unittest
import sys
from parameterized import parameterized

from st_common import CommonBase,fn_timer

class CommonBaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # print("在每个类之前执行，如创建一个类，创建数据库链接，初始化日志对象")
        cls.commonbase = CommonBase(log_file="test.log")
    @classmethod
    def tearDownClass(cls) -> None:
        # print("在每个类之后执行，如销毁一个类，销毁数据库链接，销毁日志对象")
        pass
    def setUp(self) -> None:
        return super().setUp()
    def tearDown(self) -> None:
        return super().tearDown()
    
    @parameterized.expand([
        ("hello world!")
        ])
    # @unittest.skip(reason="test_hello_world pass")
    def test_hello_world(self,msg):
        # print(msg)
        self.commonbase.logger.info(msg)
    
    def test_commonbase_init_log(self):
        self.commonbase.logger.info("hello st123")
        
    
    @parameterized.expand([
        (1123,False),("asdf",False),("123asdf",False),
        ("你好",True),("你好，world",True)
        ])
    
    def test_is_contains_chinese(self,strs, result):
        self.assertEqual(first=self.commonbase._is_contains_chinese(strs=strs),second=result)


    @parameterized.expand([
        ("--mode dev",{"mode":"dev"}),("--mode dev --search_mode url",{"mode":"dev", "search_mode":"url"}),
        ("-mode dev",None),("-mode dev --search_mode url",{"search_mode":"url"}),
        ("--MODE dev",{"MODE":"dev"}),
        ])
    def test_ddot2dict(self, ddot_str,dict_result):
        self.assertEqual(first=self.commonbase.ddot2dict(ddot_str=ddot_str),second=dict_result)
    

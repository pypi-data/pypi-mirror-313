import unittest
from st_common import ISZMsgReport
# from test import setting
import os
from dotenv import load_dotenv
load_dotenv()
import json
class MsgReportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # print("在每个类之前执行，如创建一个类，创建数据库链接，初始化日志对象")

        cls.msg_report = ISZMsgReport(webhook=os.getenv('ISZ_MSGRERPORT_WEBHOOK'))
    @classmethod
    def tearDownClass(cls) -> None:
        # print("在每个类之后执行，如销毁一个类，销毁数据库链接，销毁日志对象")
        pass

    # def test_helloworld(self):
    #     print("helle world: %s" % self.__class__.__name__)

    def test_isz(self):
        result = self.msg_report.chatbot_text(content="Hello world!",title="Test2",code=os.getenv('ISZ_MSGRERPORT_CODE'),touser=[os.getenv('ISZ_MSGRERPORT_USER_ID')])
        result_json = json.loads(result.text)
        self.assertTrue(result_json.get("success",False))
   
if __name__ == '__main__':
    unittest.main()
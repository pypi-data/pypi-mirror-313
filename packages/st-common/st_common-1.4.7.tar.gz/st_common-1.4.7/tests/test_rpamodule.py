import unittest
from parameterized import parameterized

# from st_common import CommonBase
from st_common.rpamodule import BaseBrowser
from st_common.rpamodule import BaseLogin
from st_common.rpamodule import TmpLoginCaptchaNumAlphaChinese
from st_common.rpamodule import TmpLoginSlideBlock
import os
from dotenv import load_dotenv
load_dotenv()


class debuggerAddressTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.basebrower = BaseBrowser(log_file="test_rpa.log",debuggerAddress='127.0.0.1:9222')

    @classmethod
    def tearDownClass(cls) -> None:
        cls.basebrower.close()
    def setUp(self) -> None:
        return super().setUp()
    def tearDown(self) -> None:
        return super().tearDown()
    def test_open_url(self):
        self.basebrower.logger.info("test_open_url")
        self.basebrower.browser.get("https://www.baidu.com/")
        self.assertEqual(self.basebrower.browser.title,"百度一下，你就知道")

    
class BaseBrowserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.basebrower = BaseBrowser(log_file="test.log")
    @classmethod
    def tearDownClass(cls) -> None:
        cls.basebrower.close()
    def setUp(self) -> None:
        return super().setUp()
    def tearDown(self) -> None:
        return super().tearDown()
    

    @parameterized.expand([
        ("http://192.168.6.247:8080/#/login",True),
        ("http://192.168.6.247:800/",False),
        ])
    @unittest.skip(reason="test_check_url pass")
    def test_check_url(self, url, state):
        tmp_url = "http://192.168.6.247:8080/#/login"
        self.basebrower.browser.get(url = tmp_url)
        self.assertEqual(first=self.basebrower.check_url(url=url),second=state)

    @parameterized.expand([
        ("penny","//input[contains(@placeholder, 'Username')]",True),
        ("pennysss","//input[contains(@*, '用户名')] ",False),
        ])
    @unittest.skip(reason="test_input_by_xpath pass")
    def test_input_by_xpath(self, keys, input_xpath, state):
        url = "http://192.168.6.247:8080/#/login"
        self.basebrower.browser.get(url = url)
        self.assertEqual(first = self.basebrower.input_by_xpath(keys=keys,input_xpath=input_xpath,delay=True),
                         second = state)
    
    @parameterized.expand([
        ('//*[@id="app"]//button/span',True),
        ('//*[@id="app"]//button/sp',False),
        ])
    @unittest.skip(reason="test_click_by_xpath pass")
    def test_click_by_xpath(self, input_xpath, state):
        url = "http://192.168.6.247:8080/#/login"
        self.basebrower.browser.get(url = url)
        self.assertEqual(first = self.basebrower.click_by_xpath(element_xpath=input_xpath,attempts=1),
                         second = state)
        
    @unittest.skip(reason="test_scroll_to_bottom pass")
    def test_scroll_to_bottom(self):
        url = "https://www.bing.com/search?q=%E6%96%B0%E9%97%BB&form=QBLH&sp=-1&ghc=1&lq=0&pq=%E6%96%B0%E9%97%BB&sc=10-2&qs=n&sk=&cvid=494ADD35800C4BC4856B16876746B6CF&ghsh=0&ghacc=0&ghpl="
        self.basebrower.browser.get(url=url)
        self.basebrower.scroll_to_bottom_step(step=5,delay=1)
        self.basebrower.scroll_to_top()

        element = self.basebrower.get_element_by_xpath_wait(xpath="//a[contains(text(),'半岛电视台今assssss日最新资讯')]",attempts=1)
        if element:
            self.basebrower.scroll_to_element(element=element)
        

import time

class BaseLoginTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        username = os.getenv('CRAWLAB_USERNAME')
        password = os.getenv('CRAWLAB_PASSWORD')
        login_url = os.getenv('CRAWLAB_LOGIN_URL')
        cls.loginbrower = BaseLogin(username=username, password=password, login_url=login_url,log_file="test.log")
    @classmethod
    def tearDownClass(cls) -> None:
        cls.loginbrower.close()
    def setUp(self) -> None:
        return super().setUp()
    def tearDown(self) -> None:
        return super().tearDown()
    
    @parameterized.expand([
        ("hello world!")
        ])
    # @unittest.skip(reason="test_hello_world pass")
    def test_hello_world(self,msg):
        print(msg)
        self.loginbrower.logger.info(msg=msg)

    @unittest.skip(reason="test_login pass")
    def test_login(self,):
        self.assertEqual(first=self.loginbrower.login(target_login_url="http://192.168.6.247:8080/#/home"),second=True)
    
    # @unittest.skip(reason="test_basic_browser pass")
    def test_basic_browser(self):
        self.assertEqual(first=self.loginbrower.login(target_login_url="http://192.168.6.247:8080/#/home"),second=True)
        self.assertEqual(first=
                         self.loginbrower.click_by_xpath(element_xpath='//*[@id="app"]/section/aside/div[2]/ul/li[4]/span',attempts=1),second=True)
        
        self.assertEqual(first=self.loginbrower.input_by_xpath(keys="penny",input_xpath="//input[contains(@placeholder, 'Search')]"),second=True)

        time.sleep(3)
        element = self.loginbrower.get_element_by_xpath_wait(xpath='//*[@id="app"]/section/section/div[3]/div/div[1]/div[2]/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div/div/div/span',
                                                             attempts=1)
        ## get text
        self.assertEqual(first=element.text,second="Penny_videoIc_Lastest")
        ## get attribute
        self.assertEqual(first=element.get_attribute("class"), second="title")
        
    @unittest.skip(reason="test_login_seller pass")
    def test_login_sellers(self):
        login_url = os.getenv('SELLER_LOGIN_URL')
        login_true_url = os.getenv('SELLER_LOGIN_TRUE_URL')
        username = os.getenv('SELLER_USERNAME')
        password = os.getenv('SELLER_PASSWORD')
        sellers_browser = TmpLoginCaptchaNumAlphaChinese(username=username, password=password, login_url=login_url,headless=False)
        sellers_browser.login(target_login_url=login_true_url)


    @unittest.skip(reason="test_login_oar pass")
    def test_login_oalu(self):
        login_url = 'None' 
        login_true_url = 'None'
        username = "None"
        password = "None"
        sellers_browser = TmpLoginSlideBlock(username=username, password=password, login_url=login_url,headless=False)
        sellers_browser.login(target_login_url=login_true_url)


from st_common.rpamodule import TmpOperationFlowLogin
from st_common.commonbase import CommonBase
class TmpOperationFlowLoginTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        commonbase = CommonBase()
        ddot_str = "--mode pro --username user --password pwd --login_url login_url --log_file test.log"
        ddot_dict = commonbase.ddot2dict(ddot_str=ddot_str)
        cls.operationflowlogin = TmpOperationFlowLogin(**ddot_dict)
    @classmethod
    def tearDownClass(cls) -> None:
        pass
    def setUp(self) -> None:
        return super().setUp()
    def tearDown(self) -> None:
        return super().tearDown()
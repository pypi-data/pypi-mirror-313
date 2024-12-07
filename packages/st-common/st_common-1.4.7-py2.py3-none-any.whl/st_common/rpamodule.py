# -*- coding: utf-8 -*-
try:
    from crawlab import save_item
    SAVE_ITEM_FLAG = True
except:
    SAVE_ITEM_FLAG = False

"""
Second choice rpa : tagui==1.50.0

project : https://github.com/sty001/TagUI-Python
cases   : https://github.com/sty001/TagUI-Python#use-cases
sample  : https://github.com/sty001/TagUI-Python/blob/master/sample.py
"""



### selenium==4.10.0

from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from typing import Union
import time
import random
import pandas as pd
import json
from PIL import Image

from st_common import CommonBase


import logging
# 获取名为当前模块名称的logger
logger = logging.getLogger('main')

def get_options_lab():
    """
    Description:
        set chrome options in lab
    Args:
    Returns: ChromeOptions
    Example:
    Raises:
        Exception: error
    """
    options = ChromeOptions()
    ### lab basic option
    options.add_argument('--headless')
    # options.add_argument("--disable-web-security")
    # options.add_argument(f'--proxy-server={PROXY}')
    # options.add_argument('--ignore-certificate-errors')  # To avoid possible SSL errors with the proxy
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    logger.info("add get_options_lab argument")
    return options

    return options

def get_options_normal_Chromium():
    options = ChromeOptions()
    logger.info("add get_options_normal_Chromium argument")
    return options

def get_options_normal(download_dir=None):
    """
    Description:
        set chrome options in normal
    Args:
        download_dir(str): download file dir
    Returns: ChromeOptions
    Example:
    Raises:
        Exception: error
    """
    options = ChromeOptions()
    prefs = {
        # 'profile.managed_default_content_settings.images': 2,  # not load picture
        'profile.default_content_settings.popups': 0,  # No Popups
        'download.default_directory': download_dir,  
    }
    options.add_experimental_option('prefs', prefs)
    logger.info("add get_options_normal argument")
    return options

def get_print_options_normal(download_dir=r'D:\issyzone\workspace\track'):
    """
    Description:
        set chrome options in normal
    Args:
        
    Returns: ChromeOptions
    Example:
    Raises:
        Exception: error
    """
    options = ChromeOptions()
    options.add_argument('--enable-print-browser')  # 启用PrintBrowser模式，其中所有内容都呈现为打印
    options.add_argument('--kiosk-printing')  # 在打印预览中自动按下打印按钮
    settings = {
        "recentDestinations": [
        {
            "id": "Save as PDF",
            "origin": "local"
        }
        ],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }
    prefs = {
        'printing.print_preview_sticky_settings.appState': json.dumps(settings),
        'savefile.default_directory': download_dir  # 下载文件保存的路径
    }
    options.add_experimental_option('prefs', prefs)
    logger.info("add get_print_options_normal argument")
    return options


class BaseBrowser(CommonBase):
    def __init__(self,headless=False,
                 impli_waitime=8,expli_waitime=24,
                 log_file=None,debuggerAddress=None,chrome_options=None,service=None,seleniumwire=False):
        """
        Description:
            base browser init
        Args:
            headless (bool): headless browser
            impli_waitime (int): implicitly wait time
            expli_waitime (int): explicitly wait time
                expli_waitime = impli_waitime * 3 (common)
            log_file (str): logger file
            debuggerAddress (str): '127.0.0.1:9992'
        Returns:
            int: The sum of a and b.
        Example:
            >>> add(1, 2)
            3
        Raises:
            Exception: error
        """
        super().__init__(log_file=log_file)
        if not chrome_options:
            chrome_options = get_options_lab() if headless else get_options_normal_Chromium()
        chrome_options.add_experimental_option("debuggerAddress", debuggerAddress) if debuggerAddress else None
        self.logger.info("webdriver chrome initing....")
        if not seleniumwire:
            from selenium import webdriver
        else:
            from seleniumwire import webdriver
        if service:
            self.browser = webdriver.Chrome(options=chrome_options,service=service)
        else:
            self.browser = webdriver.Chrome(options=chrome_options)
        self.logger.info("webdriver chrome init Over")
        self.browser.implicitly_wait(impli_waitime)
        self.__wait = WebDriverWait(self.browser, expli_waitime)
    def __del__(self):
        """
        Description:
            befor del 
        Args:
        Returns:
        Raises:
            Exception: error
        """
        self.logger.info("Browser close")
        self.close()

    def close(self):
        # self.browser.close()
        self.browser.quit()
    def check_url(self, url=None) -> bool:
        """
        Description:
            check current url
        Args:
            url (str): specify url
        Returns:
            bool: True / Flase
        Example:
        Raises:
            Exception: error
        """
        if url is None:
            url = self.target_url
        url_curr = self.browser.current_url
        # url_curr = self.browser.execute_script("return location.href")

        # if url_curr.startswith(url):
        if url_curr == url:
            self.logger.info('check_url success, current url: %s' % url_curr)
            return True
        else: 
            self.logger.warning('check_url fail, target url: %s current url is %s' % (url, url_curr))
            return False
    
    def maximize_window(self):
        self.browser.maximize_window()
    
    def refresh(self):
        self.browser.refresh()
    
    def back(self):
        self.browser.back()
    
    def forward(self):
        self.browser.forward()
    
    def get_element_by_xpath_wait(self, xpath,attempts=3,refresh=True) :
        """
        Description:
            get element by xpath wait
        Args:
            xpath(str): xpath
        Returns:
            WebElement: selenium.webdriver.remote.webelement.WebElement / None
        Example:
            >>> add(1, 2)
            3
        Raises:
            Exception: error
        """
        while attempts > 0:
            try:
                return self.__wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            except TimeoutException:
                self.logger.warning(f"xpath:{xpath} Element not found within timeout period, retrying Countdown times :{attempts}...")
                # driver.refresh()
                self.browser.refresh() if refresh else None
                time.sleep(1)
                attempts -= 1
        return False
            

    def get_element_by_link_text(self, link_text):
        """
        Description:
            get element by link text
        Args:
            link_text (str): all link_text
        Returns:
            WebElement: selenium.webdriver.remote.webelement.WebElement
        Example:
        Raises:
            Exception: error
        """
        return self.browser.find_element_by_link_text(link_text)
    
    def get_element_by_partial_link_text(self, partial_link_text):
        """
        Description:
            get element by partial link text
        Args:
            partial_link_text (str): partial link_text
        Returns:
            WebElement: selenium.webdriver.remote.webelement.WebElement
        Example:
        Raises:
            Exception: error
        """
        return self.browser.find_element_by_partial_link_text(partial_link_text)
    
    def click_by_xpath(self, element_xpath,attempts=3,refresh=True) -> bool:
        """
        Description:
            according to xpath, click
        Args:
            element_xpath (str): input box with xpath
        Returns:
            bool: True / Flase
        Example:
        Raises:
            Exception: error
        """
        try:
            element_click = self.get_element_by_xpath_wait(xpath=element_xpath,attempts=attempts,refresh=refresh)
            element_click.click()
        except AttributeError as err:
            self.logger.error(err,exc_info=True,stack_info=False)
            self.logger.error('click_by_xpath: %s , click NoneType object' % element_xpath)
            return False
        except Exception as err:
            self.logger.error(err,exc_info=True,stack_info=False)
            self.logger.error('click_by_xpath: %s , Unknown error occurred' % element_xpath)
            return False
        return True
    
    def input_by_xpath(self, keys, input_xpath, delay=True,enter=False) -> bool:
        """
        Description:
            according to xpath, input keys in input box
        Args:
            keys (str): keys
            input_xpath (str): input box with xpath
            delay (bool): delay 
        Returns:
            bool: True / Flase
        Example:
        Raises:
            Exception: error
        """
        try:
            element_input = self.get_element_by_xpath_wait(xpath=input_xpath)
            element_input.clear()
            if delay is True:
                for ehchar in keys:
                    time.sleep(random.choice([0.2, 0.3, 0.4]))
                    element_input.send_keys(ehchar)
            else:
                element_input.send_keys(keys)
            if enter:
                
                element_input.send_keys(Keys.ENTER)
        except Exception as err:
            self.logger.error(err,exc_info=True,stack_info=False)
            self.logger.error('input_by_xpath fail, xpath: %s' % input_xpath)
            return False
        return True

    
    def scroll_to_top(self) -> bool:
        """
        Description:
            scroll to top
        Args:
        Returns:
            bool: True
        Example:
        Raises:
            Exception: error
        """
        self.browser.execute_script("window.scrollTo(0, 0);")
        return True
    def scroll_to_bottom_while(self) -> bool:
        """
        Description:
            scroll to botton while
        Args:
        Returns:
            bool: True
        Example:
        Raises:
            Exception: error
        """
        SCROLL_PAUSE_TIME = 0.5
        # Get scroll height
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        return True
    def scroll_to_bottom_step(self, step=10, delay=0.25) -> bool:
        """
        Move num step  to the bottom of the page
        Args:
            step(int): step
            delay(int): delay
        Returns:
            bool: True
        Example:
        Raises:
            Exception: error
        """
        for eh in range(step):
            self.browser.execute_script('window.scrollTo(0, parseInt(document.body.scrollHeight / %d * %d))' % (step, eh+1))
            time.sleep(delay)
        return True
    
    def scroll_to_element(self, element):
        """
        Description:
            scroll to specify element 
            work but Not precise scroll
        Args:
            element (selenium.webdriver.remote.webelement.WebElement): specify element by xpath
        Returns:
        Example:
        Raises:
            Exception: error
        """
        self.browser.execute_script("arguments[0].scrollIntoView();", element)
    def is_element_in_viewport(self, element):
        """
        Description:
            Check if the given element is in the viewport
        Args:
            element (selenium.webdriver.remote.webelement.WebElement): The element to check
        Returns:
            bool: True if the element is in the viewport, False otherwise
        Example:
            scroll_to_element(self, element)
            if not is_element_in_viewport(self, element):
                raise Exception("Scrolling to element did not work.")  
        """
        element_top = element.location['y']
        element_bottom = element_top + element.size['height']
        viewport_top = self.browser.execute_script("return window.pageYOffset;")
        viewport_bottom = viewport_top + self.browser.execute_script("return window.innerHeight;")
        return element_top >= viewport_top and element_bottom <= viewport_bottom
    
    def move_to_element(self,element_xpath):
        """move_to_element _summary_

        _extended_summary_

        Args:
            element (selenium.webdriver.remote.webelement.WebElement): specify element by xpath
        Returns:
        Example:
        Raises:
            Exception: error
        """
        # 找到要移动鼠标的元素
        element = self.get_element_by_xpath_wait(element_xpath)
        # 创建一个ActionChains对象
        actions = ActionChains(self.browser)
        # 移动鼠标到指定元素
        return actions.move_to_element(element).perform()

    def get_table_data_as_dataframe(self, table_xpath):
        """
        使用selenium获取指定XPath表格的数据，并将其转换成pandas DataFrame。
        
        :param driver: 已实例化的Selenium WebDriver对象。
        :param table_xpath: 目标表格的XPath字符串。
        :return: 包含表格数据的pandas DataFrame对象。
        """
        # 定位到表格
        table = self.browser.find_element(By.XPATH, table_xpath)
        
        # 获取所有行
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        # 获取表头信息
        headers = [header.text for header in rows[0].find_elements(By.TAG_NAME, "th")]
        
        # 遍历表格中的每一行并获取数据
        table_data = []
        for row in rows[1:]:  # 跳过首行的表头
            # 获取当前行的所有单元格数据
            cells = row.find_elements(By.TAG_NAME, "td")
            cell_data = [cell.text for cell in cells]
            table_data.append(cell_data)
        
        # 将数据转换成pandas DataFrame
        df = pd.DataFrame(table_data, columns=headers)
        
        return df
    
    #### snapshot
    def capture_from_element_xpath(self,xpath='//*[@id="forecast-map-wrap"]',
                                        picture_name="tmp.png",
                                        picture_dir=None,
                                        direct=None
                                        ,direct_num=2,
                                        width=0,height=0):


        ### 滚动到指定位置
        map = self.get_element_by_xpath_wait(xpath=xpath)
        
        self.scroll_to_element(element=map)
        if direct:
            actions = ActionChains(self.browser)
            ## 按键 次
            for i in range(0,direct_num):
                actions.send_keys(direct).perform()
                time.sleep(1)
        
        ### 保存到缓存本地，一定要保存到本地，不然页面会重新刷新，有广告页出现会导致像素定位错误
        map.screenshot(picture_name)

        ### 保存到本地
        # im = Image.open(picture_name)

        # if width != 0 and height != 0:
        #     im = im.crop((0,0,width,height))
        # im.save(os.path.join(picture_dir,picture_name)) if picture_dir else im.save(picture_name)
        return True


    def capture_from_points(self,result_picture_path,start_element_xpath=None,left_top_point=None, right_bottom_point=None,tmp_png = '_full_screenshot.png'):

        ### 可视化
        
        start_element = self.get_element_by_xpath_wait(xpath=start_element_xpath)
        self.scroll_to_element(element=start_element)
        ####
        """
        p1 = (425: start., 130)
        p2 = (1125, 824)
        tmp_element_xpath = '//*[@id="main-column"]/section/ul'
        tmp_element = self.get_element_by_xpath_wait(xpath=tmp_element_xpath)
        """
        time.sleep(2)
        if left_top_point and right_bottom_point:
            self.browser.save_screenshot(filename=tmp_png)
            im = Image.open(tmp_png)
            im = im.crop((left_top_point[0],left_top_point[1], right_bottom_point[0],right_bottom_point[1]))
            im.save(result_picture_path)
        else:
            start_element.screenshot(result_picture_path)
        self.logger.info(f"saving result_picture_path:{result_picture_path}")

    
    def select_from_name(self,select_name_value:str="pjname",visible_text:str=None)-> bool:
        """select_from_name _summary_

        _extended_summary_

        Args:
            select_name_value (str, optional): _description_. Defaults to "pjname".
            visible_text (str, optional): _description_. Defaults to None.

        Returns:
            bool: _description_
        """
        ### 正常情况下下是，直接选择，如果加上其他判断，需要重新该函数
        month_select_element = Select(self.browser.find_element(By.NAME, select_name_value))
        return month_select_element.select_by_visible_text(visible_text)
    def add_handle(self, url):
        """
            add handle tab page
        :param url:
        :return:
        """
        js = 'window.open("%s")' % url
        self.browser.execute_script(js)
        handles_all = self.browser.window_handles
        self.browser.switch_to.window(handles_all[-1])
        handle_now = self.browser.current_window_handle
        self.handles_list.append(handle_now)
    def remove_handle(self, handle):
        """
            remove handle tab page
        :param handle: str,
        """
        # 切换到指定句柄
        self.browser.switch_to.window(handle)
        time.sleep(1)
        self.browser.close()
        self.handles_list.remove(handle)
        handle_all = self.browser.window_handles
        self.browser.switch_to.window(handle_all[-1])

class BaseLogin(BaseBrowser):
    def __init__(self, username, password, login_url, headless=False, impli_waitime=8, expli_waitime=24,log_file=None):
        super().__init__(headless, impli_waitime, expli_waitime,log_file=log_file)
        self.username = username
        self.password = password
        self.login_url = login_url

    def click_account(self,username_xpath, password_xpath,button_xpath,delay=True) ->bool:
        """
        input username password and click button
        """
        res_username = self.input_by_xpath(keys= self.username, input_xpath=username_xpath,delay=delay)
        time.sleep(1)
        res_password = self.input_by_xpath(keys=self.password, input_xpath=password_xpath,delay=delay)
        res_login_button = self.click_by_xpath(element_xpath=button_xpath)
        return True if res_username and res_password and res_login_button else False

    def pass_captcha(self) -> bool:
        """
        captcha: including slider verification codes, image verification codes, etc
        """
        pass

    def login(self,target_login_url=None,
              retry=3,
              username_xpath="//input[contains(@placeholder, 'Username')]", 
              password_xpath="//input[contains(@placeholder, 'Password')]",
              button_xpath='//*[@id="app"]//button/span') -> bool:
        """
        Login process, *_xpath:dome
        """
        pass
        self.browser.get(self.login_url)
        time.sleep(1)
        res = self.click_account(username_xpath=username_xpath,
                           password_xpath=password_xpath,
                           button_xpath=button_xpath)
        if not res:
            self.logger.error("click account username/password/button is False")
            return False
        time.sleep(3)

        login_res = self.check_url(url=target_login_url)
        if login_res:
            return True
        for i in range(retry):
            self.logger.info('login, try pass count log() %d times' % (i+1))
            time.sleep(3)
            login_res = self.check_url(url=target_login_url)
            if login_res is True:
                self.logger.info('login success')
                return True
        self.logger.warning('login fail')
        return False
    

    def slide_by_xpath(self, element_xpath, x, y) -> bool:
        """
        Drag the element to the specified position based on xpath
        : param element_ Xpath: str, element to be dragged
        : param x: str, specify position x
        : param y: str, specify position y
        : return:
            True - Element exists, operation completed
            False - Element does not exist, operation failed
        """
        try:
            slice_btn = self.get_element_by_xpath_wait(xpath = element_xpath)
        except Exception as err:
            self.logger.warning('slide_by_xpath fail, xpath: %s' % element_xpath)
            return False
        else:
            ActionChains(self.browser).click_and_hold(slice_btn).perform()
            time.sleep(0.5)
            tmp = int(x / 2)
            ActionChains(self.browser).move_by_offset(xoffset=tmp, yoffset=y).perform()
            time.sleep(0.5)
            ActionChains(self.browser).move_by_offset(xoffset=int(x - tmp), yoffset=y).perform()
            time.sleep(0.5)
            ActionChains(self.browser).move_by_offset(xoffset=5, yoffset=0).perform()
            time.sleep(0.5)
            ActionChains(self.browser).move_by_offset(xoffset=-5, yoffset=0).perform()
            time.sleep(0.5)
            ActionChains(self.browser).release().perform()
        return True

    def slide_block_by_xpath(self, slider_xpath, slider_bg_xpath, release=True) -> bool:
        """
        Slider verification, provided that you switch to the corresponding page/iframe, which will be used in other places besides login
        : param slider_ Xpath: str, slider xpath
        : param slider_ Bg_ Xpath: str, slider background xpath
        : param release: bool, whether to release after dragging the slider, True - release, False - do not release
        : return:
            True - Successful sliding
            False - sliding failed
        """

        try:
            slider = self.get_element_by_xpath_wait(xpath=slider_xpath)
            slider_bg = self.get_element_by_xpath_wait(xpath=slider_bg_xpath)
        except Exception as err:
            self.logger.error(msg=err,exc_info=True, stack_info=False,)
            self.logger.info('slide_block_by_xpath fail, xpath1: %s, xpath2: %s' % (slider_xpath, slider_bg_xpath))
            return False
        else:
            slider_bg_width = int(slider_bg.size['width'])
            ActionChains(self.browser).click_and_hold(slider).perform()
            time.sleep(0.5)
            ActionChains(self.browser).move_by_offset(xoffset=100, yoffset=0).perform()
            time.sleep(0.5)
            ActionChains(self.browser).move_by_offset(xoffset=50, yoffset=0).perform()
            time.sleep(0.5)
            ActionChains(self.browser).move_by_offset(xoffset=slider_bg_width - 150, yoffset=0).perform()
            time.sleep(0.5)
            if release is True:
                ActionChains(self.browser).release().perform()
        return True



from st_common.famodule import kaptcha_text

class TmpLoginCaptchaNumAlphaChinese(BaseLogin):
    def __init__(self, username, password, login_url, headless=False, impli_waitime=8, expli_waitime=24,log_file=None) -> None:
        super().__init__(username, password, login_url, headless, impli_waitime, expli_waitime,log_file=log_file)


    def pass_captcha(self)->str:
        """
        captcha : number alpha chinese
        """
        pic_element = self.get_element_by_xpath_wait(element_xpath='//div[@class="input-group-append mb-6"]//img')
        if pic_element is False:
            return False

        img_path = "tmp_sellers_kaptcha_text.png"
        pic_element.screenshot(img_path)
        
        # ocr 
        tmp_ocr_result = kaptcha_text(ocr_yaml="config_paddleorc_sellersprite.yaml",img_path=img_path)
        self.logger.info(tmp_ocr_result)
        if tmp_ocr_result is None :
            return False
        
        # Delete non numbers or letters
        ocr_result = [string for string in tmp_ocr_result if string.isalnum() and string != ""]
        self.logger.info(ocr_result)

        self.input_by_xpath(keys=ocr_result, input_xpath='//input[contains(@placeholder, "验证码")]')
        # click login
        self.click_by_xpath("//button[contains(text(), '我不是机器人') or contains(text(), '确定')]")
        return True

    def login(self,target_login_url,retry=3) -> bool:
        """
        Login process template, it is recommended to rewrite the specific login process, simple, and input account and password
        
        """
        self.browser.get(self.login_url)
        time.sleep(1)

        ## click account login 
        if not self.click_by_xpath('//*[@id="pills-login"]/li[2]/a'):
            self.logger.error("choice username/password fail")
            return False
        time.sleep(1)
        ## input username password
        username_xpath = '//*[@id="form_signin_password"]//input[@placeholder="手机号/邮箱/子账号"]'
        password_xpath = '//*[@id="form_signin_password"]//input[@placeholder="密 码"]'
        button_xpath = '//*[@id="form_signin_passW"]//button'
        res = self.click_account(username_xpath=username_xpath,
                           password_xpath=password_xpath,
                           button_xpath=button_xpath)
        
        if not res:
            self.logger.error("click account username/password/button is False")
            return False
        time.sleep(3)

        login_res = self.check_url(url=target_login_url)
        if login_res:
            return True
        for i in range(retry):
            self.logger.info('login, try pass count log() %d times' % (i+1))
            capt_res = self.pass_captcha()
            time.sleep(3)
            login_res = self.check_url(url=target_login_url)
            if login_res is True:
                self.logger.info('login success')
                return True
        self.logger.warning('login fail')
        return False
    
from st_common.famodule import block_bg_distance,format_style
import re
from st_common.famodule import url2img
class TmpLoginSlideBlock(BaseLogin):
    def __init__(self, username, password, login_url, headless=False, impli_waitime=8, expli_waitime=24,log_file=None):
        super().__init__(username, password, login_url, headless, impli_waitime, expli_waitime,log_file=log_file)

    def extract_url_bg(self, input_string) -> Union[str, None]:
        """
        Description:
            extract url with background
        Args:
            input_string (str): input string
        Returns:
            String / None
        Example:
        Raises:
            Exception: error
        """
        url_pattern = re.compile(r'background-image: url\(\"(.*?)\"\);')
        match = url_pattern.search(input_string)
        if match:
            return match.group(1)
        else:
            return None
    def pass_captcha(self) -> bool:
        """
        captcha : slide block
        """
        # Three Elements: 
        ## Background image, small slider image, small slider style
        element_bg = self.get_element_by_xpath_wait(xpath="//div[contains(@class, 'geetest_bg')]")
        bg_url_style_str = element_bg.get_attribute("style")
        bg_url = self.extract_url_bg(input_string=bg_url_style_str)

        element_slice_bg = self.get_element_by_xpath_wait(xpath="//div[contains(@class, 'geetest_slice_bg')]")
        slice_bg_url_style_str = element_slice_bg.get_attribute("style")
        slice_bg_url = self.extract_url_bg(input_string=slice_bg_url_style_str)

        element_slice_bg_block = self.get_element_by_xpath_wait(xpath="//div[contains(@class, 'geetest_slice')]") 
        style_block = element_slice_bg_block.get_attribute("style")

        (height_bg, width_bg, channels_bg) = url2img(bg_url).shape
        style_bg = f"width: {width_bg*0.888}px; height: {height_bg*0.888}px;"

        if (len(style_bg) > 0) and (len(style_block) > 0) and (len(bg_url) > 0) and (len(slice_bg_url) > 0):
            style_block = format_style(style_block[0])
            style_block["left"] = 12
            style_bg = format_style(style_bg)

            img_block = url2img(slice_bg_url)
            img_bg = url2img(bg_url)


            dist = block_bg_distance(img_bg=img_bg, img_block=img_block)
            dist = int((dist*0.88)-12)
            self.logger.info('pass_captcha: slider need to move %s px' % str(dist))
            return self.slide_by_xpath(element_xpath="//div[contains(@class, 'geetest_btn')]", x=dist, y=0)# geetest_btn
        pass

    def login(self,target_login_url,retry=3) -> bool:
        """
        login process
        """
        self.browser.get(self.login_url)
        time.sleep(1)

        ## 选择账号登陆
        if not self.click_by_xpath('//*[@id="user"]/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div'):
            self.logger.error("choice username/password fail")
            exit(0)
        time.sleep(1)

        username_xpath = '//input[@placeholder="输入手机号"]'
        password_xpath = '//input[@placeholder="输入密码"]'
        button_xpath = '//*[@id="user"]/div/div/div[2]/div/div[2]/div/div[2]/button'
        res = self.click_account(username_xpath=username_xpath,
                           password_xpath=password_xpath,
                           button_xpath=button_xpath)
        
        if not res:
            self.logger.error("click account username/password/button is False")
            exit(0)
        time.sleep(3)

        login_res = self.check_url(url=target_login_url)
        if login_res:
            return True

        for i in range(retry):
            self.logger.info('login, try pass count log() %d times' % (i+1))
            capt_res = self.pass_captcha()
            time.sleep(3)
            login_res = self.check_url(url=target_login_url)
            if login_res is True:
                self.logger.info('login success')
                return True
        self.logger.warning('login fail')
        return False
    
from typing import Callable
from functools import wraps
from urllib.parse import urlparse,parse_qs
import os 
from st_common import Secure
from st_common import SQLDatabase
def _requires_login(func: Callable) -> Callable:
    """Decorator to raise an exception if herewith-decorated function is called without being logged in"""
    @wraps(func)
    def call(tmpoperationflowlogin, *args, **kwargs):
        special_str = "login"
        url = tmpoperationflowlogin.browser.current_url
        parsed_url = urlparse(url)
        if special_str in parsed_url.path:
            params = parse_qs(parsed_url.query)
            login_true_url = "login_true_url"
            tmpoperationflowlogin.login(login_url=url,login_ttype_intrue_url=login_true_url)
        return func(tmpoperationflowlogin, *args, **kwargs)
    return call
class TmpOperationFlowLogin(TmpLoginCaptchaNumAlphaChinese,TmpLoginSlideBlock):
    def __init__(self, username, password, login_url, headless=False, impli_waitime=8, expli_waitime=24, mode="dev",log_file=None) -> None:
        """
        Description:
            operation flow init
        Args:
            Any
        Returns:
            None
        Example:
        Raises:
            Exception: error
        """
        ### super init either-or
        # TmpLoginSlideBlock.__init__(self,username, password, login_url, headless)
        # TmpLoginCaptchaNumAlphaChinese.__init__(self,username, password, login_url, headless)
        super().__init__(username, password, login_url, headless, impli_waitime, expli_waitime,log_file=log_file)


        self.mode = mode
        # init self.sqldatabase
        secure = Secure(key_string = os.getenv("DEBIAN_FRONTEND"))
        en_config_database = self.read_file(file_path="test/setting.json")
        self.config_database = secure.decrypt_dict_variable(cipher_dict=en_config_database)
        if self.mode == "pro":
            db_string=self.config_database["PRO_MYSQL_DB_STRING"]
        else:
            db_string=self.config_database["DEV_MYSQL_DB_STRING"]

        self.sqldatabase = SQLDatabase(db_string=db_string)

        ## Initialize notification mechanism and logger
        webhook = "None"
        self.logger.info(f"self.msg_report = ISZMsgReport(webhook={webhook})")

        ## Initialize Operation parameter
        pass
    def __del__(self):
        self.sqldatabase.close()
        return super().__del__()
    def run(self,args_dict):
        ### 初始化 init TmpOperationFlow， pass argument -> None
        ### 输入数据 input data: from local or database -> bool
        ### account管理
        ### 缓存数据 read cache_result as input_items -> list
        ### 请求 request(dict) -> bool
        ### 解析 extract(dict) -> list
        ### 合并结果，按照最小计量维度 all_list += tmp_list
        ### 校正 compare(int,list) cache_result and real_result & Judge whether it is empty -> bool
        ### 入库 entry_dicts -> bool
        pass
    def extract_tmp(self, item:dict) -> dict:
        pass

    


#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   base.py
@Time    :   2023/08/09 12:43:25
@Python Version:  3.10.0
@Version :   1.0
@Desc    :   作为开发方便工具箱
'''
from typing import Any
import os
import re
import time
import yaml
import json
from dotenv import load_dotenv, find_dotenv
import platform

import logging

### time costs
from functools import wraps
def fn_timer(function):
  @wraps(function)
  def function_timer(*args, **kwargs):
    t0 = time.time()
    result = function(*args, **kwargs)
    t1 = time.time()
    print(f"Total time running: {str(t1-t0)} seconds" )
    return result
  return function_timer


# 定义装饰器
def check_runtime(limit_in_seconds):
    def decorator(func):
        start_time = time.time()
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 调用被装饰的函数
            result = func(*args, **kwargs)
            # 计算运行时间
            elapsed_time = time.time() - start_time
            # elapsed_time = time.time() - func.start_time
            
            # 判断是否超过限定的时间
            if elapsed_time > limit_in_seconds:
                raise Exception(f"Function '{func.__name__}' exceeded the time limit of {limit_in_seconds} seconds.")
            else:
                print(f"Function '{func.__name__}' completed within the time limit.")
            
            return result
        return wrapper
    return decorator


### 持久化环境变量
def load_and_persist_env():
    # 尝试找到并加载 .env 文件
    dotenv_path = find_dotenv()

    if not dotenv_path:
        print(".env 文件不存在")
        return
    
    load_dotenv(dotenv_path)
    print(".env 文件已加载")

    # 获取所有环境变量
    env_vars = {
        key: os.getenv(key) for key in os.environ.keys()
        if key not in os.environ._mutable_keys
    }

    # 检测当前操作系统类型
    os_type = platform.system()

    if os_type == "Windows":
        persist_env_windows(env_vars)
    elif os_type in ["Linux", "Darwin"]:  # Darwin 是 MacOS 的标识符
        persist_env_unix(env_vars)
    else:
        print("未支持的操作系统")

def persist_env_windows(env_vars):
    for key, value in env_vars.items():
        # 使用 setx 命令设置环境变量
        os.system(f'setx {key} "{value}"')

    print("Windows 环境变量已经设置，请重新启动命令提示符以使更改生效")

def persist_env_unix(env_vars):
    # 写入到 .bashrc 或 .zshrc 文件
    shell_config_file = os.path.expanduser("~/.bashrc")  # 或使用 ~/.zshrc，根据你的实际情况选择

    with open(shell_config_file, "a") as file:
        file.write("\n# 从 .env 文件加载的环境变量\n")
        for key, value in env_vars.items():
            file.write(f'export {key}="{value}"\n')

    print(f"Unix 环境变量已写入 {shell_config_file}，请重新启动终端或执行 'source {shell_config_file}' 来应用更改")



class tmpClass:
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        return instance
    def __reduce__(self) -> str:
        """
        `__reduce__` 方法用于定义对象的序列化方法，通常与 `pickle` 模块一起使用。
        当我们需要将一个对象保存到磁盘或通过网络传输时，就需要对其进行序列化。
        `__reduce__` 方法应返回一个包含构造新实例所需信息的元组。
        """
        pass
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        """
        callable_obj(2)  # 调用对象，相当于执行 callable_obj.__call__(2)
        """
        self.logger.debug("Call %s instance" % self.__name__)
        pass

    def __del__(self):
        """
        在Python中,可以使用`__del__`魔法方法作为类的“析构函数”。
        当一个对象不再被使用或者程序结束时,Python解释器会自动调用`__del__`方法来清理资源。
        需要注意的是，`__del__`方法不是显式地销毁对象，而是在对象被垃圾回收时执行。
        所以，在大多数情况下，我们不需要重写`__del__`方法,因为Python解释器会自动管理内存。
        但如果你需要在删除对象时做一些额外操作（例如关闭文件，断开网络连接等）,可以考虑实现`__del__`方法。
        """
        # self.logger.debug("Destroying %s instance" % self.__name__)
        pass

class CountingHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        super(CountingHandler, self).__init__(*args, **kwargs)
        self.error_count = 0
        self.error_messages = []
        self.warning_count = 0
        self.warning_messages = []
    def emit(self, record):
        if record.levelno == logging.ERROR:
            self.error_count += 1
            self.error_messages.append(record.getMessage())
        elif record.levelno == logging.WARNING:
            self.warning_count += 1
            self.warning_messages.append(record.getMessage())
class BaseLogger:
    def __init__(self, level=logging.DEBUG, log_file=None):
        # self.logger = logging.getLogger(self.__class__.__name__)
        self.logger = logging.getLogger('main')
        self.logger.setLevel(level)
        # # 检查是否已经存在相应的Handler，防止重复添加
        # if not self.logger.hasHandlers():
        if log_file is not None:
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        else:
            handler = logging.StreamHandler()  # 输出到终端
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        ### 用于日志信息统计
        self.counting_handler = CountingHandler()
        self.counting_handler.set_name('counting_handler')
        self.logger.addHandler(self.counting_handler)
    
    def get_logger(self):
        return self.logger
class CommonBase(BaseLogger):
    def __init__(self, level=logging.DEBUG, log_file=None):
        super().__init__(level, log_file)
    def _is_contains_chinese(self, strs):
        """
        检验是否含有中文
        :param strs:
        :return:
        """
        if isinstance(strs, str):
            for _char in strs:
                if '\u4e00' <= _char <= '\u9fa5':
                    return True
        return False

    def extract_email(self, text:str):
        """
        Description:
            extract_email
        Args:
            text (str): The first integer to add.
        Returns:
            list: 
        Example:
            >>> # 使用示例
            text = '这是一个示例文本，包含两个邮箱地址：example@example.com 和 another@example.org'
            emails = extract_email(text)
            print(emails)  # 输出：['example@example.com', 'another@example.org']
        Raises:
            Exception: error
        """
        # 定义一个正则表达式，匹配邮箱地址
        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        # 在文本中查找匹配的邮箱地址
        emails = re.findall(email_regex, text)
        return emails
 
    def is_valid_filename(self, filename, platform="linux"):
        """
        Description:
            检查字符串是否符合win系统或者linux系统的文件命名
        Args:
            filename (str): filename 
            platform (str): linux / windows
        Returns:
            bool : True 符合 / Flase 不符合
        Example:
            >>> add(1, 2)
            3
        Raises:
            Exception: error
        """
        pass
        if platform.lower() == "windows":
            return not bool(re.search(r'[<>:"\\/|?*]', filename))
        elif platform.lower() == "linux":
            return "/" not in filename
        else:
            raise ValueError("Unsupported platform")
    
    def clean_filename(self, filename):
        """
        Description:
            Liunx and window clean filename 
        Args:
            a (str): filename
        Returns:
            str: clean filename 
        Example:

        Raises:
            Exception: error
        """
        pass
        # 不允许的字符
        invalid_chars = '<>:\"/\\|?*'
        
        # 删除不允许的字符
        cleaned_filename = re.sub('[' + re.escape(invalid_chars) + ']', '', filename)
        
        # 移除开始和结尾处的空格和点
        cleaned_filename = cleaned_filename.strip(' .')
        return cleaned_filename
    def search_file(self, directory, target_string, is_sort=True, sort_num=None):
        """
        Description:
            search file
        Args:
            directory (str): directory 
            target_string (str): target_string
        Returns:
            list: abs file path
        Example:
        Raises:
            Exception: error
        """
        filename_list = os.listdir(directory)
        result_list = []
        for filename in filename_list:
            if target_string in filename:
                file_path = os.path.join(directory, filename)
                absolute_path = os.path.abspath(file_path)
                result_list.append(absolute_path)

        # 按创建时间降序排列，最新的在前
        result_list.sort(key=lambda x: os.path.getctime(x), reverse=is_sort)
        
        # 如果 sort_num 为 None，则设置为 result_list 的长度
        num = sort_num if sort_num is not None else len(result_list)

        return result_list[:num]  # 返回文件的路径
    def get_filename_dict_in_filepath(self, dirpath:str, file_ext: str) -> dict :
        """
        Description:
            get filename with dict in filepath 
        Args:
            dirpath (str): dir path
            file_ext (str): file extender
        Returns:
            dict:  filename: filename dirpath
        Example:
            >>> get_filename_dict_in_filepath("/root", "py")

        Raises:
            Exception: error
        """
        pass
        valid_checkpoints_dict = {
            f.split('/')[-1].split('.')[0]: os.path.join(dirpath, f)
            for f in os.listdir(dirpath)
            if (f.endswith(file_ext) and os.path.exists(os.path.join(dirpath, f)))
        }
        return valid_checkpoints_dict
        
    def get_file(self,root_path,all_files=[]):
        """
        Description:
            get all files in root_path
        Args:
            root_path (str): root path
            all_files (list): all files
        Returns:
            list: all files
        Example:
            >>> get_file("/root")

        Raises:
            Exception: error
        """
        files = os.listdir(root_path)
        for file in files:
            file_path = os.path.join(root_path , file)
            if not os.path.isdir(file_path):   # not a dir
                all_files.append(file_path)
            else:  # is a dir
                self.get_file(file_path,all_files)
        return all_files

    def signal_wait(self):
        signal_file = "signal_file"
        while not os.path.exists(signal_file):
            self.logger.info("Bad Request,look before , Waiting for signal...")
            time.sleep(3)
        self.logger.info("Signal received, continue processing...")
        os.remove(path=signal_file)
        self.logger.info("del Signal file")
    def find_path(self, nested_dict: dict , target_key: str) -> list:
        """
        Description:
            使用递归函数遍历, 在嵌套字典中查找键名的访问路径
        Args:
            nested_dict (dict): 嵌套的字典或者嵌套的数组字典
            target_key (str): 查找的目标键
        Returns:
            list: 路径数组
        Example:
            >>> # 找到 commentCount , likeCount videoDescriptionHeaderRenderer
            >>> self.find_path(nested_dict=json_data,target_key="videoDescriptionHeaderRenderer")
        Raises:
            Exception: error
        """
        def _find_path(current_structure, target_key, path_so_far):
            if isinstance(current_structure, dict):
                for key, value in current_structure.items():
                    new_path = path_so_far + [key]
                    if key == target_key:
                        return new_path
                    result = _find_path(value, target_key, new_path)
                    if result is not None:
                        return result
            elif isinstance(current_structure, list):
                for idx, item in enumerate(current_structure):
                    result = _find_path(item, target_key, path_so_far + [idx])
                    if result is not None:
                        return result
            return None
        return _find_path(nested_dict, target_key, [])

    def get_value_by_path(self, nested_structure: dict, path_array:list = []) -> dict:
        """
        Description:
            从嵌套结构中获取与路径对应的值。(与find_path配合使用)
        Args:
            nested_structure (dict): 嵌套结构字典
            path_array (array): 数组路径
        Returns:
            Any: 路径对应的值
        Example:
            >>> self.get_value_by_path(nested_structure=json_data,path_array=self.find_path
                    (nested_dict=json_data,target_key="videoDescriptionHeaderRenderer"))
            3
        Raises:
            Exception: error
        """
        for step in path_array:
            nested_structure = nested_structure[step]
        return nested_structure
    
    def is_comma_separated_number(self, str_num: str = "123,456.789") -> int:
        """
        Description:
            确定一个含有分号的字符串是否是由数字构成
        Args:
            str_num (int): 字符串数字
        Returns:
            int: 数字
        Example:
            >>> is_comma_separated_number("123,456.789")
            123456.789
        Raises:
            Exception: error
        """
        # 去除分号
        str_num = ''.join(str_num.split(','))
        # 判断是否数字
        return int(str_num) if str_num.isdigit() else 0
    
    def find_numbers_in_string(self, s:str):
        """find_numbers_in_string _summary_

         输入一串字符，提取字符里面的数字并返回

        Args:
            s (str): str

        Returns:
            list: [123, 456]
        """
        return [int(n.replace(',', '')) for n in re.findall('\d+(?:,\d+)*', s)]
    
    def save_file(self, file_data: any, file_path:str = 'test.html') -> bool:
        """
        Description:
            保存html文件
        Args:
            file_path (str): 文件路径
            file_data (any): 文件数据
        Returns:
            bool: True 写入成功, False 写入失败
        Example:
            >>> save_file(file_data=html,file_path=file_path)
            True
        Raises:
            Exception: error
        """
        state = False
        try:
            with open(file=file_path,mode="w+",encoding="utf-8") as fp:
                _, file_extension = os.path.splitext(file_path)
                file_extension = file_extension.lower()
                if file_extension == '.json':
                    if type(file_data) is str:
                        file_data = json.loads(file_data)
                    json.dump(file_data, fp, ensure_ascii=False, indent=4)
                elif file_extension in ['.html', ".txt",".log"]:
                    fp.write(file_data)
                    pass
            state = True
            self.logger.info("success write file :%s",file_path)
        except Exception as e:
            self.logger.error("Error occurred:%s", e) 
        finally:
            fp.close()
            return state
        
    def read_file(self, file_path:str = "test.json") -> Any:
        """
        Description:
            从给定的文件路径读取文件，并返回解析后的数据。
        Args:
            file_path (str): 文件的路径
        Returns:
            Any: 解析后的数据（通常是字典或字典列表）
        Raises:
            Exception: error
        """
        data = None
        try:
            with open(file_path, "r", encoding="utf-8") as fp:
                _, file_extension = os.path.splitext(file_path)
                file_extension = file_extension.lower()
                if file_extension == '.json':
                    data = json.load(fp)
                elif file_extension == ".yaml":
                    data =  yaml.safe_load(fp)
                elif file_extension in ['.html', ".txt",".log"]:
                    data = fp.read()
        except Exception as e: 
            self.logger.error("Error occurred:%s", e) 
        finally:
            fp.close()
            return data

    def ddot2dict(self, ddot_str:str) -> dict:
        """
        Description:
            dot dot string 2 dict
        Args:
            ddot_str : dot dot string --name=value

        Returns:
            dict: {name:value}
        Example:
        Raises:
            Exception: error
        """ 
        matches = re.findall(r'--(\w+)\s+([^-\s]+)', ddot_str)
        return dict(matches) if matches else None
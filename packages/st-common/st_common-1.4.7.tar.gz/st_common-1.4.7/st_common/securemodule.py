
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   securemodule.py
@Time    :   2023/08/30 17:23:32
Python Version:  python 3.10 
@Version :   1.0
@Desc    :   输入明文变量(dict / str)
             输出加密变量 pkl
'''
import hashlib
from Crypto.Cipher import AES
import base64

import logging
# 获取名为当前模块名称的logger
logger = logging.getLogger('main')
class Secure(object):
    def __init__(self,key_string: str =None) -> None:
        """
        Description:
            init: 
        Args:
            key_string(str) : key secrte
        Returns:
            None
        Example:
            >>> Secure(key_string="noninteractive")
        Raises:
            Exception: error
        """
        # key_string = os.getenv("DEBIAN_FRONTEND") if os.getenv("DEBIAN_FRONTEND") else "/root"
        self.cipher = AES.new(hashlib.sha256(key_string.encode("utf-8")).digest(), AES.MODE_ECB)


    def encrypt_dict_variable(self,clear_var_dict:dict = None):
        """
        Description:
            secret dict value
        Args:
            clear_var_dict (dict): want to secret dict
        Returns:
            dict: secreted dict
        Example:
            >>> clear_var_dict = {'name': 'John', 'age': 30, 'gender': 'male'}
            >>> encrypt_dict_variable(clear_var_dict=clear_var_dict)
            {'name': '3OOVGbJCdt7HIes9qDomqA==', 'age': 30, 'gender': '4VIKQ6m/IRT08WrXuZQgSg=='}
        Raises:
            Exception: error
        """
        if not clear_var_dict:
            clear_var_dict = self.clear_var_dict
        cipher_dict = clear_var_dict.copy()
        for dict_key, dict_value in clear_var_dict.items():
            cipher_dict[dict_key] = self._encrypt(data=dict_value)
            pass
        return cipher_dict

    def decrypt_dict_variable(self,cipher_dict:dict = None):
        """
        Description:
            decrypt dict variable
        Args:
            cipher_dict (dict): decrypt dict 
        Returns:
            clear_var_dict (dict): clear dict
        Example:
            >>> cipher_dict = {'name': '3OOVGbJCdt7HIes9qDomqA==', 'age': 30, 'gender': '4VIKQ6m/IRT08WrXuZQgSg=='}
            >>> decrypt_dict_variable(cipher_dict=cipher_dict)
            {'name': 'John', 'age': 30, 'gender': 'male'}

        Raises:
            Exception: error
        """
        if not cipher_dict:
            cipher_dict = self.cipher_dict
        clear_dict = cipher_dict.copy()

        for dict_key, dict_value in cipher_dict.items():
            clear_dict[dict_key] = self._decrypt(data=dict_value)
            pass
        return clear_dict
    

    def _encrypt(self, data:str = None):
        """
        Description:
            encrypt value data
        Args:
            data (str): want to encrypt data
        Returns:
            ecrypt data
        Example:
            >>> data = "Hello, World!"
            >>> _encrypt(data=data)
            igjUXnl/qeGS93Ixb+IpZg==
        Raises:
            Exception: error
        """
        if isinstance(data,int):
            logger.info("data is int , no encrypt")
            return data
        padded_data = data + (AES.block_size - len(data) % AES.block_size) * chr(AES.block_size - len(data) % AES.block_size)
        encrypted_data = self.cipher.encrypt(padded_data.encode('utf-8'))
        return base64.b64encode(encrypted_data).decode('utf-8')

    def _decrypt(self, data:str = None):
        """
        Description:
            decrypt value data
        Args:
            data (str /int): 
        Returns:
            decrypt data
        Example:
            >>> data = "igjUXnl/qeGS93Ixb+IpZg=="
            >>> _decrypt(data=data)
            Hello, World!
        Raises:
            Exception: error
        """
        if isinstance(data,int):
            logger.info("data is int , no decrypt")
            return data
        encrypted_data = base64.b64decode(data)
        decrypted_data = self.cipher.decrypt(encrypted_data).decode('utf-8')
        return decrypted_data.rstrip(chr(ord(decrypted_data[-1])))



import unittest
from parameterized import parameterized

from st_common import Secure

    


class SecureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # print("在每个类之前执行，如创建一个类，创建数据库链接，初始化日志对象")
        cls.secure = Secure(key_string="noninteractive")
    @classmethod
    def tearDownClass(cls) -> None:
        # print("在每个类之后执行，如销毁一个类，销毁数据库链接，销毁日志对象")
        pass

    def test_helloworld(self):
        print("helle world: %s" % self.__class__.__name__)

    @parameterized.expand([
        ('Hello, World!'),(123456),("123456")
        ])
    def test_encrypt(self, data):
        rst = self.secure._encrypt(data=data)
        print(rst)
    @parameterized.expand([
        ('igjUXnl/qeGS93Ixb+IpZg==','Hello, World!'),
        ("bRHN95oLZy1ofqpUyHrKWg==","123456")
        ])
    def test_decrypt(self,en_data, de_data):
        self.assertEqual(first=self.secure._decrypt(data=en_data), second=de_data)


    @parameterized.expand([
        ({"name":"ststst"},),
        ({'name': 'John', 'age': 30, 'gender': 'male'},)
        ])
    @unittest.skip(reason="test_001 pass")
    def test_encrypt_dict_variable(self, data):
        rst = self.secure.encrypt_dict_variable(clear_var_dict=data)
        print(rst)


    @parameterized.expand([
        ({'name': '3OOVGbJCdt7HIes9qDomqA==', 'age': 30, 'gender': '4VIKQ6m/IRT08WrXuZQgSg=='}, {'name': 'John', 'age': 30, 'gender': 'male'},),
        ({'name': 'Ov0PvnPqX2vn2+Q2HxoWdQ=='}, {'name': 'ststst'})
        ])
    
    def test_decrypt_dict_variable(self,en_data, de_data):
        self.assertEqual(first=self.secure.decrypt_dict_variable(cipher_dict=en_data), second=de_data)
# -*- coding: utf-8 -*-
"""
st_common cookies - 通用的cookies处理模块
"""
from glob import glob
from os.path import expanduser
from platform import system

from sqlite3 import OperationalError, connect
import http.cookiejar as cookielib


import requests
import pickle
def check_expires(cookies_list):
    """
    check cookies expires time
    :param cookies_list: list of dict, [{'name': ..., 'value': ...,'expires':...}]
    :return : first expires
    """
    cookies_list.sort(key=lambda x: x.get('expires', 'Nan'))
    return cookies_list[0]
def get_cookiefile() -> str:
    """
    Description:
        Obtain the sqlite file for storing cookies from Firefox browser
    Args:
        None
    Returns:
        str: Obtain the file path for storing cookies in Firefox browser
    Example:
        >>> get_cookiefile()
    Raises:
        Exception: error
    """
    default_cookiefile = {
        "Windows": "~/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite",
        "Darwin": "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite",
    }.get(system(), "~/.mozilla/firefox/*/cookies.sqlite")
    cookiefiles = glob(expanduser(default_cookiefile))
    if not cookiefiles:
        raise SystemExit("No Firefox cookies.sqlite file found. Use -c COOKIEFILE.")
    return cookiefiles[0]
    
def cookiefile_to_cookiesjar(cookiefile:str = None, domain:str ="example.com") -> cookielib.CookieJar:
    """
    Description:
        Obtaining from a cookie file through an SQL statement
    Args:
        cookiefile (str): sqlite 
        domain(str) : domain
    Returns:
        CookieJar: Cookie 
    Example:
        >>> base = Base()
        >>> cookiefile_path = base.get_cookiefile()
        >>> cj = base.cookiefile_to_dict(cookiefile=cookiefile_path, domain="example.com")
            <CookieJar>
            r_session = requests.Session()
            r_session.cookies = cj
    Raises:
        Exception: error
    """
    conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT host, path, isSecure, expiry, name, value FROM moz_cookies WHERE baseDomain='{domain}'")
    except OperationalError:
        cur.execute(f"SELECT host, path, isSecure, expiry, name, value FROM moz_cookies WHERE host LIKE '%{domain}'")
    cj = cookielib.CookieJar()
    for item in cur.fetchall():
        c = cookielib.Cookie(0, item[4], item[5],
                            None, False,
                            item[0], item[0].startswith('.'), item[0].startswith('.'),
                            item[1], False,
                            item[2],
                            item[3], item[3]=="",
                            None, None, {})
        cj.set_cookie(c)
    return cj

def cookiejar_to_str(cookies_jar):
    """
    Description:
        Convert CookieJar to a cookie string in the headers field of requests.request
    Args:
        cookies_jar (CookieJar): Cookie
    Returns:
        str: Cookies for the headers field
    Example:
        >>> base = Base()
        >>> cookiefile_path = base.get_cookiefile()
        >>> cookies_jar = base.cookiefile_to_dict(cookiefile=cookiefile_path)
            cookies_str = base.cookiejar_to_str(cookies_jar=cookies_jar)
            headers = {'cookies': cookies_str}
    Raises:
        Exception: error
    """
    cookies_dict = requests.utils.dict_from_cookiejar(cookies_jar)
    cookies_str = "; ".join([f"{k}={v}" for k, v in cookies_dict.items()])
    return cookies_str
    
    
def cookies_str_to_dict(cookies_str:str):
    """
    Description:
        cookies_str_to_dict
    Args:
        cookies_str (str): cookies "key1=value1; key2=value2; key3=value3"
    Returns:
        dict: cookies dict
    Example:
        >>> cookies_str_to_dict
    Raises:
        Exception: error
    """
    cookies_dict = {i.split('=')[0]: i.split('=')[1] for i in cookies_str.split('; ')}
    return cookies_dict
    
def cookies_dict_to_cookiejar(cookies_dict, domain, path):
    """
    Description:
        dict 2 cookiejar
    Args:
        cookies_dict (dict): cookies_dict
    Returns:
        cookies_jar (CookieJar): Cookie 
    Example:
        >>> cookies_dict = {'key1': 'value1', 'key2': 'value2'}
        >>> cookiejar = dict_to_cookiejar(cookies_dict, 'www.example.com', '/')
    Raises:
        Exception: error
    """

    cookiejar = cookielib.CookieJar()
    for key, value in cookies_dict.items():
        cookie = cookielib.Cookie(
            version=0,
            name=key,
            value=value,
            port=None,
            port_specified=False,
            domain=domain,
            domain_specified=True,
            domain_initial_dot=False,
            path=path,
            path_specified=True,
            secure=False,
            expires=None,
            discard=True,
            comment=None,
            comment_url=None,
            rest={}
        )
        cookiejar.set_cookie(cookie)
    return cookiejar
    
def cookiejar_to_sessionfile(cookies_jar: cookielib.CookieJar = None ,session_file:str ="session-test") -> None:
    """
    Description:
        CookieJar 2 sessionfile
    Args:
        cookies_jar (CookieJar): Cookie 
        session_file (str): session_file 
    Returns:
        None
    Example:
        >>> base = Base()
        >>> cookiefile_path = base.get_cookiefile()
        >>> cookies_jar = base.cookiefile_to_dict(cookiefile=cookiefile_path)
            base.cookiejar_to_sessionfile(cookies_jar=cookies_jar,session_file="session-test")
            with open('cookies.pkl', 'rb') as f:
                cookies_dict = pickle.load(f)
            s = requests.Session()
            s.cookies.update(cookies_dict)
            s.cookies.update(cookies_dict)   
    Raises:
        Exception: error

    """
    cookies_dict = requests.utils.dict_from_cookiejar(cookies_jar)
    with open(session_file, 'wb') as f:
        pickle.dump(cookies_dict, f)


def list2dict(cookies_list):
    """
    cookies list2dict
    :param cookies_list: list of dict, [{'name': ..., 'value': ...}]
    :return: dict, like: {key1: value1, key2: value2, ...}
    """
    cookies_dict = dict()
    for ehe in cookies_list:
        cookies_dict[ehe['name']] = ehe['value']
    return cookies_dict


def list2str(cookies_list, sep='; ', equ='='):
    """
    cookie list2str
    :param cookies_list: list of dict, [{'name': ..., 'value': ...}]
    :param sep: str,
    :param equ: str,
    :return: str, like: 'key1=value1; key2=value2'
    """
    cookies_str = [x['name'] + equ + x['value'] for x in cookies_list]
    cookies_str = sep.join(cookies_str)
    return cookies_str


def str2dict(cookies_str, sep='; ', equ='='):
    """
    cookies str2dict
    :param cookies_str: str,
    :param sep: str,
    :param equ: str,
    :return: dict, like: {key1: value1, key2: value2, ...}
    """
    cookies_dict = dict()
    list_tmp = cookies_str.split(sep)
    for ehe in list_tmp:
        tmp = ehe.split(equ)
        if len(tmp) > 1:
            cookies_dict[tmp[0]] = equ.join(tmp[1:])
    return cookies_dict


def dict2str(cookies_dict, sep='; ', equ='='):
    """
    cookies dict2str
    :param cookies_dict: dict,
    :param sep: str,
    :param equ: str,
    :return: str, like: 'key1=value1; key2=value2'
    """
    cookies_str = [ehkey + equ + cookies_dict[ehkey] for ehkey in cookies_dict.keys()]
    cookies_str = sep.join(cookies_str)
    return cookies_str

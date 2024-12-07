#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   dbmodule.py
@Time    :   2023/08/16 09:42:54
Python Version:  3.10
@Version :   1.0
@Desc    :   
数据驱动层, 也叫DAO层,是用于封装对数据库的访问。
在Python中,我们可以创建一个通用的数据驱动层接口,然后分别为MongoDB,MySQL和Oracle,Redis实现这个接口。
SQLAlchemy 主要用于关系型数据库，并且不直接支持 MongoDB 和 Redis,所以对于这两种类型的数据库我们需要单独处理。
'''

import logging
# 获取名为当前模块名称的logger
logger = logging.getLogger('main')

from urllib.parse import quote_plus

def orm_update_or_insert(session, data, filtkeys, table, update=False, updatekeys=None):
    """
    基于orm更新/插入数据
    :param session: sessionmaker(),
    :param data: dict/series,
    :param filtkeys: list, 键名, 用于筛选数据
    :param table:
    :param update: bool, 是否update数据
    :param updatekeys: list, 键名, 用于update数据
    example: 
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        conn = create_engine(settings.DSN)
        sessmaker = sessionmaker(conn)
        sess = sessmaker()
        for eh, ehrow in df.iterrows():
            ehrow = ehrow.dropna()  # 删除nan值
            ehdict = ehrow.to_dict()
            update_keys = list(set(ehdict.keys()) - set(primary_keys))
            dbmodule.orm_update_or_insert(sess, ehdict, primary_keys, tables.JztReportidea,
                                            update=True, updatekeys=update_keys)
        sessmaker.close_all()
    """
    filt_dict = dict()
    for ehfkey in filtkeys:
        filt_dict[ehfkey] = data[ehfkey]
    res_filted = session.query(table).filter_by(**filt_dict).all()
    if len(res_filted) > 0:
        if (update is True) and isinstance(updatekeys, list):
            for ehrf in res_filted:
                for ehukey in updatekeys:
                    # logger.info(ehukey, data[ehukey])
                    if hasattr(ehrf, ehukey):
                        setattr(ehrf, ehukey, data[ehukey])
                session.commit()
    # insert
    elif len(res_filted) <= 0:
        data_insert = table(**data)
        session.add(data_insert)
        session.commit()


def update_or_insert(session, data, filtkeys, tbn, update=False, updatekeys=None):
    """
    基于sql语句更新/插入数据
    :param session: sessionmaker(),
    :param data: dict/series,
    :param filtkeys: list, 键名, 用于筛选数据
    :param tbn: str, table name
    :param update: bool, 是否update数据
    :param updatekeys: list, 键名, 用于update数据
    """
    filt_dict = dict()
    for ehfkey in filtkeys:
        filt_dict[ehfkey] = data[ehfkey]
    filt_str = ['`%s`="%s"' % (x, filt_dict[x]) for x in filt_dict.keys()]
    filt_str = ' AND '.join(filt_str)
    sql = 'SELECT * FROM `%s` WHERE %s' % (tbn, filt_str)
    logger.info(sql)
    res = session.execute(sql)
    if res.rowcount > 0:
        if update is True:
            update_str = ['`%s`="%s"' % (x, data[x]) for x in updatekeys]
            update_str = ', '.join(update_str)
            sql = 'UPDATE `%s` SET %s WHERE %s' % (tbn, update_str, filt_str)
        else:
            return None
    else:
        sql = 'INSERT INTO `%s` (`%s`) VALUES (%s)' % \
              (tbn, '`, `'.join(list(data.keys())), ', '.join(['"%s"' % data[x] for x in data.keys()]))
    logger.info(sql)
    session.execute(sql)
    session.commit()


def replace_c(session, data, filtkeys, tbn, update=False, updatekeys=None):
    """
    改版 update_or_insert 省去 第一步查询
    基于sql语句更新/插入数据
    :param session: sessionmaker(),
    :param data: dict/series,
    :param filtkeys: list, 键名, 用于筛选数据
    :param tbn: str, table name
    :param update: bool, 是否update数据
    :param updatekeys: list, 键名, 用于update数据
    """
    sql = 'REPLACE INTO `%s` (`%s`) VALUES (%s)' % \
          (tbn, '`, `'.join(list(data.keys())), ', '.join(['"%s"' % data[x] for x in data.keys()]))
    session.execute(sql)
    session.commit()


def read_sql(filepath=None):
    # 读取 sql 文件文本内容
    sql = open(filepath, 'r', encoding='utf8')
    sqltxt = sql.readlines()
    # 此时 sqltxt 为 list 类型
    # 读取之后关闭文件
    sql.close()
    # list 转 str
    sql = "".join(sqltxt)
    return sql


from sqlalchemy import create_engine, MetaData, Table, select, insert, update, delete,and_, inspect,Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import traceback
# SQLAlchemy for MySQL and Oracle
class SQLDatabase(object):
    def __init__(self, db_string) -> None:
        """
        Description:
            SQLDatabase init 
        Args:
            db_string (str): db_string
        Returns:
            None
        Example:
        Raises:
            Exception: error
        """
        try:
            self.engine = create_engine(url = db_string)
            self.metadata = MetaData()
            ### Please refer to session.close_all_sessions()
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
        except Exception as e:
            logger.info(f"Failed to connect to database with error: {e}")
            logger.info(traceback.format_exc())
    
    def __del__(self):
        """
        Description:
            before quit
        Args:
            a (int): The first integer to add.
            b (int): The second integer to add
        Returns:
            int: The sum of a and b.
        Example:
            >>> add(1, 2)
            3
        Raises:
            Exception: error
        """
        self.close()
        logger.info("SQLDatabase close()")
    def _get_columns_name(self,table_name:str) -> str:
        """
        Description:
            get columns comment with dict
        Args:
            table_name (str): table name
        Returns:
            str : columns_name_1, columns_name_2,....
        Example:
        Raises:
            Exception: error
        """
        return ",".join([colunms["name"] for colunms in inspect(self.engine).get_columns(table_name)])
    def _get_columns_comment_dict(self,table_name:str) -> dict:
        """
        Description:
            get columns comment with dict
        Args:
            table_name (str): table name
        Returns:
            dict : {columns_name_1 : comment_name_1, columns_name_2 : comment_name_2}
        Example:
            >>> add(1, 2)
            3
        Raises:
            Exception: error
        """
        tmp = {}
        for colunms in inspect(self.engine).get_columns(table_name):
            tmp[colunms["name"]] = colunms["comment"]
        return tmp
    def _table_exists(self, table_name:str) -> bool:
        return inspect(self.engine).has_table(table_name=table_name)
        # return self.engine.dialect.has_table(connection=self.engine,table_name=table_name)
    def _get_primary_key(self, table_name:str) -> list:
        return inspect(self.engine).get_pk_constraint(table_name=table_name)["constrained_columns"]
    def _get_unique_key(self, table_name:str) -> list:
        unique_fields = []
        for constraint in inspect(self.engine).get_unique_constraints(table_name):
            unique_fields.extend(constraint['column_names'])
        return unique_fields
    def create_table(self, table_name:str=None, columns:Column=None, declarative_base_table:declarative_base =None)-> bool:
        """
        Description:
            create first table name 
        Args:
            table_name (str): The first integer to add.
            columns (Column): Column('id', Integer, primary_key=True)
        Returns:
            int: The sum of a and b.
        Example:
            >>> columns = [
                    Column('id', Integer, primary_key=True),
                    Column('name', String(255)),
                    Column('age', Integer)
                    ]
            >>> create_table(table_name="test",columns=columns)
        Raises:
            Exception: error
        """
        try:
            if not self._table_exists(table_name=table_name):
                logger.info('Table"{}" not exists'.format(table_name))
                declarative_base_table.metadata.create_all(self.engine) if declarative_base_table else Table(
                        table_name, 
                        self.metadata,
                        *columns
                    ).metadata.create_all(bind=self.engine)
            else:
                logger.info('Table"{}" exists'.format(table_name))
        except SQLAlchemyError as e:
            logger.error("Error occurred during Table creation!")
            logger.error(traceback.format_exc())
            return False
        else:
            return True

    def fetch(self, table_name:str,filt_dict:dict=None):
        """
        Description:
            sql fetch table  in filt_dict 
        Args:
            table_name (str): table name 
            filt_dict (dict): filt dict
        Returns:
            fetchall
        Example:
            pd.DataFrame(fetch(...))
        Raises:
            Exception: error
        """
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        if filt_dict :
            conditions = [table.c[key] == value for key, value in filt_dict.items()]
            query = select(table).where(and_(*conditions))
        else: 
            query = select(table)
        result = self.session.execute(query)
        return result.fetchall()
    def insert_data(self, table_name:str, data_dict:dict) -> bool:
        """
        Description:
            insert data with table name in dict
        Args:
            table_name (str): table name 
            data_dict (dict): data dict  {"A":123}
        Returns:
            bool
        Example:

        Raises:
            Exception: error
        """
        try:
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            stmt = insert(table).values(data_dict)
            self.session.execute(stmt)
        except IntegrityError as e :
            logger.info(e.args[0] + " pass !!")
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.info("Error occurred during record insertion!")
            logger.error(traceback.format_exc())
            return False
        else:
            self.session.commit()
            return True
    def update_data(self, table_name:str, condition_dict:dict, new_data_dict:dict) -> bool:
        """
        Description:
            update data in table name condition_dict with new_data_dict
        Args:
            table_name (str): table name
            condition_dict (dict): condition dict
            new_data_dict (dict): new data dict
        Returns:
            bool
        Example:

        Raises:
            Exception: error
        """
        try:
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            where_clause = and_(*[table.columns[key] == value for key, value in condition_dict.items()])
            stmt = update(table).where(where_clause).values(new_data_dict)
            self.session.execute(stmt)
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.info("Error occurred during record update!")
            # logger.error(traceback.format_exc())
            logger.error(traceback.format_exc())
            return False
        else:
            self.session.commit()
            return True
    def update_or_insert_data(self,table_name:str,data_dict:dict,deduplicate_mode = "primary") ->bool:
        """
        Description:
            update or insert data in no/has record with IntegrityError
        Args:
            table_name (str): table name 
            data_dict (dict): data dict  {"A":123}. must contain prime key
            deduplicate_mode (str): primary / unique
        Returns:
            int: The sum of a and b.
        Example:
            >>> add(1, 2)
            3
        Raises:
            Exception: error
        """
        try:
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            stmt = insert(table).values(data_dict)
            self.session.execute(stmt)
        except IntegrityError as e :
            self.session.rollback()  # 回滚事务以清除错误状态
            condition_dict = {}
            if deduplicate_mode == "primary":
                deduplicate_keys = self._get_primary_key(table_name=table_name)
            elif deduplicate_mode == "unique":
                deduplicate_keys = self._get_unique_key(table_name=table_name)

            for key in deduplicate_keys:
                condition_dict.update({key:data_dict[key]})
            where_clause = and_(*[table.columns[key] == value for key, value in condition_dict.items()])
            stmt = update(table).where(where_clause).values(data_dict)
            self.session.execute(stmt)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error("Error occurred during record update_or_insert_data!")
            logger.error(traceback.format_exc())
            return False
        else:
            self.session.commit()
            return True
    def delete_data(self, table_name:str, condition_dict:dict) -> bool:
        """
        Description:
            delete data with table name in condition dict
        Args:
            table_name (str): table name
            condition_dict (dict): condition dict
        Returns:
            bool 
        Example:
            >>> 
        Raises:
            Exception: error
        """
        try:
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            where_clause = and_(*[table.columns[key] == value for key, value in condition_dict.items()])
            stmt = delete(table).where(where_clause)
            self.session.execute(stmt)
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error("Error occurred during record deletion!")
            logger.error(str(e))
            return False
        else:
            self.session.commit()
            return True
    def close(self)->bool:
        try:
            self.session.close()
            self.engine.dispose() # Dispose the engine
            return True
        except Exception as e:
            logger.error("Error occurred while closing the connection!")
            logger.error(str(e))
            return False

from pymongo import MongoClient, errors as mongo_errors

# ###  PyMongo for MongoDB
class MongoDBClient(object):
    def __init__(self,db_string)->None:
        """
        Description:
            初始化 MongoDB 客户端。
        Args:
            db_string (str): mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
        Returns:
            None
        Raises:
            Exception: error
        """
        super().__init__()
        self.client = MongoClient(db_string)
    def save_to_mongo(self,database_name: str, collection_name: str, doc: dict) -> bool:
        """
        Description:
            根据集合名字和文档保存在mongodb
        Args:
            database_name(str): 数据库名称
            collection_name (str): 集合名称
            doc (dict): 文档
        Returns:
            bool : True / Flase
        Example:
            >>> add(1, 2)
            3
        Raises:
            Exception: error
        """
        acknowledged, message = self.insert_document(database_name= database_name,
                                          collection_name= collection_name, document=doc)
        if acknowledged:
            return True
        else:
            return False
        
    def get_database(self, database_name:str):
        """
        Description:
           获取指定名称的数据库。
        Args:
            database_name (str): database name
        Returns:
            pymongo.database.Database : 数据库对象
        Example:
            >>> get_database(database_name)
        Raises:
            Exception: error
        """
        return self.client[database_name]
    def get_collection(self, database_name: str, collection_name: str):
        """
        Description:
            获取集合
        Args:
            database_name (str): database name
            collection_name (str): collection name
        Returns:
            pymongo.collection.Collection: 数据库.集合对象
        Example:
            >>> collection = get_collection(database_name, collection_name)
        Raises:
            Exception: error
        """
        db = self.get_database(database_name)
        return db[collection_name]
    def insert_document(self, database_name: str, collection_name: str, document: any) -> bool:
        """
        Description:
            insert_one 新增一个文档,只会追加
        Args:
            database_name (str): 数据库名
            collection_name (str): 集合名
            document(any): 要插入的文档（字典形式）
        Returns:
            bson.objectid.ObjectId: 插入的文档的 ID
        Example:
            >>> mongo_client.insert_document("my_database", "my_collection", document)
            649ab29c82106bf9f8ded991
        Raises:
            Exception: error
        """
        collection = self.get_collection(database_name, collection_name)
        try:
            if type(document) is list:
                result = collection.insert_many(document)
            elif type(document) is dict :
                result = collection.insert_one(document)
            return result.acknowledged, None
        except Exception as e:
            return False, e
    
    def find_documents(self, database_name: str, collection_name: str, query=None):
        """
        Description:
            根据查询条件获取指定集合中的文档。
        Args:
            database_name (str): 数据库名称
            collection_name (str): 集合名称
            query(dict): 查询条件（字典形式），默认为 {}，表示获取所有文档。
        Returns:
            list: 文档列表。
        Example:
            >>> mongo_client.find_documents("my_database", "my_collection")
            [{'_id': ObjectId('649ab73858fdf99180733f7d'), 'name': 'John', 'age': 30, 'city': 'New York'}]
        Raises:
            Exception: error
        """
        if query is None:
            query = {}
        collection = self.get_collection(database_name, collection_name)
        return list(collection.find(query))
    def update_documents(self, database_name: str, collection_name: str, query: dict, new_values: dict) -> int:
        """
        Description:
            根据查询条件更新指定集合中的文档。
        Args:
            database_name (str): 数据库名称
            collection_name (str): 集合名称
            query (dict): 查询条件（字典形式）。
            new_values (dict): 要更新的字段和新值（字典形式）
        Returns:
            int: 更新的文档数量。
        Example:
            >>> mongo_client.update_documents("my_database", "my_collection", 
                    {"$set": {"city": "San Francisco"}}, {"city": "New York"})
            3
        Raises:
            Exception: error
        """
        collection = self.get_collection(database_name, collection_name)
        result = collection.update_many(query, new_values)
        return result.modified_count
    def delete_documents(self, database_name, collection_name, query) -> int:
        """
        Description:
            根据查询条件删除指定集合中的文档。
        Args:
            database_name (str): 数据库名称
            collection_name (str): 集合名称
            query (dict): 查询条件（字典形式）
        Returns:
            int: 删除的文档数量
        Example:
            >>> mongo_client.delete_documents("my_database", "my_collection",
                 {"age": {"$gt": 25}})
            3
        Raises:
            Exception: error
        """
        collection = self.get_collection(database_name, collection_name)
        result = collection.delete_many(query)
        return result.deleted_count
    def close(self):
        """
        Description:
            关闭 MongoDB 客户端连接
        Args:
            None
        Returns:
            None
        Example:
            >>> mongo_client.close()
        Raises:
            Exception: error
        """
        self.client.close()
# Redis-Py for Redis
import redis
class RedisDB:
    def __init__(self, host, port):
        try:
            self.db = redis.Redis(host=host, port=port)
        except redis.ConnectionError as e:
            logger.info(f"Failed to connect to Redis with error: {e}")
            logger.info(traceback.format_exc())
    def fetch(self, name):
        return self.db.get(name)
    def insert_data(self, name, value):
        self.db.set(name, value)
    def update_data(self, name, value):
        self.insert_data(name, value)
    def delete_data(self, key):
        self.db.delete(key)

import json

from datetime import datetime
class RedisCookies(object):
    """
    本地redis的cookies存储/读取处理
    """
    def __init__(self,host='localhost', port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db)
        #self.remote_rdb = redis.Redis(host="10.2.0.98", password="cww981995")

    def save_cookies2hash(self, hname, kname, kvalue):
        """
        保存cookies到redis数据库-hash内
        :param kname: str, hash内的键名
        :param kvalue: str, hash内的键名对应值
        :param hname: str, hash名称
        :return:
            1 - 操作成功
            0 - 操作失败
        """
        return self.redis.hset(hname, kname, kvalue)

    def read_cookies2hash(self, hname, kname):
        """
        从redis数据库-hash内获取cookies
        :param hname: str, hash名称
        :param kname: str, hash内的键名
        :return: None/str, hash内的键名对应值
        """
        kvalue = self.redis.hget(hname, kname)
        if hname.startswith("ali"):
            kvalue = self.remote_rdb.hget(hname, kname)
        if hname.startswith("feigua"):
            kvalue = self.remote_rdb.hget(hname, kname)
        if hname.startswith("luonet"):
            kvalue = self.remote_rdb.hget(hname, kname)
        if kvalue is not None:
            kvalue = kvalue.decode('utf-8')
        logger.info(f'hname :{hname}, kname :{kname}, kvalue:{kvalue}')
        return kvalue

    def save_cookies2hash_withtime(self, hname, kvalue):
        """
        保存cookies到redis数据库-hash内, 包括插入时间和cookies值
        数据结构为: hname: {insertime: value, cookies: value}
        :param hname: str, hash名称
        :param kvalue: str, hash内的键名对应值
        :return:
            1 - 操作成功
            0 - 操作失败
        """
        today = datetime.today()
        today_str = today.strftime('%Y-%m-%d %H:%M:%S')
        self.redis.hset(hname, 'inserttime', today_str)
        return self.redis.hset(hname, 'cookies', kvalue)

    def read_cookies2hash_withtime(self, hname):
        """
        从redis数据库-hash内获取cookies, 不包括插入时间
        数据结构为: hname: {insertime: value, cookies: value}
        :param hname: str, hash名称
        :return: None/str, hash内的键名对应值
        """
        kvalue = self.redis.hget(hname, 'cookies')
        if kvalue is not None:
            kvalue = kvalue.decode('utf-8')
        return kvalue

    def save_cookies(self, kname, kvalue, ex=None):
        """
        直接保存cookies到redis数据库内
        :param kname: str, 键名
        :param kvalue: str, 键名对应值
        :param ex: int, 过期时间(s), 默认None, 不过期
        :return:
            1 - 操作成功
            0 - 操作失败
        """
        return self.redis.set(kname, kvalue, ex=ex)

    def read_cookies(self, kname):
        """
        从redis数据库内获取cookies
        :param kname: str, 键名
        :return: None/str, 键名对应值
        """
        kvalue = self.redis.get(kname)
        if kvalue is not None:
            kvalue = kvalue.decode('utf-8')
        return kvalue

    def close(self):
        self.redis.close()


class RedisPriorityQueue(object):
    ## Redis 有序优先级队列
    def __init__(self, name, host='localhost', port=6379, db=0):
        self.name = name
        self.redis = redis.Redis(host=host, port=port, db=db)
    def push(self, item_primary_key:str,item:[str,dict], priority):
        if isinstance(item, dict):
            # 使用JSON格式将字典转换为字符串以便存储
            item_str = json.dumps(item)
        elif isinstance(item, str):
            item_str = item
        else:
            logger.info("The input is neither a dictionary nor a string.")
            return False
        
        """ 将项推入队列，带有指定的优先级（越低的分数具有越高的优先级）"""
        if not self.redis.zscore(self.name, item_primary_key):
            self.redis.zadd(self.name, {item_str: priority})
            logger.info(f"键名：{self.name}, zadd {item_str}, priority:{priority} successful")
            return True
        else:
            logger.info(f"键名：{self.name}, zadd {item_str}, priority:{priority} is exist item_primary_key:{item_primary_key}")
            return True
    def pop(self) -> str:
        """
        Description:
            弹出具有最高优先级（最低分数）的项 
        Args:
            None
        Returns:
            str:
        Example:
        Raises:
            Exception: error
        """
        # 使用事务确保操作的原子性
        with self.redis.pipeline() as pipe:
            while True:
                try:
                    pipe.watch(self.name)
                    item_data = pipe.zrange(self.name, 0, 0, withscores=True)
                    if item_data:
                        item_str, _ = item_data[0]
                        pipe.multi()
                        pipe.zrem(self.name, item_str)
                        pipe.execute()
                        return item_str
                    else:
                        return None
                except redis.exceptions.WatchError:
                    # 发生并发修改时继续重试
                    continue
    # def get_zset_size(self):
    #     return int(self.redis.zcard(self.name))
    ## 返回地址，无法识别到大小
    def peek(self):
        """ 查看具有最高优先级的项而不删除它 """
        items = self.redis.zrange(self.name, 0, 0)
        if items:
            return json.loads(items[0])  # 将字符串转换回字典
        return None
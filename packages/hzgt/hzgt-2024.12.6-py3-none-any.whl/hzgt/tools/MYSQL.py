# -*- coding: utf-8 -*-

import os
import sys
import re

from ..strop import restrop
from ..sc import SCError


import pymysql

VALID_MYSQL_DATA_TYPES = ['TINYINT', 'SMALLINT', 'INT', 'INTEGER', 'BIGINT', 'FLOAT', 'DOUBLE', 'DECIMAL', 'DATE',
                          'TIME', 'DATETIME', 'TIMESTAMP', 'CHAR', 'VARCHAR', 'TEXT', 'BLOB', 'LONGBLOB', 'ENUM',
                          'SET', 'JSON']


class Mysqlop:
    def __init__(self, host: str, port: int, user: str, passwd: str, charset: str = "utf8"):
        """
        初始化mmysql类

        :param host: MYSQL数据库地址
        :param port: 端口
        :param user: 用户名
        :param passwd: 密码
        :param charset: 编码 默认 UTF8
        """
        self.__config = {"host": str(host), "port": int(port), "user": str(user), "passwd": str(passwd), 'charset': charset}
        self.__con = None
        self.__cur = None
        self.__selected_db = None  # 已选择的数据库
        self.__selected_table = None  # 已选择的数据库表

    def start(self):
        """
        启动服务器连接

        :return: 
        """
        try:
            self.__con = pymysql.connect(**self.__config, autocommit=False)
            self.__cur = self.__con.cursor()
        except Exception as e:
            raise Exception(f'数据库连接失败. Error: {e.__class__.__name__}: {e}') from None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        return self.start()

    def close(self):
        if self.__con:
            self.__con.rollback()  # Ensure any pending transaction is rolled back
            self.__cur.close()
            self.__con.close()
            self.__con = None
            self.__cur = None

    def __execute(self, sql: str, args: tuple = None, bool_commit: bool = True):
        """
        执行sql语句

        :param sql: sql语句
        :param args: 其它参数
        :param bool_commit: 是否自动提交 默认 True
        :return:
        """
        try:
            if args:
                self.__cur.execute(sql, args)
            else:
                self.__cur.execute(sql)
            if bool_commit:
                self.__con.commit()
            return self.__cur.fetchall()
        except Exception as e:
            self.__con.rollback()
            raise Exception(f'执行数据库SQL语句失败: {e.__class__.__name__}: {e}') from None

    def get_curuser(self):
        return self.__execute("SELECT USER()")

    def get_version(self):
        return self.__execute("SELECT VERSION()")

    def get_all_db(self):
        """
        获取所有数据库名

        :return: list: 返回所有数据库名
        """
        return [db[0] for db in self.__execute("SHOW DATABASES")]

    def get_all_nonsys_db(self):
        """
        获取除系统数据库外的所有数据库名

        :return: list: 返回所有非系统数据库名
        """
        exclude_list = ["sys", "information_schema", "mysql", "performance_schema"]
        return [db for db in self.get_all_db() if db not in exclude_list]

    def get_tables(self, dbname: str = ""):
        """
        获取已选择的数据库的所有表

        :return: list: 返回已选择的数据库的所有表
        """
        dbname = dbname or self.__selected_db
        return [table[0] for table in self.__execute(f"SHOW TABLES FROM {dbname}")]

    def get_table_index(self, tablename: str = ''):
        """
        获取已选择的表的索引信息

        :return: list: 返回已选择的表的索引信息
        """
        tablename = tablename or self.__selected_table
        return self.__execute(f"DESCRIBE {tablename}")

    def select_db(self, dbname: str):
        """
        选择数据库

        :param dbname: 数据库名
        :return:
        """
        self.__con.select_db(dbname)
        self.__selected_db = dbname

    def create_db(self, dbname: str, bool_autoselect: bool = True):
        """
        创建数据库

        :param dbname: 需要创建的数据库名
        :param bool_autoselect: 是否自动选择该数据库
        :return:
        """
        self.__execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}` CHARACTER SET utf8 COLLATE utf8_general_ci")
        if bool_autoselect:
            self.select_db(dbname)

    def drop_db(self, dbname: str):
        """
        删除数据库

        :param dbname: 需要删除的数据库名
        :return:
        """
        self.__execute(f"DROP DATABASE IF EXISTS `{dbname}`")
        if dbname == self.__selected_db:
            self.__selected_db = None

    def select_table(self, tablename: str):
        """
        选择数据库表

        :param tablename: 需要选择的表名
        :return:
        """
        self.__selected_table = tablename

    def create_table(self, tablename: str, attr_dict: dict, primary_key: list[str] = None,
                     bool_id: bool = True, bool_autoselect: bool = True):
        """
        创建表

        '''

        + 整数类型

            + TINYINT:  1字节, 范围从-128到127（有符号）, 0到255（无符号）. 适用于存储小整数值, 如状态标志或性别.
            + SMALLINT:  2字节, 范围从-32,768到32,767（有符号）, 0到65,535（无符号）. 用于中等大小的整数.
            + INT或INTEGER:  4字节, 范围从-2,147,483,648到2,147,483,647（有符号）, 0到4,294,967,295（无符号）. 通常用于存储一般整数数据.
            + BIGINT:  8字节, 范围更大, 适用于非常大的整数, 如用户ID或订单号.

        + 浮点数类型

            + FLOAT:  4字节, 单精度浮点数. 用于存储大约7位有效数字的浮点数.
            + DOUBLE:  8字节, 双精度浮点数. 用于存储大约15位有效数字的浮点数.

        + 定点数类型

            + DECIMAL:  根据指定的精度和小数位数占用不同字节数. 适用于货币和精确计算, 因为它不会引入浮点数舍入误差.

        + 日期和时间类型

            + DATE:  3字节, 用于存储日期（年、月、日）.
            + TIME:  3字节, 用于存储时间（时、分、秒）.
            + DATETIME:  8字节, 用于存储日期和时间.
            + TIMESTAMP:  4字节, 通常用于记录创建和修改时间, 存储范围受限于32位UNIX时间戳.

        + 字符串类型

            + CHAR:  定长字符串, 占用的字节数等于指定的长度, 最大长度为255个字符. 适用于固定长度的数据, 如国家代码.
            + VARCHAR:  可变长度字符串, 占用的字节数根据存储的数据长度而变化, 最多65,535字节. 适用于可变长度的文本数据, 如用户名和评论.
            + TEXT:  用于存储长文本数据, 有TINYTEXT、TEXT、MEDIUMTEXT和LONGTEXT四种类型, 分别对应不同的存储长度.

        + 二进制类型

            + BLOB:  用于存储二进制数据, 可变长度, 最大容量根据存储引擎和配置设置而不同.
            + LONGBLOB:  用于存储更大的二进制数据.

        + 特殊类型

            + ENUM:  枚举类型, 用于存储单一值, 可以选择一个预定义的集合.
            + SET:  集合类型, 用于存储多个值, 可以选择多个预定义的集合.
            + JSON:  用于存储JSON数据, 从MySQL 5.7版本开始支持.
        '''

        :param tablename: 需要创建的表名
        :param attr_dict: 字典 {列名: MYSQL数据类型}, 表示表中的列及其数据类型
        :param primary_key: 主键列表. 其中的元素应为字符串
        :param bool_id: 是否添加 id 为自增主键
        :param bool_autoselect: 创建表格后是否自动选择该表格, 默认为自动选择
        :return: 无返回值, 在数据库中创建指定的表
        """
        tablename = tablename or self.__selected_table

        # 检查tablename是否是有效的表名
        if not re.match(r'^[a-zA-Z0 - 9_]+$', tablename):
            raise ValueError("tablename只能包含字母、数字和下划线.")

        # 检查attr_dict是否为字典类型
        if not isinstance(attr_dict, dict):
            raise TypeError("attr_dict必须是一个字典.")

        if primary_key is None:
            primary_key = []

        if bool_id:
            if "id" not in list(attr_dict.keys()):
                primary_key.append("id")

        # 检查attr_dict的键和值是否符合要求
        for col_name, data_type in attr_dict.items():
            if not re.match(r'^[a-zA-Z0-9_]+$', col_name):
                raise ValueError("列名只能包含字母、数字和下划线.")
            data_type = data_type.upper()

            # 验证数据类型是否有效，考虑带参数的数据类型
            match = re.match(r'(' + '|'.join(VALID_MYSQL_DATA_TYPES) + ')', data_type)
            if not match:
                raise ValueError(f"{data_type}不是有效的MySQL数据类型.")

        # 检查primary_key中是否有重复元素
        if len(set(primary_key)) != len(primary_key):
            raise ValueError("primary_key中不能有重复元素")

        # 检查primary_key中的元素是否为字符串
        for key in primary_key:
            if not isinstance(key, str):
                raise TypeError("primary_key中的元素必须是字符串.")

        # 检查primary_key中的元素是否为空字符串
        for key in primary_key:
            if key == "":
                raise ValueError("primary_key中的元素不能为空字符串")

        col_definitions = []
        if bool_id and 'id' not in attr_dict:
            col_definitions.append("`id` INT AUTO_INCREMENT")
        for col_name, data_type in attr_dict.items():
            col_definitions.append(f"`{col_name}` {data_type}")
        columns = ', '.join(col_definitions)
        pk_definition = f"PRIMARY KEY (`{', '.join(primary_key)}`)"

        sql = f"CREATE TABLE IF NOT EXISTS `{tablename}` ({columns}, {pk_definition}) ENGINE=InnoDB DEFAULT CHARSET=utf8"
        self.__execute(sql)
        if bool_autoselect:
            self.__selected_table = tablename

    # =-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=
    def insert(self, tablename: str = '', record: dict = None):
        """
        插入数据

        :param tablename: 数据库表名
        :param record: 需要插入的数据
        :return:
        """
        tablename = tablename or self.__selected_table

        columns = list(record.keys())
        values = list(record.values())
        # 构建查询条件
        query_conditions = []
        for col, val in zip(columns, values):
            query_conditions.append(f"{col} = '{val}'")
        query_condition = " AND ".join(query_conditions) if len(query_conditions) > 1 else query_conditions
        # 先查询是否已存在
        existing = self.select(conditions=record)
        if not existing:
            columns_str = ', '.join(columns)
            values_str = ', '.join([f"'{value}'" for value in values])
            sql = f"INSERT INTO {tablename} ({columns_str}) VALUES ({values_str})"
            try:
                self.__execute(sql)
            except Exception as e:
                raise Exception(f"插入失败: {e.__class__.__name__}: {e}") from None
        else:
            print(f"记录 {record} 已存在，未执行插入操作。")

    def select(self, tablename: str = '', conditions: dict = None, order: dict = '', fields: list = ['*']):

        """
        查询数据

        :param tablename: 数据库表名. 如果未提供此参数或参数为空, 函数将使用 self.__selected_table 作为默认的表名
        :param conditions: 指定查询的条件. 键是表中的列名, 值是用于匹配的条件值. 例如: {"age": 30, "gender": "male"}意味着查询age为30且gender为"male"的记录.
        :param order: 指定查询结果的排序方式，格式为字典，键为列名，值为""（升序）、"DESC"（降序）或"ASC"（升序）
        :param fields: 用于指定查询结果中包含的列. 默认值'*'表示查询所有列. 如果提供一个列表, 如["name", "age"], 则只查询name和age这两列.
        :return: 返回查询到的数据
        """
        tablename = tablename or self.__selected_table

        conditions = conditions or {}
        where_clause_parts = []
        for k in conditions:
            value = conditions[k]
            if isinstance(value, str):
                # 根据实际情况决定是否转义
                where_clause_parts.append(f"`{k}` = '{value}'")
            else:
                where_clause_parts.append(f"`{k}` = {value}")
        where_clause = ' AND '.join(where_clause_parts)

        if not isinstance(fields, list) or (fields != ['*'] and not all(isinstance(f, str) for f in fields)):
            raise ValueError("fields参数应该为'*'或者字符串列表")
        fields_clause = ', '.join(fields) if isinstance(fields, list) and fields != ['*'] else '*'
        sql = f"SELECT {fields_clause} FROM {tablename}"
        if conditions:
            sql += f" WHERE {where_clause}"
        if order:
            order_clause_parts = []
            for col, direction in order.items():
                if direction not in ["", "DESC", "ASC"]:
                    raise ValueError(f"无效的排序方向 '{direction}'，应为''、'DESC'或'ASC'")
                order_clause_parts.append(f"`{col}` {direction}")
            order_clause = ', '.join(order_clause_parts)
            sql += f" ORDER BY {order_clause}"

        try:
            return self.__execute(sql)
        except Exception as e:
            raise Exception(f"查询数据失败: {e.__class__.__name__}: {e}") from None

    def delete(self, tablename: str = '', conditions: dict = None):
        """
        删除数据

        :param tablename: 表名
        :param conditions: dict 删除
        :return:
        """
        tablename = tablename or self.__selected_table

        conditions = conditions or {}
        where_clause = ' AND '.join([f"`{k}` = %s" for k in conditions])
        sql = f"DELETE FROM {tablename}"
        if conditions:
            sql += f" WHERE {where_clause}"

        try:
            self.__execute(sql, list(conditions.values()))
        except Exception as e:
            raise Exception(f"删除数据失败: {e.__class__.__name__}: {e}") from None

    def update(self, tablename: str = '', update_values: dict = None, conditions: dict = None):
        """
        更新数据

        :param tablename: 数据库表名
        :param update_values: 新数据
        :param conditions: 匹配数据字典(原数据)
        :return:
        """
        tablename = tablename or self.__selected_table

        conditions = conditions or {}
        set_clause = ', '.join([f"`{k}` = %s" for k in update_values])
        where_clause = ' AND '.join([f"`{k}` = %s" for k in conditions])
        sql = f"UPDATE {tablename} SET {set_clause}"
        if conditions:
            sql += f" WHERE {where_clause}"

        try:
            self.__execute(sql, list(update_values.values()) + list(conditions.values()))
        except Exception as e:
            raise Exception(f"更新数据失败: {e.__class__.__name__}: {e}") from None

    def drop_table(self, tablename: str = ''):
        """
        删除数据库表

        :param tablename: 数据库表名
        """
        tablename = tablename or self.__selected_table

        sql = f"DROP TABLE IF EXISTS {tablename}"
        try:
            self.__execute(sql)
        except Exception as e:
            raise Exception(f"数据库表删除失败: {e.__class__.__name__}: {e}") from None

    def purge(self, tablename: str = ''):
        """
        清除数据库表的数据

        :param tablename: 数据库表名
        :return:
        """
        tablename = tablename or self.__selected_table

        sql = f"TRUNCATE TABLE {tablename}"
        try:
            self.__execute(sql)
        except Exception as e:
            raise Exception(f"数据库表数据清除失败: {e.__class__.__name__}: {e}") from None

    # =-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=
    def change_passwd(self, username: str, new_password: str, host: str = "localhost"):
        """
        修改密码

        :param username: 用户名
        :param new_password: 新密码
        :param host: 用户登录数据库的主机地址 默认 localhost
        :return:
        """
        host = host or "localhost"
        sql = f"ALTER USER '{username}'@'{host}' IDENTIFIED BY '{new_password}'"
        try:
            self.__execute(sql)
            self.close()
        except Exception as e:
            raise Exception(f"修改密码失败: {e.__class__.__name__}: {e}") from None

    def get_curuser_permissions(self):
        """
        查询当前用户的权限信息

        :return: 元组格式: ([英文基础权限列表, 英文高级权限列表], [中文基础权限列表, 中文高级权限列表])
        """
        # SQL语句用于查询当前用户的权限
        # SHOW GRANTS FOR CURRENT_USER() 显示当前用户的权限
        sql = "SHOW GRANTS FOR CURRENT_USER();"

        def permissions2list(_privileges: list[str]):
            """
            将MySQL权限列表转换为中文解释

            :param _privileges: 权限列表, 每个元素是一个表示权限的字符串
            :return : tuple of ([英文基础权限列表, 英文高级权限列表], [中文基础权限列表, 中文高级权限列表])
            """
            from ..CONST import PRIVILEGE_TRANSLATION

            # 用于存储中文解释的列表
            english_explanations = []
            chinese_explanations = []

            def ceexp(prinames: list):
                prinames[-1] = prinames[-1].split(" ON ")[0]  # 处理最后的"*** ON *.* TO `root`@`%` WITH GRANT OPTION"
                _temp = [PRIVILEGE_TRANSLATION.get(priname, '未知权限') for priname in prinames] # 翻译权限名称
                english_explanations.append(prinames)  # 添加到结果列表
                chinese_explanations.append(_temp)

            temp_names = _privileges[0][6:].split(', ')  # 处理前面的"GRANT " 以及 ", "分离
            ceexp(temp_names)

            temp_names = _privileges[1][6:].split(',')  # 处理前面的"GRANT " 以及 ","分离
            ceexp(temp_names)

            return {
                'en_low': english_explanations[0],
                'en_high': english_explanations[1],
                'zh_low': chinese_explanations[0],
                'zh_high': chinese_explanations[1]
            }

        try:
            privileges = self.__execute(sql)
            return permissions2list([privileges[0][0], privileges[1][0]])
        except Exception as e:
            error = '执行查询用户权限的SQL语句失败(%s): %s' % (e.args, e.args[1])
            raise Exception(error + f"{e.__class__.__name__}: {e}") from None

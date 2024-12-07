import os
import sys

from ..strop import restrop
from ..CONST import INSTALLCMD
from ..sc import SCError

try:
    import pymysql
except Exception as err:
    print(err)
    os.system(INSTALLCMD("pymysql==1.1.0"))
    import pymysql


class Mysqlop:
    def __init__(self, host: str, port: int, user: str, passwd: str, charset: str = "utf8"):
        """
        初始化类
        :param host: MYSQL数据库地址
        :param port: 端口
        :param user: 用户名
        :param passwd: 密码
        :param charset: 编码 默认 UTF8
        """
        self.__config = {"host": host, "port": port, "user": user, "passwd": passwd, 'charset': charset}
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
        except pymysql.err.OperationalError as e:
            raise SCError(f'数据库连接失败. Error: {e}') from None

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
            raise SCError(f'执行数据库SQL语句失败: {e}') from None

    def get_curuser(self):
        return self.__execute("SELECT USER()")

    def get_version(self):
        return self.__execute("SELECT VERSION()")

    def get_all_db(self):
        """
        获取所有数据库名
        """
        return [db[0] for db in self.__execute("SHOW DATABASES")]

    def get_all_nonsys_db(self):
        """
        获取除系统数据库外的所有数据库名
        """
        exclude_list = ["sys", "information_schema", "mysql", "performance_schema"]
        return [db for db in self.get_all_db() if db not in exclude_list]

    def get_tables(self, dbname: str = ""):
        """
        获取已选择的数据库的所有表
        """
        dbname = dbname or self.__selected_db
        return [table[0] for table in self.__execute(f"SHOW TABLES FROM {dbname}")]

    def get_table_index(self, tablename: str = ''):
        """
        获取已选择的表的索引信息
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
        self.__execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}` CHARACTER SET utf8 COLLATE utf8_general_ci", commit=True)
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

    def create_table(self, tablename: str, attr_dict: dict, primary_key: list[str] = ["id"],
                    bool_autoselect: bool = True):
        """
        创建表
        :param tablename: 需要创建的表名
        :param attr_dict: 字典 {列名: MYSQL数据类型}
        :param primary_key: 主键列表 默认为 ["id"]
        :param bool_autoselect: 创建表格后是否自动选择该表格 默认为子哦对那个选择
        :return:
        """
        columns = ', '.join([f"`{k}` {v}" for k, v in attr_dict.items()])
        if not primary_key or primary_key == [""]:
            primary_key = ["id"]
        if len(primary_key) == 1:
            tempkeys = primary_key[0]
        else:
            tempkeys = ", ".join(primary_key)
        sql = f"CREATE TABLE IF NOT EXISTS `{tablename}` ({columns}, PRIMARY KEY (`{tempkeys}`)) ENGINE=InnoDB DEFAULT CHARSET=utf8"
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

        if not record:
            raise SCError("插入需要携带数据") from None

        columns = ', '.join(record.keys())
        values = ', '.join(['%s'] * len(record))
        sql = f"INSERT INTO {tablename} ({columns}) VALUES ({values})"
        try:
            self.__execute(sql, list(record.values()))
        except IntegrityError as e:
            raise SCError(f"由于违反约束, 插入失败: {e}") from None

    def select(self, tablename: str = '', conditions: dict = None, order: str = '', fields: list = '*'):
        """
        查询数据
        :param tablename: 数据库表名. 如果未提供此参数或参数为空, 函数将使用 self.__selected_table 作为默认的表名
        :param conditions: 指定查询的条件. 键是表中的列名, 值是用于匹配的条件值。例如: {"age": 30, "gender": "male"}意味着查询age为30且gender为"male"的记录。
        :param order: 指定查询结果的排序方式
        :param fields: 用于指定查询结果中包含的列. 默认值'*'表示查询所有列. 如果提供一个列表, 如["name", "age"], 则只查询name和age这两列。
        :return: 返回查询到的数据
        """
        tablename = tablename or self.__selected_table

        conditions = conditions or {}
        where_clause = ' AND '.join([f"`{k}` = %s" for k in conditions])
        fields_clause = ', '.join(fields) if isinstance(fields, list) and fields != ['*'] else '*'
        sql = f"SELECT {fields_clause} FROM {tablename}"
        if conditions:
            sql += f" WHERE {where_clause}"
        if order:
            sql += f" ORDER BY {order}"

        try:
            self.__execute(sql, list(conditions.values()))
        except Exception as e:
            raise SCError(f"查询数据失败: {e}") from None

    def delete(self, tablename: str = '', conditions: dict = None):
        tablename = tablename or self.__selected_table

        conditions = conditions or {}
        where_clause = ' AND '.join([f"`{k}` = %s" for k in conditions])
        sql = f"DELETE FROM {tablename}"
        if conditions:
            sql += f" WHERE {where_clause}"

        try:
            self.__execute(sql, list(conditions.values()))
        except Exception as e:
            raise SCError(f"删除数据失败: {e}") from None

    def update(self, tablename: str = '', update_values: dict = None, conditions: dict = None):
        """
        更新数据
        :param tablename: 数据库表名
        :param update_values: 新数据
        :param conditions: 匹配数据
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
            raise SCError(f"更新数据失败: {e}") from None

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
            raise SCError(f"数据库表删除失败: {e}")

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
            raise SCError(f"数据库表数据清除失败: {e}") from None

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
            raise SCError(f"修改密码失败: {e}") from None

    def get_curuser_permissions(self):
        """
        查询当前用户的权限信息
        :return : tuple of ([英文基础权限列表, 英文高级权限列表], [中文基础权限列表, 中文高级权限列表])
        """
        # SQL语句用于查询当前用户的权限
        # SHOW GRANTS FOR CURRENT_USER() 显示当前用户的权限
        sql = "SHOW GRANTS FOR CURRENT_USER();"

        def permissions2list(_privileges: list[str]):
            """
            将MySQL权限列表转换为中文解释
            :param _privileges: 权限列表，每个元素是一个表示权限的字符串
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

            return english_explanations, chinese_explanations

        try:
            privileges = self.__execute(sql)
            return permissions2list([privileges[0][0], privileges[1][0]])
        except Exception as e:
            error = '执行查询用户权限的SQL语句失败(%s): %s' % (e.args, e.args[1])
            raise SCError(error) from None

import sys
import locale
import getpass

import logging


CURRENT_SYSTEM_DEFAULT_ENCODING: str = sys.getdefaultencoding()  # 当前系统所使用的默认字符编码
DEFAULT_ENCODING: str = locale.getpreferredencoding()  # 获取用户设定的系统默认编码

PLATFORM: str = sys.platform  # 获取操作系统类型
CURRENT_USERNAME: str = getpass.getuser()  # 获取当前用户名
PYTHON_VERSION: tuple = sys.version_info[:3]  # 获取python的版本

def INSTALLCMD(library: str):
    """
    返回需要安装包的cmd命令
    :param library: str 第三方库
    :return:
    """
    _cmd = ['pip', 'install', '']
    if PYTHON_VERSION[0] == 3 and 'linux' in PLATFORM:
        _cmd[0] = 'pip3'
    _cmd[2] = library
    return "%s %s %s" % (_cmd[0], _cmd[1], _cmd[2])


LOG_LEVEL: dict = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }


STYLE: dict = {
    'mode':
        {  # 显示模式
            "": 0,

            'mormal': 0,  # 终端默认设置
            "0": 0,
            0: 0,

            'bold': 1,  # 高亮显示
            "1": 1,
            1: 1,

            'underline': 4,  # 使用下划线
            "4": 4,
            4: 4,

            'blink': 5,  # 闪烁
            "5": 5,
            5: 5,

            'invert': 7,  # 反白显示
            "7": 7,
            7: 7,

            'hide': 8,  # 不可见
            "8": 8,
            8: 8,
        },

    'fore':
        {  # 前景色
            '': '',  # 默认字体颜色

            'black': 30,  # 黑色
            "30": 30,
            0: 30,
            30: 30,

            'red': 31,  # 红色
            "31": 31,
            1: 31,
            31: 31,

            'green': 32,  # 绿色
            "32": 32,
            2: 32,
            32: 32,

            'yellow': 33,  # 黄色
            "33": 33,
            3: 33,
            33: 33,

            'blue': 34,  # 蓝色
            "34": 34,
            4: 34,
            34: 34,

            'purple': 35,  # 紫红色
            "35": 35,
            5: 35,
            35: 35,

            'cyan': 36,  # 青蓝色
            "36": 36,
            6: 36,
            36: 36,

            'white': 37,  # 灰白色
            '37': 37,
            7: 37,
            37: 37,
        },

    'back':
        {  # 背景
            '': 40,  # 默认背景黑色

            'black': 40,  # 黑色
            "40": 40,
            0: 40,
            40: 40,

            'red': 41,  # 红色
            "41": 41,
            1: 41,
            41: 41,

            'green': 42,  # 绿色
            "42": 42,
            2: 42,
            42: 42,

            'yellow': 43,  # 黄色
            "43": 43,
            3: 43,
            43: 43,

            'blue': 44,  # 蓝色
            "44": 44,
            4: 44,
            44: 44,

            'purple': 45,  # 紫红色
            "45": 45,
            5: 45,
            45: 45,

            'cyan': 46,  # 青蓝色
            "46": 46,
            6: 46,
            46: 46,

            'white': 47,  # 灰白色
            "47": 47,
            7: 47,
            47: 47,
        },

    'default':
        {
            'end': 0,
        },
}

# 权限英文到中文的映射字典
PRIVILEGE_TRANSLATION = {
    # 基本权限
    'SELECT': '查询数据',
    'INSERT': '插入数据',
    'UPDATE': '更新数据',
    'DELETE': '删除数据',
    'CREATE': '创建数据库/表',
    'DROP': '删除数据库/表',
    'RELOAD': '重新加载',
    'SHUTDOWN': '关闭服务器',
    'PROCESS': '查看进程',
    'FILE': '文件操作',
    'REFERENCES': '外键约束',
    'INDEX': '创建索引',
    'ALTER': '修改数据库/表',
    'SHOW DATABASES': '显示数据库',
    'SUPER': '超级权限',
    'CREATE TEMPORARY TABLES': '创建临时表',
    'LOCK TABLES': '锁定表',
    'EXECUTE': '执行存储过程',
    'REPLICATION SLAVE': '复制从属',
    'REPLICATION CLIENT': '复制客户端',
    'CREATE VIEW': '创建视图',
    'SHOW VIEW': '显示视图',
    'CREATE ROUTINE': '创建例程',
    'ALTER ROUTINE': '修改例程',
    'CREATE USER': '创建用户',
    'EVENT': '事件管理',
    'TRIGGER': '触发器',
    'CREATE TABLESPACE': '创建表空间',
    'CREATE ROLE': '创建角色',
    'DROP ROLE': '删除角色',
    # 高级权限
    'ALLOW_NONEXISTENT_DEFINER': '允许不存在的定义者',
    'APPLICATION_PASSWORD_ADMIN': '应用密码管理',
    'AUDIT_ABORT_EXEMPT': '审计中止豁免',
    'AUDIT_ADMIN': '审计管理',
    'AUTHENTICATION_POLICY_ADMIN': '认证策略管理',
    'BACKUP_ADMIN': '备份管理',
    'BINLOG_ADMIN': '二进制日志管理',
    'BINLOG_ENCRYPTION_ADMIN': '二进制日志加密管理',
    'CLONE_ADMIN': '克隆管理',
    'CONNECTION_ADMIN': '连接管理',
    'ENCRYPTION_KEY_ADMIN': '加密密钥管理',
    'FIREWALL_EXEMPT': '防火墙豁免',
    'FLUSH_OPTIMIZER_COSTS': '刷新优化器成本',
    'FLUSH_STATUS': '刷新状态',
    'FLUSH_TABLES': '刷新表',
    'FLUSH_USER_RESOURCES': '刷新用户资源',
    'GROUP_REPLICATION_ADMIN': '组复制管理',
    'GROUP_REPLICATION_STREAM': '组复制流',
    'INNODB_REDO_LOG_ARCHIVE': 'InnoDB重做日志归档',
    'INNODB_REDO_LOG_ENABLE': '启用InnoDB重做日志',
    'PASSWORDLESS_USER_ADMIN': '无密码用户管理',
    'PERSIST_RO_VARIABLES_ADMIN': '持久化只读变量管理',
    'REPLICATION_APPLIER': '复制应用者',
    'REPLICATION_SLAVE_ADMIN': '复制从属管理员',
    'RESOURCE_GROUP_ADMIN': '资源组管理',
    'RESOURCE_GROUP_USER': '资源组用户',
    'ROLE_ADMIN': '角色管理',
    'SENSITIVE_VARIABLES_OBSERVER': '敏感变量观察者',
    'SERVICE_CONNECTION_ADMIN': '服务连接管理',
    'SESSION_VARIABLES_ADMIN': '会话变量管理',
    'SET_ANY_DEFINER': '设置任何定义者',
    'SHOW_ROUTINE': '显示例程',
    'SYSTEM_USER': '系统用户',
    'SYSTEM_VARIABLES_ADMIN': '系统变量管理',
    'TABLE_ENCRYPTION_ADMIN': '表加密管理',
    'TELEMETRY_LOG_ADMIN': '遥测日志管理',
    'TRANSACTION_GTID_TAG': '交易GTID标记',
    'XA_RECOVER_ADMIN': 'XA恢复管理',
}

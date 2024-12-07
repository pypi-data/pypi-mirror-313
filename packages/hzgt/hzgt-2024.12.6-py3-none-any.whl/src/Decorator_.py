import datetime
import time
import inspect
import logging
import os
from .strop import restrop, restrop_list

def gettime(func):
    """
    使用方法：装饰器

    在需要显示运算时间的函数前加@gettime

    :param func:
    :return: None
    """
    def get(*args, **kwargs):
        start = datetime.datetime.now()
        starttime = time.time()
        print(restrop_list(["=== ",
                            "开始时间 ", start.strftime('%Y-%m-%d  %H:%M:%S'),
                            "     %s.%s()" % (func.__module__, func.__name__),
                            ],
                           [1,
                            -1, 3,
                            5,
                            ])
              )

        _result = func(*args, **kwargs) # func

        end = datetime.datetime.now()
        spentedtime = time.time() - starttime
        print(restrop_list(["=== ",
                            "结束时间 ", end.strftime('%Y-%m-%d  %H:%M:%S'),
                            "     总耗时 ", f"{spentedtime:.2f}", " s"
                            ],
                           [1,
                            -1, 4,
                            -1, 5, -1
                            ])
              )
        return _result
    return get

def timelog(loglevel="debug"):
    """
        使用方法：装饰器

    在需要显示运算时间的函数前加 @timelog()

    loglevel
        * "debug": logging.DEBUG,
        * "info": logging.INFO,
        * "warning": logging.WARNING,
        * "error": logging.ERROR,
        * "critical": logging.CRITICAL

    :param func:
    :return: None
    """
    LOG_LEVEL = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }

    def timelog(func):
        def RetrieveName():
            stacks = inspect.stack()  # 获取函数调用链
            return stacks[-1].filename, stacks[-1].lineno
        logger = logging.getLogger(__name__)
        logger.setLevel(LOG_LEVEL[loglevel])
        rten = RetrieveName()
        formatter = logging.Formatter(f"%(asctime)s - [{rten[0]}][line:{rten[1]}] - %(levelname)s: %(message)s")

        # 文件输出渠道
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # 创建目录&.log文件
        log_dir = os.path.join(os.getcwd(), "logs")
        lt = time.localtime(time.time())
        yearmonth = time.strftime('%Y%m', lt)
        day = time.strftime('%d', lt)
        full_path = os.path.join(log_dir, yearmonth)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        log_path = os.path.join(full_path, day + ".log")

        file_handler = logging.FileHandler(log_path, encoding="utf8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


        def inner(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
                logger.info(f"func: {func.__name__} {args} -> {res}")
                return res
            except Exception as err:
                logger.error(f"func: {func.__name__} {args} -> {err}")
                return err

        return inner
    return timelog

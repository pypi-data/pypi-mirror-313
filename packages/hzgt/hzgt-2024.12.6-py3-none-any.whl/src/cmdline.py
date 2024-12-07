# -*- coding: utf-8 -*-
import os
import sys
import locale
import subprocess
import threading
import time

from .CONST import INSTALLCMD

try:
    import click
except Exception as err:
    print(err)
    os.system(INSTALLCMD("click"))
    import click

from .strop import restrop
from .CONST import DEFAULT_ENCODING, PLATFORM, CURRENT_USERNAME

@click.group()
def losf():
    """
    - d 命令行 下载模块\n
        - m: 必填~功能参数 1-文件下载 2-github仓库下载 3-音视频下载\n
        - u: 必填~文件/仓库/视频所在的url\n
        - s: 选填~保存路径
    """
    pass

@click.command()
@click.option("-m", "--mode", default=None, type=click.INT, help="必填~mode 1-文件下载 2-github仓库下载 3-音视频下载")
@click.option("-u", "--url", default=None, type=click.STRING, help="必填~url 文件/仓库/视频所在的url")
def d(mode, url):
    """
    命令行 下载
    """
    if mode is None:
        os.system("hzgt d --help")
        exit()
    if mode not in [1, 2, 3]:
        print(f"mode {mode} 无效")
        exit()
    from .download.download import downloadmain
    if 'linux' in PLATFORM:  # linux
        downloadmain(mode, url, savepath=os.path.join("/home", CURRENT_USERNAME, "Download"))
    elif 'win' in PLATFORM:  # win
        downloadmain(mode, url, savepath=os.path.join("d:", "Download"))
    else:
        currentpath = os.getcwd()
        downloadmain(mode, url, savepath=currentpath)


losf.add_command(d)
if __name__ == "__main__":
    losf()
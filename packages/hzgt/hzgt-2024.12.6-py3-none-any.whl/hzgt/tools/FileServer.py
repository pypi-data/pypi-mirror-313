import os
import socket
import ssl
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler as RH
from socketserver import TCPServer
from .INI import readini

from typing import Union


def getip(index: int = None) -> Union[str, list[str]]:
    """
    获取本机IP地址
    :param index: 如果指定 index, 则返回 IP地址列表 中索引为 index 的 IP, 否则返回 IP地址列表
    :return: IP地址 或 IP地址列表
    """
    if index is not None and not isinstance(index, int):
        raise TypeError("参数 index 必须为整数 或为 None")

    resl: list = socket.gethostbyname_ex(socket.gethostname())[-1]
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        st.connect(('10.255.255.255', 1))
        _ip = st.getsockname()[0]
        if _ip not in resl:
            resl.append(_ip)
    except Exception:
        if '127.0.0.1' not in resl:
            resl.insert(0, "127.0.0.1")
    finally:
        st.close()

    if index is None:
        return resl
    else:
        return resl[index]


class EnhancedHTTPRequestHandler(RH):
    @staticmethod
    def get_default_extensions_map():
        """
        返回提供文件的默认 MIME 类型映射
        """

        extensions_map = readini(os.path.join(os.path.dirname(__file__), "extensions_map.ini"))["default"]
        # 这里的路径问题就得这么写, 不能直接用相对路径, 不然经过多脚本接连调用后会报错
        # FileNotFoundError: [Errno 2] No such file or directory: 'extensions_map.ini'

        return extensions_map

    def __init__(self, *args, **kwargs):
        self.extensions_map = self.get_default_extensions_map()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        path = self.translate_path(self.path)
        if os.path.isfile(path):
            file_size = os.path.getsize(path)

            fpath, filename = os.path.split(path)
            basename, extension = os.path.splitext(filename)
            self.send_response(200)

            self.send_header("Content-Type", self.extensions_map.get(extension, "application/octet-stream") + "; charset=utf-8")

            # 设置Content-Disposition头，使得文件被下载
            self.send_header("Content-Disposition", f'attachment')
            self.send_header("Content-Length", str(file_size))

            self.end_headers()
            # 现在发送文件数据
            with open(path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            super().do_GET()


    def send_head(self):
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        # Add charset=UTF-8 for text files
        if ctype.startswith('text/'):
            ctype += '; charset=UTF-8'
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f

def Fileserver(path: str = ".", res: str = "", port: int = 5001,
                bool_https: bool = False, certfile="cert.pem", keyfile="privkey.pem"):
    """
    快速构建文件服务器，默认使用 HTTP

    :param path: 工作目录(共享目录路径)
    :param res: IP 默认为本地计算机的IP地址
    :param port: 端口 默认为5001
    :param bool_https: 是否启用HTTPS，默认为False
    :param certfile: SSL证书文件路径，默认同目录下的cert.pem
    :param keyfile: SSL私钥文件路径，默认同目录下的privkey.pem
    :return: None
    """
    if not res:
        res = getip(-1)

    if bool_https:
        httpd = HTTPServer((res, port), EnhancedHTTPRequestHandler)
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile, keyfile)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        print(f"HTTPS running at https://{res}:{port}")
    else:
        httpd = TCPServer((res, port), EnhancedHTTPRequestHandler)
        print(f"HTTP running at http://{res}:{port}")

    os.chdir(path)  # 设置工作目录作为共享目录路径
    httpd.serve_forever()

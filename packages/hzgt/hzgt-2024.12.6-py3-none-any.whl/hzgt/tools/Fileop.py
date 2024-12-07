import os
import sys
import socket
import ssl
import html
import io
import base64
import urllib.parse
import http.client
from http.server import HTTPServer, SimpleHTTPRequestHandler as RH
from socketserver import TCPServer
from http import HTTPStatus
import urllib

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
        pass
    finally:
        st.close()

    if '127.0.0.1' not in resl:
            resl.insert(0, "127.0.0.1")

    if '0.0.0.0' not in resl:
            resl.insert(0, "0.0.0.0")

    if index is None:
        return resl
    else:
        return resl[index]

def _ul_li_css(_ico_base64):
    return f"""
    body {{
        background-color: #808080;
    }}
    
    .header-container {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 10%;
        background-color: #808080;
        display: flex;
        align-items: center;
    }}
    .fixed-title {{
        font-size: 20px;
        margin-left: 3%;
        display: inline-block;
        vertical-align: middle;
    }}
    :root {{
        --icon-size: 48px;
    }}
    #icon-div {{
        width: var(--icon-size);
        height: var(--icon-size);
        background-image: url('data:image/x - icon;base64,{_ico_base64}');
        /* background-size: cover;  调整背景图像大小以适应div */
        margin: 10px;
        margin-left: 3%;
        z-index: 2;
    }}

    ul.custom-list {{
        list-style: none;
        padding-left: 0;
    }}
    ul.custom-list li.folder::before {{
        content: "\\1F4C1"; /* Unicode 文件夹符号 */
        margin-right: 10px;
        color: blue;
        display: inline-flex;
    }}
    ul.custom-list li.file::before {{
        content: "\\1F4C4"; /* Unicode 文件符号 */
        margin-right: 10px;
        color: gray;
        display: inline-flex;
    }}

    li:hover {{
        color: #ff6900;
        background-color: #f0f000; /* 悬停时的背景色 */
        text-decoration: underline; /* 悬停时添加下划线 */
        
        animation: li_hover_animation 1s;
    }}
    @keyframes li_hover_animation {{
        from {{ background-color: #ffffff; }}
        to {{ background-color: #f0f000; }}
    }}
    
    li:active {{
        color: #0066cc;
        background-color: #c0c0c0;
    }}
    
    li {{
        flex: 1 0 auto;
        margin: 1%; /* 增加li元素之间的间距 */
        color: blue;
        background-color: #c0c0c0; /* 背景色 */
        border-style: dotted; /* 使用虚线边框，自适应长度 */
        border-color: gray;
        border-radius: 8px; /* 边框的圆角半径 */
        display: flex;
        cursor: pointer;
        z-index: 0;
    }}
    
    li a {{
        display: block;
        padding: 3px;
        text-decoration: none;
    }}
"""

def _ul_li_js():
    return """
    const ul = document.querySelector('ul');
    const items = document.querySelectorAll('li');
    const loadThreshold = 0.5; // 当元素进入视口50%时加载
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                observer.unobserve(entry.target);
            }
        });
    }, {
        root: null,
        rootMargin: '0px',
        threshold: loadThreshold
    });
    
    items.forEach((item) => {
        observer.observe(item);
    });
    
    const ulcl = document.querySelector('ul.custom-list');
    ulcl.addEventListener('click', function (event) {
        const target = event.target;
        let link;
        if (target.tagName === 'LI') {
            link = target.querySelector('a');
        } else if (target.tagName === 'A') {
            link = target;
        }
        if (link) {
            link.click();
        }
    });
    
    document.addEventListener('DOMContentLoaded', function () {
        const listItems = document.querySelectorAll('ul.custom-list li');
        listItems.forEach((item) => {
            const text = item.textContent.trim();
            if (text.endsWith('/')) {
                item.classList.add('folder');
            } else {
                item.classList.add('file');
            }
        });
    });
    
    document.addEventListener('DOMContentLoaded', function () {
        const h1Element = document.querySelector('div.header-container');
        const h1Height = h1Element.offsetHeight;
        const ulElement = document.querySelector('ul.custom-list');
        ulElement.style.marginTop = `${h1Height + 20}px`;
    });
    """

def _list2ul_li(titlepath: str, _path: str, pathlist: list):
    """
    将列表转换为lu的li样式
    :return:
    """
    _r = []
    parts = titlepath.split('/')
    result = []
    current_path = ''
    for part in parts:  # 处理标题样式
        if part:
            current_path += '/' + part
            link = f"<a href='{current_path}' style='color: #40E0D0;'>{part}</a>"
            result.append(link)

    common_part = "<a href='/' style='color: #40E0D0;'>...</a>/"
    if result:
        end_title = common_part + '/'.join(result) + "/"
    else:
        end_title = common_part

    for name in pathlist:  # 处理文件夹和文件li
        fullname = os.path.join(_path, name)
        displayname = linkname = name
        if os.path.isdir(fullname):
            displayname = name + '/'
            linkname = name + '/'
        if os.path.islink(fullname):
            displayname = name + "@"
        _r.append("<li><a href='%s' style='color: #000080;'>%s</a></li>"
                % (urllib.parse.quote(linkname,
                                      errors='surrogatepass'),
                   html.escape(displayname, quote=False)))
    return f"""
    <div class="header-container">
        <div id="icon-div"></div>
        <div class="fixed-title">
            HZGT 文件服务器<br/>当前路径: {end_title}
        </div>
    </div>""", _r

def _convert_favicon_to_base64():
    with open(os.path.join(os.path.dirname(__file__), 'favicon.ico'), 'rb') as f:
        data = f.read()
        b64_data = base64.b64encode(data).decode('utf-8')
    return b64_data


class EnhancedHTTPRequestHandler(RH):
    @staticmethod
    def get_default_extensions_map():
        """
        返回提供文件的默认 MIME 类型映射
        """

        extensions_map = readini(os.path.join(os.path.dirname(__file__), "extensions_map.ini"))["default"]
        # 不能直接用相对路径, 不然经过多脚本接连调用后会报错
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
        if ctype.startswith('text/'):
            ctype += '; charset=UTF-8'
        try:
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

    def list_directory(self, path):
        try:
            _list = os.listdir(path)
        except OSError:
            self.send_error(
                HTTPStatus.NOT_FOUND,
                "没有列出目录的权限")
            return None
        _list.sort(key=lambda a: a.lower())
        r = []
        try:
            displaypath = urllib.parse.unquote(self.path, errors='surrogatepass')
        except UnicodeDecodeError:
            displaypath = urllib.parse.unquote(path)
        displaypath = html.escape(displaypath, quote=False)
        enc = sys.getfilesystemencoding()

        ico_base64 = _convert_favicon_to_base64()
        title, li_list = _list2ul_li(displaypath, path, _list)  # 显示在浏览器窗口

        r.append('<!DOCTYPE HTML>')
        r.append('<html lang="zh">')
        r.append('<head>')
        r.append(f'<meta charset="{enc}">\n<title>HZGT 文件服务器 {displaypath}</title>\n')  # 显示在浏览器标题栏
        r.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        r.append(f'''<link rel="icon" href="data:image/x-icon;base64,{ico_base64}" type="image/x-icon">''')
        r.append('<style>')
        r.append(_ul_li_css(ico_base64))
        r.append('</style>')

        r.append(f'</head>')
        r.append(f'<body>\n')

        r.append(title)  # 标题
        r.append('<hr>\n<ul class="custom-list">')
        for _li in li_list:
            r.append(_li)
        r.append('</ul>\n<hr>\n')

        r.append("<script>")
        r.append(_ul_li_js())
        r.append("</script>")

        r.append('</body>\n</html>\n')
        encoded = '\n'.join(r).encode(enc, 'surrogateescape')

        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f

def Fileserver(path: str = ".", host: str = "", port: int = 5001,
                bool_https: bool = False, certfile="cert.pem", keyfile="privkey.pem"):
    """
    快速构建文件服务器. 阻塞进程. 默认使用 HTTP

    :param path: 工作目录(共享目录路径)
    :param host: IP 默认为本地计算机的IP地址
    :param port: 端口 默认为5001
    :param bool_https: 是否启用HTTPS. 默认为False
    :param certfile: SSL证书文件路径. 默认同目录下的 cert.pem
    :param keyfile: SSL私钥文件路径. 默认同目录下的 privkey.pem
    :return: None
    """
    if not host:
        host = getip(-1)

    if bool_https:
        httpd = HTTPServer((host, port), EnhancedHTTPRequestHandler)
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile, keyfile)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        print(f"HTTPS running at https://{host}:{port}")
    else:
        httpd = TCPServer((host, port), EnhancedHTTPRequestHandler)
        print(f"HTTP running at http://{host}:{port}")

    os.chdir(path)  # 设置工作目录作为共享目录路径
    httpd.serve_forever()


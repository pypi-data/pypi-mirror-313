# 以下内容为 ini-parser 库[版本 1.2.1 / MIT许可]的内容
# The following is the content of the library called ini-parser [version 1.2.1 / MIT License].
# 详细内容可见: https://pypi.org/project/ini-parser/
# Details are available here: https://pypi.org/project/ini-parser/

# ===================================================== ini-parser =====================================================
import json
import os
import re


def _parse_value(value):
    if isinstance(value, int) or value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
        return int(value)

    if re.match(r'^\d*\.\d+$', value):
        return float(value)

    return value


def encode(obj, opt=None):
    children = []
    out = ''

    if isinstance(opt, str):
        opt = {
            'section': opt,
            'whitespace': True
        }
    else:
        opt = opt or {}
        opt['whitespace'] = opt.get('whitespace', True)

    separator = ' = ' if opt['whitespace'] else '='

    for k, v in obj.items():
        if v and isinstance(v, list):
            for item in v:
                out += safe(k + '[]') + separator + safe(item) + '\n'
        elif v and isinstance(v, dict):
            children.append(k)
        else:
            out += safe(k) + separator + safe(v) + '\n'

    if opt.get('section') and len(out):
        out = '[' + safe(opt['section']) + ']' + '\n' + out

    for k in children:
        nk = '.'.join(_dot_split(k))
        section = (opt['section'] + '.' if opt.get('section') else '') + nk
        child = encode(obj[k], {
            'section': section,
            'whitespace': opt['whitespace']
        })
        if len(out) and len(child):
            out += '\n'
        out += child

    return out


def _dot_split(string):
    return re.sub(r'\\\.', '\u0001', string).split('.')


EMPTY_KEY_SENTINEL = object()


def decode(string, on_empty_key=EMPTY_KEY_SENTINEL):
    out = {}
    p = out
    section = None
    regex = re.compile(r'^\[([^\]]*)\]$|^([^=]+)(=(.*))?$', re.IGNORECASE)
    lines = re.split(r'[\r\n]+', string)

    for line in lines:
        if not line or re.match(r'^\s*[;#]', line):
            continue
        match = regex.match(line)
        if not match:
            continue
        if match[1]:
            section = unsafe(match[1])
            p = out[section] = out.get(section, {})
            continue
        key = unsafe(match[2])
        if match[3]:
            if match[4].strip():
                value = _parse_value(unsafe(match[4]))
            elif on_empty_key is EMPTY_KEY_SENTINEL:
                raise ValueError(key)
            else:
                value = on_empty_key
        else:
            value = True
        if value in ('true', 'True'):
            value = True
        elif value in ('false', 'False'):
            value = False
        elif value in ('null', 'None'):
            value = None

        # Convert keys with '[]' suffix to an array
        if len(key) > 2 and key[-2:] == '[]':
            key = key[:-2]
            if key not in p:
                p[key] = []
            elif not isinstance(p[key], list):
                p[key] = [p[key]]

        # safeguard against resetting a previously defined
        # array by accidentally forgetting the brackets
        if isinstance(p.get(key), list):
            p[key].append(value)
        else:
            p[key] = value

    # {a:{y:1},"a.b":{x:2}} --> {a:{y:1,b:{x:2}}}
    # use a filter to return the keys that have to be deleted.
    _out = dict(out)
    for k in _out.keys():
        if not out[k] or not isinstance(out[k], dict) or isinstance(out[k], list):
            continue
        # see if the parent section is also an object.
        # if so, add it to that, and mark this one for deletion
        parts = _dot_split(k)
        p = out
        l = parts.pop()
        nl = re.sub(r'\\\.', '.', l)
        for part in parts:
            if part not in p or not isinstance(p[part], dict):
                p[part] = {}
            p = p[part]
        if p == out and nl == l:
            continue
        p[nl] = out[k]
        del out[k]

    return out


def _is_quoted(val):
    return (val[0] == '"' and val[-1] == '"') or (val[0] == "'" and val[-1] == "'")


def safe(val):
    return json.dumps(val) if \
        (not isinstance(val, str) or
         re.match(r'[=\r\n]', val) or
         re.match(r'^\[', val) or
         (len(val) > 1 and _is_quoted(val)) or
         val != val.strip()) else \
        val.replace(';', '\\;').replace('#', '\\#')


def unsafe(val):
    val = (val or '').strip()
    if _is_quoted(val):
        # remove the single quotes before calling JSON.parse
        if val[0] == "'":
            val = val[1:-1]
        try:
            val = json.loads(val)
        except:
            pass
    else:
        # walk the val to find the first not-escaped ; character
        esc = False
        unesc = ''
        for i in range(len(val)):
            c = val[i]
            if esc:
                if c in '\\;#':
                    unesc += c
                else:
                    unesc += '\\' + c
                esc = False
            elif c in ';#':
                break
            elif c == '\\':
                esc = True
            else:
                unesc += c
        if esc:
            unesc += '\\'
        return unesc.strip()
    return val


parse = decode
stringify = encode


# 以上内容为 ini-parser 库[版本 1.2.1 / MIT许可]的内容
# The above is the content of the library called ini-parser [version 1.2.1 / MIT License].
# ===================================================== ini-parser =====================================================
def readini(inifile: str) -> dict:
    """
    读取 ini 文件 返回字典
    :param inifile: ini 文件路径
    :return: dict ini 对应嵌套字典
    """
    return parse(open(inifile).read())


def saveini(savename: str, iniconfig: dict, section_prefix: str = "", bool_space: bool = True) -> None:
    """
    保存嵌套字典为ini文件
    :param savename: 保存文件名 可不包含后缀名 .ini
    :param iniconfig: 嵌套字典
    :param section_prefix: ini文件的 section 部分前缀 默认为空[即不添加前缀]
    :param bool_space: 等号前后是否添加空格 默认为 True[即默认添加空格]
    :return:
    """
    file_name, extension = os.path.splitext(savename)
    if ".ini" != extension:
        savename = savename + ".ini"

    with open(savename, "w+") as fp:
        fp.write(stringify(iniconfig,
                      {"section": section_prefix,  # 各项前缀
                            "whitespace": bool_space  # 等号两边是否添加空格
                            }))

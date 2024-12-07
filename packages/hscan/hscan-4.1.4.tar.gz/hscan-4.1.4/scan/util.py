import datetime
import hashlib


def get_local_ip():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        pass
    finally:
        s.close()
    return ip


def get_local_name():
    import socket
    return socket.gethostname()


def encrypt(char, method='md5'):
    """
    支持md5和sha1加密方式
    :param char:
    :param method:
    :return:
    """
    char = str(char)
    if method == 'md5':
        m = hashlib.md5()
    elif method == 'sha1':
        m = hashlib.sha1()
    m.update(char.encode('utf8'))
    return m.hexdigest()


def date_to_char(type='s'):
    """
    当前时间转成年月日时分秒形式
    :return:
    """
    if type == 's':
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    elif type == 'm':
        return datetime.datetime.now().strftime('%Y%m%d%H%M')
    elif type == 'd':
        return datetime.datetime.now().strftime('%Y%m%d')


def js_str_to_json(input_str):
    import execjs
    import json
    js_code = """
    function convertToJson(inputString) {
        var jsonObject = eval('(' + inputString + ')');
        var jsonString = JSON.stringify(jsonObject);
        return jsonString;
    }
    """
    ctx = execjs.compile(js_code)
    try:
        output_json_string = ctx.call("convertToJson", input_str)
        data = json.loads(output_json_string)
        return data
    except Exception:
        return

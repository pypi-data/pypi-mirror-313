from yplib.index import *
from bs4 import BeautifulSoup
import requests


# from requests.packages.urllib3.exceptions import InsecureRequestWarning


# 有关 http 的工具类

# 解析 html 中的数据
# file_path :   html 文件的路径
# html_data :   html 数据
# selector  :   选择器
def do_parser(file_path=None, html_data='', selector=None):
    if file_path is not None:
        html_str = ''.join(to_list(file_path))
    else:
        if isinstance(html_data, list):
            html_str = ''.join(html_data)
        else:
            html_str = str(html_data)
    return BeautifulSoup(html_str, 'html.parser').select(selector)


# div_list_content = do_parser(r'D:\notepad_file\202306\asfdf.html', selector='table.reference')[4].select('tr')
#
# for i in range(len(div_list_content) - 1):
#     td = div_list_content[i + 1].select('td')
#     num = td[0].text
#     fun_name = td[1].select('a')[0].text
#     fun_desc = td[1].text.replace(fun_name, '')
#     print(f'{num} : {fun_name} , {fun_desc}')


# get 类型的请求
# session : session , 默认 : requests.session()
# headers : headers
# cookie  : cookie
# auth    : auth
# verify  : verify
# r_json : 返回的数据是否是一个 json 类型的数据
def do_get_response(url=None,
                    session=None,
                    headers=None,
                    cookie=None,
                    auth=None,
                    timeout=1000,
                    verify=False):
    if session is None:
        session = requests.session()
    requests.packages.urllib3.disable_warnings()
    return session.get(url=url, headers=headers, auth=auth, timeout=timeout, verify=verify, cookies=cookie)


def do_get(url=None,
           session=None,
           headers=None,
           cookie=None,
           auth=None,
           timeout=1000,
           verify=False,
           r_json=False):
    response = do_get_response(url=url, session=session, headers=headers, cookie=cookie, auth=auth, timeout=timeout, verify=verify)
    response.encoding = 'utf-8'
    return json.loads(response.text.strip()) if r_json else response.text.strip()


# 返回的是一个 json 数据
def do_get_json(url=None,
                session=None,
                headers=None,
                cookie=None,
                auth=None,
                timeout=1000,
                verify=False):
    return do_get(url=url, session=session, headers=headers, cookie=cookie, auth=auth, timeout=timeout, verify=verify,
                  r_json=True)


# 下载
# file_name   : 文件名 , 默认 txt
#               当文件名是 C:\Users\yangpu\Desktop\study\abc\d\e\f\a.txt 这种类型的时候, 可以直接创建文件夹,
#                   会赋值 file_path=C:\Users\yangpu\Desktop\study\abc\d\e\f,
#                         file_name=a.txt,
#                         fixed_name=True
#               当文件名是 abc 的时候, 按照正常值,计算
# file_path   : 文件路径
def do_download(url=None,
                file_name=None,
                file_path='download',
                session=None,
                headers=None,
                cookie=None,
                auth=None,
                timeout=1000,
                verify=False):
    if session is None:
        session = requests.session()
    requests.packages.urllib3.disable_warnings()
    response = session.get(url=url, headers=headers, auth=auth, timeout=timeout, verify=verify, cookies=cookie)
    if response.status_code != 200:
        to_log_file('error', url, response.status_code)
        return
    # 默认的文件路径,
    file_name = url[url.rfind('/') + 1: len(url)] if file_name is None else file_name
    if file_name is not None:
        file_name = str(file_name)
        for sep in ['\\', '/']:
            # C:\Users\yangpu\Desktop\study\abc\d\e\f\a.txt
            f_n = file_name.split(sep)
            if len(f_n) > 1:
                # a.txt
                file_name = f_n[-1]
                # C:\Users\yangpu\Desktop\study\abc\d\e\f
                file_path = sep.join(f_n[0:-1])
    # 检查路径 file_path
    while file_path.endswith('/'):
        file_path = file_path[0:-1]
    check_file(file_path)
    # 去掉文件名称中的非法字符
    file_name = re.sub('[^a-zA-Z0-9._]', '', file_name)
    path_name = file_path + '/' + file_name
    # 重复下载的删掉以前的
    if os.path.exists(path_name):
        os.remove(path_name)
    # 下载的文件
    with open(path_name, 'wb') as f:
        f.write(response.content)
    # 返回全路径名称, 文件名, 路径名
    return path_name, file_name, file_path


# print(do_download('https://www.runoob.com/?s=sorted', r'C:\Users\yangpu\Desktop\study\abc\d\e\f\a.txt'))
# print(do_get('https://www.runoob.com/?s=sorted'))
# print(do_get('http://10.6.180.156:18000/login/need'))
# print(do_get('http://10.6.180.156:18000/login/need', r_json=True))


# get 类型的请求
# data         : data post 体中的数据
# is_form_data : 是否是 form 表单
# headers : headers
# cookie  : cookie
# auth    : auth
# verify  : verify
# r_json : 返回的数据是否是一个 json 类型的数据
def do_post_response(url=None,
                     data=None,
                     is_form_data=False,
                     session=None,
                     headers=None,
                     cookie=None,
                     auth=None,
                     timeout=1000,
                     verify=False):
    # headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # data = {}
    # data['appkey'] = APP_KEY
    # data['secretkey'] = SECRET_KEY
    # data['content'] = content
    # data['phone'] = obtainMobileIndonesia(mobile)
    # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    # response = requests.post(URL, headers=headers, verify=False, data=data)
    # response.encoding = 'utf-8'
    # text = response.text
    # text = text.replace('\n', '')
    # text = text.replace('\r', '')
    # return text
    if session is None:
        session = requests.session()
    requests.packages.urllib3.disable_warnings()
    d = data if is_form_data else json.dumps(data)
    headers = {} if headers is None else headers
    content_type = headers['Content-Type'] if 'Content-Type' in headers else 'application/json;charset=UTF-8'
    if 'Content-Type' not in headers and is_form_data:
        content_type = 'application/x-www-form-urlencoded'
    headers['Content-Type'] = content_type
    return session.post(url=url, data=d, headers=headers, auth=auth, timeout=timeout, verify=verify, cookies=cookie)


def do_post(url=None,
            data=None,
            is_form_data=False,
            session=None,
            headers=None,
            cookie=None,
            auth=None,
            timeout=1000,
            verify=False,
            r_json=False):
    response = do_post_response(url=url, data=data, is_form_data=is_form_data, session=session, headers=headers, cookie=cookie, auth=auth, timeout=timeout,
                                verify=verify)
    response.encoding = 'utf-8'
    return json.loads(response.text.strip()) if r_json else response.text.strip()

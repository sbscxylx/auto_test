from common.Request import RequestsHandler
from common.Retrun_Response import dict_style
from common.Csv_User import user_data
from Conf.conf import *
from common import Assert
from conftest import apptype, version, STRESS_LIST, RESULT_LIST
from common.Logs import Log
import datetime, sys, os, requests, json, base64, ast



file = os.path.basename(sys.argv[0])
print(file)
log = Log(file)
logger = log.Logger

def_name = sys._getframe().f_code.co_name
test_Assert = Assert.Assertions(def_name)
logger.info('开始执行脚本%s:\n', def_name)

# 初始headers参数
headers = {'applicationType': apptype, 'version': version,
               'timestamp': str(datetime.datetime.now().timestamp()), 'uid': '', 'token': ''}


# 第三方解析图形验证码
class Get_code:
    # 解析图形验证码接口
    def image_to_code():
        '''解析图形验证码接口'''
        # 首先将图片读入
        # 由于要发送json，所以需要对byte进行str解码
        with open('./tuxing_code/code.png', 'rb') as f:
            img_byte = base64.b64encode(f.read())
        img_str = img_byte.decode('ascii')
        # 接入第三方平台
        url = 'http://api.ttshitu.com/base64'
        data = {'username': 'xiaoxinxing', 'password': 'abc09292752', 'typeid': '1', 'image': img_str}
        response = requests.post(url=url, data=data)
        # 转换成python可以识别的json格式
        str_result = response.json()
        return str_result

    # 解析图形验证报错接口
    def image_to_code_err(id):
        '''图形验证码解析失败接口'''
        data = {'id': id}
        result = requests.post('http://api.ttshitu.com/reporterror.json', json=data).json()
        if result['success']:
            return '报错成功'
        else:
            return result['message']


# 数据加解密
class Rsa:
    # 加密数据接口
    def encrypt(json_data):
        '''加密数据接口'''
        url = server_ip('test') + '/app/v2/CommonController/get_encryt_data'
        data = {'data': json_data}
        res = RequestsHandler.vist_Req(method='post', url=url, params='', data=data, json='', headers=headers)
        is_json, res = dict_style(res)
        # 获取加密数据
        encrypt_data = res['data']
        return encrypt_data

    # 解密数据接口
    def decrypt(res_data):
        '''解密数据接口'''
        is_encrypt = res_data['encrption']
        if str(is_encrypt) == '1':
            url = server_ip('test') + '/app/v2/CommonController/get_decrypt_data'
            data = {'data': res_data['data']}
            decrypt_data = RequestsHandler.vist_Req(method='post', url=url, params='', data=data, json='',
                                                     headers=headers)
            is_json, decrypt_data = dict_style(decrypt_data)
            return decrypt_data
        else:
            return res_data


''' 获取图形验证码 '''
class Tuxing_code:
    def tuxing_code():
        method = user_data[0][0]
        url = server_ip('test') + user_data[0][1]
        params = {'data': Rsa.encrypt(user_data[0][2])}
        data = user_data[0][3]
        json = user_data[0][4]
        res = RequestsHandler.vist_Req(method=method, url=url, params=params, data=data, json=json, headers=headers)
        response_time = res.elapsed.total_seconds()
        logger.info('响应时间：' + str(response_time))
        is_time = test_Assert.assert_time(response_time, float(user_data[0][7]))
        if is_time:
            STRESS_LIST.append('pass')
        else:
            logger.error("请求超时")
        is_json, res = dict_style(res)
        if not is_json:
            RESULT_LIST.append('pass')
            logger.error('不是json格式的数据')
        else:
            logger.info('json数据')
        with open('./tuxing_code/code.png', 'wb') as f:
            # 对于图片类型的通过r.content方式访问响应内容，将响应内容写入code.png中
            f.write(res.content)
        # 解析图形验证码
        code_result = Get_code.image_to_code()
        if code_result['success']:
            return code_result
        else:
            logger.error(code_result['message'])


# 登录
method = user_data[1][0]
url = server_ip('test') + user_data[1][1]
params = {'data': Rsa.encrypt(user_data[1][2])}
while True:
    # 替换图形验证码
    new_data = ast.literal_eval(user_data[1][3])  # 转换字典形式
    code_result = Tuxing_code.tuxing_code()
    new_data['imageCode'] = code_result['data']['result']
    new_data = str(new_data)  # 转换字符串形式
    new_data = new_data.replace("'", '"')  # 数据格式为双引号
    data = {'data': Rsa.encrypt(new_data)}
    json = user_data[1][4]
    res = RequestsHandler.vist_Req(method=method, url=url, params=params, data=data, json=json, headers=headers)
    response_time = res.elapsed.total_seconds()
    logger.info('响应时间：' + str(response_time))
    is_time = test_Assert.assert_time(response_time, float(user_data[1][7]))
    if is_time:
        STRESS_LIST.append('pass')
    else:
        logger.error('请求超时')
    is_json, res = dict_style(res)
    if not is_json:
        logger.error('不是json格式的数据')
    else:
        is_success1 = test_Assert.assert_code(str(res['code']), user_data[1][5])
        if is_success1:
            decrypt_data = Rsa.decrypt(res)
            is_success2 = test_Assert.assert_body(decrypt_data['data']['obj'], 'uid', user_data[1][6])
            if is_success2:
                RESULT_LIST.append('pass')
                uid = decrypt_data['data']['obj']['uid']  # 设置uid
                token = decrypt_data['data']['obj']['token']  # 设置token
                break
            else:
                logger.error('data error!')
                break
        elif res['message'] == '图形验证码错误':
            result_code_err = Get_code.image_to_code_err(id=code_result['data']['id'])
            logger.info(result_code_err)
        else:
            logger.error('api error!')
            break


# headers参数
def header():
    headers = {'applicationType': apptype, 'version': version,
               'timestamp': str(datetime.datetime.now().timestamp()), 'uid': uid,
               'token': token}
    return headers


# 获取用户信息
method = user_data[2][0]
url = server_ip('test') + user_data[2][1] + uid
params = {'data': Rsa.encrypt(user_data[1][2])}
data = {'data': Rsa.encrypt(user_data[2][3])}
json = user_data[2][4]
res = RequestsHandler.vist_Req(method=method, url=url, params=params, data=data, json=json, headers=header())
response_time = res.elapsed.total_seconds()
logger.info('响应时间：' + str(response_time))
is_time = test_Assert.assert_time(response_time, float(user_data[2][7]))
if is_time:
    STRESS_LIST.append('pass')
else:
    logger.error('请求超时')
is_json, res = dict_style(res)
if not is_json:
    logger.error('不是json格式的数据')
else:
    is_success1 = test_Assert.assert_code(str(res['code']), user_data[2][5])
    if is_success1:
        decrypt_data = Rsa.decrypt(res)
        is_success2 = test_Assert.assert_body(decrypt_data['data']['obj'], 'id', user_data[2][6])
        if is_success2:
            RESULT_LIST.append('pass')
            user_info = decrypt_data['data']['obj']  # 设置user_info
        else:
            logger.error('data error!')
    else:
        logger.error('api error!')





# print(RESULT_LIST)
# print(STRESS_LIST)










from common.Request import RequestsHandler
from common.Retrun_Response import dict_style
from common.Csv_Perpetual_Contract import perpetual_contract_apis
from Conf.conf import *
from common import Assert
from conftest import STRESS_LIST, RESULT_LIST
from common import User_info
from common.Logs import Log
import datetime, sys, os, requests, json, base64, ast, pytest


file = os.path.basename(sys.argv[0])
print(file)
log = Log(file)
logger = log.Logger

def_name = sys._getframe().f_code.co_name
test_Assert = Assert.Assertions(def_name)
logger.info('开始执行脚本%s:\n', def_name)


''' api请求体 '''
class Api:
    def api_response(self, i, params, data):
        result = False
        method = perpetual_contract_apis[i][0]
        url = server_ip('test') + perpetual_contract_apis[i][1]
        json = perpetual_contract_apis[i][4]
        res = RequestsHandler.vist_Req(
            method=method, url=url, params=params, data=data, json=json, headers=User_info.header())
        response_time = res.elapsed.total_seconds()
        logger.info('响应时间：' + str(response_time))
        is_time = test_Assert.assert_time(response_time, float(perpetual_contract_apis[i][7]))
        if is_time:
            STRESS_LIST.append('pass')
        else:
            logger.error('请求超时')
        is_json, res = dict_style(res)
        if not is_json:
            logger.error('不是json格式的数据')
        else:
            is_success1 = test_Assert.assert_code(str(res['code']), perpetual_contract_apis[i][5])
            is_success2 = test_Assert.assert_body(res, 'message', perpetual_contract_apis[i][6])
            if is_success1 and is_success2:
                RESULT_LIST.append('pass')
                decrypt_data = User_info.Rsa.decrypt(res)
                result = True
            else:
                logger.error('data error!')
        return result, decrypt_data


# 永续合约api测试
class Test_perpetual_contract:
    def test_notices(self):
        '''获取公告和永续合约开关'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[0][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[0][3])}
        result, decrypt_data = Api.api_response(self, 0, params, data)
        assert result

    @pytest.mark.xfail(reason="预期失败")
    def test_create_account(self):
        '''创建币安子账户'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[1][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[1][3])}
        result, decrypt_data = Api.api_response(self, 1, params, data)
        assert result

    @pytest.mark.skip(reason="跳过执行这条case")
    def test_transfer(self):
        '''永续划转交易'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[2][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[2][3])}
        result, decrypt_data = Api.api_response(self, 2, params, data)
        assert result

    def test_transfer_records(self):
        '''划转记录'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[3][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[3][3])}
        result, decrypt_data = Api.api_response(self, 3, params, data)
        assert result

    def test_get_index_price(self):
        '''获取行情'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[4][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[4][3])}
        result, decrypt_data = Api.api_response(self, 4, params, data)
        assert result

    def test_add_favorite_trading_pair(self):
        '''添加自选'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[5][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[5][3])}
        result, decrypt_data = Api.api_response(self, 5, params, data)
        assert result

    def test_delete_favorite_trading_pair(self):
        '''删除自选'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[6][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[6][3])}
        result, decrypt_data = Api.api_response(self, 6, params, data)
        assert result

    def test_get_favorite_trading_pair(self):
        '''获取自选交易对'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[7][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[7][3])}
        result, decrypt_data = Api.api_response(self, 7, params, data)
        assert result

    def test_get_user_wallet(self):
        '''获取用户资产'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[8][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[8][3])}
        result, decrypt_data = Api.api_response(self, 8, params, data)
        assert result

    def test_set_leverage(self):
        '''设置杠杆率'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[9][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[9][3])}
        result, decrypt_data = Api.api_response(self, 9, params, data)
        assert result

    def test_get_leverage(self):
        '''获取杠杆率'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[10][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[10][3])}
        result, decrypt_data = Api.api_response(self, 10, params, data)
        assert result

    def test_add_order(self):
        '''下单'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[11][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[11][3])}
        result, decrypt_data = Api.api_response(self, 11, params, data)
        assert result

    def test_get_current_open(self):
        '''获取当前挂单'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[12][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[12][3])}
        result, decrypt_data = Api.api_response(self, 12, params, data)
        assert result

    def test_cancel_order(self):
        '''撤单'''
        # 获取当前挂单的ID
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[12][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[12][3])}
        result, decrypt_data = Api.api_response(self, 12, params, data)
        id = decrypt_data['data']['list'][0]['clientOrderId']
        # 撤单最新的一条挂单
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[13][2])}
        data_dict = ast.literal_eval(perpetual_contract_apis[13][3])  # 转换字典形式
        data_dict['id'] = id
        new_data = str(data_dict)  # 转换字符串形式
        new_data = new_data.replace("'", '"')  # 数据格式为双引号
        data = {'data': User_info.Rsa.encrypt(new_data)}
        result, decrypt_data = Api.api_response(self, 13, params, data)
        assert result

    def test_get_order_list(self):
        '''获取订单列表'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[14][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[14][3])}
        result, decrypt_data = Api.api_response(self, 14, params, data)
        assert result

    def test_get_order_detail(self):
        '''获取订单详情'''
        # 获取订单列表的第一条ID
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[14][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[14][3])}
        result, decrypt_data = Api.api_response(self, 14, params, data)
        id = decrypt_data['data']['list'][0]['clientOrderId']
        # 获取最新的一条订单详情
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[15][2])}
        data_dict = ast.literal_eval(perpetual_contract_apis[15][3])  # 转换字典形式
        data_dict['id'] = id
        new_data = str(data_dict)  # 转换字符串形式
        new_data = new_data.replace("'", '"')  # 数据格式为双引号
        data = {'data': User_info.Rsa.encrypt(new_data)}
        result, decrypt_data = Api.api_response(self, 15, params, data)
        assert result

    def test_get_trade_list(self):
        '''获取订单分笔成交明细'''
        # 获取订单列表的第一条已成交的ID
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[14][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[14][3])}
        result, decrypt_data = Api.api_response(self, 14, params, data)
        i = len(decrypt_data['data']['list'])
        for a in range(i):
            if decrypt_data['data']['list'][a]['status'] == 'FILLED':
                id = decrypt_data['data']['list'][a]['clientOrderId']
            else:
                continue
        # 获取最新的一条成交订单的成交明细
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[16][2])}
        data_dict = ast.literal_eval(perpetual_contract_apis[16][3])  # 转换字典形式
        data_dict['id'] = id
        new_data = str(data_dict)  # 转换字符串形式
        new_data = new_data.replace("'", '"')  # 数据格式为双引号
        data = {'data': User_info.Rsa.encrypt(new_data)}
        result, decrypt_data = Api.api_response(self, 16, params, data)
        assert result

    def test_get_account_info(self):
        '''获取账户信息'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[17][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[17][3])}
        result, decrypt_data = Api.api_response(self, 17, params, data)
        assert result

    def test_coins_transfer_info(self):
        '''获取币种划转信息'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[18][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[18][3])}
        result, decrypt_data = Api.api_response(self, 18, params, data)
        assert result

    def test_get_listenkey(self):
        '''获取listen key'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[19][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[19][3])}
        result, decrypt_data = Api.api_response(self, 19, params, data)
        assert result

    def test_keep_listenkey(self):
        '''延长listen key'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[20][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[20][3])}
        result, decrypt_data = Api.api_response(self, 20, params, data)
        assert result

    def test_close_listenkey(self):
        '''关闭listen key'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[21][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[21][3])}
        result, decrypt_data = Api.api_response(self, 21, params, data)
        assert result

    def test_get_market_depth(self):
        '''获取实时行情'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[22][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[22][3])}
        result, decrypt_data = Api.api_response(self, 22, params, data)
        assert result

    def test_get_lastprice(self):
        '''获取当前交易对最新价'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[23][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[23][3])}
        result, decrypt_data = Api.api_response(self, 23, params, data)
        assert result

    def test_get_fundingfee_list(self):
        '''获取资金费历史'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[24][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[24][3])}
        result, decrypt_data = Api.api_response(self, 24, params, data)
        assert result

    def test_get_account_risk(self):
        '''获取当前持仓及风险'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[25][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[25][3])}
        result, decrypt_data = Api.api_response(self, 25, params, data)
        assert result

    def test_calc_order(self):
        '''计算最大可开仓数量'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[26][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[26][3])}
        result, decrypt_data = Api.api_response(self, 26, params, data)
        assert result

    def test_margin_order(self):
        '''计算开仓所需保证金'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[27][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[27][3])}
        result, decrypt_data = Api.api_response(self, 27, params, data)
        assert result

    def test_leverage_max_value(self):
        '''获取最大名义价值'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[28][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[28][3])}
        result, decrypt_data = Api.api_response(self, 28, params, data)
        assert result

    def test_get_trade_listall(self):
        '''获取分笔成交历史'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[29][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[29][3])}
        result, decrypt_data = Api.api_response(self, 29, params, data)
        assert result

    def test_get_kline(self):
        '''获取K线'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[30][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[30][3])}
        result, decrypt_data = Api.api_response(self, 30, params, data)
        assert result

    def test_market_fundingrate_list(self):
        '''获取市场资金费率历史'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[31][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[31][3])}
        result, decrypt_data = Api.api_response(self, 31, params, data)
        assert result

    def test_get_max_leverage(self):
        '''获取最大可设置杠杆率'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[32][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[32][3])}
        result, decrypt_data = Api.api_response(self, 32, params, data)
        assert result

    def test_get_trade_his(self):
        '''获取最近市场成交'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[33][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[33][3])}
        result, decrypt_data = Api.api_response(self, 33, params, data)
        assert result

    def test_get_symbol_list(self):
        '''获取交易对列表'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[34][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[34][3])}
        result, decrypt_data = Api.api_response(self, 34, params, data)
        assert result

    def test_get_symbol_info(self):
        '''获取交易对详情'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[35][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[35][3])}
        result, decrypt_data = Api.api_response(self, 35, params, data)
        assert result

    def test_calc_order_max_close(self):
        '''计算最大可平仓数量'''
        params = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[36][2])}
        data = {'data': User_info.Rsa.encrypt(perpetual_contract_apis[36][3])}
        result, decrypt_data = Api.api_response(self, 36, params, data)
        assert result










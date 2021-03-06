import requests
import hashlib
from urllib.parse import urlencode,unquote


class VMQ:

    def __init__(self,payment='wechat'):
        from service.util.pay.pay_config import get_config
        if payment == 'wechat':
            config = get_config('V免签微信')
            self.v_type = 1
        else:
            config = get_config('V免签支付宝')
            self.v_type = 2
        self.key = config['KEY']   #填写通信密钥
        self.host_api = config['API']

    def create_order(self,name,out_trade_no,total_price):

        data = {
            'payId':out_trade_no,
            'type':self.v_type,
            'price':total_price,
            'param':name
        }        
        data['sign'] = hashlib.md5((data['payId']+str(data['param'])+str(data['type'])+str(data['price'])+self.key).encode('utf8')).hexdigest()

        r = requests.post(self.host_api+'/createOrder',json=data)
        # print(r.json())
        if r.status_code == 200:
            if r.json()['code'] == 1:
                # return r.json()['data']     # 包含payUrl,orderId
                res = r.json()['data']
                return {'qr_code':res['payUrl'],'payjs_order_id':res['orderId'],'reallyPrice':res['reallyPrice']}
        return False

    def check(self,orderId):     #这里是上一步主动生成的订单，单独调用
        data = {
            'orderId': orderId
        }
        r = requests.post(self.host_api+'/checkOrder',json=data)
        print(r.json())
        if r.status_code == 200:
            if r.json()['code'] == 1:
                return True
        return False
        
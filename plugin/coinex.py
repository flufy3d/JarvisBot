import time
import hashlib
import json as complex_json
import requests
import config

class RequestClient(object):
    __headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    }

    def __init__(self, headers={}):
        self.access_id = config.coinex_api_id
        self.secret_key = config.coinex_api_key
        self.headers = self.__headers
        self.headers.update(headers)

    @staticmethod
    def get_sign(params, secret_key):
        sort_params = sorted(params)
        data = []
        for item in sort_params:
            data.append(item + '=' + str(params[item]))
        str_params = "{0}&secret_key={1}".format('&'.join(data), secret_key)
        token = hashlib.md5(str.encode(str_params)).hexdigest().upper()
        return token

    def set_authorization(self, params):
        params['access_id'] = self.access_id
        params['tonce'] = int(time.time()*1000)
        self.headers['AUTHORIZATION'] = self.get_sign(params, self.secret_key)

    def request(self, method, url, params={}, data='', json={}):
        method = method.upper()
        if method == 'GET':
            self.set_authorization(params)
            result = requests.request('GET', url, params=params, headers=self.headers)
        else:
            if data:
                json.update(complex_json.loads(data))
            self.set_authorization(json)
            result = requests.request(method, url, json=json, headers=self.headers)
        return result



def balance():
    ret = 'Coinex Balance:\n'
    request_client = RequestClient()
    response = request_client.request('GET', 'https://api.coinex.com/v1/balance/')
 
    data = complex_json.loads(response.text)
    for i in data['data']:
        _available = float(data['data'][i]['available'])
        if _available != 0:
            _str = '%s %.4f\n' % (i.lower(),_available)
            ret += _str
        
    return ret

def ticker():
    ret = 'Coinex Ticker:\n'
    request_client = RequestClient()
    response = request_client.request('GET', 'https://api.coinex.com/v1/market/ticker?market=BTCBCH')
 
    data = complex_json.loads(response.text)

    bch_price = 1.0/float(data['data']['ticker']['last'])


    response = request_client.request('GET', 'https://api.coinex.com/v1/market/ticker?market=CETBCH')
 
    data = complex_json.loads(response.text)

    cet_price = float(data['data']['ticker']['last'])


    ret += 'bchbtc: %.4f\n' % (bch_price)
    ret += 'cetbch: %.8f\n' % (cet_price)

    return ret


def test_ticker():
    print(ticker())

def test_balance():
    print(balance())


    

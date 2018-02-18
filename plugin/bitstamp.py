import time
import base64
import hmac
#import urllib.request
#import urllib.parse
#import urllib.error
import hashlib
import sys
import json
import requests
import config

class PrivateBitstamp():
    balance_url = "https://www.bitstamp.net/api/v2/balance/"
    buy_url = "https://www.bitstamp.net/api/v2/buy/"
    sell_url = "https://www.bitstamp.net/api/v2/sell/"
    ticker_url = "https://www.bitstamp.net/api/v2/ticker/"

    def __init__(self):
        self.proxydict = None
        self.client_id = config.bitstamp_client_id
        self.api_key = config.bitstamp_api_key
        self.api_secret = config.bitstamp_api_secret    
        
    def _create_nonce(self):
        return int(time.time() * 1000000)

    def _send_request(self, url, params={}, extra_headers=None):
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        }
        if extra_headers is not None:
            for k, v in extra_headers.items():
                headers[k] = v
        nonce = str(self._create_nonce())
        message = nonce + self.client_id + self.api_key
        if sys.version_info.major == 2:
            signature = hmac.new(self.api_secret, msg=message, digestmod=hashlib.sha256).hexdigest().upper()
        else:
            signature = hmac.new(str.encode(self.api_secret), msg=str.encode(message), digestmod=hashlib.sha256).hexdigest().upper()
        params['key'] = self.api_key
        params['signature'] = signature
        params['nonce'] = nonce
        #postdata = urllib.parse.urlencode(params).encode("utf-8")
        #req = urllib.request.Request(url, postdata, headers=headers)
        #print ("req=", postdata)
        #response = urllib.request.urlopen(req)
        response = requests.post(url, data=params, proxies=self.proxydict)
        #code = response.getcode()
        code = response.status_code
        if code == 200:
            #jsonstr = response.read().decode('utf-8')
            #return json.loads(jsonstr)
            return response.json()
        return None

    def _buy(self, amount, price, pair):
        """Create a buy limit order"""
        params = {"amount": round(amount,8), "price": round(price,8)}
        response = self._send_request(self.buy_url + pair + '/', params)
        if "status" in response and "error" == response["status"]:
            raise TradeException(response["reason"])

    def _sell(self, amount, price, pair):
        """Create a sell limit order"""
        params = {"amount": round(amount,8), "price": round(price,8)}
        response = self._send_request(self.sell_url + pair + '/', params)
        if "status" in response and "error" == response["status"]:
            raise TradeException(response["reason"])

    def get_info(self):
        """Get balance"""
        response = self._send_request(self.balance_url)
        if "status" in response and "error" == response["status"]:
            raise GetInfoException(response["reason"])
            return

        #print(json.dumps(response)) 
        return response
    def get_ticker(self,pair):
        response = self._send_request(self.ticker_url + pair)
        if "status" in response and "error" == response["status"]:
            raise GetInfoException(response["reason"])
            return

        #print(json.dumps(response)) 
        return response    
  


def balance():
    ret = 'Bitstamp Balance:\n'
    _exchange = PrivateBitstamp()
    data  = _exchange.get_info()
    for i in data:
        if '_available' in i:
            _available = float(data[i])
            if _available != 0:
                _str = '%s %.4f\n' % (i.replace('_available', ''),_available)
                ret += _str
    return ret

def ticker():
    ret = 'Coinex Ticker:\n'
    _exchange = PrivateBitstamp()
    data = _exchange.get_ticker('btcusd')
    btcusd_price = float(data['last'])

    data = _exchange.get_ticker('bchbtc')
    bchbtc_price = float(data['last'])

    data = _exchange.get_ticker('eurusd')
    eurusd_price = float(data['last'])
    ret += 'btcusd: %.2f\n' % (btcusd_price)
    ret += 'bchbtc: %.4f\n' % (bchbtc_price)
    ret += 'eurusd: %.4f\n' % (eurusd_price)

    return ret


def test_ticker():
    print(ticker())

def test_balance():
    print(balance())
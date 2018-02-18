import config
import json
#from plugin.util.bitmex_websocket import BitMEXWebsocket
from plugin.util.bitmex_http import bitmex

def balance():
    ret = 'Bitmex Balance:\n'
    """
    ws = BitMEXWebsocket(endpoint="https://www.bitmex.com/api/v1", symbol="XBTM18",
                         api_key=config.bitmex_api_id, api_secret=config.bitmex_api_secret)

    print("Funds: %s" % ws.funds())

    ws.exit()
    """
    ret += 'Position: \n'
    client = bitmex(test=False, api_key=config.bitmex_api_id, api_secret=config.bitmex_api_secret)

    data = client.Position.Position_get(filter=json.dumps({'symbol': 'XBTUSD','symbol': 'XBTM18'})).result()
    for i in data[0]:
        ret += '    symbol:%s\n' % (i['symbol'])
        ret += '        currentQty:%d\n' % (i['currentQty'])
        ret += '        unrealisedPnl:%.4f\n' % (float(i['unrealisedPnl'])*0.00000001)
        ret += '        unrealisedRoePcnt:%.2f%%\n' % (float(i['unrealisedRoePcnt'])*100)
        ret += '        liquidationPrice:%.1f\n' % (i['liquidationPrice'])
        ret += '        lastPrice:%.1f\n' % (i['lastPrice'])
        

    ret += 'Fund: \n'
    data = client.User.User_getMargin(currency='XBt').result()
    ret += '    walletBalance: %.4f\n' % (float(data[0]['walletBalance'])*0.00000001)
    ret += '    withdrawableMargin: %.4f\n' % (float(data[0]['withdrawableMargin'])*0.00000001)
    ret += '    marginLeverage: %.2f\n' % (data[0]['marginLeverage'])
    return ret

def ticker():
    ret = 'Bitmex Ticker:\n'
    """
    ws = BitMEXWebsocket(endpoint="https://www.bitmex.com/api/v1", symbol="XBTUSD",
                         api_key=config.bitmex_api_id, api_secret=config.bitmex_api_secret)

    print("Instrument data: %s" % ws.get_instrument())
    print("Ticker: %s" % ws.get_ticker())

    ws.exit()
    """
    client = bitmex(test=False)
    #ret = client.Quote.Quote_get(symbol='XBTUSD',count=1,reverse=True).result()
    #print(ret)
    data = client.Instrument.Instrument_get(symbol='XBTUSD').result()
    ret += 'xbtusd: %.2f\n' % (float(data[0][0]['lastPrice']))
    ret += 'rate: %.4f%%\n' % (float(data[0][0]['fundingRate'])*100.0)
    ret += 'irate: %.4f%%\n' % (float(data[0][0]['indicativeFundingRate'])*100.0)
    _fundingTimestamp = data[0][0]['fundingTimestamp']
    _timestamp = data[0][0]['timestamp']
    rest_time = str(_fundingTimestamp - _timestamp).split('.', 2)[0]
    ret += 'countdown: %s' % (rest_time)

    return ret

def test_ticker():
    print(ticker())

def test_balance():
    print(balance())

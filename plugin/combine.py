import plugin
from plugin.util.unformat import unformat

def balance():
    ret = 'Combine Balance:\n'
    _bch_a=_bch_t=_btc_a=_btc_t=0

    _origin_str = plugin.bitstamp.balance()
    _format_str = '%s Balance:\n%s(a/t): %f %f\n%s(a/t): %f %f\n'
    _tuple = unformat(_format_str,_origin_str)
    _bch_a += _tuple[2]
    _bch_t += _tuple[3]

    _btc_a += _tuple[5]
    _btc_t += _tuple[6]

    _origin_str = plugin.coinex.balance()
    _format_str = '%s Balance:\n%s(a/t): %f %f\n%s(a/t): %f %f\n'
    _tuple = unformat(_format_str,_origin_str)
    _bch_a += _tuple[2]
    _bch_t += _tuple[3]

    _btc_a += _tuple[5]
    _btc_t += _tuple[6]

    ret += '%s(a/t): %.4f %.4f\n' % ('bch',_bch_a,_bch_t)
    ret += '%s(a/t): %.4f %.4f\n' % ('btc',_btc_a,_btc_t)

    return ret

def ticker():
    ret = ''
    _bitstamp = plugin.bitstamp.ticker()
    _coinex = plugin.coinex.ticker()
    _bitmex = plugin.bitmex.ticker()

    ret += _bitstamp
    ret += _coinex
    ret += _bitmex

    return ret

def test_balance():
    print(balance())
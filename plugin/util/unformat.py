import re

class conv(object):
    @staticmethod
    def int(s):
        return int(s)
    
    @staticmethod
    def oct(s):
        return int(s, base=8)
    
    @staticmethod
    def hex(s):
        return int(s, base=16)
    
    @staticmethod
    def float(s):
        return float(s)
    
    @staticmethod
    def str(s):
        return str(s)

formats = {
    'd': (r'-?\d+', conv.int), # signed integer decimal
    'i': (r'-?\d+', conv.int), # signed integer decimal
    'o': (r'-?[0-7]+', conv.oct), # signed octal value
    'x': (r'-?[0-9a-f]+', conv.hex), # signed hexadecimal (lowercase)
    'X': (r'-?[0-9A-F]+', conv.hex), # signed hexadecimal (uppercase)
    'f': (r'-?\d+(?:\.\d+)', conv.float), # floating point decimal format
    'F': (r'-?\d+(?:\.\d+)', conv.float), # floating point decimal format
    's': (r'.*', conv.str), # string
    
    'e': (), # Floating point exponential format (lowercase). # TODO
    'E': (), # Floating point exponential format (uppercase). # TODO
    'g': (), # Floating point format. Uses lowercase exponential format if exponent is less than -4 or not less than precision, decimal format otherwise. # TODO
    'G': (), # Floating point format. Uses uppercase exponential format if exponent is less than -4 or not less than precision, decimal format otherwise. # TODO
    'c': (), # Single character (accepts integer or single character string). # TODO
    'r': (), # String (converts any Python object using repr()). # TODO
}

rxp_format = re.compile('\\%%([%s])' % ''.join(formats))

def sub_format(m):
    letter = m.group(1)
    return '(%s)' % formats[letter][0]

def make_rxp(format_str):
    escaped = re.escape(format_str).replace('\\%', '%')
    rxp = re.sub(rxp_format, sub_format, escaped)
    
    return re.compile('^%s$' % rxp)

def unformat(format_str, s):
    rxp = make_rxp(format_str)
    match = rxp.search(s)
    assert match is not None, '"%s" does not match %s' % (s, rxp.pattern)
    l = []
    for m, v in zip(rxp_format.finditer(format_str), match.groups()):
        fn = formats[m.group(1)][1]
        l.append(fn(v))
    return tuple(l)

if __name__ == '__main__':
    print(unformat('%d', '123'))
    print(unformat('%d %d', '123 456'))
    print(unformat('%d %f', '123 42.42'))
    print(unformat('%s %f %f\n%s %f %f\n', 'bch(a/t): 123.031 213.0233\nbth(a/t): 23.031 23.0233\n'))
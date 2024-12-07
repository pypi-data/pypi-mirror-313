'''Mathematical functions for tabulate's decimal numbers
'''
import decimal
import itertools
import math
import re

# pylint: disable=C0103

decimal.getcontext().prec = 12

PIC = ''.join('''3.1415926535 8979323846 2643383279 5028841971
6939937510 5820974944 5923078164 0628620899 8628034825 3421170679'''.split())
PI = 0 + decimal.Decimal(PIC)
TAU = PI + PI
ONE = decimal.Decimal('1')
ZERO = decimal.Decimal('0')
one = decimal.Decimal('1.0000000000')

def gcd_for_decimals(*decimals):
    '''convert to int and return gcd (as int..)
    >>> gcd(34,3)
    1
    >>> gcd(299,702)
    13
    '''
    return math.gcd(*list(map(int,decimals)))


def degrees(x):
    '''return radians -> degrees
    >>> degrees(1)
    Decimal('57.2957795131')
    >>> degrees(TAU)
    Decimal('360')
    >>> degrees(0)
    Decimal('0')
    '''
    if not x:
        return ZERO
    return x / PI * 180


def radians(x):
    ''' return degrees -> radians
    >>> radians(90)
    Decimal('1.57079632679')
    >>> radians(0)
    Decimal('0')
    '''
    if not x:
        return ZERO
    return x * PI / 180


def sin(x):
    '''sine

    >>> sin(0)
    Decimal('0')
    >>> sin(PI/6)
    Decimal('0.5')
    >>> sin(PI/2)
    Decimal('1')
    '''
    return decimal.Decimal(math.sin(x)).quantize(one).normalize()


def cos(x):
    '''cosine

    >>> cos(PI/2)
    Decimal('-0')
    >>> cos(PI/3)
    Decimal('0.5')
    >>> cos(0)
    Decimal('1')
    '''
    return decimal.Decimal(math.cos(x)).quantize(one).normalize()


def tan(x):
    '''tangent
    >>> tan(PI/4)
    Decimal('1')
    '''
    return decimal.Decimal(math.tan(x)).quantize(one).normalize()


def sind(x):
    '''sin in degrees

    >>> sind(0)
    Decimal('0')
    >>> sind(30)
    Decimal('0.5')
    >>> sind(90)
    Decimal('1')
    '''
    return decimal.Decimal(math.sin(math.radians(x))).quantize(one).normalize()


def cosd(x):
    '''cosine in degrees

    >>> cosd(90)
    Decimal('0')
    >>> cosd(60)
    Decimal('0.5')
    >>> cosd(0)
    Decimal('1')
    '''
    return decimal.Decimal(math.cos(math.radians(x))).quantize(one).normalize()


def tand(x):
    '''tan in degrees
    >>> tand(90)
    Decimal('Infinity')
    >>> tand(45)
    Decimal('1')
    >>> tand(0)
    Decimal('0')
    '''
    if x % 360 in (90, 270):
        return decimal.Decimal('Inf')

    return decimal.Decimal(math.tan(math.radians(x))).quantize(one).normalize()


def pyth_add(a, b):
    '''Pythagorean addition

    >>> pyth_add(5, 12)
    Decimal('13')
    '''
    return (ONE * a * a + b * b).sqrt()


def angle(a, b):
    '''Like MP
    >>> angle(4,3)
    Decimal('36.8698976462')
    '''
    return degrees(decimal.Decimal(math.atan2(b, a)).quantize(one).normalize())


def dir(t):
    '''from MP
    >>> dir(0)
    (Decimal('1'), Decimal('0'))
    >>> dir(45)
    (Decimal('0.7071067812'), Decimal('0.7071067812'))
    '''
    return (cosd(t), sind(t))


def mexp(x):
    '''from MP = exp(x/256)
    >>> mexp(0)
    Decimal('1')
    >>> mexp(256)
    Decimal('2.71828182846')
    '''
    return (decimal.Decimal(x)/256).exp()


def mlog(x):
    ''' from MP = 256 log(x)
    >>> mlog(10)
    Decimal('589.461783805')
    '''
    return 256 * decimal.Decimal(x).ln()


def decimal_to_hex(d):
    '''decimal to hexadecimal...

    >>> decimal_to_hex(decimal.Decimal('0'))
    '0x0'
    >>> decimal_to_hex(decimal.Decimal('3.14'))
    '0x3.23d70a3d70'
    >>> decimal_to_hex(decimal.Decimal('100'))
    '0x64'

    '''

    digits = '0123456789abcdef'
    i, d = divmod(d, 1)
    a = hex(int(i))
    if d > 0:
        a += '.'
    while d > 0 and len(a) < 2 + decimal.getcontext().prec:
        d *= 16
        i, d = divmod(d, 1)
        a += digits[int(i)]
    return a


def decimal_to_oct(d):
    '''decimal to octal...

    >>> decimal_to_oct(decimal.Decimal('0'))
    '0o0'
    >>> decimal_to_oct(decimal.Decimal('3.14'))
    '0o3.1075341217'
    >>> decimal_to_oct(decimal.Decimal('100'))
    '0o144'

    '''

    digits = '01234567'
    i, d = divmod(d, 1)
    a = oct(int(i))
    if d > 0:
        a += '.'
    while d > 0 and len(a) < 2 + decimal.getcontext().prec:
        d *= 8
        i, d = divmod(d, 1)
        a += digits[int(i)]
    return a


def si(amount):
    """If amount is a number, add largest possible SI suffix,
    otherwise try to remove the suffix and return a value
    >>> si('10M')
    Decimal('10000000')
    >>> si(12315350)
    '12.315 M'
    >>> si(10)
    '10.000'
    >>> si('.2 k')
    Decimal('200.0')
    >>> si('Heading')
    'Heading'

    """
    sips = ' kMGTPE'
    sipat = re.compile(rf'([-+]?(?:\d+\.\d*|\.\d+|0|[1-9]\d*))\s*([{sips}])\Z')
    if (m := sipat.match(str(amount))) is not None:
        return decimal.Decimal(m.group(1)) * 10 ** (3 * sips.index(m.group(2)))

    try:
        n = decimal.Decimal(amount)
    except decimal.InvalidOperation:
        return amount
    else:
        e = min(int(n.log10() / 3), len(sips) - 1)
        return '{:7.3f} {}'.format(n / (10 ** (3 * e)), sips[e]).strip()


def factors(n):
    '''find the factors of n and return them in a tuple ... only use this for small numbers
    >>> factors(12345)
    (3, 5, 823)
    >>> factors(128)
    (2, 2, 2, 2, 2, 2, 2)
    >>> factors(817)
    (19, 43)
    >>> factors(1000038)
    (2, 3, 13, 12821)
    >>> factors(1000039)
    (1000039,)
    >>> factors(8761591) 
    (2957, 2963)
    '''
    out = []
    f = 2
    for incr in itertools.chain([1, 2, 2], itertools.cycle([4, 2, 4, 2, 4, 6, 2, 6])):
        if f * f > n:
            break
        while n % f == 0:
            out.append(f)
            n //= f
        f += incr
    if n > 1:
        out.append(n)
    return tuple(out)

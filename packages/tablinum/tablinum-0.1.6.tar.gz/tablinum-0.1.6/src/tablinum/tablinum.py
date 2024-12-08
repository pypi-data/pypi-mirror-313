#! /usr/bin/env python3
'''Tablinum

A module to line up text tables.
Toby Thurston -- 30 May 2024
'''

import argparse
import builtins
import collections
import csv
import decimal
import io
import itertools
import math
import os
import random
import re
import statistics
import string
import sys
import textwrap
import tokenize

import tablinum.tab_fun_dates as tab_fun_dates
import tablinum.tab_fun_maths as tab_fun_maths
import tablinum.tab_fun_useful as tab_fun_useful
# import tab_fun_dates
# import tab_fun_maths
# import tab_fun_useful


# Panther is a big cat of functions for column maths, using the Decimal
# versions.  This is used to limit the scope of the `eval` function when
# evaluating expressions in DSL options.  So if you are calculating a new
# column value with arr, or sorting on a calculated value etc, you can only use
# the functions in this dictionary.  The idea is that the keys are what you the
# user types and the values are the names of actual functions, either built-in
# or provided by the helper modules.

Panther = {
    'abs': builtins.abs,
    'bool': builtins.bool,
    'chr': builtins.chr,
    'divmod': builtins.divmod,
    'format': builtins.format,
    'int': builtins.int,
    'ord': builtins.ord,
    'pow': builtins.pow,
    'round': builtins.round,
    'str': builtins.str,
    'reversed': lambda x: ''.join(reversed(x)),
    'exp': lambda x: decimal.Decimal(x).exp(),
    'log': lambda x: decimal.Decimal(x).ln(),
    'log10': lambda x: decimal.Decimal(x).log10(),
    'sqrt': lambda x: decimal.Decimal(x).sqrt(),
    'caps': lambda x: str(x).capitalize(),
    'lower': lambda x: str(x).lower(),
    'upper': lambda x: str(x).upper(),
    'randomd': lambda: decimal.Decimal(str(random.random())),
    'floor': math.floor,
    'time': tab_fun_dates.as_time,
    'base': tab_fun_dates.base,
    'date': tab_fun_dates.date,
    'dow': tab_fun_dates.dow,
    'epoch': tab_fun_dates.epoch,
    'make_date': tab_fun_dates.make_date,
    'hms': tab_fun_dates.hms,
    'hr': tab_fun_dates.hr,
    'mins': tab_fun_dates.mins,
    'secs': tab_fun_dates.secs,
    'uktaxyear': tab_fun_dates.UK_tax_year,
    'angle': tab_fun_maths.angle,
    'cos': tab_fun_maths.cos, 'cosd': tab_fun_maths.cosd,
    'tan': tab_fun_maths.cos, 'tand': tab_fun_maths.tand,
    'gcd': tab_fun_maths.gcd_for_decimals,
    'lcm': tab_fun_maths.lcm_for_decimals,
    'comb': tab_fun_maths.comb_for_decimals,
    'perm': tab_fun_maths.perm_for_decimals,
    'hex': tab_fun_maths.decimal_to_hex,
    'oct': tab_fun_maths.decimal_to_oct,
    'dir': tab_fun_maths.dir,
    'factors': tab_fun_maths.factors,
    'mexp': tab_fun_maths.mexp,
    'mlog': tab_fun_maths.mlog,
    'pi': tab_fun_maths.PI,
    'hypot': tab_fun_maths.pyth_add,
    'sin': tab_fun_maths.sin, 'sind': tab_fun_maths.sind,
    'tau': tab_fun_maths.TAU,
    'len': tab_fun_useful.length,
    'all': tab_fun_useful.t_all,
    'any': tab_fun_useful.t_any,
    'max': tab_fun_useful.t_max,
    'min': tab_fun_useful.t_min,
    'minp': tab_fun_useful.t_minp,
    'sorted': tab_fun_useful.t_sorted,
    'sum': tab_fun_useful.t_sum,
    'Decimal': decimal.Decimal,
    '__builtins__': {},
}

# various number utils at this level


def as_numeric_tuple(x, backwards=False):
    '''return something for sort to work with
    >>> as_numeric_tuple("a")
    (-1000000000000.0, 'A')

    >>> as_numeric_tuple("a", True)
    (1000000000000.0, 'A')

    >>> as_numeric_tuple(None)
    (1000000000000.0, '')

    >>> as_numeric_tuple("3.14")
    (3.14, '3.14')

    >>> as_numeric_tuple("2020-05-01")
    (737546, '2020-05-01')

    >>> as_numeric_tuple("2 May 2020")
    (737547, '2 MAY 2020')

    >>> as_numeric_tuple("A19")
    (-1000000000000.0, 'A000000000000019')

    >>> as_numeric_tuple("A:1")
    (-1000000000000.0, 'A:000000000000001')
    >>> as_numeric_tuple('"A:19"')
    (-1000000000000.0, '"A:00000000000019"')

    >>> as_numeric_tuple("The War of the Roses")
    (-1000000000000.0, 'WAR OF THE ROSES')

    >>> as_numeric_tuple("")
    (1000000000000.0, '')

    >>> as_numeric_tuple("50k")
    (50000.0, '50K')

    >>> as_numeric_tuple("4 MiB")
    (4194304.0, '4 MIB')

    >>> as_numeric_tuple("1.12 GB")
    (1202590842.88, '1.12 GB')

    >>> as_numeric_tuple("8:56.2")
    (536.2, '8:56.2')

    >>> as_numeric_tuple("13:34:20")
    (48860.0, '13:34:20')

    >>> as_numeric_tuple("Monday") < as_numeric_tuple("Friday")
    True

    >>> as_numeric_tuple('192.168.0.1')
    (3232235521, '192.168.0.1')

    >>> as_numeric_tuple('00:01:E6:2C:42:1D')
    (8156627485, '00:01:E6:2C:42:1D')

    '''

    alpha, omega = -1e12, 1e12
    if backwards:
        alpha, omega = omega, alpha

    if x is None or x == '':
        return (omega, '')  # put it at the bottom

    x = x.upper()

    try:
        return (float(x), x)
    except ValueError:
        pass

    try:
        # try to parse the date and return an ordinal number
        return (tab_fun_dates.parse_date(x).toordinal(), x)
    except ValueError:
        pass

    # is this a time?
    if (m := re.match(r'(\d+):([0-5]\d):([0-5]\d(\.\d+)?)\Z', x)) is not None:
        return (int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)), x)

    if (m := re.match(r'(\d+):([0-5]\d(\.\d+)?\Z)', x)) is not None:
        return (int(m.group(1)) * 60 + float(m.group(2)), x)

    # is this an IP4 address?
    if (m := re.match(r'(\d+)\.(\d+)\.(\d+)\.(\d+)\Z', x)) is not None:
        a, b, c, d = map(int, m.groups())
        if all(t < 256 for t in (a, b, c, d)):
            return (a * 16777216 + b * 65536 + c * 256 + d, x)

    # is this a MAC address
    if all(t in '0123456789ABCDEF:' for t in x):
        if x.count(':') == 5:
            if len(x) == 17:
                return (int(x.replace(':', ''), 16), x)

    # pad trailing numbers with zeros
    # Make A1, A2, A10 etc sortable...
    if (m := re.match(r'(\D+)(\d+["\']?)\Z', x)) is not None:
        return (alpha, m.group(1) + m.group(2).zfill(15))

    si_values = {
        'B': 1, 'K': 1000, 'M': 1000000, 'G': 1000000000, 'T': 1000000000000,
        'KB': 1024, 'MB': 1048576, 'GB': 1073741824, 'TB': 1099511627776,
        'KIB': 1024, 'MIB': 1048576, 'GIB': 1073741824, 'TIB': 1099511627776,
    }
    if (m := re.match(r'(\d+\.\d*|\.?\d+)\s?([BKMGT](I?B)?)', x)) is not None:
        return (float(m.group(1)) * si_values.get(m.group(2), 1), x)

    # remove leading articles (Library sort)
    words = x.split()
    if len(words) > 1 and words.pop(0) in ('A', 'AN', 'THE'):
        return (alpha, ' '.join(words))

    return (alpha, x)


def is_as_number(sss):
    '''Input (string) Output (boolean, any)
    if boolean is True, any is Decimal
    else any is string
    >>> is_as_number('')
    (False, '')
    >>> is_as_number("Label")
    (False, 'Label')
    >>> is_as_number("False")
    (True, False)
    >>> is_as_number("3.14")
    (True, Decimal('3.14'))
    >>> is_as_number('0')
    (True, Decimal('0'))
    >>> is_as_number('0x4F')
    (True, Decimal('79'))
    >>> is_as_number('0x40.0')
    (False, '0x40.0')
    >>> is_as_number('1,234,567')
    (True, Decimal('1234567'))
    >>> is_as_number('43%')
    (True, Decimal('0.43'))
    >>> is_as_number('-')
    (False, '-')
    >>> is_as_number('-902')
    (True, Decimal('-902'))
    >>> is_as_number('£34.00')
    (True, Decimal('34.00'))
    >>> is_as_number('1E-12')
    (True, Decimal('1E-12'))
    >>> is_as_number('14¾')
    (True, Decimal('14.75'))
    '''
    digits = '1234567890'
    ignore = '£$,_'
    signs = '+-'
    point = '.'
    alphabetics = 'xoabcdef'
    suffix = '%¼½¾'

    if sss in ('True', 'False'):
        return (True, sss == 'True')

    if not all((c in digits + point + signs + ignore + alphabetics + suffix) for c in sss.lower()):
        return (False, sss)

    if not any((c in digits) for c in sss):
        return (False, sss)

    trial_number = ''.join(c for c in sss.lower() if c in digits + point + signs + alphabetics + suffix)

    # with the base=0 argument int() will throw a ValueError unless "trial_number" 
    # looks like a base10 integer
    try:
        return (True, decimal.Decimal(int(trial_number, 0)))
    except (ValueError, SyntaxError):
        pass

    try:
        if trial_number.endswith('%'):
            return (True, decimal.Decimal(trial_number[:-1]) / 100)
        if trial_number[-1] in suffix:
            quarters = decimal.Decimal(suffix.index(trial_number[-1])) / 4
            return (True, decimal.Decimal(trial_number[:-1]) + quarters)
        return (True, decimal.Decimal(trial_number))
    except ArithmeticError:
        pass

    return (False, sss)


def as_decimal(n=0, na_value=decimal.Decimal('0')):
    '''Make this a decimal

    >>> as_decimal('123.45')
    Decimal('123.45')
    >>> as_decimal()
    Decimal('0')
    >>> as_decimal('1E234')
    Decimal('1E+234')
    >>> as_decimal('1E2341412541245251234534')
    Decimal('0')
    '''
    try:
        return decimal.Decimal(n)
    except decimal.DecimalException:
        return na_value


def siggy(s, n):
    '''Reduce to n sig figs
    >>> siggy('1,234', 2)
    '1200'
    >>> siggy('Text', 1)
    'Text'
    >>> siggy('0', 10)
    '0'
    >>> siggy('True', 1)
    'True'
    '''
    flag, number = is_as_number(s)
    if not flag or isinstance(number, bool):
        return s
    if number.is_zero():
        return '0'
    figs = n - math.floor(abs(number).log10()) - 1
    return f'{round(number, figs):f}'


def rounders(s, n):
    '''Round to n fixed places, if possible
    >>> rounders('4',0)
    '4'
    >>> rounders('Text', 1)
    'Text'
    >>> rounders('45%', 3)
    '0.450'
    >>> rounders('45%', 1)
    '0.4'
    '''
    flag, number = is_as_number(s)
    return f'{number:.{n}f}' if flag else s


def looks_like_sequence(numbers):
    '''Do these decimals appear to be a list of years, or some other numeric labels?
    We are trying to see if they are in arithmetic progression... (sort of)
    Usually the list will *not* be a sequence, so we can be more
    efficient by using `all` than just sorting everything.

    >>> looks_like_sequence((1,2,3))
    True
    >>> looks_like_sequence((1990, 1980, 1970))
    True
    >>> looks_like_sequence((3.14, 2.718, 6.28))
    False
    >>> looks_like_sequence((28, 44, 20, 0))
    False
    >>> looks_like_sequence((1,1,1,1,1))
    False
    >>> looks_like_sequence((28, 44))
    False
    >>> looks_like_sequence((28,))
    False
    >>> looks_like_sequence([])
    False
    '''
    try:
        delta = numbers[0] - numbers[1]
    except IndexError:
        return False

    n = len(numbers)
    return n > 2 and delta != 0 \
        and all(x == int(x) for x in numbers) \
        and all(delta == numbers[x - 1] - numbers[x] for x in range(2, n))


def looks_like_formula(expression):
    '''Is this a formula?

    >>> looks_like_formula('')
    False
    >>> looks_like_formula('Abc')
    False
    >>> looks_like_formula('-1')
    False
    >>> looks_like_formula('a-1')
    True
    '''
    if all(x in string.ascii_letters for x in expression):
        return False

    try:
        int(expression)
    except (TypeError, ValueError):
        return True

    return False


def is_multiplicated(s):
    '''is this an accidental string multiplication?

    >>> is_multiplicated('VolVolVolVolVol')
    True
    >>> is_multiplicated('Pressure')
    False
    >>> is_multiplicated('Algorithm')
    False
    >>> is_multiplicated('aaa')
    False
    '''

    return len(s) > 3 and re.match(r'(\w+?)\1+\Z', s) is not None


def find_kmp(needle, haystack):
    '''Find sublist in list -- adapted from https://stackoverflow.com/a/60823752/1274254

    >>> find_kmp([1,2], [3,4,5])
    -1
    >>> find_kmp([1,2], [1,2,3,4,5])
    0
    >>> find_kmp([1,2], [0,1,2,3,4,5])
    1
    '''
    n = len(haystack)
    m = len(needle)
    # : compute offsets
    offsets = [0] * m
    j = 1
    k = 0
    while j < m:
        if needle[j] == needle[k]:
            k += 1
            offsets[j] = k
            j += 1
        else:
            if k != 0:
                k = offsets[k - 1]
            else:
                offsets[j] = 0
                j += 1
    # : find matches
    i = j = 0
    while i < n:
        if haystack[i] == needle[j]:
            i += 1
            j += 1
        if j == m:
            return i - j
            j = offsets[j - 1]
        elif i < n and haystack[i] != needle[j]:
            if j != 0:
                j = offsets[j - 1]
            else:
                i += 1

    return -1


def compile_as_decimal(expr):
    '''This function takes as expression given as an argument to
    one of the verbs like arr or filter or sort or tap, and compiles
    it so that we can execute it more efficiently.

    Several bits of syntactic sugar are applied to the expression, after tokenization

    - allow <> for != (easier to write on the Vi command line
    - allow mod for % (ditto)
    - allow = for == in comparisons (checkout the negative look behind in the regex)
    - make all tokens that look like floats (NUMBER and contains '.') into
      Decimals, so that we avoid the normal FP accuracy & rounding issues.
    - translate '?' into a (decimal) random number.

    Then a couple more "corrections" to the out list:

    - allow a++b as dyadic equivalent of hypot(a,b)
    - allow 2a for 2*a

    Finally we untokenize the expression and compile it with the compile BIF.

    '''

    out = []
    try:
        for tn, tv, _, _, _ in tokenize.generate_tokens(io.StringIO(expr).readline):
            if tn == tokenize.NUMBER and ('.' in tv or 'e' in tv.lower()):
                out.append((tokenize.NAME, 'Decimal'))
                out.append((tokenize.OP, '('))
                out.append((tokenize.STRING, repr(tv)))
                out.append((tokenize.OP, ')'))
            elif tn == tokenize.NAME and tv == 'mod':
                out.append((tokenize.OP, '%'))
            elif tn == tokenize.OP and tv == '=':
                out.append((tokenize.OP, '=='))
            elif tn == tokenize.OP and tv == '<>':
                out.append((tokenize.OP, '!='))
            elif tv == '?':
                out.append((tokenize.NAME, 'randomd'))
                out.append((tokenize.OP, '('))
                out.append((tokenize.OP, ')'))
            elif tn == tokenize.FSTRING_MIDDLE and tv.endswith('d'):
                out.append((tn, tv[:-1]))  # remove trailing d (to avoid Decimal error)
            else:
                out.append((tn, tv))
    except tokenize.TokenError:
        return (False, '?! tokens ' + expr)

    def op(s):
        return (tokenize.OP, s)

    # change a++b -> hypot(a,b)
    double_plus = [op('+'), op('+')]
    while True:
        n = find_kmp(double_plus, out[1:])
        if n < 0:
            break
        out[n:n + 4] = [(tokenize.NAME, 'hypot'), op('('), out[n], op(','), out[n + 3], op(')')]

    # # allow 2a .5b etc
    while True:
        n = find_kmp([tokenize.NUMBER, tokenize.NAME], [tn for tn, _ in out])
        if n < 0:
            break
        out[n:n + 2] = [op('('), out[n], op('*'), out[n+1], op(')')]

    new_expr = tokenize.untokenize(out)

    try:
        cc = compile(new_expr, '<string>', 'eval')
    except (SyntaxError, ValueError):
        return (False, '?! syntax ' + expr)

    return (True, cc)


def _replace_values(failed_expression, known_variables):
    '''replace the variables that we know about in the expression
    This is used when an eval fails.  The idea is that we replace the value
    with the expression that did not work.  This is often helpful for
    title rows.

    >>> _replace_values('sin(a)', {'a': 'angle'})
    'sin(angle)'
    >>> _replace_values("a/x", {'a': 'count', 'x': 'hide_this'})
    'count/hide_this'
    >>> _replace_values("a*3+0", {'a': 'count', 'x': 'hide_this'})
    'count*3'
    >>> _replace_values("(s/x)", {'s': 'ex', 'x': 'hide_this'})
    'ex/hide_this'
    '''
    out = []
    for tn, tv, _, _, _ in tokenize.generate_tokens(io.StringIO(failed_expression).readline):
        if tn == tokenize.NAME and tv in known_variables:
            out.append((tokenize.NAME, str(known_variables[tv])))
        else:
            out.append((tn, tv))
    new = tokenize.untokenize(out).replace(' ', '')
    if new.endswith('+0'):
        new = new[:-2]
    if new.startswith('(') and new.endswith(')'):
        new = new[1:-1]
    return new


def quantile(ordered_data, p):
    '''get a particular linearly-interpolated percentile from sorted data

    >>> quantile([1,2,3,4,5], 0.5)
    Decimal('3')
    >>> quantile([1,2,3,4,5], 0.25)
    Decimal('2')
    >>> quantile([1,2,3,4,5], 0)
    Decimal('1')
    >>> quantile([1,2,3,4,5], 1)
    Decimal('5')
    >>> quantile([1,2,3,4,5], 2)
    '''
    n = len(ordered_data)
    if not 0 <= p <= 1:
        return None

    if p == 1:
        return decimal.Decimal(ordered_data[-1])

    f = math.floor(p * (n - 1))
    w = decimal.Decimal(p * (n - 1)) - f
    return decimal.Decimal((1 - w) * ordered_data[f] + w * ordered_data[f + 1])


def quantiles(data, pvalues=(0, 0.25, 0.5, 0.75, 1)):
    '''return a list of percentiles as defined in S.
    >>> quantiles([68, 86, 29, 8, 75, 38, 87, 74, 40])
    [Decimal('8'), Decimal('38'), Decimal('68'), Decimal('75'), Decimal('87')]
    '''
    x = sorted(data)
    return [quantile(x, p) for p in pvalues]


def statistical_summary(numbers):
    '''return a 4/6 field summary of a list of numbers
    >>> statistical_summary([])
    ''

    >>> tdat = [decimal.Decimal(x) for x in '36.4 67.1 82.7 34.2 96.8 10.9 19.1 71.8 66.0 29.2'.split()]
    >>> statistical_summary(tdat)
    'Min: 10.9  Mean: 51.42  Max: 96.8'
    >>> tdat = [decimal.Decimal(x) for x in '0 1 2 3 4 5 6 8 9 36.4 67.1 82.7 34.2 96.8 10.9 29.2'.split()]
    >>> statistical_summary(tdat)
    'Min: 0  Q25: 3.75  Median: 8.5  Mean: 24.70625  Q75: 34.750  Max: 96.8'

    '''
    if not numbers:
        return ''

    me = statistics.mean(numbers)
    if len(numbers) > 10:
        mi, lq, md, uq, ma = quantiles(numbers)
        return f'Min: {mi}  Q25: {lq}  Median: {md}  Mean: {me}  Q75: {uq}  Max: {ma}'

    return f'Min: {builtins.min(numbers)}  Mean: {me}  Max: {builtins.max(numbers)}'


def counting_summary(factors, n=5):
    '''summarize different levels in a factor

    >>> counting_summary('a b c d e f g h a b b b a c w'.split())
    'b 4, a 3, c 2, d 1, e 1 (and 4 others...)'
    '''
    counter = collections.Counter(factors)
    if all(x == 1 for x in counter.values()):
        analysis = "All distinct."
    else:
        analysis = ', '.join(f'{k} {v}' for k, v in counter.most_common(n))
        if len(counter) > n:
            analysis += f' (and {len(counter)-n} others...)'

    return analysis


class Table:
    '''A class to hold a table -- and some functions thereon'''

    def __init__(self):
        " empty data and no rows or cols "
        decimal.getcontext().prec = 12
        self.data = []
        self.cols = 0
        self.indent = 0
        self.extras = collections.defaultdict(set)
        self.form = 'plain'
        self.messages = []
        self.stack = []  # used to cache popped items
        self.operations = {
            'add': self._append_reduction,
            'arr': self._rearrange_columns,
            'clear': self.clear,
            'ditto': self._copy_down,
            'dp': self._fix_decimal_places,
            'dup': self._duplicate_item,
            'filter': self._select_matching_rows,
            'gen': self._generate_new_rows,
            'group': self._add_grouping_blanks,
            'help': self._describe_operations,
            'make': self._set_output_form,
            'label': self._label_columns,
            'levels': self._show_column_counts,
            'nospace': self._remove_spaces_from_values,
            'noblanks': self._remove_blank_extras,
            'pivot': self._wrangle,
            'pop': self.pop,
            'push': self.push,
            'roll': self._roll_by_col,
            'rule': self.add_rule,
            'tap': self._apply_function_to_numeric_values,
            'sf': self._fix_sigfigs,
            'shuffle': self._shuffle_rows,
            'sort': self._sort_rows_by_col,
            'uniq': self._remove_duplicates_by_col,
            'unwrap': self._unrapper,
            'unzip': self._unzipper,
            'wrap': self._rapper,
            'xp': self.transpose,
            'zip': self._zipper,
        }

    def __str__(self):
        "Print neatly"

        out = self.messages + list(self.tabulate())
        self.messages.clear()
        return "\n".join(out)

    def __getitem__(self, i):
        "Like a list..."
        return self.data[i]

    def __len__(self):
        "Also like a list..."
        return len(self.data)

    def _describe_operations(self, dsl_verb=''):
        '''What commands are defined?'''
        if dsl_verb.lower() == 'arr':
            verbs = sorted(x for x in Panther if x[0] in string.ascii_lowercase)
            msg = f'Functions for arr: {" ".join(verbs)}'
        else:
            msg = f'Try one of these: {" ".join(sorted(self.operations))}'
        self.messages.extend(textwrap.wrap(msg))

    def clear(self, unused_variable_to_allow_blank_from_do=None):
        "Clear data etc"
        self.data.clear()
        self.extras.clear()
        self.cols = 0
        self.indent = 0

    def _duplicate_item(self, n):
        "Duplicate an item"
        self.stack.append(self.pop(n))  # pop puts it on the stack first, so this does it twice
        self.push(n)
        self.push(n)

    def parse_tex(self, lines_thing, append=False):
        "Read lines from an iterable thing of TeX source, and append to self"

        if not append:
            self.clear()
        self.indent = 0
        eol_pattern = re.compile(r'\s*\\(cr|\\)\Z')
        amp_pattern = re.compile(r'\s*&\s*')
        for line in lines_thing:
            line = eol_pattern.sub('', line.strip())
            if line == "\\noalign{\\medskip}":
                self.add_blank()
            elif line == "\\hline":
                self.add_rule()
            elif line == "\\noalign{\\vskip2pt\\hrule\\vskip4pt}":
                self.add_rule()
            elif line.startswith('%'):
                self.add_comment(line[1:].rstrip())
            else:
                self.append(amp_pattern.split(line))

    def parse_lines(self, lines_thing, splitter=re.compile(r'\s\s+'), splits=0, append=False):
        "Read lines from an iterable thing, and append to self"

        if not append:
            self.clear()
            self.indent = 99

        for raw_line in lines_thing:
            raw_line = raw_line.replace("\t", "    ")
            stripped_line = raw_line.strip()
            if not stripped_line:
                self.add_blank()
            elif set(stripped_line) == {'-'}:
                self.add_rule()
            elif stripped_line.startswith('#'):
                self.add_comment(stripped_line)
            else:
                self.append(splitter.split(stripped_line, maxsplit=splits))
                if not append:
                    self.indent = min(self.indent, len(raw_line) - len(raw_line.lstrip()))
        # catch empty tables
        if not self.data:
            self.indent = 0

    def parse_lol(self, list_of_iterables, append=False, filler=''):
        "pass lol into self.data"
        if not append:
            self.clear()
        for r in list_of_iterables:
            if not r:
                self.add_blank()
            elif set(''.join(str(x) for x in r)) == {'-'}:
                self.add_rule()
            else:
                self.append(r, filler)

    def pop(self, n=None):
        '''Remove an entire row, saving it in case we want it later
        and allow them to be pushed back'''

        if n is None or n == '':
            r = self.data.pop()
        else:
            try:
                r = self.data.pop(int(n))
            except (IndexError, ValueError):
                r = None

        if r is not None:
            self.stack.append(r)

        return r

    def push(self, n=None):
        '''Put back a popped row, if possible'''
        try:
            r = self.stack.pop()
        except IndexError:
            return  # do nothing if stack is empty

        try:
            n = int(n)
        except (ValueError, TypeError):
            n = len(self.data)
        self.insert(n, r)  # the semantics of insert take care of indexes out of bounds

    def append(self, iterable, filler=''):
        "insert at the end"
        self.insert(len(self.data), iterable, filler)

    def insert(self, i, iterable, filler=''):
        "add a row, maintaining cols"
        row = list(filler if x == '' else x for x in iterable)
        n = len(row)
        if n < self.cols:
            row.extend([filler] * (self.cols - n))
        elif self.cols < n:
            for r in self.data:
                r.extend([filler] * (n - self.cols))
            self.cols = n

        # if there are any cells in the new row, then insert at "i"
        # make sure values are strings, and normalize space in last cell
        if n > 0:
            self.data.insert(i, [str(x) for x in row[:-1]] + [' '.join(str(row[-1]).split())])

    def copy(self):
        "Implement the standard copy method"
        return self.data[:]

    def do(self, agenda=None):
        "Do what we've been asked..."
        if agenda is None:
            return

        if not isinstance(agenda, list):
            agenda = agenda.split()

        while agenda:
            op = agenda.pop(0)
            if op not in self.operations:
                self.messages.append(f'?? {op}')
                break

            # get any arguments
            argument = []
            while agenda and agenda[0] not in self.operations:
                argument.append(agenda.pop(0))

            self.operations[op](' '.join(argument))
            if self.messages:
                break

    def _label_columns(self, names=''):
        "add some labels"
        # make list of pairs like so (word from names or None, letter)
        # we can then "overlay" the names using the a or b construction
        # below.  The point of doing this is to make sure that if the
        # user only gives two names, the 3rd, 4th etc cols will still
        # be labelled c, d, etc.  If you have more than 26 cols
        # cols 27+ will get fillers instead of labels
        if self.cols:
            pairs = itertools.zip_longest(names.split(), string.ascii_lowercase)
            self.insert(0, list(a or b for a, b in pairs)[:self.cols])
        else:
            self.insert(0, names.split())  # if no columns just insert these names

    def column(self, i):
        "get a column from the table - zero indexed"
        try:
            return [is_as_number(r[i]) for r in self.data]
        except IndexError:
            return []

    def _valid_data_index(self, s):
        '''turn s into an index for self.data
        default to len(self.data)
        '''
        n = len(self.data)
        try:
            i = int(s)
        except (TypeError, ValueError):
            return n
        if i + n < 0:
            return 0
        if i < 0:
            return i + n
        if i > n:
            return n
        return i

    def add_blank(self, n=None):
        "flag a blank"
        self.extras[self._valid_data_index(n)].add("blank")

    def add_rule(self, n=None):
        "mark a rule"
        self.extras[self._valid_data_index(n)].add("rule")

    def add_comment(self, contents, n=None):
        "stash a comment line"
        self.extras[self._valid_data_index(n)].add('#' + contents.lstrip('#'))

    def _set_output_form(self, form_name):
        "Set the form name, used in `tabulate`"
        self.form = form_name.lower()

    def transpose(self, _=None):
        '''Swap rows and columns
        '''
        self.cols = len(self.data)
        self.data = list(list(r) for r in zip(*self.data))
        self.extras.clear()

    def _select_matching_rows(self, expression):
        '''Filter the table to rows where expression is true
        '''
        if not expression:
            return

        header = None
        if '@' in expression:
            header = self.pop(0)
            expression = expression.replace('@', '')

        ok, cc = compile_as_decimal(expression)
        if not ok:
            self.messages.append(cc)
        else:
            old_data = self.data[:]
            self.data.clear()
            identity = string.ascii_lowercase[:self.cols]
            value_dict = {}
            value_dict['rows'] = len(old_data)
            for k in identity:
                value_dict[k.upper()] = 0  # accumulators

            # the idea here is that we treat unknown names as strings, to allow you to say b=whatever
            # instead of having to write b='whatever'.  The co_names attribute of the compiled code
            # is a list of the names in the compiled object
            for n in cc.co_names:
                if n not in identity and n not in Panther and n not in value_dict:
                    value_dict[n] = n

            for i, r in enumerate(old_data):
                value_dict['row_number'] = i + 1
                for k, v in zip(identity, r):
                    flag, value_dict[k] = is_as_number(v)
                    if flag:
                        value_dict[k.upper()] += value_dict[k]

                try:
                    wanted = eval(cc, Panther, value_dict)
                except (TypeError, NameError, ArithmeticError):
                    wanted = True  # default to keeping the row
                if wanted:
                    self.append(r)
                elif i > 1 and i in self.extras:
                    self.extras.pop(i)  # remove extras if line not wanted (unless we are at the top)

        if header is not None:
            self.insert(0, header)

        if not self.data:
            self.cols = 0

    def _shuffle_rows(self, col_spec):
        '''Re-arrange the data at random'''
        header = None
        if '@' in col_spec:
            header = self.pop(0)
            col_spec = col_spec.replace('@', '')

        if not col_spec:
            random.shuffle(self.data)
            self.extras.clear()
        else:
            self.data = list(map(list, zip(*self.data)))
            for c in col_spec:
                i, _ = self._fancy_col_index(c)
                if i is None:
                    continue
                random.shuffle(self.data[i])
            self.data = list(map(list, zip(*self.data)))

        if header is not None:
            self.insert(0, header)

    def _remove_blank_extras(self, _):
        for i in range(len(self.data)):
            self.extras[i].discard('blank')

    def _remove_spaces_from_values(self, joiner):
        '''Remove spaces from values -- this can make it easier to import into R'''
        if joiner:
            self.data = [[joiner.join(cell.split()) for cell in row] for row in self.data]
        else:
            self.data = [[''.join(cell.title().split()) for cell in row] for row in self.data]

    def _apply_function_to_numeric_values(self, fstring):
        '''fstring should be a maths expression with an x, as x+1 or 2**x etc
        which is to be applied to each numeric value in the table. If there is
        no x in the expression, we add one to the front, so you can write things
        like "+1" or "/4" as fstrings....
        '''
        if not fstring:
            return

        if "x" not in fstring and fstring[0] in ('*', '/', '+', '-', '<', '>', '='):
            fstring = "x" + fstring

        ok, cc = compile_as_decimal(fstring)
        if not ok:
            self.messages.append(cc)
            return

        values = {
            "x": 0,
            "rows": len(self.data),
            "cols": self.cols,
            "total": sum(as_decimal(x) for row in self.data for x in row),
            "row_number": 0,
        }
        col_totals = [sum(as_decimal(x[1]) for x in self.column(i) if x[0]) for i in range(self.cols)]

        old_rows = self.data[:]
        self.data.clear()
        for row in old_rows:
            new_row = []
            values['row_number'] += 1
            values['row_total'] = sum(as_decimal(x) for x in row)
            for i, cell in enumerate(row):
                values['col_number'] = i + 1
                values['col_total'] = col_totals[i]
                cell_is_a_number, values['x'] = is_as_number(cell)
                try:
                    new_value = eval(cc, Panther, values)
                except Exception:
                    new_row.append(cell)
                else:
                    if isinstance(new_value, tuple):
                        new_row.extend(new_value)
                    elif not cell_is_a_number and f"{new_value}".count(cell) > 2:
                        # this was probably 'string'*9 or similar
                        new_row.append(cell)
                    elif not cell_is_a_number and f"{new_value}" == "0":
                        # this was probably a title row or col...
                        new_row.append(cell)
                    else:
                        new_row.append(new_value)

            self.append(new_row)

    def _apply_formats(self, f_string, f_function):
        "Used for DP and SF"
        if f_string is None or not f_string.isdigit():
            return
        # extend as needed (you could use zip_longest, but this just as simple)
        f_values = list(int(x) for x in f_string) + [int(f_string[-1])] * (self.cols - len(f_string))
        self.data = list(list(f_function(c, v) for c, v in zip(r, f_values)) for r in self.data)

    def _fix_decimal_places(self, dp_string):
        "Round all the numerical fields in each row"
        self._apply_formats(dp_string, rounders)

    def _fix_sigfigs(self, sf_string):
        "Round to n sig figs all the numeric fields in each row"
        self._apply_formats(sf_string, siggy)

    def _generate_new_rows(self, count_or_range):
        "Add some more data on the bottom"

        if (m := re.match(r'([-+]?\d+)', count_or_range)) is not None:
            alpha = int(m.group(1))

            if (m := re.match(r'(?:[-+]?\d+)(?:\D+?)([-+]?\d+)$', count_or_range)) is not None:
                omega = int(m.group(1))
            else:
                omega = 1

            if alpha > omega:
                (alpha, omega) = (omega, alpha)

            self.parse_lol(list([x] for x in range(alpha, omega + 1)), append=True)
            return

        # Labels * Cols...
        if (m := re.match(r'([A-Za-z]+)(\d)?$', count_or_range)) is not None:
            labels = m.group(1)
            columns = 1 if m.group(2) is None else int(m.group(2))
            self.parse_lol(list([*x] for x in itertools.product(labels, repeat=columns)), append=True)
            return

    def _copy_down(self, marker):
        '''Fix up ditto marks'''
        if marker.strip() == "":
            marker = '"'
        for i, row in enumerate(self.data):
            for j, cell in enumerate(row):
                if cell == marker and i > 0:
                    self.data[i][j] = self.data[i - 1][j]

    def _zipper(self, n):
        '''Put n rows side by side
        '''
        try:
            rows_to_zip = int(n)
        except (ValueError, TypeError):
            rows_to_zip = 2

        if rows_to_zip < 2:
            return

        old_data = self.data.copy()
        self.data.clear()
        self.cols = 0
        while old_data:
            new_row = []
            for _ in range(rows_to_zip):
                if old_data:
                    new_row.extend(old_data.pop(0))
            self.append(new_row)

        self.extras.clear()

    def _unzipper(self, n):
        '''The opposite of zip.  Split rows so that there are cols/n cols in each'''
        try:
            splits = int(n)
        except (ValueError, TypeError):
            splits = 2

        desired_cols = math.ceil(self.cols / splits)

        old_data = self.data.copy()
        self.data.clear()
        self.cols = 0
        for r in old_data:
            for i in range(splits):
                start = i * desired_cols
                stop = start + desired_cols
                self.append(r[start:stop])

        self.extras.clear()

    def _rapper(self, n):
        '''It's a wrap.'''
        try:
            groups = int(n)
        except (ValueError, TypeError):
            groups = 2

        if groups < 2:  # catch bad input
            return

        rows_per_group = math.ceil(len(self.data) / groups)

        old_data = self.data.copy()
        self.data.clear()

        for i in range(rows_per_group):
            new_row = []
            for j in range(groups):
                k = i + j * rows_per_group
                try:
                    new_row += old_data[k]
                except IndexError:
                    pass
            self.append(new_row)

        self.extras.clear()

    def _splitme(self, r, p):
        '''Splits a range object r into p pieces
        each of which is a smaller range object.

        So (for example):
           _splitme(range(0, 9), 3) will first yield: range(0, 3)
         and then call
             _splitme(range(3, 9), 2) which will yield: range(3, 6)
          and call
               _splitme(range(6, 9), 1) which will yield: range(6, 9)
           and then make no further recursive calls because p is not > 1

        '''
        size = math.ceil(len(r) / p)
        yield r[:size]
        if p > 1:
            yield from self._splitme(r[size:], p - 1)

    def _unrapper(self, n):
        '''It's not a wrap'''
        try:
            groups = int(n)
        except (ValueError, TypeError):
            groups = 2

        if groups < 2:  # catch bad user input -- groups=1 would be a no-op
            return

        old_data = self.data.copy()
        old_cols = self.cols
        groups = min(groups, old_cols)  # no blanks on the end thank you

        self.data.clear()
        self.cols = 0
        self.extras.clear()

        for col_list in self._splitme(range(old_cols), groups):
            for r in old_data:
                self.append([r[x] for x in col_list])

    def _append_reduction(self, fun_list):
        '''Reduce column and append result to foot of table
        fun is the name, func is the callable.
        first see if this is the name of something in stats
        or something from builtins that we like, if none of those ignore it with msg
        '''
        if not fun_list:
            fun_list = 'total'
        else:
            fun_list = fun_list.replace('summary', 'min median mean max')

        for fun in (f.lower() for f in fun_list.split()):
            if hasattr(statistics, fun):
                func = getattr(statistics, fun)
            elif fun in "min max all any sum".split():
                func = getattr(builtins, fun)
            elif fun == "total":
                func = builtins.sum
            else:
                self.messages.append(f'? {fun}')
                continue

            footer = []
            for c in range(self.cols):
                booleans, values = zip(*self.column(c))
                decimals = list(itertools.compress(values, booleans))
                if not any(booleans) or (c == 0 and looks_like_sequence(decimals)):
                    footer.append(fun.title())
                else:
                    footer.append(func(decimals))

            self.append(footer)

    def _wrangle(self, shape):
        '''Reflow / pivot / reshape from wide to long or long to wide

        pivot wide assumes that col -1 has values and -2 has col head values
        and everything else are keys. Does nothing if there are less than 3 cols.

        pivot long assumes only key is col A but you can add a letter or number
        to show where the keys stop -- so if the first three are keys then use "longc"
        or "long3" -- numbering from a=1

        '''
        if not shape or self.cols < 3:
            return

        pivot_functions_for = {
            'wide': (builtins.sum, as_decimal),
            'sum': (builtins.sum, as_decimal),
            'count': (builtins.len, as_decimal),
            'mean': (lambda a: statistics.mean(a) if a else 'NA', as_decimal),
            'any': (builtins.any, as_decimal),
            'alpha': (lambda a: a[0] if a else '-', str),
            'omega': (lambda a: a[-1] if a else '-', str),
        }

        shape = shape.lower()

        for k in pivot_functions_for:
            if k.startswith(shape):
                self._wrangle_wide(*pivot_functions_for[k])
                return

        if (m := re.match(r'long([1-9a-o])?$', shape)) is None:
            return

        if m.group(1) is None:
            last_key_col = 1
        else:
            try:
                last_key_col = int(m.group(1))
            except ValueError:
                last_key_col = ord(m.group(1)) - ord('a') + 1

        if self.cols - last_key_col > 1:
            self._wrangle_long(last_key_col)

    def _wrangle_wide(self, fun=sum, prep=as_decimal):
        '''Reflow wide'''
        bags = collections.defaultdict(list)
        names_seen = dict()
        keys_seen = dict()
        header = self.data[0][:-2]
        for r in self.data[1:]:
            *key, name, value = r
            key = tuple(key)
            names_seen[name] = True
            keys_seen[key] = True
            bags[(key, name)].append(prep(value))

        self.data = []
        self.cols = 0
        names = list(names_seen)
        self.append(header + names)
        for k in keys_seen:
            self.append(list(k) + [fun(bags[(k, n)]) for n in names])

    def _wrangle_long(self, keystop):
        '''Reflow long'''
        header = self.data[0][:keystop] + ['Name', 'Value']
        names = self.data[0][keystop:]
        wide_data = self.data[1:]
        self.data = []
        self.cols = 0

        self.append(header)
        for r in wide_data:
            for n, v in zip(names, r[keystop:]):
                self.append(r[:keystop] + [n, v])

    def _get_expr_list(self, given):
        '''Turn the user's argument into a tuple of expression strings

        >>> t = Table()
        >>> a = (1, 2, 3, 4, 5, 6, 7, 8)
        >>> t.parse_lol((a, a))
        >>> t._get_expr_list("-abc")
        ['a', 'b', 'c']
        >>> t._get_expr_list("abcA")
        ['a', 'b', 'c', 'A']
        >>> t._get_expr_list("abc()e")
        ['a', 'b', 'c', 'e']
        >>> t._get_expr_list("abc(2+2)e")
        ['a', 'b', 'c', '(2+2)', 'e']
        >>> t._get_expr_list("abc(2+2**(4+3.5))e")
        ['a', 'b', 'c', '(2+2**(4+3.5))', 'e']
        >>>  # allow missing trailing parens
        >>> t._get_expr_list("abc(2+2")
        ['a', 'b', 'c', '(2+2)']
        >>> t._get_expr_list("a..e")
        ['a', 'b', 'c', 'd', 'e']
        >>> t._get_expr_list("a..E")
        ['a', 'E']
        >>> t._get_expr_list("a..Z")
        ['a', 'H']
        >>> t._get_expr_list("e..a")
        ['e', 'd', 'c', 'b', 'a']
        >>> t._get_expr_list("a..z")
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        >>> t._get_expr_list("~z")
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'h']
        >>> t._get_expr_list("xyz")
        ['f', 'g', 'h']
        >>> t._get_expr_list("z")
        ['h']
        >>> t._get_expr_list("~(d/e)")
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', '(d/e)']
        >>> t._get_expr_list("(a..c/2)")
        ['(a/2)', '(b/2)', '(c/2)']
        >>> t._get_expr_list("a(date(base('Monday')+7*a))")
        ['a', "(date(base('Monday')+7*a))"]
        >>> t._get_expr_list("ab(f'{a:04d}-{b:02}')")
        ['a', 'b', "(f'{a:04d}-{b:02}')"]
        '''
        identity = string.ascii_lowercase[:self.cols]
        in_parens = 0
        out = []
        expr = []

        # Allow counting from the right (but only xxyz)
        # only for simple_rearrangement here -- this shold probably refactor to there...
        if '(' not in given and self.cols < 22:
            for a, b in zip("zyxw", reversed(identity)):
                given = given.replace(a, b)
                given = given.replace(a.upper(), b.upper())

        # this is a kuldge to attempt to support ranges in calcs...
        def _replicate(mob):
            '''replicate the string from the mob'''
            prefix, a, b, suffix = mob.groups()
            if prefix is None:
                prefix = ''
            if suffix is None:
                suffix = ''
            a = min(ord(a), ord(identity[-1]))
            b = min(ord(b), ord(identity[-1]))
            if a > b:
                r = range(a, b - 1, -1)
            else:
                r = range(a, b + 1)

            return ''.join([prefix + chr(x) + suffix for x in r])

        given = re.sub(r'(.*?[^a-z])?([a-z])\.\.([a-z])([^a-z].*)?', _replicate, given)

        for c in given:
            if in_parens == 0:
                if c.lower() in identity + '?':
                    out.append(c)
                elif c in '({':
                    in_parens = 1
                    expr = ['(']
                elif c == '~':
                    out.extend(x for x in identity)
                else:
                    pass  # ignore anything else outside parens
            else:
                if c == '}' and in_parens == 1:  # allow } as ) at top level
                    c = ')'
                expr.append(c)
                if c in '({':
                    in_parens += 1
                elif c in ')}':
                    in_parens -= 1
                if in_parens == 0:
                    if len(expr) > 2:  # ignore ()
                        out.append(''.join(expr))
        if in_parens > 0:
            out.append(''.join(expr) + ')' * in_parens)

        return out

    def _rearrange_columns(self, perm):
        '''Re-arrange the columns -- first handle the stack then do the work
        '''

        # empty perm is a no-op
        if not perm:
            return

        # include the stack rows in the data
        stack_rows = len(self.stack)
        self.data.extend(self.stack)
        self.stack.clear()

        # do the work
        self._calculate_data(perm)
        self.cols = len(self.data[0])

        # restore the stack
        for _ in range(stack_rows):
            self.stack.append(self.pop())
        return

    def _calculate_data(self, raw_perm):
        '''Do the work for "arr"
        '''
        # fix up xyz etc and split up the perm into expressions
        expressions = self._get_expr_list(raw_perm)
        identity = string.ascii_lowercase[:self.cols]

        # now do deletions (note that _get_expr_list will have ignored the leading -)
        if raw_perm[0] == '-':
            if all(c in string.ascii_lowercase for c in raw_perm[1:]):
                delenda = list(ord(x) - ord('a') for x in expressions)
                self.data = list(list(x for i, x in enumerate(r) if i not in delenda) for r in self.data)
            else:
                self.messages.append("Only lowercase ASCII allowed after -")
            return

        def _get_value(row, c):
            '''Find a suitable value given the perm character and a row of data
            '''
            return str(random.random()) if c == '?' else row[ord(c) - ord('a')]

        # simple case of re-arrangement and/or random values
        if all(len(x) == 1 and x in identity + '?' for x in expressions):
            self.data = list(list(_get_value(r, x) for x in expressions) for r in self.data)
            return

        # now we have to calculate at least one cell
        desiderata = []
        for x in expressions:
            ok, cc = compile_as_decimal(x)
            if not ok:
                self.messages.append(cc)
                return
            desiderata.append((cc, x))

        values = {
            "rows": len(self.data),
            "cols": self.cols,
            "total": sum(as_decimal(x) for row in self.data for x in row),
            "row_number": 0,
        }
        for k in identity:
            values[k.upper()] = 0  # accumulators

        old_data = self.data.copy()
        self.data.clear()
        self.cols = 0

        for r in old_data:
            for k, v in zip(identity, r):
                flag, values[k] = is_as_number(v)
                if flag:
                    values[k.upper()] += values[k]

            # allow xyz to refer to cells counted from the end...
            # you need this here to allow for xyz in expressions like (y/z)
            for j, k in zip("zyxw", reversed(identity)):
                values[j] = values[k]
                values[j.upper()] = values[k.upper()]

            # and note the line number
            values['row_number'] += 1
            values['row_total'] = sum(as_decimal(x) for x in r)

            new_row = []
            for compiled_code, literal_code in desiderata:
                try:
                    new_value = eval(compiled_code, Panther, values)
                    if isinstance(new_value, tuple):
                        new_row.extend(new_value)
                    elif isinstance(new_value, str) and is_multiplicated(new_value):
                        # unwanted string multiplication...
                        new_row.append(_replace_values(literal_code, values))
                    else:
                        new_row.append(new_value)
                except (KeyError, ValueError, TypeError, NameError, AttributeError, decimal.InvalidOperation):
                    new_row.append(_replace_values(literal_code, values))
                except ZeroDivisionError:
                    new_row.append("-")
            self.append(new_row)

    def _fancy_col_index(self, column_letter):
        '''Find me an index, returns index + T/F to say if letter was upper case

        >>> t = Table()
        >>> a = (1, 2, 3, 4, 5, 6, 7, 8)
        >>> b = (5, 23, 41, 2, 3, 4, 5, 6)
        >>> t.parse_lol((a, b))
        >>> t._fancy_col_index('a')
        (0, False)
        >>> t._fancy_col_index('B')
        (1, True)
        >>> t._fancy_col_index('Z')
        (7, True)
        >>> t._fancy_col_index('5')
        (5, False)
        >>> t._fancy_col_index('!!')
        (None, False)

        '''

        flag = False
        if column_letter in string.ascii_uppercase:
            flag = True
            column_letter = column_letter.lower()

        if column_letter in string.ascii_lowercase:
            column_letter = ord(column_letter) - ord('a')

        try:
            c = int(column_letter)
        except ValueError:
            self.messages.append('?! colspec ' + column_letter)
            return (None, flag)

        if c >= self.cols:
            c = self.cols - 1
        return (c, flag)

    def _sort_rows_by_col(self, col_spec=None):
        '''Sort the table
        By default sort by all columns left to right.

        Sort in groups where the col spec indicates the groups of cols

        a means use row[0] as the key

        abc means use the concatenation of row[0] + row[1] + row[2]

        upper case groups mean reverse sort

        groups are done right to left...

        @ at the front of the colspec means pop first row, sort, then push row bacl
        = at the front of the colspec means plain sort without smarts

        '''
        header = None
        want_smart = True

        if col_spec.startswith('@'):
            col_spec = col_spec[1:]
            header = self.pop(0)

        if col_spec.startswith('='):
            col_spec = col_spec[1:]
            want_smart = False

        if col_spec is None or col_spec == '':
            col_spec = string.ascii_lowercase[:self.cols]

        if looks_like_formula(col_spec):
            self.do(f"arr ({col_spec})~ sort a arr -a")

        else:
            for col in col_spec[::-1]:
                c, want_reverse = self._fancy_col_index(col)
                if c is None:
                    continue
                if want_smart:
                    self.data.sort(key=lambda row: as_numeric_tuple(row[c], want_reverse),
                                   reverse=want_reverse)
                else:
                    self.data.sort(key=lambda row: row[c], reverse=want_reverse)

        if header is not None:
            self.insert(0, header)

    def _remove_duplicates_by_col(self, col_spec):
        '''like uniq, remove row if key cols match the row above
        '''
        header = None
        if '@' in col_spec:
            header = self.pop(0)
            col_spec = col_spec.replace('@', '')

        if col_spec is None or col_spec == '':
            cols_to_check = list(range(self.cols))
        else:
            cols_to_check = []
            for c in col_spec:
                i, _ = self._fancy_col_index(c)
                if i is None:
                    continue
                cols_to_check.append(i)

        if cols_to_check:
            rows_to_delete = []
            previous_t = ''
            for i, row in enumerate(self.data):
                this_t = ' '.join(row[j] for j in cols_to_check)
                if previous_t == this_t:
                    rows_to_delete.append(i)
                else:
                    previous_t = this_t

            for i in reversed(rows_to_delete):
                del self.data[i]

        if header is not None:
            self.insert(0, header)

    def _add_grouping_blanks(self, col_spec):
        '''Add blanks to show groups in given column
        '''
        if not col_spec:
            col_spec = 'a'

        cols_to_check = []
        for c in col_spec:
            i, _ = self._fancy_col_index(c)
            if i is None:
                continue
            cols_to_check.append(i)
        last_tag = ''
        for i, row in enumerate(self.data):
            this_tag = ' '.join(row[j] for j in cols_to_check)
            if i > 0 and this_tag != last_tag and not self.extras[i]:
                self.extras[i].add("blank")
            last_tag = this_tag

    def _show_column_counts(self, col_spec):
        '''show messages with analysis of given cols
        '''
        if not col_spec:
            return

        for c in col_spec:
            i, use_first_for_label = self._fancy_col_index(c)
            if i is None:
                continue
            flags, data = zip(*self.column(i))
            if use_first_for_label:
                label, *data = data
                _, *flags = flags
            else:
                label = chr(ord('a') + i)

            if all(flags):
                analysis = statistical_summary(data)
            else:
                analysis = counting_summary(data, 20)

            self.messages.append(f'# {label}: {analysis}')

    def _roll_by_col(self, col_spec):
        '''Roll columns, up, or down
        '''
        header = None
        if '@' in col_spec:
            header = self.pop(0)
            col_spec = col_spec.replace('@', '')

        if not col_spec:
            self.data.insert(0, self.data.pop())
        else:
            self.data = list(map(list, zip(*self.data)))
            for c in col_spec:
                i, up = self._fancy_col_index(c)
                if i is None:
                    continue
                if up:
                    self.data[i].append(self.data[i].pop(0))
                else:
                    self.data[i].insert(0, self.data[i].pop())
            self.data = list(map(list, zip(*self.data)))

        if header is not None:
            self.insert(0, header)

    def tabulate(self):
        '''Generate nicely lined up rows
        '''
        # this roundabout approach makes tabulate more consistent
        # for speed you could make csv write directly to sys.stdout
        if self.form == 'csv':
            out = io.StringIO()
            w = csv.writer(out, lineterminator=os.linesep)
            w.writerows(self.data)
            for line in out.getvalue().splitlines():
                yield line
            out.close()
            return

        eol_marker = ''
        separator = '  '
        blank_line = None
        comment_marker = None
        ruler = None
        if self.form == 'tex':
            separator = ' & '
            eol_marker = ' \\cr'
            comment_marker = '%'
            blank_line = "\\noalign{\\medskip}"
            ruler = "\\noalign{\\vskip2pt\\hrule\\vskip4pt}"
        elif self.form == 'latex':
            separator = ' & '
            eol_marker = ' \\\\'
            comment_marker = '%'
            blank_line = "\\noalign{\\medskip}"
            ruler = "\\hline"
        elif self.form == 'tsv':
            separator = '\t'
        elif self.form == 'pipe':
            separator = ' | '
            ruler = 'piped'
        else:
            blank_line = ''
            comment_marker = '#'
            ruler = 'plain'

        widths = [max(len(row[i]) for row in self.data) for i in range(self.cols)]
        aligns = []
        for i in range(self.cols):
            booleans, _ = zip(*self.column(i))
            aligns.append('>' if sum(booleans) / len(booleans) > 0.5 else '<')

        def _pipe_rule(w, a):
            '''A rule for piped format, given width and alignment
            '''
            return '-' * (w - 1) + (':' if a == '>' else '-')

        # generate nicely lined up rows
        for i, row in enumerate(self.data):
            for ex in self.extras[i]:
                if ex == 'rule' and ruler is not None:
                    if ruler == "plain":
                        yield ' ' * self.indent \
                            + '-' * (sum(widths) + (self.cols - 1) * len(separator) + len(eol_marker))
                    elif ruler == "piped":
                        yield ' ' * self.indent \
                            + separator.join(_pipe_rule(w, a) for w, a in zip(widths, aligns))
                    else:
                        yield ruler

                elif ex == 'blank' and blank_line is not None:
                    yield blank_line

                elif ex.startswith('#') and comment_marker is not None:
                    yield comment_marker + ex[1:]

            out = []
            for j, cell in enumerate(row):
                out.append(f'{cell:{aligns[j]}{widths[j]}}')

            yield ' ' * self.indent + separator.join(out).rstrip() + eol_marker  # no trailing blanks


def filter():
    parser = argparse.ArgumentParser()
    parser.add_argument("agenda", nargs='*', help="[delimiter.maxsplit] [verb [option]]...")
    parser.add_argument("--file", help="Source file name, defaults to STDIN")
    args = parser.parse_args()

    # Join the agenda args into one string, remove any backslash (for Vim),
    # and split into a list
    agenda = ' '.join(args.agenda).replace('\\', '').split()

    # Get the delimiter from the agenda if possible
    try:
        delim = agenda.pop(0)
    except IndexError:
        delim = ''
    else:
        # If the removed delim starts with alphabetic, put it back and reset delim to None
        if re.match(r'^[a-zA-Z]', delim):
            agenda.insert(0, delim)
            delim = ''

    table = Table()
    fh = open(args.file) if args.file else io.StringIO("" if sys.stdin.isatty() else sys.stdin.read())

    if not delim:
        first_line = fh.readline().strip()
        fh.seek(0)
        # guess delim from content: tex & latex & pipe |
        if first_line.count('&') > 0 and first_line.endswith("\\cr"):
            table.parse_tex(fh)
            table.do('make tex')

        elif first_line.count('&') > 0 and first_line.endswith("\\\\"):
            table.parse_tex(fh)
            table.do('make latex')

        elif first_line.count('|') > 2:
            table.parse_lines(fh, splitter=re.compile(r'\s*\|\s*'))

        else:
            table.parse_lines(fh, splitter=re.compile(r'\s{2,}'))

    elif delim == ',':
        try:
            dialect = csv.Sniffer().sniff(fh.read(1024))
            fh.seek(0)
            table.parse_lol(csv.reader(fh, dialect), filler='-')
        except csv.Error:
            fh.seek(0)
            table.parse_lol(csv.reader(fh))

    else:
        # check for a maxsplit spec ".3", "2.4" etc
        if (m := re.match(r'(\d*)\.(\d+)', delim)) is not None:
            delim = m.group(1)
            if delim == '':
                delim = '2'
            cell_limit = int(m.group(2))
        else:
            cell_limit = 0

        if delim.isdigit():
            in_sep = re.compile(rf'\s{{{delim},}}')
        else:
            in_sep = re.compile(re.escape(delim))

        table.parse_lines(fh, splitter=in_sep, splits=cell_limit)

    table.do(agenda)
    print(table)

    if args.file is not None:
        fh.close()


if __name__ == "__main__":
    filter()

#! /usr/bin/env python3

def t_sorted(*args, reverse=False):
    '''sorted, allowing list of args or a single iterable
    and returning a tuple not a list

    >>> t_sorted((3,1,2))
    (1, 2, 3)

    >>> t_sorted(3,4,5,1,0)
    (0, 1, 3, 4, 5)

    >>> t_sorted(3,4,5,1,0, reverse=True)
    (5, 4, 3, 1, 0)

    '''
    try:
        it = iter(*args)
    except TypeError:
        return tuple(sorted(args, reverse=reverse))
    else:
        return tuple(sorted(it, reverse=reverse))


def t_apply(*args, fun=all):
    '''Apply fun allowing args to be separate or a tuple

    >>> t_apply(0,1,0,1)
    False
    >>> t_apply((True, True, True))
    True
    >>> t_apply(0,1,0,1, fun=sum)
    2
    >>> t_apply((37, 73, 99), fun=sum)
    209

    '''
    try:
        it = iter(*args)
    except TypeError:
        return fun(args)
    else:
        return fun(it)


def t_all(*args):
    '''
    >>> t_all(0,1,1)
    False
    '''
    return t_apply(args)


def t_any(*args):
    '''
    >>> t_any(0,1,1)
    True
    '''
    return t_apply(args, fun=any)


def t_min(*args):
    '''
    >>> t_min(0,1,1)
    0
    '''
    return t_apply(args, fun=min)


def t_minp(*args):
    '''
    >>> t_minp(0,1,5)
    1
    '''
    return min(x for x in args if x)


def t_max(*args):
    '''
    >>> t_max(0,1,1)
    1
    '''
    return t_apply(args, fun=max)


def t_sum(*args):
    '''
    >>> t_sum(0,1,1)
    2
    '''
    return t_apply(args, fun=sum)

def length(s):
    '''Length of strings *or* integers
    >>> length("This")
    4
    >>> length(987613)
    6

    '''
    return len(str(s))

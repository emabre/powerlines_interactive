def to_numbers(*args):
    '''
    args: iterable of numbers or strings (which may be converted to complex)
    returns: the numbers (or the strings converted to numbers) contained insisde args
    '''

    for a in args:
        print(a.strip())

    t = tuple(map(lambda a: complex(a.strip()) if isinstance(a, str) else a,
                  args)
             )
    return t
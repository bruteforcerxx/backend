def bal_converter(x):
    print(len(x))
    if len(x) == 6:
        a = x[0]
        b = x[1:]
        return f'{a},{b}'
    elif len(x) == 7:
        a = x[:2]
        b = x[2:]
        return f'{a},{b}'
    elif len(x) == 8:
        a = x[:3]
        b = x[3:]
        return f'{a},{b}'
    elif len(x) == 9:
        a = x[0]
        b = x[1:4]
        c = x[4:]
        return f'{a},{b},{c}'
    elif len(x) == 10:
        a = x[:2]
        b = x[2:5]
        c = x[5:]
        return f'{a},{b},{c}'
    elif len(x) == 11:
        a = x[:2]
        b = x[2:5]
        c = x[5:]
        return f'{a},{b},{c}'
    else:
        return x
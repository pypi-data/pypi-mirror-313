def lenzf(o):
    if type(o)==int:
        o = abs(o)
        if o==0:
            return 0
        else:
            s=0
            while o//(10**s)!=0:
                s+=1
            return s
    elif type(o)==tuple or type(o)==list or type(o)==dict or type(o)==set or type(o) == bytes or type(o) == bytearray or type(o) == range:
        s=0
        for i in o:
            s+=1
        return s
    elif type(o) == float:
        parts = str(o).split('.')
        before_decimal = 0
        for digit in parts[0].lstrip('0'):
            if digit.isdigit():
                before_decimal += 1
        after_decimal = 0
        for digit in parts[1].rstrip('0'):
            after_decimal += 1
        return [before_decimal, after_decimal]
    else:
        raise TypeError(f"Unsupported type '{type(o).__name__}' in lens() function.")
#coding=utf-8

maps = {
    '"': '"', '\\': '\\', '/': '/',
    'b': '\b', 'f': '\f', 'n': '\n', 'r': '\r', 't': '\t',
}
bmaps = {k.encode()[0]:v.encode() for k,v in maps.items()}
def ustr(s):
    i = 0
    l=len(s)
    rs = ""
    while i<l:
        c = s[i]
        i+=1
        if c == '\\':
            x = s[i]
            i+=1
            if x == 'u':
                v = int(s[i:i+4], 16)
                r = chr(v)
                rs+=r
                i+=4
                continue
            elif x in maps:
                r = maps[x]
                rs+=r
                continue
        rs+=c
    return rs

pass
bl2,bu = b'\\u'
def ubytes(s, code = "utf-8"):
    i = 0
    l=len(s)
    rs = b""
    while i<l:
        c = s[i]
        i+=1
        if c == bl2:
            x = s[i]
            i+=1
            if x == bu:
                v = int(s[i:i+4], 16)
                r = chr(v).encode(code)
                rs+=r
                i+=4
                continue
            elif x in bmaps:
                r = bmaps[x]
                rs+=r
                continue
        rs+=bytes([c])
    return rs

pass
def ub2s(s, code = "utf-8"):
    return ubytes(s, code).decode(code)

pass
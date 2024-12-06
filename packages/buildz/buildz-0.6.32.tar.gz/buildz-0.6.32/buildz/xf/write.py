
from .writer import mg, itemz, base, conf
from .writer.deal import listz, mapz, strz, reval, jsonval
from . import file
pts = [
    "[\+\-]?\d+",
    "[\+\-]?\d+\.\d+",
    "[\+\-]?\d+e[\+\-]?\d+",
    "null",
    "true",
    "false",
    "[\s\S]*[\n\r\t\:\[\]\{\}\(\)\,\:\=\'\<\>\" \|\#\;\/][\s\S]*"
]
def build(json_format=False):
    mgs = mg.Manager()
    if not json_format:
        mgs.add(strz.StrDeal('"','"', pts))
        mgs.add(reval.ValDeal(float, lambda x:str(x)))
        mgs.add(reval.ValDeal(int, lambda x:str(x)))
        mgs.add(reval.ValDeal(type(None), lambda x:'null'))
        mgs.add(reval.ValDeal(bool, lambda x:'true' if x else 'false'))
    else:
        mgs.add(jsonval.ValDeal())
    mgs.add(listz.ListDeal('[',']',','))
    mgs.add(mapz.MapDeal('{','}',':',','))
    return mgs

pass
def dumps(obj, bytes = 0, format = 0, deep = 0, json_format= 0):
    cf = conf.Conf()
    cf.set(bytes=bytes, format=format, deep=deep)
    if format:
        cf.set(set=1, prev=1,line=4, spc=' ')
    else:
        cf.set(set=1, prev=1)
    mgs = build(json_format)
    return mgs.dump(obj, cf)

pass

def dumpf(obj, filepath, bytes = 0, format = 0, deep = 0, json_format= 0, mode = 'w'):
    s = dumps(obj, bytes = bytes, format = format, deep = deep, json_format= json_format)
    file.fwrite(s, filepath, mode)

pass

def dump(output, obj, *argv, **maps):
    rs = dumps(obj, *argv, **maps)
    output(rs)

pass

#coding=utf-8
import os
"""
读写文件再简化
"""
def fread(fp, mode='rb'):
    with open(fp, mode) as f:
        return f.read()

pass
read=fread
def freads(fp, mode = 'rb', size=1024*1024):
    with open(fp, mode) as f:
        while True:
            bs = f.read(size)
            if len(bs)==0:
                break
            yield bs

pass
reads=freads

def fwrite(ct, fp, mode = 'wb'):
    with open(fp, mode) as f:
        f.write(ct)

pass
write = fwrite
def fwrites(cts, fp, mode = 'wb'):
    with open(fp, mode) as f:
        for ct in cts:
            f.write(ct)

pass
writes = fwrites

def makedir(dp):
    if os.path.isdir(dp):
        return
    os.makedirs(dp)

pass
def makefdir(fp):
    fp = os.path.abspath(fp)
    dp = os.path.dirname(fp)
    makedir(dp)

pass

def dirpath(fp, n=1):
    for i in range(n):
        fp = os.path.dirname(fp)
    return fp

pass

dirname = dirpath

def fcover(filepath, wsize = 1024*10):
	st = os.stat(filepath)
	size = st.st_size
	bs = b'a'*wsize
	with open(filepath, 'wb') as f:
		for i in range(0, size, wsize):
			f.write(bs)

pass
cover = fcover
def removes(fp, cover = False):
    if not os.path.exists(fp):
        return
    if os.path.isfile(fp):
        #print(f"remove file '{fp}'")
        if cover:
            fcover(fp)
        os.remove(fp)
        return
    fps = os.listdir(fp)
    fps = [os.path.join(fp, f) for f in fps]
    [removes(f, cover) for f in fps]
    #print(f"removedirs '{fp}'")
    os.rmdir(fp)

pass
def decode(s, coding = 'utf-8'):
    coding = coding.lower()
    xcoding = 'utf-8'
    if coding == 'utf-8':
        xcoding = 'gbk'
    try:
        return s.decode(coding)
    except:
        return s.decode(xcoding)

pass

def sread(fp, code='utf-8', mode='r'):
    if mode.find("b")<0:
        mode+="b"
    return decode(read(fp, mode), code)

pass
def swrite(dt, fp, code="utf-8", mode = "w"):
    if mode.find("b")<0:
        mode+="b"
    if type(dt)!=bytes:
        dt = dt.encode(code)
    write(dt, fp, mode)

pass

def is_abs(fp):
    if fp is None:
        return False
    if fp.strip()=="":
        return False
    fp = fp.strip().replace("\\", "/")
    if fp[0]=="/":
        return True
    arr = fp.split("/")
    if arr[0].find(":")>=0:
        return True
    return False

pass
    
#Kage Park
#Kage's important(basic) libraries
#Open this source to the public to want
#If you find any issue then please leave a note on GitHub
#Basically I designed it should work in AI style.
#(basically Not crashing, keep doing process with possibly 
#  data like human understanding, if give a option then it 
#  can make to crash for the issue)
import os
import gc
import re
import bz2
import sys
import ast
import copy
import json
import gzip
import zlib
import time
import uuid
import fcntl
import random
import shutil
import codecs
import ctypes
import socket
import struct
import pprint
import pickle
import inspect
import getpass
import warnings
import datetime
import platform
import traceback
import subprocess
from threading import Thread
#from datetime import datetime
from importlib import import_module
# If importing "from kmport import *" then
# adding "global  printf_log_base",
# adding .... then use printf_log_base,... parameter
printf_log_base=None
printf_caller_detail=False
printf_caller_tree=False
printf_caller_name=False
printf_scr_dbg=False
printf_ignore_empty=True
printf_dbg_empty=False
krc_ext='python'

krc_define={
  'GOOD':[True,'True','Good','Ok','Pass','Sure',{'OK'}],
  'FAIL':[False,'False','Fail',{'FAL'}],
  'NONE':[None,'None','Nothing','Empty','Null','N/A',{'NA'}],
  'IGNO':['IGNO','Ignore',{'IGN'}],
  'ERRO':['ERR','Erro','Error',{'ERR'}],
  'WARN':['Warn','Warning',{'WAR'}],
  'UNKN':['Unknown','UNKN',"Don't know",'Not sure',{'UNK'}],
  'JUMP':['Jump',{'JUMP'}],
  'TOUT':['TimeOut','Time Out','TMOUT','TOUT',{'TOUT'}],
  'REVD':['Cancel','Canceled','REV','REVD','Revoked','Revoke',{'REVD'}],
  'LOST':['Lost','Connection Lost','Lost Connection',{'LOST'}],
  'NFND':['File not found','Not Found','Can not found',{'NFND'}],
  'STOP':['Stop','Stopped',{'STOP'}]
}
# REVD(Cancel) : Whole Stop 
# STOP         : Currently running process stop
# UNKN(Unknown): UNKN or not defined return code

###### Python Return #######
# True     : Good
# False    : False
# 1        : Good level user define
# 0        : False level user define (like as cancel)
#----------------------------------------------------
# if rc is True  : rc only True then True
# if rc is False : rc only False then True
# if rc == True  : rc is 1 or True then True
# if rc == False : rc is 0 or False then True
# if rc is 1     : rc only 1 then True
# if rc is 0     : rc only 0 then True

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

__version__='2.0.15'

'''
Base Module
if you want requests then you need must pre-loaded below module when you use compiled binary file using pyinstaller

example)
from http.cookies import Morsel
Import('import requests')

Without build then import requests is ok. but if you build it then it need pre-loaded Morsel module for Import('import requests') command
'''
class PRINTED:
    def __init__(self,data=None,mode=None,mode_data=True):
        if type(data).__name__ == 'PRINTED':
            self.data=data.data
        elif isinstance(data,dict):
            self.data=data
        else:
            self.data={}
        if isinstance(self.data,dict) and mode:
            mode=list(mode) if isinstance(mode,str) else [mode]
            for dd in mode:
                self.data[dd]=mode_data if isinstance(mode_data,bool) else True
        elif isinstance(data,bool):
            self.data['a']=data
    def Put(self,mode=None,value=None):
        if mode and isinstance(value,bool):
            mode=list(mode) if isinstance(mode,str) else [mode]
            for dd in mode:
                self.data[dd]=value
    def Del(self,mode=None):
        if isinstance(self.data,dict) and mode:
            mode=list(mode) if isinstance(mode,str) else [mode]
            for dd in mode:
                if dd in self.data: self.data.pop(dd)
        elif self.data is True:
            self.data=False
    def Get(self,mode=None):
        if isinstance(self.data,dict) and mode:
            mode=list(mode) if isinstance(mode,str) else [mode]
            for dd in mode:
                #if dd in ['d','a'] and self.data: return True
                if dd == 'd' and True in self.data.values(): return True
                elif dd == 'a': # auto(a): a,s,e
                   if self.data.get('a') or self.data.get('s') or self.data.get('e'):
                       return True
                # s,e,f
                elif self.data.get(dd) is True: return True
        elif self.data is True:
            return True
        return False

printf_newline_info=PRINTED()

def Global_bak(loc=0,ignores=['__builtins__','__spec__','__loader__','__cached__','__doc__','__package__','__name__','__file__','__annotations__'],InFunc=False):
    env={'__name__':[],'__file__':[]}
    stacks=inspect.stack()
    max_n=len(stacks)
    abs_loc=abs(loc)
    if loc != 0 and 0 < max_n - abs_loc < max_n:
        mod_name=sys._getframe(loc).f_code.co_name
        a=dict(inspect.getmembers(stacks[loc][0]))["f_globals"]
        env['__name__'].append(mod_name)
        for i in a:
            if i == '__file__': env['__file__'].append(a[i])
            if i in ignores: continue
            if ii <= 2:
                env[i]=a[i]
            else:
                if i not in env: env[i]=a[i]
        if InFunc:
            b=dict(inspect.getmembers(stacks[loc][0]))["f_locals"]
            for i in b:
                if i in ignores: continue
                if i not in env: env[i]=b[i]
    else:
        for ii in range(1,max_n):
            mod_name=sys._getframe(ii).f_code.co_name
            a=dict(inspect.getmembers(stacks[ii][0]))["f_globals"]
            env['__name__'].append(mod_name)
            for i in a:
                if i == '__file__': env['__file__'].append(a[i])
                if i in ignores: continue
                if ii <= 2:
                    env[i]=a[i]
                else:
                    if i not in env: env[i]=a[i]
            if InFunc:
                b=dict(inspect.getmembers(stacks[ii][0]))["f_locals"]
                for i in b:
                    if i in ignores: continue
                    if i not in env: env[i]=b[i]
    return env

def GetGlobal(key=None,loc=None,ignores=[],default=None,_type_='global',UptoTop=False):
    _ignores_=['__builtins__','__spec__','__loader__','__cached__','__doc__','__package__','__name__','__file__','__annotations__']
    if isinstance(ignores,list) and ignores: _ignores_=_ignores_+ignores
    # overwriting Top data to my script
    # It it need backorder?
    env={'__name__':[],'__file__':[]}
    stacks=inspect.stack()
    max_n=len(stacks)
    if IsIn(loc,['top']): loc=-1
    elif IsIn(loc,['bottom']): loc=0
    def GetParameters(env,ii,stacks,key=None,UptoTop=False):
        if _type_ == 'global': #global
            a=dict(inspect.getmembers(stacks[ii][0]))["f_globals"]
        else: # local
            a=dict(inspect.getmembers(stacks[ii][0]))["f_locals"]
        if key and not UptoTop:
            return a.get(key,{'none'})
        else:
            for i in a:
                if i in _ignores_: continue
                if i == '__file__': env['__file__'].append(a[i])
                if UptoTop or i not in env: 
                    env[i]=a[i] 
            return {'none'}
    if IsInt(loc): # Read special point's variables
        loc=int(loc)
        if loc >= 0:
            loc=loc+1 if loc < max_n-1 else max_n
        else:
            loc = 1 if abs(loc) >= max_n else max_n + loc
        mod_name=sys._getframe(loc).f_code.co_name
        _a_=GetParameters(env,loc,stacks,key)
        if key:
            if _a_ != {'none'}: return _a_
            return default
        env['__name__'].append(mod_name)
    else:
        if isinstance(loc,str) and ':' in loc:
            loc_a=loc.split(':')
            start=int(loc_a[0]) if IsInt(loc_a[0]) else 0
            end=int(loc_a[1]) if IsInt(loc_a[1]) else max_n
            if abs(start) >= max_n-1:
                start=1 if start<=0 else max_n-1
            else:
                if start >= 0 : start=start+1
            if abs(end) >= max_n-1:
                if end>0: end=max_n
        else:
            start=1
            end=max_n
        for ii in range(start,end): # Read All available's variables
            mod_name=sys._getframe(ii).f_code.co_name
            if key and not UptoTop: # found key
                _a_=GetParameters(env,ii,stacks,key)
                if _a_ != {'none'}: return _a_
            else:
                env['__name__'].append(mod_name)
                GetParameters(env,ii,stacks,UptoTop=UptoTop)
            #if mod_name == '<module>': break # My App's Top then break
    if key:
        if UptoTop:
            return env.get(key,default) #over write then here
        return default #not found key
    return env

def SetGlobal(name,value,ignores=[],loc=None,Append=True,_type_='global',Top=True):
    _ignores_=['__builtins__','__spec__','__loader__','__cached__','__doc__','__package__','__name__','__file__','__annotations__']
    if isinstance(ignores,list) and ignores: _ignores_=_ignores_+ignores
    if Top: Append=True
    stacks=inspect.stack()
    max_n=len(stacks)
    if IsIn(loc,['top']): loc=-1
    elif IsIn(loc,['bottom']): loc=0
    if IsInt(loc): # Read special point's variables
        loc=int(loc)
        if loc >= 0:
            loc=loc+1 if loc < max_n-1 else max_n
        else:
            loc = 1 if abs(loc) >= max_n else max_n + loc
        if _type_ == 'global': #global
            a=dict(inspect.getmembers(stacks[loc][0]))["f_globals"]
        else: # local
            a=dict(inspect.getmembers(stacks[loc][0]))["f_locals"]
        if Top:
            #if name not in a:
            if Get(a,name,default={'none'}) == {'none'}:
                if _type_ == 'global': #global
                    a=dict(inspect.getmembers(stacks[-1][0]))["f_globals"]
                else: # local
                    a=dict(inspect.getmembers(stacks[-1][0]))["f_locals"]
        return Set(a,name,value,force=Append)
        #if Append: #If not replaced variable then adding at my Top
        #    a[name]=value
        #    return True
        #else:
        #    if name in a:
        #        a[name]=value
        #        return True
    else:
        if not Top:
            if isinstance(loc,str) and '-' in loc:
                loc_a=loc.split('-')
                start=int(loc_a[0])+1 if IsInt(loc_a[0]) else 1
                if start >= max_n -1: start=max_n-1
                end=int(loc_a[1]) if IsInt(loc_a[1]) else max_n
                if end >= max_n: end=max_n
            else:
                start=1
                end=max_n
            for ii in range(start,end): # Read All available's variables
                if _type_ == 'global': #global
                    a=dict(inspect.getmembers(stacks[loc][0]))["f_globals"]
                else: # local
                    a=dict(inspect.getmembers(stacks[loc][0]))["f_locals"]
                #if name in a:
                #    a[name]=value
                #    return True
                if Get(a,name,default={'none'}) != {'none'}:
                    return Set(a,name,value)
        if Append:
            if _type_ == 'global': #global
                a=dict(inspect.getmembers(stacks[-1][0]))["f_globals"]
            else: # local
                a=dict(inspect.getmembers(stacks[-1][0]))["f_locals"]
            return Set(a,name,value,force=True)
            #a[name]=value
            #return True
    return False #Can not add (Something error)

def StdOut(msg):
    '''
    Standard Output Print without new line symbol
    '''
    try:
        if type(msg).__name__ == 'bytes':
            sys.stdout.buffer.write(msg)
        else:
            sys.stdout.write(msg)
        sys.stdout.flush()
    except:
        StdErr('Wrong output data format\n')

def StdErr(msg):
    '''
    Standard Error Print without new line symbol
    '''
    try:
        sys.stderr.write(msg)
    except:
        sys.stderr.write('Wrong Error data format\n')
    sys.stderr.flush()

def PyVer(*ver,**opts):
    '''
    python version check
    '''
    cver=None
    msym=None
    ver_sym=['=','==','>','<','>=','<=','!=']
    if len(ver) > 0:
        if ver[0] in ver_sym:
            msym=ver[0]
        else:
            cver='{}'.format(ver[0])
        if len(ver) > 1:
            if msym:
                for i in ver[1:]:
                    if cver:
                        cver=cver+'.{}'.format(i)
                    else:
                        cver='{}'.format(i)
            else:
                for i in ver[1:]:
                    if i in ver_sym:
                        msym=i
                        break
                    else:
                        cver=cver+'.{}'.format(i)
    if cver is None:
        if opts.get('main'): cver='{}'.format(opts.get('main'))
        if cver and opts.get('miner') and '.' not in cver: cver='{}.{}'.format(cver,opts.get('miner'))
    if cver is None: return '{}.{}'.format(sys.version_info[0],sys.version_info[1])
    if msym is None: msym=opts.get('msym','==')
    if msym=='=': msym='=='
    cver_a=cver.split('.')
    cver_l=len(cver_a)
    for x in range(0,len(sys.version_info)):
        if x < cver_l-1:
            cmsym=msym+'=' if '=' not in msym else msym
            if not eval('{} {} {}'.format(sys.version_info[x],cmsym,cver_a[x])):
                return False
        elif x == cver_l-1:
            if not eval('{} {} {}'.format(sys.version_info[x],msym,cver_a[x])):
                return False
    return True

def find_executable(executable,path=None):
    if not Type(executable,'str',data=True): return None
    if not Type(path,'str',data=True):
        path=os.environ['PATH']
    path_a=path.split(os.pathsep)
    if os.name == 'os2':
        (base,ext)=os.path.splitex(executable)
        if not ext:
            executable=executable+'.exe'
    elif sys.platform == 'win32':
        (base,ext)=os.path.splitex(executable)
        if not ext:
            executable=executable+'.exe'
    for p in path_a:
        f=os.path.join(p,executable)
        if os.path.isfile(f):
            return f
    return None

def ByteName(src):
    '''
    Get Byte type name
    '''
    if PyVer(3) and isinstance(src,bytes):
        if src.startswith(b'\xff\xfe\x00\x00') and src.endswith(b'\x00\x00\x00'):
            return True,'utf-32-le'
        elif src.startswith(b'\x00\x00\x00') and src.endswith(b'\xff\xfe\x00\x00'):
            return True,'utf-32-be'
        elif src.startswith(b'\xff\xfe') and src.endswith(b'\x00'):
            return True,'utf-16-le'
        elif src.startswith(b'\x00') and src.endswith(b'\xff\xfe'):
            return True,'utf-16-be'
        else:
            return True,'bytes'
    return False,None

def Bytes(src,**opts):
    '''
    Convert data to bytes data
    '''
    encode=opts.get('encode','utf-8')
    default=opts.get('default',{'org'})
    def _bytes_(src,encode,default):
        if type(src).__name__ == 'unicode': src=str(src)
        if isinstance(src,bytes): return src
        if isinstance(src,str):
            try:
                return bytes(src,encode)
            except:
                pass
        if default in ['org',{'org'}]: return src
        return default

    if isinstance(src,list):
        return [ _bytes_(x,encode,default) for x in src ]
    elif isinstance(src,tuple):
        return tuple([ _bytes_(x,encode,default) for x in src ])
    elif isinstance(src,dict):
        for ii in src:
            if isinstance(src[ii],(list,tuple,dict)):
                src[ii]=Bytes(src[ii],encode=encode,default=default)
            else:
                src[ii]=_bytes_(src[ii],encode,default)
        return src
    else:
        return _bytes_(src,encode,default)
def Int2Bytes(src,default='org'):
    try:
        #struct.pack('>I', src)[1:]
        #struct.pack('>L', src)[1:]
        return struct.pack('>BH', src >> 16, src & 0xFFFF)
    except:
        if default in ['org',{'org'}]: return src
        return default

def Bytes2Int(src,encode='utf-8',default='org'):
    if PyVer(3):
        bsrc=Bytes(src,encode=encode)
        if isinstance(bsrc,bytes):
            return int(bsrc.hex(),16)
        if default in ['org',{'org'}]: return src
        return default
    try:
        return int(src.encode('hex'),16)
    except:
        if default in ['org',{'org'}]: return src
        return default

class STR(str):
    def __init__(self,src,byte=None):
        if isinstance(byte,bool):
            if byte:
                self.src=Bytes(src)
            else:
                self.src=Str(src)
        else:
            self.src=src

    def Rand(self,length=8,strs=None,mode='*'):
        return Random(length=length,strs=strs,mode=mode)

    def Cut(self,head_len=None,body_len=None,new_line='\n',out=str):
        if not isinstance(self.src,str):
           self.src='''{}'''.format(self.src)
        return Cut(self.src,head_len,body_len,new_line,out)

    def Space(num=1,fill=' ',mode='space'):
        return Space(num,fill,mode)

    def Reduce(self,start=0,end=None,sym=None,default=None):
        if isinstance(self.src,str):
            if sym:
                arr=self.src.split(sym)
                if isinstance(end,int):
                    return Join(arr[start:end],symbol=sym)
                else:
                    return Join(arr[start],symbol=sym)
            else:
                if isinstance(end,int):
                    return self.src[start:end]
                else:
                    return self.src[start:]
        return default

    def Find(self,find,src='_#_',prs=None,sym='\n',pattern=True,default=[],out=None,findall=True,word=False,line_num=False,peel=None):
        if IsNone(src,chk_val=['_#_'],chk_only=True): src=self.src
        return FIND(src).Find(find,prs=prs,sym=sym,default=default,out=out,findall=findall,word=word,mode='value',line_num=line_num,peel=peel)

    def Index(self,find,start=None,end=None,sym='\n',default=[],word=False,pattern=False,findall=False,out=None):
        if not isinstance(self.src,str): return default
        rt=[]
        source=self.src.split(sym)
        for row in range(0,len(source)):
            for ff in self.Find(find,src=source[row],pattern=pattern,word=word,findall=findall,default=[],out=list):
                if findall:
                    rt=rt+[(row,[m.start() for m in re.finditer(ff,source[row])])]
                else:
                    idx=source[row].index(ff,start,end)
                    if idx >= 0:
                        rt.append((row,idx))
        if rt:
            if out in ['tuple',tuple]: return tuple(rt)
            if out not in ['list',list] and len(rt) == 1 and rt[0][0] == 0:
                if len(rt[0][1]) == 1:return rt[0][1][0]
                return rt[0][1]
            return rt
        return default

    def Replace(self,replace_what,replace_to,default=None):
        if isinstance(self.src,str):
            if replace_what[-1] == '$' or replace_what[0] == '^':
                return re.sub(replace_what, replace_to, self.src)
            else:
                head, _sep, tail = self.src.rpartition(replace_what)
                return head + replace_to + tail
        return default

    def RemoveNewline(self,src='_#_',mode='edge',newline='\n',byte=None):
        if IsNone(src,chk_val=['_#_'],chk_only=True): src=self.src
        if isinstance(byte,bool):
            if byte:
                src=Bytes(src)
            else:
                src=Str(src)
        src_a=Split(src,newline,default=False,listonly=False)
        if src_a is False:
            return src
        if mode in ['edge','both']:
            if not src_a[0].strip() and not src_a[-1].strip():
                return Join(src_a[1:-1],symbol=newline)
            elif not src_a[0].strip():
                return Join(src_a[1:],symbol=newline)
            elif not src_a[-1].strip():
                return Join(src_a[:-1],symbol=newline)
        elif mode in ['first','start',0]:
            if not src_a[0].strip():
                return Join(src_a[1:],symbol=newline)
        elif mode in ['end','last',-1]:
            if not src_a[-1].strip():
                return Join(src_a[:-1],symbol=newline)
        elif mode in ['*','all','everything']:
            return Join(src_a,symbol='')
        return src

    def Tap(self,**opts):
        fspace=opts.get('space',opts.get('fspace',''))
        nspace=opts.get('nspace',fspace)
        sym=opts.get('sym',opts.get('new_line','\n'))
        default=opts.get('default','org')
        NFLT=opts.get('NFLT',False)
        out=opts.get('out',str)
        mode=opts.get('mode','space')
        if isinstance(fspace,str):
            fspace=len(fspace)
        return WrapString(self.src,fspace=fspace,nspace=nspace,new_line=sym,NFLT=NFLT,mode=mode)

def Str(src,**opts):
    '''
    Convert data to String data
    encode : default 'utf-8','latin1','windows-1252'
    default : return to original value, if you define default value then return to the defined value
    mode : auto, if exist data then convert to string, not then return to the form.
           'force','fix','fixed' : everything convert to string
    remove: if you want remove data then define here. (:whitespace: will remove white space to single space)
    color_code:  <color>[:<attr>]
    '''
    encode=opts.get('encode',None)
    default=opts.get('default','org')
    mode=opts.get('mode','auto')
    remove=opts.get('remove',None)
    color_code=opts.get('color_code')

    color_db=opts.get('color_db',{'color':
                                   {'blue': 34, 'grey': 30, 'yellow': 33, 'green': 32, 'cyan': 36, 'magenta': 35, 'white': 37, 'red': 31},
                                  'bg':{'cyan': 46, 'white': 47, 'grey': 40, 'yellow': 43, 'blue': 44, 'magenta': 45, 'red': 41, 'green': 42},
                                  'attr':{'reverse': 7, 'blink': 5,'concealed': 8, 'underline': 4, 'bold': 1}})

    if isinstance(color_code,str):
        color_code_a=color_code.split(':')
        cmode=color_code_a[1] if len(color_code_a) == 2 else None
        color=color_code_a[0]
        if cmode:
            color_code=color_db.get(cmode,{}).get(color)
        else:
            color_code=color_db.get('color',{}).get(color)

    if not isinstance(encode,(str,list,tuple)): encode=['utf-8','latin1','windows-1252']
    def _byte2str_(src,encode,remove=None,color_code=None):
        if isinstance(encode,str): encode=[encode]
        byte,bname=ByteName(src)
        if byte:
            if bname == 'bytes':
                for i in encode:
                    try:
                        if remove:
                            src_d=src.decode(i)
                            if IsSame(remove,':whitespace:'):
                                return ' '.join(src_d.split())
                            elif remove in src_d:
                                return src_d.replace(remove,'')
                        return src.decode(i)
                    except:
                        pass
            else:
                try:
                    if remove:
                        src_d=src.decode(bname)
                        if IsSame(remove,':whitespace:'):
                            return ' '.join(src_d.split())
                        elif remove in src_d:
                            return src_d.replace(remove,'')
                    return src.decode(bname)
                except:
                    pass
        elif type(src).__name__=='unicode':
            for i in encode:
                try:
                    if remove:
                        src_d=src.encode(i)
                        if IsSame(remove,':whitespace:'):
                            return ' '.join(src_d.split())
                        elif remove in src_d:
                            return src_d.replace(remove,'')
                    return src.encode(i)
                except:
                    pass

        if isinstance(color_code,int) and color_code and IsNone(os.getenv('ANSI_COLORS_DISABLED')):
            reset='''\033[0m'''
            fmt_msg='''\033[%dm%s'''
            msg=fmt_msg % (color_code,src)
            return msg+reset
        return src
    tuple_data=False
    if isinstance(src,tuple):
        src=list(src)
        tuple_data=True
    if isinstance(src,list):
        for i in range(0,len(src)):
            if isinstance(src[i],list):
                src[i]=Str(src[i],encode=encode,remove=remove)
            elif isinstance(src[i],dict):
                for z in src[i]:
                    if isinstance(src[i][z],(dict,list)):
                        src[i][z]=Str(src[i][z],encode=encode,remove=remove)
                    else:
                        src[i][z]=_byte2str_(src[i][z],encode,remove)
            else:
                src[i]=_byte2str_(src[i],encode)
    elif isinstance(src,dict):
        for i in src:
            if isinstance(src[i],(dict,list)):
                src[i]=Str(src[i],encode=encode,remove=remove,color_code=color_code)
            else:
                src[i]=_byte2str_(src[i],encode,remove,color_code=color_code)
    else:
        src=_byte2str_(src,encode,remove,color_code=color_code)

    # Force make all to string
    if mode not in ['force','fix','fixed'] and isinstance(src,(list,tuple,dict)):
        if tuple_data: return tuple(src)
        return src
    return '''{}'''.format(src)

def Strings(*src,merge_symbol=' ',excludes=None,split_symbol=' ',mode=None):
    '''
    merge multiple strings to single string
    merge_symbol=' ' : default ' '. merge with that symbol between strings
    split_symbol=' ' : default ' '. split each strings with the symbol for check excludes
    excludes   : excluding strings(str with comma, list, tuple), which is not support space
    '''
    def string_to_shell_line(src):
        new_shell_line=''
        src_a=src.split('\n')
        src_mx=len(src_a)
        src_m=len(src_a)-1
        for i in range(0,src_mx):
            i_a=src_a[i].strip().split()
            if i_a:
                if i_a[-1] in ['do','then','else']:
                    new_shell_line=new_shell_line+' '+src_a[i].lstrip()
                else:
                    if i >= src_m:
                        new_shell_line=new_shell_line+' '+src_a[i].lstrip()
                    else:
                        new_shell_line=new_shell_line+' '+src_a[i].lstrip()+';'
        return new_shell_line

    out=[]
    if mode == 'shell':
        if isinstance(src,str):
            return string_to_shell_line(src)
        elif isinstance(src,tuple) and len(src) == 1 and isinstance(src[0],str):
            return string_to_shell_line(src[0])
    else:
        if isinstance(excludes,(str,list,tuple)):
            if isinstance(excludes,str):
                excludes=excludes.split(',')
        if isinstance(excludes,(list,tuple)) and excludes:
            for i in src:
                i_o=[]
                if Type(i,('str','bytes')):
                    for ii in Split(i,split_symbol):
                        if IsIn(ii,excludes): continue
                        i_o.append(ii)
                if i_o: out.append(Join(i_o,symbol=split_symbol))
            return Join(out,symbol=merge_symbol)
        else:
            return Join(src,symbol=merge_symbol)
        
            
def Default(a,b=None):
    '''
    Make a return value
    b is org then return original value a
    if b not org then return b 
    '''
    if b in ['org','original',{'org'}]:
        return a
    return b

def Peel(i,mode=True,default='org',err=True,output_check=True):
    '''
    Peel list,tuple,dict to data, if not peelable then return original data
      - single data : just get data
      - multi data  : get first data
    if peeled data is None then return default
    default : 'org'(default) : return original data
    err     : True :(default) if not single data then return default, False: whatever it will return first data
    mode    : True :(default), peeling data, False: not peeling(return original)
    output_check: True:(default) If peeled data is list,tuple,dict then return default, False: just return peeled data
    '''
    if mode is False: return i
    elif mode == 'force':
        err=False
        output_check=False
    if isinstance(i,(list,tuple,dict)):
        #Error condition
        if len(i) == 0: return Default(i,default)
        if len(i) > 1:
            if err is True: return Default(i,default)
        rt=i[0] if isinstance(i,(list,tuple)) else i[Next(i)]
        if output_check is True:
            #Check output data format
            if isinstance(rt,(list,tuple,dict)):
                return Default(i,default)
        return rt
    else:
        #Not peelable
        return i

def Int(i,default='org',sym=None,err=False):
    '''
    Convert data to Int data when possible. if not then return default (original data)
    support data type: int,float,digit number,list,tuple
    default: (default org)
        org : fail then return or keeping the input data
        True,False,None: fail then return default value in single data or ignore the item in list
    sym     : split symbol when input is string
    err     : 
        False: replace data for possible positions
        True : if convert error in list/tuple then return default
    '''
    if isinstance(i,bool): return Default(i,default)
    if isinstance(i,int): return i
    i_type=TypeName(i)
    if i_type in ('str','bytes'):
        if sym:
            sym=Bytes(sym) if i_type == 'bytes' else Str(sym)
            i=i.split(sym)
            i_type=TypeName(i)
        else:
            try:
                return int(float(i))
            except:
                return Default(i,default)
    if i_type in ('list','tuple'):
        tuple_out=True if i_type == 'tuple' else False
        rt=[]
        for a in i:
           try:
               rt.append(int(float(a)))
           except:
               if err: return Default(i,default)
               #rt.append(a)
               rt.append(Default(a,default))
        return tuple(rt) if tuple_out else rt
    return Default(i,default)

def Join(*inps,symbol='_-_',byte=None,ignore_type=(dict,bool,None),ignore_data=(),append_front='',append_end='',default=None,err=False):
    '''
    Similar as 'symbol'.join([list]) function
    '''
    def _ignore_(src,ignore_type,ignore_data):
        rt=[]
        for i in src:
            if type(i) in ignore_type: continue
            elif ignore_data and i in ignore_data: continue
            rt.append(i)
        return rt
    if ignore_type:
        if None in ignore_type:
            ignore_type=list(ignore_type)
            ignore_type[ignore_type.index(None)]=type(None)
    src=[]
    if len(inps) == 1 and isinstance(inps[0],(list,tuple)):
        src=src+_ignore_(inps[0],ignore_type,ignore_data)
    # if missing symbol option then just take end of inputs
    elif len(inps) >=2:
        mx=len(inps)
        if symbol=='_-_':
            symbol=inps[-1]
            mx=mx-1
        for i in inps[:mx]:
            if isinstance(i,(list,tuple)):
                src=src+_ignore_(i,ignore_type,ignore_data)
            elif type(i) in ignore_type or i in ignore_data:
                continue
            else:
                src.append(i)
    # OR    
    # Only two input and first is list then missing symbol option then last one is symbol
    #elif len(inps) == 2 and isinstance(inps[0],(list,tuple)) and symbol=='_-_':
    #    src=src+_ignore_(inps[0],ignore_type,ignore_data)
    #    symbol=inps[1]
    #else:
    #    for ii in inps:
    #        if isinstance(ii,(list,tuple)):
    #            src=src+_ignore_(ii,ignore_type,ignore_data)
    #        elif type(ii) in ignore_type:
    #            continue
    #        elif ii in ignore_data:
    #            continue
    #        else:
    #            src.append(ii)
    #if symbol=='_-_': symbol=''
    rt=''
    if isinstance(byte,bool):
        if byte:
            rt=b''
            symbol=Bytes(symbol)
            append_front=Bytes(append_front)
            append_end=Bytes(append_end)
        else:
            symbol=Str(symbol)
            append_front=Str(append_front)
            append_end=Str(append_end)
    else:
        byte=False
        if src and isinstance(src,(list,tuple)):
            if IsBytes(src[0]):
                rt=b''
                byte=True
                symbol=Bytes(symbol)
                append_front=Bytes(append_front)
                append_end=Bytes(append_end)
    init_none=None
    for i in src:
        if not isinstance(i,(str,bytes)):
            if err:
                return Default(inps,default)
            i='{}'.format(i)
        if byte:
            i=Bytes(i)
        else:
            i=Str(i)
        if init_none is None:
            rt=i
            init_none=1
        else:
            rt=rt+symbol+append_front+i+append_end
    return rt

def FixIndex(src,idx,default=False,err=False):
    '''
    Find Index number in the list,tuple,str,dict
    default   : if wrong or error then return default
    err : default False
        False: fixing index to correcting index without error
        True: if wrong index then return default value
    '''
    if isinstance(src,(list,tuple,str,dict)) and isinstance(idx,int):
        if idx < 0:
            if len(src) > abs(idx):
                idx=len(src)-abs(idx)
            else:
                if err: return default
                idx=0
        else:
            if len(src) <= idx:
                if err: return default
                idx=len(src)-1
        return idx
    return default


def Next(src,step=0,out=None,default='org'):
    '''
    Get Next data or first key of the dict 
    '''
    if isinstance(src,(list,tuple,dict)):
        step=FixIndex(src,step,default=0)
        iterator=iter(src)
        for i in range(-1,step):
            rt=next(iterator)
        return rt
    elif isinstance(src,str):
        step=FixIndex(src,step,default=0)
        if len(src) == 0:
            return ''
        elif len(src) >= 0 or len(src) <= step:
            return src[step]
    return Default(src,default)

def Copy(src,deep=False):
    '''
    Copy data 
    '''
    if isinstance(src,(list,tuple)): return src[:]
    if isinstance(src,dict):
        return copy.deepcopy(src) if deep else src.copy()
    if isinstance(src,str): return '{}'.format(src)
    if isinstance(src,bool): return src
    if isinstance(src,int): return int('{}'.format(src))
    if isinstance(src,float): return float('{}'.format(src))
    if PyVer(2):
        if isinstance(src,long): return long('{}'.format(src))
    return src

def Insert(src,*inps,**opts):
    '''
    src is dict then same as Insert and Update
    src is list,tuple,str then insert data at 'at'
    at : 
      src is list,tuple,str then number
      src is dict then path (/a/b/c)
    uniq: src is list ,tuple then make to uniq data
    err is True then, if any issue then return default value, False then ignore
    '''
    at=opts.pop('at',0)
    default=opts.pop('default',False)
    err=opts.pop('err',False)
    force=opts.pop('force',False)
    uniq=opts.pop('uniq',False)
    if isinstance(src,(list,tuple,str)):
        tuple_out=False
        if isinstance(src,tuple) and force:
            src=list(src)
            tuple_out=True
        if uniq: inps=tuple(set(inps))
        if isinstance(at,str):
            if at in ['start','first']: src=list(inps)+src
            elif at in ['end','last']: src=src+list(inps)
        elif len(src) == 0:
            src=list(inps)
        elif isinstance(at,int) and not isinstance(at,bool) and len(src) > at:
            src=src[:at]+list(inps)+src[at:]
        else:
            if err:
                return default
            src=src+list(inps)
        if tuple_out: return tuple(src)
    elif isinstance(src,dict):
        if isinstance(at,str):
            at_a=at.split('/')
            for i in at_a:
                if i in src:
                    src=src[i]
                else:
                    print('KEY({} of at({})) not found in source'.format(at,i))
                    return False
        for ii in inps:
            if isinstance(ii,dict):
                 src.update(ii)
        if opts:
            src.update(opts)
    return src

def Update(src,*inps,**opts):
    '''
    src is dict then same as Insert and Update
    src is list,tuple,str then replace data at 'at'
    at : 
      src is list,tuple,str then number
      src is dict then path (/a/b/c)
    err is True then, if any issue then return default value, False then ignore
    sym for src is string(str). split src with sym
    '''
    at=opts.pop('at',0)
    err=opts.pop('err',False)
    default=opts.pop('default',False)
    force=opts.pop('force',False)
    sym=opts.pop('sym',None)
    if isinstance(src,(list,tuple,str)):
        if isinstance(src,str) and sym: src=src.split(sym)
        tuple_out=False
        if isinstance(src,tuple) and force:
            src=list(src)
            tuple_out=True
        n=len(src)
        if n == 0:
            if err is True:
                return default
            else:
                src=list(inps)
        elif isinstance(at,int) and n > at:
            for i in range(0,len(inps)):
                if n > at+i:
                    src[at+i]=inps[i]
                elif err is True:
                    return default
                else:
                    src=src+list(inps)[i:]
                    break
        elif isinstance(at,(tuple,list)):
            if len(inps) == len(at):
                for i in range(0,len(at)):
                    if isinstance(at[i],int) and n > at[i]:
                        src[at[i]]=inps[i]
                    elif err is True:
                        return default
                    else:
                        src.append(inps[i])
        if tuple_out: return tuple(src)
        return src
    elif isinstance(src,dict):
        if isinstance(at,str):
            at_a=at.split('/')
            for i in at_a:
                if i in src:
                    src=src[i]
                else:
                    print('KEY({} of at({})) not found in source'.format(at,i))
                    return False
        for ii in inps:
           if isinstance(ii,dict):
               src.update(ii)
        if opts:
           src.update(opts)
    return src

def TypeName(obj):
    '''
    Get input's Type,Instance's name
    '''
    def safe_dir(obj, seen=None):
        if seen is None:
            seen = set()
        
        if id(obj) in seen:
            return []  # Avoid circular reference
        seen.add(id(obj))
        
        try:
            attributes = [attr for attr in dir(obj) if not attr.startswith('__')]
            return attributes
        except Exception:
            return []

    obj_name=type(obj).__name__
    if obj_name in ['function','ImmutableMultiDict']: return obj_name
    # Special Type of Class : Remove according to below code
    #elif obj_name in ['kDict','kList']+[name for name, obj in inspect.getmembers(sys.modules[__name__]) if inspect.isclass(obj)]: # Special case name
    #    print('>>> TypeName2:',obj_name, '<=', obj)
    #    return obj_name
    elif obj_name in ['int','float','str','dict','tuple','list','bool','NoneType']:
    #elif obj_name in ['str']:
        #try:
        #    obj_tmp=eval(obj)
        #    if type(obj_tmp).__name__ not in ['module','classobj','function','response','request']:
        #        obj_name=eval(obj).__name__
        #        if obj_name.lower() == obj.lower(): return obj.lower()
        #except:
        #    if obj.lower() in ['module','classobj','function','unknown','response','request']:
        #        return obj.lower()
        #    elif obj in ['kDict','kList','DICT']: # Special case name
        #        return obj
    #    return 'str'
        return obj_name
    try:
        #obj_dir=dir(obj)
        obj_dir=safe_dir(obj)
        if '__dict__' in obj_dir: # Class Object
            # Special case Class: sub class from parent class then return parent class type
            try:
                # CN case
                parent_name=inspect.getmro(obj)[1].__name__
                if parent_name != 'object':
                    return parent_name
            except:
                # CN() case
                parent_name=inspect.getmro(obj.__class__)[1].__name__
                if parent_name != 'object':
                    return parent_name
            if obj_name == 'type' or inspect.isclass(obj): return 'classobj'
            if obj_name == 'Response': return 'response'
            if obj_name == 'Request': return 'request'
            return 'instance'
    except:
        pass
    #if inspect.isclass(obj): return 'classobj'
    try:
        if obj_name == 'type':
            return obj.__name__
        return obj_name if obj_name in ['kDict','kList','DICT'] else obj_name.lower() # Object Name
    except:
        return 'unknown'

def Type(*inps,**opts):
    '''
    Similar as isinstance(A,())
    support : basic type and ('byte','bytes'),('obj','object'),('func','unboundmethod','function'),('classobj','class'),'generator','method','long',....
    '''
    def NameFix(i):
        if i == str: return 'str'
        if i in ['byte','bytes']: return 'bytes'
        if i in ['obj','object']: return 'object'
        if i in ['func','unboundmethod']: return 'function'
        if i in ['class','classobj']: return 'classobj'
        if i in ['yield','generator']: return 'generator'
        if i in ['builtinfunction','builtinmethod','builtin_function_or_method']: return 'builtin_function_or_method'
        # function: function and instance's function in Python3
        # method:  class's function in Python3
        # instancemethod: instance's and class's function in Python2
        if i in ['method','classfunction','instancemethod','unboundmethod']: return 'method'
        # Fix python version for long
        if i in ['long']:
            if PyVer('>',3): return 'int'
        return i
    inps_l=len(inps)
    if inps_l == 0:
        StdErr('minimum over 1 requirement')
        return
    obj_type=TypeName(inps[0])
    if inps_l == 1: return obj_type
    for check in inps[1:]:
        if isinstance(check,(tuple,list)):
            for i in check:
                #i=NameFix(i)
                check_type=TypeName(i)
                if check_type == 'str': check_type=NameFix(i)
                #check_type=i if a == 'str' else a
                if obj_type == check_type:
                    if opts.get('data'):
                        if IsNone(inps[0]):
                            return False
                    return True
        else:
            #check=NameFix(check)
            check_type=TypeName(check)
            if check_type == 'str':
                check_type=NameFix(check)
            if obj_type == check_type:
                if opts.get('data'):
                    if IsNone(inps[0]):
                        return False
                return True
    return False

class FIND:
    '''
    Searching regular expression form data and return the data
    '''
    def __init__(self,src=None,find=None,out='index',word=False):
        self.src=src
        if isinstance(find,str):
            find=find.replace('*','.+').replace('?','.')
            if word:
                self.find_re=re.compile(r'\b({0})\b'.format(find),flags=re.IGNORECASE)
            else:
                self.find_re=re.compile(find,flags=re.IGNORECASE)
        self.find=find
        self.out=out

    def From(self,data,symbol='\n'):
        rt=[]

        def Search(data,key,rt):
            found=self.find_re.findall(data)
            if found:
                if self.out in ['found']:
                    rt=rt+found
                elif self.out in ['index','idx','key']:
                    rt.append(key)
                elif self.out in ['all','*']:
                    rt.append((key,data))
                else:
                    rt.append(data)
            return rt

        if Type(data,str):
            data=data.split(symbol)
        if Type(data,list,tuple):
            for i in range(0,len(data)):
                if Type(data[i],(list,tuple,dict)):
                    sub=self.From(data[i],symbol=symbol)
                    if sub:
                        if self.out in ['key','index','idx']:
                            for z in sub:
                                rt.append('{}/{}'.format(i,z))
                        else:
                            rt=rt+sub
                elif Type(data[i],str):
                    rt=Search(data[i],i,rt)
        elif Type(data,dict):
            for i in data:
                if Type(data[i],(list,tuple,dict)):
                    sub=self.From(data[i],symbol=symbol)
                    if sub:
                        if self.out in ['key','index','idx']:
                            for z in sub:
                                rt.append('{}/{}'.format(i,z))
                        else:
                            rt=rt+sub
                elif Type(data[i],str):
                    rt=Search(data[i],i,rt)
        else:
             return 'Unknown format'
        return rt

    def Find(self,find,src='_#_',sym='\n',default=[],out=None,findall=True,word=False,mode='value',prs=None,line_num=False,peel=None,idx=None):
        if IsNone(src,chk_val=['_#_'],chk_only=True): src=self.src
        #if Type(src,'instance','classobj'):
        # if src is instance or classobj then search in description and made function name at key
        if isinstance(src,(list,tuple)):
            rt=[]
            for i in range(0,len(src)):
                a=self.Find(find,src[i],sym=sym,default=[],out='list',findall=findall,word=word,mode=mode,prs=prs,line_num=line_num,peel=peel,idx=idx)
                if a: rt=rt+a
            if len(rt):
                return rt
        elif isinstance(src,dict):
            path=[]
            for key in src:
                if mode in ['key','*','all']: # find in key only
                    if find == key:
                        path.append(key)
                found=src.get(key,None)
                if isinstance(found,dict):
                    if dep in found:
                         if mode in ['value','*','all'] and (find == found[dep] or (type(found[dep]) in [DICT,dict,list,tuple] and find in found[dep]) or (type(find) is str and type(found[dep]) is str and find in found[dep])): # find in 'find' only
                              # Value find
                              path.append(key)
                         elif isinstance(found[dep], dict): # recursing
                              path=path+self.Find(find,found[dep],proper=proper,mode=mode)
                    else:
                         if mode in ['value','*','all'] and find == found or (type(found) in [list,tuple] and find in found) or (type(find) is str and type(found) is str and find in found):
                             path.append(key)
                         else:
                             for kk in self.Find(find,src[key],proper=proper,mode=mode,out=dict,default={}): # recursing
                                 path.append(key+'/'+kk)
                else:
                    if mode in ['value','*','all'] and find == found or (type(found) in [list,tuple] and find in found) or (type(find) is str and type(found) is str and find in found):
                        path.append(key)
            return path
        elif isinstance(src,str):
            if findall:
                if prs == '$': idx=-1
                if prs == '^': idx=0
                if sym:
                    string_a=src.split(sym)
                else:
                    string_a=[src]
                if isinstance(find,dict):
                    found={}
                    for nn in range(0,len(string_a)):
                        for dd in find:
                            didx=None
                            if isinstance(find[dd],dict):
                                fmt=next(iter(find[dd]))
                                try:
                                    didx=int(find[dd][fmt].get('idx'))
                                except:
                                    didx=None
                            else:
                                fmt=find[dd]
#                            aa=re.compile(fmt).findall(string_a[nn])
                            if word:
                                aa=re.compile(r'\b({0})\b'.format(fmt),flags=re.IGNORECASE).findall(string_a[nn])
                            else:
                                aa=re.compile(fmt,flags=re.IGNORECASE).findall(string_a[nn])
                            if aa:
                                for mm in aa:
                                    if isinstance(mm,(tuple,list)) and isinstance(didx,int):
                                        if line_num:
                                            found.update({dd:{'data':mm[didx],'line':nn,'src':string_a[nn]}})
                                        else:
                                            found.update({dd:mm[didx]})
                                    else:
                                        if line_num:
                                            found.update({dd:{'data':mm,'line':nn,'src':string_a[nn]}})
                                        else:
                                            found.update({dd:mm})
                    #if found: return OutFormat(found,out=out,peel=peel)
                    return OutFormat(found,out=out,peel=peel,org=src,default=default)
                else:
                    found=[]
                    for nn in range(0,len(string_a)):
                        if isinstance(find,(list,tuple)):
                            find=list(find)
                        else:
                            find=[find]
                        for ff in find:
                            #aa=re.compile(ff).findall(string_a[nn])
                            if word:
                                aa=re.compile(r'\b({0})\b'.format(ff),flags=re.IGNORECASE).findall(string_a[nn])
                            else:
                                aa=re.compile(ff,flags=re.IGNORECASE).findall(string_a[nn])
                            for mm in aa:
                                if isinstance(idx,int):
                                    if isinstance(mm,(tuple,list)):
                                        if line_num:
                                            found.append((mm[idx],nn,string_a[nn]))
                                        else:
                                            found.append(mm[idx])
                                else:
                                    if line_num:
                                        found.append((mm,nn,string_a[nn]))
                                    else:
                                        found.append(mm)
                    #if found:return OutFormat(found,out=out,peel=peel)
                    return OutFormat(found,out=out,peel=peel,org=src,default=default)
#                match=find_re.findall(src)
#                if match: return OutFormat(match,out=out)
            elif isinstance(find,str):
                if word:
                    find_re=re.compile(r'\b({0})\b'.format(find),flags=re.IGNORECASE)
                else:
                    find_re=re.compile(find,flags=re.IGNORECASE)
                match=find_re.search(src)
                if match: return OutFormat([match.group()],out=out,peel=peel)
        #return OutFormat(default,out=out,peel=peel)
        return OutFormat([],out=out,peel=peel,org=src,default=default)
def Found(data,find,digitstring=False,word=False,white_space=True,sense=True,location=False,pythonlike=False):
    '''
    if found <find> in <data> then return True, not then False
    If find "[All]" then you can type "\[All\]" at the <find> location
    if not then "[]" will be work with re expression
    <find> rule:
       re.compile regular expression
       any keep characters  : *
       any single character : ?
       ^                    : start
       $                    : end
    <option>
       sense                : True:(default) sensetive, False: lower and upper is same
       white_space          : True:(default) keep white_space, False: ignore white_space
       word                 : True: <find> is correct word, False:(default) <find> in insde string
       digitstring          : True: string and intiger is same, False:(default) different
       location             : True: return found location ex:(3,10), False:(default) return True/False
    '''
    def _Found_(data,find,word,sense,location):
        data_type=type(data).__name__
        if data_type == 'bytes':
            find=Bytes(find)
        elif data_type == 'str':
            find=Str(find)
        if data == find: #Same Data
            if location: return [(0,len(data))]
            return True 
        if data_type == 'bytes':
            find=find.replace(b'*',b'.+').replace(b'?',b'.') # Fix * or ? case
            if word and find: find=Bytes(r'\b(')+find+Bytes(')\b')
        elif data_type == 'str':
            find=find.replace('*','.+').replace('?','.') # Fix * or ? case
            if word and find: find=r'\b({0})\b'.format(find)
        if not find: return False
        try:
            if sense:
                mm=re.compile(find)
            else:
                mm=re.compile(find,flags=re.IGNORECASE)
        except:
            return False
        #if word:
        #    ff=re.match(mm,data) # Find First Matched(word type) location
        #else:
        #    #ff=mm.findall(data) # Find All Data
        ff=mm.finditer(data)
        if bool(ff):
            rt=[]
            for i in list(ff): # when change list(ff) then lost data
                rt.append(i.span())
            if location: return rt
            return True if rt else False
        return False

    data=WhiteStrip(data,BoolOperation(white_space,mode='oppisit'))
    type_data=type(data).__name__
    type_find=type(find).__name__
    if pythonlike:
        if type_data in ['NoneType','bool','str']:
            data='{}'.format(data).capitalize()
            if data == 'Null': data='None'
            type_data='str'
        if type_find in ['NoneType','bool','str']:
            find='{}'.format(find).capitalize()
            if find == 'Null': find='None'
            type_find='str'
    if digitstring:
        if type_data in ['int','float']:
            data='{}'.format(data)
            type_data='str'
        if type_find in ['int','float']:
            find='{}'.format(find)
            type_find='str'
    if type_data in ['str','bytes'] and type_find in ['str','bytes']:
        return _Found_(data,find,word,sense,location)
    if sense:
        return type(data) == type(find) and data == find
    return data == find

def IsSame(src,dest,sense=False,order=False,_type_=False,digitstring=True,white_space=False,pythonlike=False,ignore_keys=[]):
    '''
    return True/False
    Check same data or not between src and dest datas
    <dest> rule:
       re.compile format
       any keep characters  : *
       any single character : ?
       ^                    : start
       $                    : end
    <option>
       order                : True: if list,tuple then check ordering too, False:(default) just check data is same or not
       Type                 : True: check Type only, False:(default) check data
       sense                : True: sensetive, False:(default) lower and upper is same
       white_space          : True: keep white space, False:(default) ignore white_space
       digitstring          : True:(default) string and intiger is same, False: different
    exact same : sense=True,order=True,digitstring=False,white_space=True,pythonlike=False
    same data  : sense=True,digitstring=False[,white_space=True,pythonlike=False]
    '''
    if _type_ is True: # If check type only
        return Type(src,dest)
    if Type(src,('str','bytes')) and Type(dest,('str','bytes')):# and dest:
        if Type(dest,'bytes') or Type(src,'bytes'):
            src=Bytes(src)
            dest=Bytes(dest)
            if src == dest: return True
            if dest:
                if dest[0] != b'^': dest=b'^'+dest
                if dest[-1] != b'$': dest=dest+b'$'
        else:
            src=Str(src)
            dest=Str(dest)
            if src == dest: return True
            if dest:
                if dest[0] != '^': dest='^'+dest
                if dest[-1] != '$': dest=dest+'$'
    if pythonlike:
        if isinstance(src,str):
            src=FormData(src)
        if isinstance(dest,str):
            dest=FormData(dest)
    if isinstance(src,(list,tuple)) and isinstance(dest,(list,tuple)):
        if sense and order: return src == dest
        if len(src) != len(dest): return False
        if order:
            for j in range(0,len(src)):
                if not Found(src[j],dest[j],digitstring=digitstring,white_space=white_space,sense=sense,pythonlike=pythonlike): return False
            return True
        else:
            a=list(src[:])
            b=list(dest[:])
            for j in range(0,len(src)):
                for i in range(0,len(dest)):
                    if (isinstance(src[j],dict) and isinstance(dest[j],dict)) or (isinstance(src[j],(list,tuple)) and isinstance(dest[j],(list,tuple))):
                        if IsSame(src[j],dest[i],sense,order,_type_,digitstring,white_space,pythonlike,ignore_keys):
                            a[j]=None
                            b[i]=None
                    elif Found(src[j],dest[i],digitstring=digitstring,white_space=white_space,sense=sense,pythonlike=pythonlike):
                        a[j]=None
                        b[i]=None
            if a.count(None) == len(a) and b.count(None) == len(b): return True
            return False
    elif isinstance(src,dict) and isinstance(dest,dict):
        if sense: return src == dest
        if len(src) != len(dest): return False
        for s in src:
            if s in ignore_keys: continue
            if s in dest:
                if (isinstance(src[s],dict) and isinstance(dest[s],dict)) or (isinstance(src[s],(list,tuple)) and isinstance(dest[s],(list,tuple))):
                    if not IsSame(src[s],dest[s],sense,order,_type_,digitstring,white_space,pythonlike,ignore_keys): return False
                else:
                    if not Found(src[s],dest[s],digitstring=digitstring,white_space=white_space,sense=sense,pythonlike=pythonlike): return False
        return True
    else:
        return Found(src,dest,digitstring=digitstring,white_space=white_space,sense=sense,pythonlike=pythonlike)

def IsIn(find,dest,idx=False,default=False,sense=False,startswith=True,endswith=True,digitstring=True,word=True,white_space=False,order=False,**opts):
    '''
    Check key or value in the dict, list or tuple then True, not then False
    return True/False
    Check same data or not between src and dest datas
    <dest> rule:
       re.compile format
       any keep characters  : *
       any single character : ?
       ^                    : start
       $                    : end
    <option>
       order                : True: if list,tuple then check ordering too, False:(default) just check data is same or not
       startswith           : True:(default) Find "^ABC" type, False: according to <dest>
       endswith             : True:(default) Find "ABC$" type, False: according to <dest>
       Type                 : True: check Type only, False:(default) check data
       sense                : True: sensetive, False:(default) lower and upper is same
       white_space          : True: keep white space, False:(default) ignore white_space
       word                 : True:(default) <find> is correct word, False: <find> in insde string
       digitstring          : True:(default) string and intiger is same, False: different
    '''
    _type_=opts.get('Type',opts.get('_type_',False))
    #dest_type=TypeName(dest)
    #if dest_type in ['list','tuple','str','bytes']:
    if Type(dest,('list','tuple','str','bytes')):
        #if TypeName(idx) == 'int':
        if Type(idx,'int'):
            idx=FixIndex(dest,idx,default=False,err=True)
            if idx is False: return default
            #if dest_type in ['str','bytes']:
            if Type(dest,('str','bytes')):
                if Found(dest[idx:],find,digitstring,word,white_space,sense): return True
            else:
                if Found(dest[idx],find,digitstring,word,white_space,sense): return True
        else:
            for i in dest:
                if IsSame(i,find,sense,order,_type_,digitstring,white_space): return True
    elif isinstance(dest, dict):
        if idx in [None,'',False]:
            for i in dest:
                if IsSame(i,find,sense,order,_type_,digitstring,white_space): return True
        else:
            if Found(dest.get(idx),find,digitstring,word,white_space,sense): return True
    return default

def BoolOperation(a,mode=bool):
    if type(a).__name__ == 'bool':
        if mode is bool: return a
        if mode in ['opposition','opposit']:
            return not a

def Bool(src,want=True,auto_bool=False,shell_code=True):
    if want in [True,False,'True','False',b'True',b'False']:
        if type(want).__name__ in ['str','bytes']: want=eval(want) # convert string bool to bool
        if auto_bool and isinstance(src, (list,tuple,dict)) and src: # convert list,tuple,dict to bool
            if isinstance(src,(list,tuple)):
                src=src[0]
            elif isinstance(src,dict):
                src=src.get('rc')
        elif src in [True,False,'True','False',b'True',b'False']: # Convert string bool to bool
            if type(src).__name__ in ['str','bytes']: src=eval(src)
        if shell_code and isinstance(src,int) and not isinstance(src,bool): # Convert shell rc to bool
            src=True if src == 0 else False
        return src == want
    elif want in [str,'str',int,'int',dict,'dict',list,'list',tuple,'tuple',None,'None']:
        if type(want).__name__ in ['str','bytes']: want=eval(want) # convert string bool to bool
        if want is None:
            if src == '': src=None
            return src == want
        else:
            return isinstance(src,want)
    return False

def PyDefine(aa):
    if IsIn(aa,[None,"'None'",'"None"','None','null',"'null'",'"null"']):
        return None
    elif IsIn(aa,[True,"'True'",'"True"','True','ok']):
        return True
    elif IsIn(aa,[False,"'False'",'"False"','False','fail']):
        return False
    return aa

def WhiteStrip(src,mode=True):
    '''
    remove multi space to single space, remove first and end space
    others return original
    '''
    if mode is True and type(src).__name__ in ('str','bytes'): return src.strip()
    return src

def IsNone(src,**opts):
    '''
    Check the SRC is similar None type data('',None) or not
    -check_type=<type> : include above and if different type then the return True
    -list_none :
      - False: check index item in the source (default)
      - True : check all list of source
    -index   : if source is list then just want check index item
    -space   :
      - True : aprove space to data in source
      - False: ignore space data in source
    '''
    value=opts.get('value',opts.get('chk_val',['',None]))
    space=opts.get('space',True)
    chk_only=opts.get('chk_only',opts.get('check_only',False))
    index=opts.get('index',opts.get('idx'))
    list_none=opts.get('LIST',False)

    #check type
    CheckType=opts.get('check_type',None)
    _type_=False
    if CheckType is not None:
        value=value+[CheckType]
        _type_=True
    def _IsIn_(src,value,sense=False):
        if isinstance(value,(list,tuple)):
            for i in value:
                if not sense and  type(i).__name__ in ['str','bytes'] and type(src).__name__ in ['str','bytes']:
                    if Str(i).lower() == Str(src).lower(): return True
                else:
                    if i == src: return True
        else:
            if not sense and type(value).__name__ in ['str','bytes'] and type(src).__name__ in ['str','bytes']:
                if Str(value).lower() == Str(src).lower(): return True
            else:
                if value == src: return True
        return False
        
    src=WhiteStrip(src,BoolOperation(space,mode='opposit'))
    if _IsIn_(src,value,sense=False): return True
    if src:
        if isinstance(src,(list,tuple)):
            if list_none:
                for i in src:
                    if not _IsIn_(WhiteStrip(i,BoolOperation(space,mode='opposit')),value,sense=False): return False
                return True
            elif isinstance(index,int) and len(src) > abs(index):
                if _IsIn_(WhiteStrip(src[index],BoolOperation(space,mode='opposit')),value,sense=False): return True
        elif isinstance(src,dict):
            if index in src:
                if _IsIn_(WhiteStrip(src[index],BoolOperation(space,mode='opposit')),value,sense=False): return True
    if chk_only:
        # i want check Type then different type then return True
        if _type_:
            #if TypeName(src) != TypeName(CheckType): return True
            return False if Type(src,CheckType) else True
        return False
    if not isinstance(src,(bool,int)):
        if not src: return True
    # i want check Type then different type then return True
    if _type_:
        #if TypeName(src) != TypeName(CheckType): return True
        return False if Type(src,CheckType) else True
    return False

def IsExist(src,**opts):
    # check up for data is exist or not 
    # or the data is my want's type and existing or not
    data_type=opts.get('type',opts.get('data_type',opts.get('_type_','_NA_')))
    if data_type != '_NA_':
        if data_type is None and src is None: return True
        elif type(data_type).__name__ == 'type':
            if type(src) == data_type:
                return True
        else:
             if src == data_type: return True
        return False
    else: 
        if isinstance(src,(list,tuple,dict,str)):
            if not src: return False
        #elif src is None: return True
        #elif isinstance(src,(bool,int)):
        #    return True
        return True

def IsVar(src,obj=None,default=False,mode='all',parent=0):
    '''
    Check the input(src) is Variable name or not (in OBJ or in my function)
    '''
    oo=Variable(src,obj=obj,parent=1+parent,history=False,default='_#_',mode=mode)
    if oo == '_#_': return default
    return True

def IsFunction(src=None,find='_#_',builtin=False):
    '''
    Check the find is Function in src object
    '''
    if IsNone(src):
        if isinstance(find,str) and find != '_#_':
            find=GetGlobal().get(find)
        return inspect.isfunction(find)
    else:
        if builtin:
            if type(src).__name__ in ['function','instancemethod','method','builtin_function_or_method']: return True # src is function then
        else:
            if type(src).__name__ in ['function','instancemethod','method']: return True # src is function then
    # find function in object
    aa=[]
    if type(find).__name__ == 'function': find=find.__name__
    if not isinstance(find,str): return False
    if isinstance(src,str): src=sys.modules.get(src)
    if inspect.ismodule(src) or inspect.isclass(src):
        for name,fobj in inspect.getmembers(src):
            if inspect.isfunction(fobj): # inspect.ismodule(obj) check the obj is module or not
                aa.append(name)
    else:
        for name,fobj in inspect.getmembers(src):
            if inspect.ismethod(fobj): # inspect.ismodule(obj) check the obj is module or not
                aa.append(name)
    if find in aa: return True
    return False

def IsBytes(src):
    '''
    Check data is Bytes or not
    '''
    if PyVer(3):
        if isinstance(src,bytes):
            return True
    return False

def IsInt(src,mode='all'):
    '''
    Check data is Int or not
    - mode : int => check only int
             str => int type string only
             all => Int and int type string
    '''
    def _int_(data):
        try:
            int(data)
            return True
        except:
            return False

    if not isinstance(src,bool):
        if mode in [int,'int']:
            if isinstance(src,int):
                return True
        elif mode in [str,'str','text','string']:
            if Type(src,('str','bytes')):
                return _int_(src)
        else:
            return _int_(src)
    return False

def _obj_max_idx_(obj,idx,err=True):
    #Get Object's max length
    obj_len=len(obj)
    if obj_len == 0: return None
    if not isinstance(idx,int):
        if err is True: return False
        return obj_len-1
    if idx >= 0:
        if obj_len <= idx:
            if err is True: return False
            return obj_len-1
        else:
            return idx
    else:
        if obj_len < abs(idx):
            if err is True: return False
            return 0
        return obj_len+idx

def Max(obj,key=False,err=True):
    #ToDo:
    # - list,tuple:
    #    - key : True : Max of idx
    #    - key : False: get maximum number or last string
    #    - key : version: last version
    # - dict :
    #    - key : True : Max in keys
    #    - key : False: Max in values
    #    - key : None or dict: last input dict
    #print('>>',obj)
    if isinstance(obj,(list,tuple)):
        if key is True:
            return _obj_max_idx_(obj,err=err)
        elif IsIn(key,['ver','version']):
            a='0.0'
            for i in obj:
                if CompVersion(i,'>',a):
                    a=i
            if a=='0.0':
                if err:
                    return False
            return a
        elif key is False:
            a=-1 #number
            b=[] #string
            for i in obj:
                i=Int(i)
                #print('>>i:',i)
                if isinstance(i,int):
                    if a < i:
                        a=i
                elif isinstance(i,str):
                    b.append(i)
            #print('>>b:',b)
            if a > -1:
                return a
            elif b:
                b.sort()
                return b[-1]
            else:
                if err:
                    return False
                return obj[-1]
    elif isinstance(obj,dict):
        if key is True:
            return Max(list(obj.keys()),err=err)
        elif key is False:
            return Max(list(obj.values()),err=err)
        else:
            return Max(list(obj.items()),err=False)
    else:
        if err:
            return False
        else:
            return obj

class DICT(dict):
    def __init__(self, *inps,**opts):
        for i in inps:
            if isinstance(i,(dict,DICT)):
                for k in i:
                    self.__setitem__(k,i[k])
            elif isinstance(i,tuple):
                self.TupleDict(i)
            elif Type(i,'dict_items'):
                self.TupleDict(*tuple(i))
            else:
                continue
        if opts:
            for i in opts:
                self.__setitem__(i,opts[i])
    def __getitem__(self, key):
        return dict.__getitem__(self,key)

    def __setitem__(self, key, value):
        found=self.get(key,None)
        if Type(found,('DICT','dict')): #Found key in myself and the key has dictionary
            # change into dict
            super(DICT, self).__setitem__(key, found)
        else:
            # make a sub dict to dot dict
            if isinstance(value,dict) and not isinstance(value,DICT):
                value=DICT(value)
            # set dot type dict to sub dict
            super(DICT, self).__setitem__(key, value)
    def Cd(self, key,symbol='/',default=False):
        if isinstance(key,str):
            key=key.split('/')
            if key[0] == '': del key[0]
        if isinstance(key,(list,tuple)):
            for i in key:
                if i in self:
                    self=self[i]
                else:
                    return  default
            return self
        return default
    def TupleDict(self,*inps,**opts):
        #Merge *inps to DICT() data
        err=opts.get('err',False)
        default=opts.get('default',False)
        out={}
        for i in inps:
            if isinstance(i,tuple) and len(i) == 2:
                k,v=i
                if isinstance(v,(dict,DICT)):
                    v=dict(v)
                elif isinstance(v,tuple):
                    v=self.TupleDict(v,**opts)
                    if not isinstance(v,(dict,DICT)):
                        if err:
                            return Default(inps,default)
                        continue
                out[k]=v
            else:
                if err:
                    return Default(inps,default)
        for k in out:
            self.__setitem__(k,out[k])
        return self
    def Tuple(self):
        return tuple(self.items())
    def Get(self,*inps,**opts):
        if len(inps) == 1:
            idx=inps[0]
        elif len(inps) > 1:
            idx=inps[:]
        else:
            #idx=None

            return self
        default=opts.get('default')
        err=opts.get('err',opts.get('error',False))
        fill_up=opts.get('fill_up','_fAlsE_')
        idx_only=opts.get('idx_only',opts.get('index_only',opts.get('order',False)))
        _type=opts.get('_type_',opts.get('type'))
        out=opts.get('out',opts.get('out_form','raw'))
        peel=opts.get('peel')
        strip=opts.get('strip',False)
        ok,nidx=IndexForm(idx,idx_only=False)
        idx_type=type(nidx).__name__
        if ok is True:
            obj_items=list(self.items())
            if idx_type == 'tuple': #Range Index
                ss=_obj_max_idx_(obj_items,Int(nidx[0]),err)
                ee=_obj_max_idx_(obj_items,Int(nidx[1]),err)
                if Type(ss,int) and Type(ee,int):
                    return DICT(dict(obj_items[ss:ee+1]))
            elif idx_type == 'list': #OR Index
                rt=[]
                for i in nidx:
                    if idx_only:
                        ix=_obj_max_idx_(obj_items,Int(i,default=False,err=True),err)
                        if Type(ix,int):
                            rt.append(obj_items[ix])
                        elif fill_up != '_fAlsE_':
                            rt.append(fill_up)
                    else:
                        t=self.get(i)
                        if t is not None: rt.append(t)
                return OutFormat(rt,out=out,default=default,org=self,peel=peel,strip=strip)
            else:
                if idx_only:
                    ix=_obj_max_idx_(obj_items,Int(idx),err)
                    if Type(ix,int):
                        return DICT(dict((obj_items[ix],)))
                return self.get(idx,Default(self,default))
        elif ok is None: #Path Index
            for i in nidx[:-1]:
                if i not in self or not isinstance(self[i],dict): return Default(self,default)
                self=self[i]
            return self[nidx[-1]] if isinstance(self,dict) and nidx[-1] in self else Default(self,default)
        return Default(self,default)

    # make dot dict
    __setattr__, __getattr__ = __setitem__, __getitem__

def Dict(*inp,deepcopy=False,copy=False,replace=False,ignore=[],ignore_value=[],**opt):
    '''
    Dictionary
    - Define
    - marge/Update/Append
    - replace data
    support : Dict, list or tuple with 2 data, dict_items, Django request.data, request data, like path type list([('/a/b',2),('/a/c',3),...]), kDict
    deepcopy=True: duplicate with deep copy for the dictionary
    copy=True: duplicate with copy for the dictionary
    replace=True: if found same key then replace the key's data (not merge,update,append)
    '''
    if not isinstance(ignore,list): ignore=[]
    if not isinstance(ignore_value,list): ignore_value=[]
    src={}
    if len(inp) >= 1:
        if deepcopy or copy:
            src=Copy(inp[0],deep=deepcopy)
        else:
            src=inp[0]
    src_type=TypeName(src)
    if src_type in ['ImmutableMultiDict']:
        if len(src) > 0:
            tmp={}
            for ii in src:
                if ii in ignore: continue
                elif src[ii] in ignore_value: continue
                tmp[ii]=src[ii]
            src=tmp
    elif isinstance(src,dict) and src_type not in ['kDict','DICT']:
        if src_type == 'QueryDict': # Update data at request.data of Django
            try:
                src._mutable=True
            except:
                StdErr("src(QueryDict) not support _mutable=True parameter\n")
        for dest in inp[1:]:
            if not isinstance(dest,dict): continue
            for i in dest:
                if i in ignore: continue
                elif dest[i] in ignore_value: continue
                if i in src and isinstance(src[i],dict) and isinstance(dest[i],dict):
                    src[i]=Dict(src[i],dest[i],deepcopy=deepcopy,copy=copy,replace=replace,ignore=ignore,ignore_value=ignore_value)
                else:
                    src[i]=dest[i]
    elif src_type in ['dict_items']:
        src=dict(src)
#    By pass kDict and DICT
#    elif src_type in ['kDict','DICT']:
#        #src=dict(src.Get()) # maybe inifinity loop????, So convert kDict or DICT to dict
#        src=src.Get() # maybe inifinity loop????, So convert kDict or DICT to dict
    elif src_type in ['list','tuple']:
        tmp={}
        for ii in src:
            if isinstance(ii,tuple) and len(ii) == 2:
                if ii[0] in ignore: continue
                elif ii[0] in [None,'']: continue
                elif ii[1] in ignore_value: continue
                if isinstance(ii[0],str):
                    #Same as 'a/b/c' and '/a/b/c'
                    if ii[0][0] == '/':
                        src_a=ii[0].split('/')[1:]
                    else:
                        src_a=ii[0].split('/')
                    tt=tmp
                    for kk in src_a[:-1]:
                        if kk not in tt: tt[kk]={}
                        tt=tt[kk]
                    tt[src_a[-1]]=ii[1]
                else:
                    tmp[ii[0]]=ii[1]
        src=tmp
    else:
        src={}
    #Update Extra inputs
    for ext in inp[1:]:
        #if not isinstance(ext,dict): ext=Dict(ext)
        #if Type(ext,dict):
        if not Type(ext,('dict','kDict','DICT')): ext=Dict(ext)
        if Type(ext,('dict','kDict','DICT')):
            ext=dict(ext)
            #Block For duplicated parameters
            ext['deepcopy']= deepcopy
            ext['copy']= copy
            ext['replace']= replace
            ext['ignore']= ignore
            ext['ignore_value']= ignore_value
            #Dict(src,replace=replace,**ext)
            Dict(src,**ext)
    #Update Extra option data
    if opt:
        for i in opt:
            if i in ignore: continue
            elif i in [None,'']: continue
            elif opt[i] in ignore_value: continue
            if i in src and isinstance(src[i],dict) and isinstance(opt[i],dict):
                if replace:
                    src[i]=opt[i]
                else:
                    src[i]=Dict(src[i],opt[i],deepcopy=deepcopy,copy=copy,replace=replace,ignore=ignore,ignore_value=ignore_value)
            else:
                src[i]=opt[i]
    return src

def CompVersion(*inp,**opts):
    '''
    input: source, compare_symbol(>x,<x,==,!xx), destination
      return BOOL
    input: source, destination, compare_symbol='>x,<x,==,!xx'
      return BOOL
    input: source, destination
      - without compare_symbol
      - out=sym      : return symbol (>, ==, <)  (default)
      - out=int      : return 1(>), 0(==), -1(<)
      - out=str      : return bigger(>), same(==), lower(<)
    input: source
      - out=str      : return '3.0.1' (default)
      - out=tuple    : return to tuple type (3,0,1)
      - out=list     : return to list type [3,0,1]
    version_symbol or symbol : default '.'

    sort list
    <list>.sort(key=CompVersion)  or sorted(<list>,key=CompVersion)
    '''
    version_symbol=opts.get('version_symbol',opts.get('symbol','.'))
    compare_symbol=opts.get('compare_symbol',opts.get('compare'))
    if compare_symbol == 'is': compare_symbol='=='
    elif compare_symbol == 'is not': compare_symbol='!='
    out=opts.get('out',opts.get('output',str))
    def _clean_(a):
        for i in range(0,len(a)):
            if a[i] == '': a[i]=0
        for i in range(len(a)-1,0,-1):
            if i > 1 and a[i] == 0 and a[i-1]==0:
                a.pop(i)
        return a
    def Comp(src,dest):
        len_src=len(src)
        len_dest=len(dest)
        bigger=len_dest if len_dest > len_src else len_src
        for i in range(0,bigger):
            if i < len_src and i < len_dest:
                ss=src[i]
                dd=dest[i]
                if type(ss) != type(dd):
                    ss=Str(src[i])
                    dd=Str(dest[i])
                if ss > dd:
                    return 1
                elif ss < dd:
                    return -1
            elif i < len_src:
                return 1
            elif i < len_dest:
                return -1
        return 0
    def MkVerList(src,version_symbol):
        if isinstance(src,dict): src=src.get('version',src.get('__version__'))
        if Type(src,('str','bytes')):
            src=Str(src).split(version_symbol)
        elif Type(src,('int','float')):
            src=[src]
        elif isinstance(src, tuple):
            src=list(src)
        if isinstance(src,list):
            return tuple(_clean_([ Int(i) for i in src ]))
    src=[]
    dest=[]
    if len(inp) == 1:
        ver_tuple=MkVerList(inp[0],version_symbol)
        if out in [str,'str']:
            return '.'.join([Str(i) for i in ver_tuple])
        elif out in [list,'list']:
            return list(ver_tuple)
        return ver_tuple
    elif len(inp) == 2:
        src=MkVerList(inp[0],version_symbol)
        dest=MkVerList(inp[1],version_symbol)
    elif len(inp) == 3:
        src=MkVerList(inp[0],version_symbol)
        compare_symbol=inp[1]
        dest=MkVerList(inp[2],version_symbol)
    if src and dest:
        cc=Comp(src,dest)
        if isinstance(compare_symbol,str) and compare_symbol:
            rev=False
            if '!' in compare_symbol: rev=True
            if cc == 0:
                if '=' in compare_symbol:
                    return False if rev else True
            elif cc == 1:
                if '>' in compare_symbol:
                    return False if rev else True
                if rev: return True
            elif cc == -1:
                if '<' in compare_symbol:
                    return False if rev else True
            return True if rev else False
        else:
            if out in [int,'int','integer','num']: return cc
            if cc > 0:
                if out in [str,'str','string']: return 'bigger(>)'
                return '>'
            elif cc < 0:
                if out in [str,'str','string']: return 'lower(<)'
                return '<'
            if out in [str,'str','string']: return 'same(=)'
            return '=='


def ModVersion(mod):
    '''
    Find Module Version
    '''
    if PyVer(3,8,'<'): 
        import pkg_resources
        try:
            return pkg_resources.get_distribution(mod).version
        except:
            return None
    else:
        from importlib.metadata import version
        try:
            return version(mod)
        except:
            return None

# Python 2 has built in reload
if PyVer(3,4,'<='): 
    from imp import reload # Python 3.0 - 3.4 
elif PyVer(3,4,'>'): 
    from importlib import reload # Python 3.5+

def GlobalEnv(): # Get my parent's globals()
    '''
    Get Global Environment of the python code
    '''
    return dict(inspect.getmembers(inspect.stack()[1][0]))["f_globals"]

def Install(module,install_account='',mode=None,upgrade=False,version=None,force=False,pkg_map=None,err=False,install_name=None):
    '''
    Install python module file
    module name
    install_accout='' : default None,  --user : install on account's directory
    upgrade :
      False : default
      True  : Install or Upgrade the module
    version :
      None  : default
      <version>: Check the version
                 == <version> : if not Same version then install at the same version
                 >= <version> : if not bigger the version then install or upgrade
                 <= <version> : if not lower the version then install at the version
    force  : default False
      True : if installed then force re-install, not then install
    pkg_map: mapping package name and real package name
      format => { <pkg name>: <real install pkg name> }
    err    : default False
      True : if installing got any isseu then crashing
      False: if installing got any issue then return False
    '''
    # version 
    #  - same : ==1.0.0
    #  - big  : >1.0.0
    #  - or   : >=1.3.0,<1.4.0
    # pip module)
    #pip_main=None
    #if hasattr(pip,'main'):
    #    pip_main=pip.main
    #elif hasattr(pip,'_internal'):
    #    pip_main=pip._internal.main
    if pkg_map is None:
        pkg_map={
           'magic':'python-magic',
           'bdist_wheel':'wheel',
        }

    pip_main=subprocess.check_call
    if not pip_main:
        print('!! PIP module not found')
        return False

    pkg_name=module.split('.')[0]
    if not install_name: install_name=pkg_map.get(pkg_name,pkg_name)
    # Check installed package
    # pip module)
    #install_cmd=['install']
    if os.path.basename(sys.executable).startswith('python'):
        install_cmd=[sys.executable,'-m','pip','install']
    else:
        install_cmd=['python3','-m','pip','install']
    if PyVer('>=','3.2'): 
        #pip3 install setuptools  # for pkg_resources 
        import pkg_resources
        pkn=pkg_resources.working_set.__dict__.get('by_key',{}).get(install_name)
        if pkn:
            if version:
                for i in range(len(version)-1,0,-1):
                    if version[i] in ['>','<','=']: break
                ver_str=version[i+1:]
                compare_symbol=version[:i+1]
                if not CompVersion(pkn.version,compare_symbol,ver_str):
                    upgrade=True
                    install_cmd.append(install_name+version)
                else:
                    return True
            else:
                install_cmd.append(install_name)
            if force: install_cmd.append('--force-reinstall')
            if install_account: install_cmd.append(install_account)
            if not force and upgrade: install_cmd.append('--upgrade')
            if pip_main and force or upgrade:
                if err:
                    if pip_main(install_cmd) == 0: return True
                    return False
                else:
                    try:
                        if pip_main(install_cmd) == 0: return True
                        return False
                    except:
                        return False
            return True

#    if mode == 'git':
#        git.Repo.clone_from(module,'/tmp/.git.tmp',branch='master')
#        build the source and install
#        return True

    if version:
        install_cmd.append(install_name+version)
    else:
        install_cmd.append(install_name)
    if force: install_cmd.append('--force-reinstall')
    if install_account: install_cmd.append(install_account)

    if err:
        if pip_main(install_cmd) == 0: return True
    else:
        try:
            if pip_main(install_cmd) == 0: return True
        except:
            pass
    return False


def ModName(src):
    '''
    Analysis Module name from input string
    '''
    rt=True
    class_name=None
    module_name=None
    alias_name=None
    version=None
    symbol=None
    if isinstance(src,str):
        src_a=src.split()
        #remove from , import tag
        if src_a[0] in ['from','import']:
            del src_a[0]
        module_name=src_a[0]
        #remove version information
        src_a_len=len(src_a)
        for i in range(src_a_len-1,0,-1):
            if src_a[i] in ['==','=','>','>=','<','<=']:
                if i < src_a_len:
                    symbol=src_a[i]
                    version=src_a[i+1]
                break
        if 'import' in src_a:
            import_idx=src_a.index('import')
            if src_a_len > import_idx+1:
                class_name=src_a[import_idx+1]
            else:
                rt=False
        if 'as' in src_a:
            alias_idx=src_a.index('as')
            if src_a_len > alias_idx+1:
                alias_name=src_a[alias_idx+1]
            else:
                rt=False
        if alias_name is None:
            alias_name=module_name
    return rt,module_name,alias_name,class_name,version,symbol

#def ModLoad(inp,force=False,globalenv=dict(inspect.getmembers(inspect.stack()[1][0]))["f_globals"],unload=False,re_load=False):
def ModLoad(inp,force=False,globalenv=GetGlobal(),unload=False,re_load=False,ignore_warning=False):
    '''
    Load python module
    0: Loaded
    1: Load error (May be need install or Loading error with any critical issue)
    2: Unload or Not loaded
    '''
    def Reload(name):
        if isinstance(name,str):
            globalenv[name]=reload(globalenv[name])
        else:
            name=reload(name)
        return True

    def Unload(name):
        if isinstance(name,str):
            del globalenv[name]
        elif isinstance(name,type(inspect)):
            try:
                nname = name.__spec__.name
            except AttributeError:
                nname = name.__name__
            if nname in globalenv: del globalenv[nname]

    if not inp: return 0,''
#    inp_a=inp.split()
    wildcard=None
    class_name=None
#    if inp_a[0] in ['from','import']:
#        del inp_a[0]
#    name=inp_a[-1]
#    module=inp_a[0]
    ok,module,name,class_name,version,symbol=ModName(inp)
    if ok is False:
            print('*** Wrong information')
            return 0,module
    if unload:
        #if '*' not in inp and name in globalenv: # already loaded
        if class_name != '*' and name in globalenv: # already loaded
            Unload(name) #Unload
        return 2,module #Not loaded

#    import inspect,sys
#    print(inspect.stack())
#    dep=len(inspect.stack())-1
#    fname=sys._getframe(dep).f_code.co_name
#    if fname == '_bootstrap_inner' or name == '_run_code':
#        fname=sys._getframe(2).f_code.co_name
#    print('>>',fname,':::',name,class_name,module)
    #if '*' not in inp and name in globalenv: # already loaded
    if class_name != '*' and name in globalenv: # already loaded
        if re_load:
            Reload(name) # if force then reload
            return 0,module
        elif force:
            Unload(name) #if force then unload and load again
#    if 'import' in inp_a:
#        import_idx=inp_a.index('import')
#        if len(inp_a) > import_idx+1:
#            class_name=inp_a[import_idx+1]
#        else:
#            print('*** Wrong information')
#            return 0,module
    try:
        if ignore_warning:
            warnings.simplefilter("ignore")
        if class_name:
            if class_name == '*':
                wildcard=import_module(module)
            else:
                try:
                    globalenv[name]=getattr(import_module(module),class_name)
                except:
                    globalenv[name]=import_module('{}.{}'.format(module,class_name))
        else:
            globalenv[name]=import_module(module)
        #warnings.simplefilter("default")
        return wildcard,module # Loaded. So return wildcard information
    except AttributeError: # Try Loading looped Module/Class then ignore  or Wrong define
        return 0,module
    except ImportError: # Import error then try install
        return 1,module

def Import(*inps,**opts):
    '''
    basic function of import
    if not found the module then automaticall install
    version check and upgrade, reinstall according to the version
    support requirement files

    inps has "require <require file>" then install the all require files in <require file>
    Import('<module name>  >= <version>') : Check version and lower then automaticall upgrade 
    Import('<module name>  == <version>') : Check version and different then automaticall reinstall with the version
    Import('<module name>',path='AAA,BBB,CCCC') : import <module name> from default and extra AAA and BBB and CCC.
    -path=       : searching and the module in the extra path (seperate with ',' or ':' )
    -force=True  : unload and load again when already loaded (default: False)
    -reload=True : run reload when already loaded (default: False)
    -unload=True : unload module (default : False)
    -err=True    : show install or loading error (default: False)
    -dbg=True    : show comment (default : False)
    -install_account=: '--user','user','myaccount','account',myself then install at my local account
                 default: Install by System default setting

    '''
    globalenv=opts.get('globalenv',dict(inspect.getmembers(inspect.stack()[1][0]))["f_globals"]) # Get my parent's globals()
    force=opts.get('force',None) # unload and load again when already loaded (force=True)
    re_load=opts.get('reload',None) #  run reload when already loaded
    unload=opts.get('unload',False) # unload module when True
    err=opts.get('err',False) # show install or loading error when True
    default=opts.get('default',False)
    dbg=opts.get('dbg',False) # show comment when True
    auto_install=opts.get('auto_install',True) # if not found the module then automatically install
    requirements=opts.get('requirements')
    #install_account=opts.get('install_account','--user')
    install_account=opts.get('install_account','') # '--user','user','myaccount','account',myself then install at my local account
    install_name=opts.get('install_name')
    ignore_warning=opts.get('ignore_warning',False)

    #Append Module Path
    virtual_env=os.environ.get('VIRTUAL_ENV')
    env_base_dir=virtual_env if virtual_env else '/usr'
    base_lib_path=[]
    py_ver=PyVer()
    for i in ['lib/python{}/site-packages'.format(py_ver),'lib64/python{}/site-packages'.format(py_ver),'local/python{}/site-packages'.format(py_ver),'local/lib/python{}/site-packages'.format(py_ver),'local/lib64/python{}/site-packages'.format(py_ver)]:
        j=os.path.join(env_base_dir,i)
        if os.path.isdir(j):
            base_lib_path.append(j)

    path=opts.get('path') # if the module file in a special path then define path
    if not IsNone(path,check_type=str):
        if ',' in path:
            base_lib_path=base_lib_path+path.split(',')
        elif ':' in path:
            base_lib_path=base_lib_path+path.split(':')
        else:
            base_lib_path=base_lib_path+[path]
    elif isinstance(path,(list,tuple)):
        base_lib_path=base_lib_path+list(path)
    if not virtual_env:
        home=Path('~')
        if isinstance(home,str):
            base_lib_path.append('{}/.local/lib/python3.6/site-packages'.format(home))
        for ii in base_lib_path:
            if os.path.isdir(ii) and not ii in sys.path:
                #sys.path.append(ii)
                sys.path.insert(0,ii)
    if os.getcwd() not in sys.path: sys.path=[os.getcwd()]+sys.path

    if not virtual_env and install_account in ['user','--user','personal','myaccount','account','myself']:
        install_account='--user'
    else:
        install_account=''

    def CheckObj(obj):
        obj_dir=dir(obj)
        obj_name=type(obj).__name__
        if obj_name in ['function']: return obj_name
        if '__dict__' in obj_dir:
            if obj_name == 'type': return 'classobj'
            return 'instance'
        return obj_name.lower()

    ninps=[]
    for inp in inps:
        ninps=ninps+inp.split(',')
    load_failed=[]
    for inp in ninps:
        # if inp is File then automatically get the Path and file name
        # and automatically adding Path to path and import the File Name
        if os.path.isfile(inp): # special file module
            ipath=os.path.dirname(inp)
            ifile=os.path.basename(inp)
            ifile_a=ifile.split('.')
            if len(ifile_a) > 2:
                if dbg:
                    print('*** Not support {} filename'.format(inp))
                continue
            inp=ifile_a[0]
            if ipath not in sys.path:
                sys.path=[ipath]+sys.path
            loaded,module=ModLoad(inp,force=force,globalenv=globalenv,unload=unload,re_load=re_load,ignore_warning=ignore_warning)
            continue
        else: # Check Local File
            inp_a=inp.split()
            inp_chk_file='{}.py'.format(inp_a[1] if inp_a[0] in ['import','from'] else inp)
            if os.path.isfile(inp_chk_file):
                loaded,module=ModLoad(inp,force=force,globalenv=globalenv,unload=unload,re_load=re_load)
                continue
        inp_a=inp.split()
        version=None
        ver_compare=None
        if len(inp_a) in [1,2] and inp_a[0] in ['require','requirement']:
            if os.path.isfile(inp_a[1]):
                rq=[]
                with open(inp_a[1]) as f:
                    rq=f.read().split('\n')
                for ii in rq:
                    if not ii: continue
                    ii_l=ii.split()
                    version=None
                    if len(ii_l) in [2,3]:
                        if '=' in ii_l[1] or '>' in ii_l[1] or '<' in ii_l[1]:
                            if len(ii_l) == 3:
                                version=ii_l[1]+ii_l[2]
                            else:
                                version=ii_l[1]
                    ii_a=ii_l[0].split(':')
                    if len(ii_a) == 2:
                        ic=Install(ii_a[1],install_account,version=version,install_name=install_name)
                    else:
                        ic=Install(ii_a[0],install_account,version=version,install_name=install_name)
                    if ic:
                        loaded,module=ModLoad(ii_a[0],force=force,globalenv=globalenv,re_load=re_load)
            continue
        else:
            ok,module,name,class_name,version,symbol=ModName(inp)
            if ok and version and symbol:
                cur_version=ModVersion(module)
                #Mismatched version or not installed then install
                if cur_version is None or (cur_version and not CompVersion(cur_version,symbol,version)):
                    if symbol in ['>','>=']:
                        Install(module,install_account=install_account,upgrade=True,install_name=install_name)
                    elif symbol in ['==']:
                        Install(module,install_account=install_account,upgrade=True,version='== {}'.format(version),install_name=install_name)
                    elif symbol in ['<','<=']:
                        Install(module,install_account=install_account,upgrade=True,version='{} {}'.format(symbol,version),install_name=install_name)

        #Load module
        loaded,module=ModLoad(inp,force=force,globalenv=globalenv,unload=unload,re_load=re_load)
        if loaded == 2: #unloaded
            continue
        if loaded == 1: #Not found/installed Module
            if not IsNone(requirements):
                if isinstance(requirements,str):
                    requirements=requirements.split(',')
                if isinstance(requirements,(list,tuple)):
                   for i in requirements:
                        ii_l=i.split()
                        version=None
                        upgrade=False
                        if len(ii_l) == 3:
                            if ii_l[1] in ['=','==']:
                                upgrade=True
                                version='== '+ii_l[2]
                            elif ii_l[1] in ['>','>=']:
                                upgrade=True
                            elif ii_l[1] in ['<','<=']:
                                upgrade=True
                                version=ii_l[i]+' '+ii_l[2]
                        ii_a=ii_l[0].split(':')
                        if len(ii_a) == 2:
                            ic=Install(ii_a[1],install_account,version=version,upgrade=upgrade,install_name=install_name)
                        else:
                            ic=Install(ii_a[0],install_account,version=version,upgrade=upgrade,install_name=install_name)
            #Install auto_install and not installed
            elif auto_install and Install(module,install_account,install_name=install_name):
                loaded,module=ModLoad(inp,force=force,globalenv=globalenv,re_load=re_load)
            else:
                if dbg:
                    print('*** Import Error or Need install with SUDO or ROOT or --user permission')
                load_failed.append(inp)
                continue
        if loaded not in [None,0,1]: # import wildcard
            for ii in loaded.__dict__.keys():
                if ii not in ['__name__','__doc__','__package__','__loader__','__spec__','__file__','__cached__','__builtins__']:
                    if ii in globalenv:
                        # swap Same Name between module(my module of the wild card) and class(wild card import class name)
                        if ii in loaded.__dict__.keys():
                            if CheckObj(globalenv[ii]) == 'module' and CheckObj(loaded.__dict__[ii]) == 'classobj':
#                                TMP=globalenv[ii] # move to local temporay 
                                globalenv[ii]=loaded.__dict__[ii]
                                continue
                        if not force: continue # Not force then ignore same name
                    globalenv[ii]=loaded.__dict__[ii]
    return load_failed

def MethodInClass(class_name):
    '''
    Get Method list in Class
    '''
    ret=dir(class_name)
    if hasattr(class_name,'__bases__'):
        for base in class_name.__bases__:
            ret=ret+MethodInClass(base)
    return ret

def ObjInfo(obj):
    '''
    Get object information : type, name, method list, path, module_name, module_version, module
    '''
    rt={}
    rt['type']=type(obj).__name__
    rt['name']=obj.__name__
    rt['methods']=MethodInClass(obj)
    if rt['type'] in ['module']:
        rt['path']=obj.__path__
        rt['version']=ModVersion(rt['name'])
        rt['module_name']=obj.__name__
        rt['module']=obj
    elif rt['type'] in ['function']:
        rt['path']=os.path.abspath(inspect.getfile(obj))
        rt['module']=inspect.getmodule(obj)
        rt['module_name']=rt['module'].__name__
        rt['module_version']=ModVersion(rt['module_name'])
#        rt['methods']=[rt['module_name']]
    elif rt['type'] in ['class']:
        rt['module_name']=obj.__module__
        rt['path']=os.path.abspath(sys.modules[rt['module_name']].__file__)
        rt['module']=sys.modules[rt['module_name']]
        rt['module_version']=ModVersion(rt['module_name'])
    return rt

def MyModule(default=False,parent=-1):
    '''
    Get current module 
    - parent
      -1 : my current python page's module
      0  : my function's module
      1  : my parent's module
    '''
    if parent >= 0:
        loc=1+parent
    else:
        loc=parent
    try:
        #frame=inspect.stack()[-1]
        frame=inspect.stack()
        if len(frame) <= loc:
            loc=-1
        return inspect.getmodule(frame[loc][0])
    except:
        return default

def CallerName(default=False,detail=False):
    '''
    Get the caller name of my group function
    detail=True: return (func name, line number, filename)
    default    : If not found caller name then return default

    def A():               #Group A()
        CallerName()       -> Called by module's A() => A
        B()
    def B():               #Group B()
        CallerName()       -> Called my group by A() function => A
        def C():
            CallerName()   -> Called my group by A() function => A
        C()
    A()                    -> Calling def A() in python script(module)
    '''
    try:
        dep=len(inspect.stack())-2
        name=sys._getframe(dep).f_code.co_name
        if name == '_bootstrap_inner' or name == '_run_code':
            dep=3
        if detail:
            return sys._getframe(dep).f_code.co_name,sys._getframe(dep).f_lineno,sys._getframe(dep).f_code.co_filename
        return sys._getframe(dep).f_code.co_name
    except:
        return default

def Frame2Function(obj,default=False):
    '''
    Get Function Object from frame or frame info
    '''
    obj_type=TypeName(obj)
    #if obj_type == 'function': return obj
    if IsFunction(obj): return obj
    if obj_type == 'frameinfo':
        o_frame_f_code=gc.get_referrers(obj.frame.f_code)
        if isinstance(o_frame_f_code,(list,tuple)) and o_frame_f_code:
            return o_frame_f_code[0]
    elif obj_type == 'frame':
        o_f_code=gc.get_referrers(obj.f_code)
        if isinstance(o_f_code,(list,tuple)) and o_f_code:
            return o_f_code[0]
    return default

def FunctionName(parent=0,default=False,history=False,tree=False,args=False,line_number=False,full_filename=False,filename=False,obj=False,show=False):
    '''
    Get function name
     - parent
       0            : my name (default)
       1            : my parent function
       2-5          : between 2~5's parent functions
       ...          : going top parent function
     - history      : Getting history (return list)
     - tree         : tree  (return list)
                    : if exist parent parameter then history from parent to me
       - show       : show tree on screen
     - args         : show arguments
     - line_number  : show line number
     - filename     : show filename
     - full_filename: show full path filename
     - obj          : Get OBJ (return list)
    '''
    try:
        my_history=inspect.stack()
    except:
        return default
    if tree: history=True
    if history:
        rt=[]
        space=''
        #for i in range(len(my_history)-1,0,-1):
        my_history_m=len(my_history)-1
        my_history_a=[i for i in range(len(my_history)-1)]
        if isinstance(parent,str):
            if '-' in parent:
                parent_a=parent.split('-')
                try:
                    parent_e=int(parent_a[0])
                    #backword
                    end=parent_e if parent_e < len(my_history_a) else 0
                except:
                    end=0
                    parent_e=my_history_a[end]
                if len(parent_a) == 2:
                    try:
                        parent_s=int(parent_a[1])
                        #backword
                        start=parent_s if parent_s > parent_e and parent_s < len(my_history_a) else -1
                    except:
                        start=-1
                else:
                    start=-1
            else:
                start=-1
                end=0
        else:
            try:
                parent=int(parent)
                #backword
                start=my_history_a[parent] if parent < len(my_history_a) else -1
                end=0
            except:
                start=-1
                end=0
        for i in range(my_history_a[start],my_history_a[end],-1):
            if tree:
                if space:
                    pp='{} -> {}'.format(space,my_history[i].function)
                else:
                    pp=my_history[i].function
                if pp == '<module>':
                    if show:
                        print(pp)
                    else:
                        rt.append(pp)
                else:
                    if args:
                        arg=FunctionArgs(Frame2Function(my_history[i].frame),mode='string',default='')
                        if arg: pp=pp+'{}'.format(arg)
                        else: pp=pp+'()'
                    if line_number: pp=pp+' at {}'.format(my_history[i].lineno)
                    if full_filename: pp=pp+' in {}'.format(my_history[i].filename)
                    elif filename: pp=pp+' in {}'.format(os.path.basename(my_history[i].filename))
                    if show:
                        print(pp)
                    else:
                        rt.append(pp)
                space=space+'  '
            else:
                if obj:
                    if full_filename:
                        rt.append((my_history[i].function,Frame2Function(my_history[i].frame),my_history[i].lineno,my_history[i].filename))
                    else:
                        rt.append((my_history[i].function,Frame2Function(my_history[i].frame),my_history[i].lineno,os.path.basename(my_history[i].filename)))
                else:
                    if full_filename:
                        rt.append((my_history[i].function,my_history[i].lineno,my_history[i].filename))
                    else:
                        rt.append((my_history[i].function,my_history[i].lineno,os.path.basename(my_history[i].filename)))
        return rt
    elif isinstance(parent,int): # single function
        if parent >= 0:
            loc=1+parent
        else:
            loc=parent
        if len(my_history) <= loc: #out of range
            loc=-1
        if obj:
            # return name and object
            return (my_history[loc].function,Frame2Function(my_history[loc].frame))
        else:
            rt=my_history[loc].function
            if args:
                arg=FunctionArgs(Frame2Function(my_history[loc].frame),mode='string',default='')
                if arg: rt=rt+'{}'.format(arg)
                else: rt=rt+'()'
            if line_number: rt=rt+' at {}'.format(my_history[loc].lineno)
            if full_filename: rt=rt+' in {}'.format(my_history[loc].filename)
            elif filename: rt=rt+' in {}'.format(os.path.basename(my_history[loc].filename))
            return rt

def FunctionList(obj=None):
    '''
    Get function list in this object
    '''
    aa={}
    if isinstance(obj,str):
       obj=sys.modules.get(obj)
    elif IsNone(obj):
       obj=MyModule(default=None)
    if Type(obj,('classobj','module','instance')):
        if Type(obj,'instance'): obj=obj.__class__ # move CLASS() to CLASS
        for name,fobj in inspect.getmembers(obj):
            if inspect.isfunction(fobj):
                aa.update({name:fobj})
    return aa

def GetClass(obj,default=None):
    '''
    Get Class object from instance,method,function
    '''
    obj_type=TypeName(obj)
    if obj_type in ['instance']:
        obj=obj.__class__ # Convert instance to classobj
        obj_type=TypeName(obj)
    if obj_type in ['classobj']: return obj
    if obj_type in ['method']:
        obj_name = obj.__name__
        if obj.__self__:
            classes = [obj.__self__.__class__]
        else:
            #unbound method
            classes = [obj.im_class]
        while classes:
            c = classes.pop()
            if obj_name in c.__dict__:
                return c
            else:
                classes = list(c.__bases__) + classes
    elif obj_type in ['function']:
        if PyVer(3):
            #caller_module_name=inspect.currentframe().f_back.f_globals['__name__']
            #caller_module=sys.modules[caller_module_name]
            caller_module=inspect.getmodule(inspect.currentframe().f_back)
            return getattr(caller_module_name,'.'.join(obj.__qualname__.split('.')[:-1]))
    return default

def FunctionArgs(func,**opts):
    '''
    Get function's input Arguments
    - mode
      - defaults : get default (V=?,...)
      - args     : get args  (V,V2,...)
      - varargs  : get varargs (*V)
      - keywords : get keywords (**V)
      - string   : return arguments to string format
      - list,tuple: return arguments to list format
      default output : dictioniary format
    - default : if nothing then return default value (default None)
    '''
    mode=opts.get('mode',opts.get('field','defaults'))
    default=opts.get('default',None)
    #if not Type(func,'function','method'):
    if not IsFunction(func):
        return default
    rt={}
    #Not support *v parameter with getargspec()
    #args, varargs, keywords, defaults = inspect.getargspec(func)
    #if not IsNone(defaults):
    #    defaults=dict(zip(args[-len(defaults):], defaults))
    #    del args[-len(defaults):]
    #    rt['defaults']=defaults
    # inspect.getcallargs(<function>,datas....) : automatically matching and put to <functions>'s inputs : Check it later
    try:
        arg = inspect.getfullargspec(func)
    except:
        return rt

    args=arg.args
    varargs=arg.varargs
    keywords=arg.varkw
    defaults=arg.kwonlydefaults
    if not IsNone(arg.defaults):
        if defaults is None:
            defaults=dict(zip(args[-len(arg.defaults):],arg.defaults))
        else:
            defaults.update(dict(zip(args[-len(arg.defaults):],arg.defaults)))
        del args[-len(arg.defaults):]

    if not IsNone(defaults): rt['defaults']=defaults
    if args:
        if args[0] == 'self':
            args=args[1:]
        rt['args']=args
    if varargs: rt['varargs']=varargs
    if keywords: rt['keywords']=keywords
    if Type(mode,(list,tuple)):
        rts=[]
        for ii in rt:
            rts.append(rt.get(ii,default))
        return rts
    else:
        if mode in ['str','string','format']:
            return str(inspect.signature(func))
            #arg_str=''
            #if rt:
            #    for z in rt.get('args',[]):
            #         if arg_str:
            #             arg_str=arg_str+',{}'.format(z)
            #         else:
            #             arg_str='{}'.format(z)
            #    if 'varargs' in rt:
            #         if arg_str:
            #             arg_str=arg_str+',*{}'.format(rt['varargs'])
            #         else:
            #             arg_str='*{}'.format(rt['varargs'])
            #    if 'defaults' in rt:
            #        for z in rt['defaults']:
            #             if arg_str:
            #                 arg_str=arg_str+',{}='.format(z)
            #             else:
            #                 arg_str='{}='.format(z)
            #             if Type(rt['defaults'][z],str):
            #                 arg_str=arg_str+"'{}'".format(rt['defaults'][z])
            #             else:
            #                 arg_str=arg_str+"{}".format(rt['defaults'][z])
            #    if 'keywords' in rt:
            #        if arg_str:
            #             arg_str=arg_str+',**{}'.format(rt['keywords'])
            #        else:
            #             arg_str='**{}'.format(rt['keywords'])
            #return arg_str
        if mode in rt:
            return rt[mode]
        return rt

def Args(src,field='all',default={}):
    '''
    Get Class, instance's global arguments
    Get Function input parameters
    '''
    rt={}
    if Type(src,('classobj','instance')):
        try:
            src=getattr(src,'__init__')
        except:
            return src.__dict__
    #elif not Type(src,'function'):
    elif not IsFunction(src):
        return default
    return FunctionArgs(src,mode=field,default=default)

def Variable(src=None,obj=None,parent=0,history=False,default=False,mode='local',VarType=None,alltype=True):
    '''
    Get available variable data
     - src: 
       if None: return whole environment (dict)
       if string then find the string variable in the environment
       if variable then return that
     - parent 
       0 : my function (default)
       1 : my parents function
       ...
     - history: from me to my top of the functions
     - mode  : variable area
       local : function's local(inside) variable
       global: function's global variable
    '''
    src_type=TypeName(src)
    obj_type=TypeName(obj)
    parent=Int(parent)
    if not isinstance(parent,int): parent=0
    if parent >= 0:
        loc=1+parent
    else:
        loc=parent
    inspst=inspect.stack()
    #inspect.stack()[depth][0] : frame 
    #inspect.getmembers(frame) : environments
    if len(inspst) <= loc: #out of range
        loc=-1
    rt={}
    if obj_type in ['module','classobj','instance']:
        rt.update(obj.__dict__)
    else: # global and locals variables from me to top
        if history:
            for i in range(len(inspst)-1,0,-1):
                if mode in ['global','all']:
                    rt.update(dict(inspect.getmembers(inspst[i][0]))["f_globals"])
                if mode in ['local','all']:
                    rt.update(dict(inspect.getmembers(inspst[i][0]))["f_locals"])
        else:
            if mode in ['global','all']:
                rt.update(dict(inspect.getmembers(inspst[loc][0]))["f_globals"])
            if mode in ['local','all']:
                rt.update(dict(inspect.getmembers(inspst[loc][0]))["f_locals"])
    if src_type=='nonetype':
        if alltype:
            return rt
        o={}
        for i in rt:
            if i in ('__builtins__','__cached__','modules','mod_path') or TypeName(rt[i]) in ('function','module','classobj','instance','builtin_function_or_method','method'): 
                continue
            o[i]=rt[i]
        return o
    elif src_type == 'str':
        out=rt.get(src,default)
        if VarType: # if put expected type then
            if Type(out,VarType): return out # if getting data is expected type then 
            return default # if not expected then return default
        return out # just return gotten data
        #if obj_type in ['module']:
        #    # getattr(<class>,'name') : Get data
        #    # hasattr(<class>,'name') : check name
        #    # setattr(<class>,'name') : update to name
        #    # delattr(<class>,'name') : remove name
        #    if hasattr(obj,src): return getattr(obj,src)
        #elif obj_type in ['class']:
        #    obj=obj()
        #    if hasattr(obj,src): return getattr(obj,src)
        #else: #No object
        #    out=rt.get(src,default)
        #    if VarType: # if put expected type then
        #        if Type(out,VarType): return out # if getting data is expected type then 
        #        return default # if not expected then return default
        #    return out # just return gotten data
    return default

def Uniq(src,default='org',sort=False,strip=False,cstrip=False):
    '''
    make to uniq data
    default='org': return original data
    sort=False   : sort data
    strip=False  : remove white space and make to uniq
    cstrip=False : check without white space, but remain first similar data
    '''
    if isinstance(src,(list,tuple)):
        rt=[]
        if cstrip:
            nsrc=[i.strip() if isinstance(i,(str,bytes)) else i for i in src]
            c=[]
            for i,d in enumerate(nsrc):
                if d not in c:
                    c.append(d)
                    rt.append(src[i])
        else:
            if strip:
                src=[i.strip() if isinstance(i,(str,bytes)) else i for i in src]
            for i in src:
                if i not in rt: rt.append(i)
        if sort: rt=Sort(rt)
        return tuple(rt) if isinstance(src,tuple) else rt
    return Default(src,default)

def Split(src,symbol=None,default=[],sym_spliter='|',listonly=True):
    '''
    multipul split then 'a|b|...'
    without "|" then same as string split function
    symbol=None or ':whitespace:' : Remote white space and split with single space(' ')
    '''
    #SYMBOL Split
    if Type(src,(str,bytes)):
        if symbol is None or IsSame(symbol,':whitespace:'):
            return src.split()
        elif not Type(symbol,(str,bytes)):
            symbol=' '
        if len(symbol) > 1:
            if sym_spliter:
                if Type(symbol,bytes): sym_spliter=Bytes(sym_spliter)
                else: sym_spliter=Str(sym_spliter)
                symbol=Uniq(symbol.split(sym_spliter))
            try:
                msym='|'.join(map(re.escape,tuple(symbol)))
                if Type(src,'bytes'): msym=Bytes(msym)
                else: msym=Str(msym)
                return re.split(msym,src) # splited by '|' or expression
            except:
                pass
        else:
            # Normal split
            try:
                if Type(src,'bytes'): symbol=Bytes(symbol)
                else : symbol=Str(symbol)
                return src.split(symbol)
            except:
                pass
    if default in ['org',{'org'}]:
        if listonly:
            return [src]
        return src
    if listonly:
        if default == []:
            return []
        return [default]
    return default

def FormData(*src,default=None,want_type=None,err=False):
    '''
    convert string data to format
    '1' => 1
    json string to json format
    "{'a':1}" => {'a':1}
    "[1,2,3]" => [1,2,3]
    ....
    '''
    ec=False
    a_s=''
    if len(src) > 0:
        for i in src:
            a_t=Str(i,default='org')
            if isinstance(a_t,str):
                if a_s:
                    a_s=a_s+''' '''+a_t
                else:
                    a_s=a_t
            else:
                ec=True
                break
    if ec:
        if err:
            return False
        if len(src) == 1:
            return src[0]
        return src
    src=a_s
    form_src=None
    if isinstance(src,str):
        if Type(want_type,'str'): return src
        try:
            form_src=ast.literal_eval(src)
        except:
            try:
                form_src=json.loads(src)
            except:
                try:
                    form_src=eval(src)
                except:
                    return Default(src,default)
    else:
        form_src=src
    if IsNone(want_type):
        return form_src
    else:
        if Type(form_src,want_type): return form_src
        return Default(src,default)

def IndexForm(idx,idx_only=False,symbol=None):
    '''
    return : <True/False>, Index Data
     - False: not found Index form from input idx 
     - True : found Index
    Index Data
     - tuple(A,B) : Range Index (A~B)
     - list [A,B] : OR Index or keys A or B
     - Single     : int: Index, others: key
    - idx_only    : only return integer index
    - symbol   : default None, if idx is string and want split with symbol
    '''
    if IsNone(idx):
        return False,None
    elif isinstance(idx,str):
        for s in [':','-','~']: # Range Index
            if s in idx:
                idx_a=idx.split(s)
                if len(idx_a) == 2:
                    ss=Int(idx_a[0]) if IsInt(idx_a[0]) else 0
                    ee=Int(idx_a[1]) if IsInt(idx_a[1]) else -1
                    return True,(ss,ee)
                return False,None
        if '|' in idx: # OR Index
            idx_a=idx.split('|')
            if idx_only:
                rt=[]
                for i in idx_a:
                    if IsInt(i): rt.append(Int(i))
                return True,rt
            return True,idx.split('|')
        elif '/' in idx: # Path index
            idx_a=idx.split('/')
            if idx_a[0] == '':
                return None,idx_a[1:]
            return None,idx_a
        else:
            if idx_only:
                if symbol:
                    idxs=idx.split(symbol)
                    rt=[]
                    for i in idxs:
                        if IsInt(i): rt.append(Int(i))
                    if rt: return True,rt
                    return False,None
                if IsInt(idx):
                    return True,Int(idx)
                return False,None
    elif isinstance(idx,list):
        return True,idx
    elif isinstance(idx,tuple) and len(idx) == 2:
        return True,idx
    return True,idx # Return original

def Get(*inps,**opts):
    '''
    Get (Any) something
    Get('whoami')  : return my function name
    Get('funclist'): return my module's function list
     - parent=1    : my parent's function list
    Get(<list|string|dict|int|...>,<index|key|keypath>): Get data at the <index|key|keypath>
     - keypath : '/a/b/c' => {'a':{'b':{'c':1,'d'}}} => return c's 1
     - key     :
       Range Format from 1 to 5: tuple format (1,5), String format '1-5' or '1:5' or '1~5'
       OR data 1,3,5           : list format  [1,3,5], String format '1|3|5'
         - if found any data then getting that data only
         - if use fill_up option then if error of a key then fill to <fill_up> value at the error location.
     - index   : integer       : single data
    Get('_this_',<key>): my functions's <key>
    Get('<var name>')  : return variable data
    Get('_this_','args')  : return my functions Arguments
    Get(<function>,'args')  : return the functions Arguments
    <option>
      fill_up : If error of the key's value then fill up <fill_up> to right position when the <key> is list
      default : None, any issue
      err     : False, if any error then ignore the data
      idx_only: if input data is dictionary then convert dictionary's keys to input data. So, int idx can get keys(list) name
      _type_  : define to input data's data format (ex: (list,tuple))
      method  : if input is request then can define method('GET','POST',...)
      strip   : default: False, it can strip white space
      peel    : 
          force: just take first data in the list,tuple (if data format has any form also OK, just return the data)
          True : single data(list,tuple,dict) then peel to data (if data format is list,tuple,dict... then return default)
          False: return founded data (any format)
      out     : define to output data (list-> output will list, ...), if wrong format then return default
    '''
    default=opts.get('default')
    err=opts.get('err',opts.get('error',False))
    fill_up=opts.get('fill_up','_fAlsE_')
    idx_only=opts.get('idx_only',opts.get('index_only',False))
    _type=opts.get('_type_',opts.get('type'))
    out=opts.get('out',opts.get('out_form','raw'))
    peel=opts.get('peel')
    strip=opts.get('strip',False)

    if len(inps) == 0:
        return Default(inps,default)
    if len(inps) == 1:
        if inps[0] in ['whoami','myname','funcname','functionname','FunctionName']:
            return FunctionName(parent=opts.get('parent',1)) # my parent's function name
        elif isinstance(inps[0],str):
            if inps[0].lower() in ['func','function','functions','funclist','func_list','list']:
                return FunctionList(parent=opts.get('parent',-1)) # default: my page's function list
            return Variable(inps[0],parent=opts.get('parent',1)) # my parent's variable
    inps=list(inps)
    obj=inps[0]
    if IsNone(obj):
        return Default(obj,default)
    del inps[0]
    if len(inps) == 1:
        idx=inps[0]
    elif len(inps) > 1:
        if isinstance(obj,(list,tuple)) and not isinstance(inps[-1],int) and 'default' not in opts:
            idx=inps[:-1]
            default=inps[-1]
        else:
            idx=inps[:]
    else:
        idx=None
    #When check type
    if _type is not None:
        if not Type(obj,_type):
            return Default(obj,default)
    ok,nidx=IndexForm(idx,idx_only=idx_only)
    idx_type=type(nidx).__name__
    if obj == '_this_':
        obj_type='function'
    else:
        obj_type=TypeName(obj)
    if ok and obj_type in ('list','tuple','str','bytes'):
        if idx_type == 'tuple':
            ss=_obj_max_idx_(obj,Int(nidx[0]),err)
            ee=_obj_max_idx_(obj,Int(nidx[1]),err)
            if Type(ss,int) and Type(ee,int):
                return obj[ss:ee+1]
        elif idx_type == 'list':
            rt=[]
            for i in nidx:
                ix=_obj_max_idx_(obj,Int(i,default=False,err=True),err)
                if Type(ix,int):
                    rt.append(obj[ix])
                elif fill_up != '_fAlsE_':
                    rt.append(fill_up)
            return OutFormat(rt,out=out,default=default,org=obj,peel=peel,strip=strip)
        elif idx_type == 'int':
            ix=_obj_max_idx_(obj,nidx,err)
            if Type(ix,int): return obj[ix]
        if idx in dir(obj):
            return obj.__dict__.get(idx)
        return Default(obj,default)
    elif obj_type in ('dict'):
        return DICT(obj).Get(idx,**opts)
    elif obj_type in ('function'): #???
        if ok:
            if idx_type == 'str':
                if nidx.lower() in ['args','arguments']:
                    if obj == '_this_':
                        obj=inspect.getmembers(MyModule()).get(CallerName())
                    return FunctionArgs(obj)
                else:
                    if obj == '_this_':
                        return Variable(nidx,parent=1)
                    return Varable(nidx,obj)
            elif idx_type == 'list':
                rt=[]
                for i in nidx:
                    if Type(i,str) and i.lower() in ['args','arguments']:
                        if obj == '_this_':
                            obj2=inspect.getmembers(MyModule()).get(CallerName())
                            rt.append(FunctionArgs(obj2))
                        else:
                            rt.append(FunctionArgs(obj))
                    else:
                        if obj == '_this_':
                            rt.append(Variable(nidx,parent=1))
                        else:
                            rt.append(Variable(nidx,obj))
                return OutFormat(rt,out=out,default=default,org=obj,peel=peel,strip=strip)
    elif obj_type in ('instance','classobj','module','Model'):
        if Type(idx,int):
            if isinstance(obj,kRT):
                return obj.get(key=idx,default=[],mode=list)
        elif Type(idx,str) and idx.lower() in ['func','function','functions','funclist','func_list','list']:
            return FunctionList(obj)
        elif idx_type in ['list','tuple']: #OR Index
            rt=[]
            # get function object of finding string name in the class/instance
            for ff in nidx:
                if isinstance(ff,str):
                    if ff in ['__name__','method_name','__method__']: #Get Method name list in class
                        if obj_type in ('classobj'): obj=obj() # move from CLASS to CLASS()
                        if Type(obj,'instance'):
                            rt=rt+MethodInClass(obj)
                    else:
                        try:
                            rt.append(getattr(obj,ff,default))
                        except Exception as e:
                            if err:
                                print(f"An error occured: {e}")
                                raise
                            else:
                                pass
            return OutFormat(rt,out=out,default=default,org=obj,peel=peel,strip=strip)
        elif idx_type == 'str':
            if obj_type == 'classobj': obj=obj() # move CLASS to CLASS()
            return getattr(obj,nidx,Default(obj,default))
        else:
            if Type(obj,'classobj'): obj=obj() # move from CLASS to CLASS()
            if ok is False:
                return obj.__dict__
            else:
                return Get(obj.__dict__,idx,default,err) # converted obj with original idx
    elif obj_type in ('response'): # Web Data
        if ok:
            def _web_(obj,nidx):
                if nidx in ['rc','status','code','state','status_code']:
                    return obj.status_code
                elif nidx in ['data','value','json']:
                    try:
                        return FormData(obj.text)
                    except:
                        if err is True: return Default(obj,default)
                        return obj.text
                elif nidx in ['text','str','string']:
                    return obj.text
                else:
                    return obj
            if idx_type=='str':
                return _web_(obj,nidx)
            elif idx_type == 'list':
                rt=[]
                for ikey in nidx:
                    rt.append(_web_(obj,ikey))
                return OutFormat(rt,out=out,default=default,org=obj,peel=peel,strip=strip)
    elif obj_type in ('request'): # Web Data2
        rt=[]
        method=opts.get('method',None)
        if IsNone(method): method=obj.method.upper()
        elif isinstance(method,str): method=method.upper()

        if ok:
            def _web_data(obj,nkey,method,default):
                if nkey.lower() == 'method':
                    return method
                if method=='GET':
                    rt=obj.GET.get(nkey)
                    if not IsNone(rt): return rt
                    return Default(obj,default)
                elif method=='FILE':
                    rt=obj.FILES.getlist(nkey,default)
                    if not IsNone(rt):
                        return OutFormat(rt,out=out,peel=peel,strip=strip,default=default)
                    return Default(obj,default)
                elif method=='POST':
                    rt=obj.FILES.getlist(nkey)
                    if not IsNone(rt):
                        return OutFormat(rt,out=out,peel=peel,strip=strip,default=default)
                    rt=obj.POST.getlist(nkey)
                    if not IsNone(rt):
                        return OutFormat(rt,out=out,peel=peel,strip=strip,default=default)
                    return Default(obj,default)
            if idx_type == 'str':
                return _web_data(obj,nidx,method,default)
            elif idx_type == 'list':
                rt=[]
                for i in nidx:
                    rt.append(_web_data(obj,i,method,default))
                return OutFormat(rt,out=out,default=default,org=obj,peel=peel,strip=strip)
    elif obj_type in ('ImmutableMultiDict'): # Flask Web Data
        tmp={}
        if obj:
            for ii in obj:
                tmp[ii]=obj[ii]
        return Get(tmp,idx,default,err) 
    elif obj_type in ('kDict','DICT'): 
        #Block infinity loop
        #return Get(obj.Get(),idx,default,err)
        return Get(dict(obj.Get()),idx,default=default,err=err,fill_up=fill_up,idx_only=idx_only,_type=_type,out=out,peel=peel,strip=strip) 
    elif obj_type in ('kList'): 
        #Block infinity loop
        #return Get(obj.Get(),idx,default,err)
        return Get(list(obj.Get()),idx,default=default,err=err,fill_up=fill_up,idx_only=idx_only,_type=_type,out=out,peel=peel,strip=strip) 
    return OutFormat([],out=out,default=default,org=obj,peel=peel,strip=strip)

def Set(obj,key,value,**opts):
    force=opts.get('force',opts.get('append'))
    insert=opts.get('insert') # for list
    default=opts.get('default')
    if isinstance(obj,dict):
        if isinstance(key,str):
            key_a=key.split('/')
        else:
            key_a=[key]
        if key_a[0] == '':
            key_a=key_a[1:]
        for kk in key_a[:-1]:
            if kk not in obj:
                if not force: return default
                obj[kk]={} # create/insert
            obj=obj[kk]
        obj[key_a[-1]]=value # replace or put
        return True
    elif isinstance(obj,list):
        if isinstance(key,int):
            if abs(key) < len(obj):
                if insert:
                    obj=obj[:insert]+[value]+obj[insert:] # insert
                else:
                    obj[key]=value # replace
            else:
                if not force: return default
                if key < 0:
                    if insert:
                        obj=[value]+obj # insert
                    else:
                        obj[0]=value # replace
                else:
                    if insert:
                        obj.append(value) # insert
                    else:
                        obj[-1]=value # replace
            return True
    return default

def TryCode(code,default=False,_return_=True):
    '''
    Run string code
    default :False
    _return_: True: return output, False: print on screen
    '''
    if Type(code,str):
        err=None
        rt=None
        if _return_:
            # create file-like string to capture output
            codeOut = StringIO()
            codeErr = StringIO()
            sys.stdout.flush()
            sys.stderr.flush()
            sys.stdout=codeOut # Standard Out from application
            sys.stderr=codeErr # Standard Error from application
        try:
            exec(code)
        except:
            #Code Error message
            err=ExceptMessage()
        finally:
            if _return_:
                sys.stdout.flush()
                sys.stderr.flush()
                #recover/restore stdout and stderr
                sys.stdout=sys.__stdout__
                sys.stderr=sys.__stderr__
                #Get value 
                rt=codeOut.getvalue()
                er=codeErr.getvalue()
                #Close IO
                codeOut.close()
                codeErr.close()
            if err: #Code Error
                if _return_:
                    return False,rt,err
                else:
                    StdErr(err)
            if _return_:
                # Standard Out and Error
                return True,rt,er
    if _return_:
        return False,rt,'Not String code. required *STRING* Code.'  #Not a string code

def ExceptMessage(msg='',default=None):
    '''
    Try:
       AAA
    Except:
       err=ExceptMessage() => If excepting then taken error or traceback code and return it
    '''
    e=sys.exc_info()[0]
    er=traceback.format_exc()
    if e or er != 'NoneType: None\n':
        if msg:
            msg='{}\n\n{}\n\n{}'.format(msg,e,er)
        else:
            msg='\n\n{}\n\n{}'.format(e,er)
        return msg
    return default


class HOST:
    def __init__(self):
        pass

    def Name(self):
        return socket.gethostname()

    def DefaultRouteDev(self,default=None,gw=None):
        for ii in Split(cat('/proc/net/route',no_edge=True),'\n',default=[]):
            ii_a=ii.split()
            #if len(ii_a) > 8 and '00000000' == ii_a[1] and '00000000' == ii_a[7]: return ii_a[0]
            if len(ii_a) < 4 or ii_a[1] != '00000000' or not int(ii_a[3], 16) & 2:
                #If not default route or not RTF_GATEWAY, skip it
                continue
            if gw:
                if IsSame(socket.inet_ntoa(struct.pack("<L", int(ii_a[2], 16))),gw):
                    return ii_a[0]
            else:
                return ii_a[0]
        return default

    def DefaultRouteIp(self,default=None):
        for ii in Split(cat('/proc/net/route',no_edge=True),'\n'):
            ii_a=ii.split()
            if len(ii_a) < 4 or ii_a[1] != '00000000' or not int(ii_a[3], 16) & 2:
                #If not default route or not RTF_GATEWAY, skip it
                continue
            return socket.inet_ntoa(struct.pack("<L", int(ii_a[2], 16)))
        return default

    def Ip(self,ifname=None,mac=None,default=None):
        if IsNone(ifname):
            if IsNone(mac) : mac=self.Mac()
            ifname=self.DevName(mac)

        if ifname:
            if not os.path.isdir('/sys/class/net/{}'.format(ifname)):
                return default
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                return socket.inet_ntoa(fcntl.ioctl(
                    s.fileno(),
                    0x8915,  # SIOCGIFADDR
                    struct.pack('256s', ifname[:15])
                )[20:24])
            except:
                try:
                    return os.popen('ip addr show {}'.format(ifname)).read().split("inet ")[1].split("/")[0]
                except:
                    return default
        return socket.gethostbyname(socket.gethostname())

    def IpmiIp(self,default=None):
        rt=rshell('''ipmitool lan print 2>/dev/null| grep "IP Address" | grep -v Source | awk '{print $4}' ''')
        if rt[0]:return rt[1]
        return default

    def IpmiMac(self,default=None):
        rt=rshell(""" ipmitool lan print 2>/dev/null | grep "MAC Address" | awk """ + """ '{print $4}' """)
        if rt[0]:return rt[1]
        return default

    def Mac(self,ip=None,dev=None,default=None,ifname=None):
        #if dev is None and ifname: dev=ifname
        if IsNone(dev) and ifname: dev=ifname
        if IpV4(ip):
            dev_info=self.NetDevice()
            for dev in dev_info.keys():
                if self.Ip(ifname=dev) == ip:
                    return dev_info[dev]['mac']
        #ip or anyother input of device then getting default gw's dev
        if IsNone(dev): dev=self.DefaultRouteDev()
        if dev:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', Bytes(dev[:15])))
                return Join(['%02x' % ord(char) for char in Str(info[18:24])],symbol=':')
            except:
                return default
        #return ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
        return MacV4('%012x' % uuid.getnode())

    def DevName(self,mac=None,default=None):
        if IsNone(mac):
            mac=self.Mac()
        net_dir='/sys/class/net'
        if isinstance(mac,str) and os.path.isdir(net_dir):
            dirpath,dirnames,filenames = list(os.walk(net_dir))[0]
            for dev in dirnames:
                fmac=cat('{}/{}/address'.format(dirpath,dev),no_edge=True)
                if isinstance(fmac,str) and fmac.strip().lower() == mac.lower():
                    return dev
        return default

    def Info(self):
        return {
         'host_name':self.Name(),
         'host_ip':self.Ip(),
         'host_mac':self.Mac(),
         'ipmi_ip':self.IpmiIp(),
         'ipmi_mac':self.IpmiMac(),
         }

    def NetDevice(self,name=None,default=False):
        def _dev_info_(path,name):
            drv=ls('{}/{}/device/driver/module/drivers'.format(path,name))
            if drv is False:
                drv='unknown'
            else:
                drv=drv[0].split(':')[1]
            return {
                'mac':cat('{}/{}/address'.format(path,name),no_end_newline=True),
                'duplex':cat('{}/{}/duplex'.format(path,name),no_end_newline=True,file_only=False),
                'mtu':cat('{}/{}/mtu'.format(path,name),no_end_newline=True),
                'state':cat('{}/{}/operstate'.format(path,name),no_end_newline=True),
                'speed':cat('{}/{}/speed'.format(path,name),no_end_newline=True,file_only=False),
                'id':cat('{}/{}/ifindex'.format(path,name),no_end_newline=True),
                'driver':drv,
                'drv_ver':cat('{}/{}/device/driver/module/version'.format(path,name),no_end_newline=True,file_only=False,default=''),
                }


        net_dev={}
        net_dir='/sys/class/net'
        if os.path.isdir(net_dir):
            dirpath,dirnames,filenames = list(os.walk(net_dir))[0]
            if name:
                if name in dirnames:
                    net_dev[name]=_dev_info_(dirpath,name)
            else:
                for dev in dirnames:
                    net_dev[dev]=_dev_info_(dirpath,dev)
            return net_dev
        return default

    def Alive(self,ip,keep=20,interval=3,timeout=1800,default=False,log=None,cancel_func=None):
        time=TIME()
        run_time=time.Int()
        if IpV4(ip):
            if log:
                log('[',direct=True,log_level=1)
            while True:
                if time.Out(timeout_sec):
                    if log:
                        log(']\n',direct=True,log_level=1)
                    return False,'Timeout monitor'
                if IsBreak(cancel_func):
                    if log:
                        log(']\n',direct=True,log_level=1)
                    return True,'Stopped monitor by Custom'
                if ping(ip,cancel_func=cancel_func):
                    if (time.Int() - run_time) > keep:
                        if log:
                            log(']\n',direct=True,log_level=1)
                        return True,'OK'
                    if log:
                        log('-',direct=True,log_level=1)
                else:
                    run_time=time.Int()
                    if log:
                        log('.',direct=True,log_level=1)
                time.Sleep(interval)
            if log:
                log(']\n',direct=True,log_level=1)
            return False,'Timeout/Unknown issue'
        return default,'IP format error'

    def Ping(self,ip,keep_good=10,timeout=3600):
        if IpV4(ip):
            return ping(ip,keep_good=keep_good,timeout=timeout)

def IpV4(ip=None,out='str',default=False,port=None,bmc=False,used=False,pool=None,support_hostname=False,ifname=False):
    '''
    check/convert IP
    ip : int, str, domainname, ethernet dev name, None
    out:
      str : default : convert to xxx.xxx.xxx.xxx format
      int : convert to int format
      hex : convert to hex format
    port: if you want check the IP with port then type
    bmc : default False, True: check BMC port (623,664,443)
    return : IP, if fail then return default value
    used:
      * required port option, but check with single port
      False: default (not check)
      True: Check IP already used the port(return True) or still available(return False)
    pool:
      Tuple: if give IP Pool(start,end) then check the IP is in the POOL range or not.
      List : IP is in the Pool list
    ifname:
      True: ip will network device name then find ip address
    '''
    if IsIn(ip,['my_ip','local_ip','host_ip','hostip','localip','myip']):
        return HOST().Ip()
    elif IsIn(ip,['default_route','defaultroute','route','routing']):
        return HOST().DefaultRouteIp()

    if ifname is True:
        if isinstance(ip,str) and ip:
            if not os.path.isdir('/sys/class/net/{}'.format(ip)):
                return default
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                return socket.inet_ntoa(fcntl.ioctl(
                    s.fileno(),
                    0x8915,  # SIOCGIFADDR
                    struct.pack('256s', ip[:15])
                )[20:24])
            except:
                try:
                    dev_info=os.popen('ip addr show {}'.format(ip))
                    if dev_info:
                        found_ip=dev_info.read().split("inet ")[1].split("/")[0]
                        dev_info.close()
                        return found_ip
                except:
                    return default
        return socket.gethostbyname(socket.gethostname())

    if IsNone(ip): return default    

    def IsOpenPort(ip,port):
        '''
        It connectionable port(?) like as ssh, ftp, telnet, web, ...
        '''
        tcp_sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_sk.settimeout(1)
        rt=[]
        for pt in port:
            try:
                tcp_sk.connect((ip,pt))
                tcp_sk.close()
                rt.append(pt)
            except:
                pass
        return rt
    def IsUsedPort(ip,port):
        '''
        The IP already used the port, it just checkup available port or alread used
        '''
        if IsNone(ip,chk_val=[None,'','localhost','local']):
            ip='127.0.0.1'
        soc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rt=[]
        for pt in port:
            try:
                location=(ip,pt)
                rt=soc.connect_ex(location)
                soc.close()
                #rt==0 then already used
                if rt == 0: rt.append(pt)
            except:
                pass
        return rt
    if port == 'bmc':
        bmc=True
        port=None
    if bmc: # Update BMC Port
        default_bmc_port=[623,664,443]
        if not IsNone(port):
            port=Int(port,default=False)
            if isinstance(port,(list,tuple)):
                for i in port:
                    if i not in default_bmc_port: default_bmc_port.append(i)
            elif isinstance(port,int):
                if port not in default_bmc_port:
                    default_bmc_port.append(port)
        port=tuple(default_bmc_port)
    if port:
        port=Int(port,default=False)
        if port is False: return default
        if Type(port,int): port=[port]
    ip_int=None
    if isinstance(ip,str):
        ipstr=ip.strip()
        if '0x' in ipstr:
            ip_int=int(ipstr,16)
        elif ipstr.isdigit():
            ip_int=int(ipstr)
        elif '.' in ipstr:
            try:
                ip_int=struct.unpack("!I", socket.inet_aton(ipstr))[0] # convert Int IP
                #struct.unpack("!L", socket.inet_aton(ip))[0]
            except:
                if support_hostname:
                    try: # hostname abc.def case
                        return IpV4(socket.gethostbyname(ipstr),out=out,default=default,port=port,bmc=bmc,used=used,pool=pool)
                    except:
                        return default
        elif support_hostname: # hostname abc case
            try:
                return IpV4(socket.gethostbyname(ipstr),out=out,default=default,port=port,bmc=bmc,used=used,pool=pool)
            except:
                return default
    elif isinstance(ip,int) and not isinstance(ip,bool):
        try:
            socket.inet_ntoa(struct.pack("!I", ip)) # check int is IP or not
            ip_int=ip
        except:
            return default
    elif isinstance(ip,type(hex)):
        ip_int=int(ip,16)

    if not IsNone(ip_int):
        try:
            if out in ['int',int]:
                return ip_int
            elif out in ['hex',hex]:
                return hex(ip_int)
            elif isinstance(pool,tuple):
                if len(pool) == 1:
                    return IpV4(pool[0],out=int) <= ip_int
                elif len(pool) == 2:
                    if not pool[0] and pool[1]:
                        return ip_int <= IpV4(pool[1],out=int)
                    elif not pool[1] and pool[0]:
                        return IpV4(pool[0],out=int) <= ip_int 
                    elif pool[0] and pool[1]:
                        return IpV4(pool[0],out=int) <= ip_int <= IpV4(pool[1],out=int)
                    else:
                        return default
            elif isinstance(pool,list):
                pool=[IpV4(i,out=int) for i in pool]
                return ip_int in pool
            else: #default to str
                ip_str=socket.inet_ntoa(struct.pack("!I", ip_int))
                if port: # If bing Port then check the port
                    if used:
                        rt=IsUsedPort(ip_str,port)
                        if rt: return rt
                    else:
                        rt=IsOpenPort(ip_str,port)
                        if rt: return rt
                else:
                    return ip_str
        except:
            pass
    return default

def ping(host,**opts):
    ICMP_ECHO_REQUEST = 8 # Seems to be the same on Solaris. From /usr/include/linux/icmp.h;
    ICMP_CODE = socket.getprotobyname('icmp')
    ERROR_DESCR = {
        1: ' - Note that ICMP messages can only be '
           'sent from processes running as root.',
        10013: ' - Note that ICMP messages can only be sent by'
               ' users or processes with administrator rights.'
        }
    def checksum(msg):
        sum = 0
        size = (len(msg) // 2) * 2
        for c in range(0,size, 2):
            sum = (sum + ord(msg[c + 1])*256+ord(msg[c])) & 0xffffffff
        if size < len(msg):
            sum = (sum+ord(msg[len(msg) - 1])) & 0xffffffff
        ra = ~((sum >> 16) + (sum & 0xffff) + (sum >> 16)) & 0xffff
        ra = ra >> 8 | (ra << 8 & 0xff00)
        return ra

    def mk_packet(size):
        """Make a new echo request packet according to size"""
        # Header is type (8), code (8), checksum (16), id (16), sequence (16)
        header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, size, 1)
        #data = struct.calcsize('bbHHh') * 'Q'
        data = size * 'Q'
        my_checksum = checksum(Str(header) + data)
        header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0,
                             socket.htons(my_checksum), size, 1)
        return header + Bytes(data)

    def receive(my_socket, ssize, stime, timeout):
        while True:
            if timeout <= 0:
                return
            ready = select.select([my_socket], [], [], timeout)
            if ready[0] == []: # Timeout
                return
            received_time = time.time()
            packet, addr = my_socket.recvfrom(1024)
            type, code, checksum, gsize, seq = struct.unpack('bbHHh', packet[20:28]) # Get Header
            if gsize == ssize:
                return received_time - stime
            timeout -= received_time - stime

    def ping_func(ip,timeout=1,size=64):
        try:
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)
        except socket.error as e:
            if e.errno in ERROR_DESCR:
                raise socket.error(''.join((e.args[1], ERROR_DESCR[e.errno])))
                #raise socket.error(Join((e.args[1], ERROR_DESCR[e.errno]),symbol=''))
            raise
        if size in ['rnd','random']:
            # Maximum size for an unsigned short int c object(65535)
            size = int((id(timeout) * random.random()) % 65535)
        packet = mk_packet(size)
        while packet:
            sent = my_socket.sendto(packet, (ip, 1)) # ICMP have no port, So just put dummy port 1
            packet = packet[sent:]
        delay = receive(my_socket, size, TIME().Time(), timeout)
        my_socket.close()
        if delay:
            return delay,size

    def _ping_(ip,timeout=1,size=64,log_format='ping'):
            ping_cmd=find_executable('ping')
            if ping_cmd:
                ping_s=size-8 if size >= 8 else 0
                rc=rshell("ping -s {} -c 1 {}".format(ping_s,host))
                delay=[]
                if rc[0] == 0:
                    delay=[]
                    tt=rc[1].split('\n')[1].split()
                    delay=[float(tt[6].split('=')[1])/1000,tt[0]]
            else:
               delay=ping_func(ip,timeout,size)
            if log_format == 'ping':
                if delay:
                    return 0,ip,size,timeout,delay[1],round(delay[0]*1000.0,4)
                else:
                    return 1,ip,size,timeout,None,None
            else:
                if delay:
                    return 0,'.',size,timeout,None,None
                else:
                    return 1,'x',size,timeout,None,None

    '''
    same as ping command
    True : pinging
    False: can not ping
    0    : Canceled ping
    '''
    count=Int(opts.get('count'),0)
    interval=Int(opts.get('interval'),1)
    keep_good=Int(opts.get('keep_good',opts.get('keep_ping',opts.get('keep',opts.get('good',opts.get('pinging'))))),0)
    keep_bad=Int(opts.get('keep_bad',opts.get('bad')),0)
    timeout=Int(opts.get('timeout',opts.get('timeout_sec')),0)
    lost_mon=opts.get('lost_mon',False)
    log=opts.get('log',None)
    log_format=opts.get('log_format','.')
    #. : print dot(.) during process
    #ping : print linux command's ping log
    #d : print dot(.) during process
    #s : print dot(.) during process
    #i : not print during process. just return result only
    alive_port=opts.get('alive_port')
    support_hostname=opts.get('support_hostname',True)
    end_newline=opts.get('end_newline',opts.get('newline',opts.get('end','\n')))
    cancel_func=opts.get('cancel_func',opts.get('stop_func',opts.get('cancel',opts.get('stop',None))))
    cancel_args=opts.get('cancel_args',opts.get('stop_args',opts.get('cancel_arg',opts.get('stop_arg',{}))))
    if not isinstance(cancel_args,dict): cancel_args={}
    if alive_port:
        return True if IpV4(host,port=alive_port,support_hostname=support_hostname) else False
    good=False
    Time=TIME()
    gTime=TIME()
    bTime=TIME()
    dspi='d' if log_format =='d' else 's' if log_format not in ['n','i'] else 'i'
    local_printed=False
    i=0
    while True:
       if IsBreak(cancel_func,**cancel_args):
          printf('- ping({}) - Canceled/Stopped ping by cancel signal'.format(host),first_newline=True,log=log,dsp=dspi)
          break
       rc=_ping_(host,timeout=1,size=64,log_format=log_format)
       if rc[0] == 0:
          good=True
          if not count:
              bTime.Reset()
              if keep_good:
                  if gTime.Out(keep_good): break
              else:
                  break
          if log_format == 'ping':
              printf('{} bytes from {}: icmp_seq={} ttl={} time={} ms'.format(rc[4],rc[1],i,rc[2],rc[5]),log=log,dsp=dspi)
          elif dspi in ['d','s']:
              printf('.',direct=True,log=log,log_level=1,dsp=dspi,scr_dbg=False)
              local_printed=True
       else:
          good=False
          if not count:
              gTime.Reset()
              if keep_bad:
                  if bTime.Out(keep_bad): break
          if log_format == 'ping':
              printf('{} icmp_seq={} timeout ({} second)'.format(rc[1],i,rc[3]),log=log,dsp=dspi)
          elif dspi in ['d','s']:
              printf('x',direct=True,log_level=1,log=log, dsp=dspi,scr_dbg=False)
              local_printed=True
       if count:
           count-=1
           if count < 1: break
       if Time.Out(timeout): break
       time.sleep(interval)
       i+=1
    if end_newline:
        if local_printed: printf('',log=log, no_intro=True, dsp=dspi,caller_parent=1,ignore_empty=False)
    return good

class PAGE:
    '''
    Web site page and URL design
    '''
    def __init__(self,request=None,data=None,base='',others=None,prange=25):
        if request:
            self.requests=request
        else:
            Import('import requests')
            self.requests=requests
        self.prange=prange
        self.parameters=dict(self.requests.args)
        page=self.requests.args.get('page',0)
        if self.requests.method=='POST':
            parameters=dict(self.requests.form)
            self.parameters.update(parameters)
            if 'page' in self.parameters: page=self.parameters.get('page')
        try:
            self.page=int(page)
        except:
            self.page=0
        self.total=0
        if isinstance(data,(list,dict,tuple)):
            self.total=len(data)
        self.total_page=self.total//self.prange
        self.base=base
        self.others=others
        self.start=self.page*self.prange
        self.end=self.start+self.prange
    def url(self,base=None,ignore=None,**opts):
        args=''
        for i in self.parameters:
            if isinstance(ignore,list) and i in ignore: continue
            if i in opts:
                oo=opts.pop(i)
                args=args+'{}{}={}'.format('&' if args else '',i,oo)
            else:
                args=args+'{}{}={}'.format('&' if args else '',i,self.parameters[i])
        for i in opts:
            args=args+'{}{}={}'.format('&' if args else '',i,opts[i])
        if isinstance(base,str) and base:
            if base[-1] == '?':
                return base+ args
            else:
                return base+'?' + args
        else:
            return self.base+'?' + args
    def get(self,name=None):
        if isinstance(self.parameters,dict):
            if name and name in self.parameters:
                return self.parameters[name]
        if name and name in self.__dict__:
            return self.__dict__[name]
        self.parameters
    def pages(self):
        html_page=''
        if self.page > 0 :
            next_page=self.page-1
            oo=self.url(ignore=['page'])
            if oo: oo=oo+'&'
            html_page='''{0}
            <a href="{1}"> |< </a>
            <a href="{2}page={3}"> << </a>'''.format(html_page,self.url(page=0),oo,next_page)
        else:
            html_page='''{0} |< << '''.format(html_page)
        html_page='''{}[{}]'''.format(html_page,self.page)
        if self.page < self.total_page:
            next_page=self.page+1
            oo=self.url(ignore=['page'])
            if oo : oo=oo+'&'
            html_page='''{0}
            <a href="{1}page={2}"> >> </a>
            <a href="{1}page={3}"> >| </a>
           '''.format(html_page,oo,next_page,self.total_page)
        else:
            html_page='''{0}
             >>  >|
           '''.format(html_page)
        return html_page

class WEB:
    '''
    GetIP: get server or client IP
    Request: request()
    str2url: convert string to URL format
    form2dict: convert form data to dictionary format
    '''
    def __init__(self,request=None):
        if request:
            self.requests=request
        else:
            Import('import requests')
            self.requests=requests

    def Session(self):
        return self.requests.session._get_or_create_session_key()

    def GetIP(self,mode='server'):
        ''' 
        mode:
          server : get server IP (default)
          client : get client IP
        '''
        if mode == 'server':
            return self.requests.get_host().split(':')
        else:
            x_forwarded_for = self.requests.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                return x_forwarded_for.split(',')[0]
            else:
                return self.requests.META.get('REMOTE_ADDR')

    def Method(self,method_name=None,mode='lower'):
        method_n=self.requests.method
        if method_name:
            return method_name.lower() == method_n.lower()
        else:
            if mode == 'upper':
                return method_n.upper()
            else:
                return method_n.lower()

    def Request(self,host_url,**opts):
        '''
        user & password: string format
        auth: tuple format
        data: dictionary format
        json: dictionary / JSON format
        files: dictionary format
           ex) files = { '<file parameter name>': (<filename>, open(<filename>,'rb'))}
        headers: string or dictionary format
           - string example
             headers='json'
             required data or json 
           - dictionary example
             headers = { "Content-Type": "application/json"}
        dbg : True: show debuging log(default), False ignore debugging log
        ping: True: Check dest IP with ping, False: not check dest IP (default)
        max_try: default 3, retry max number when failed
        mode: default get, (get,post,patch)
        ip: dest IP
        port: default 80 or 443, arrcording to http or https, if you want special port then type
        bmc: default False, True then automaticall check BMC port
        timeout: request timeout (seconds), default None
        '''
        # remove SSL waring error message (test)
        self.requests.packages.urllib3.disable_warnings()

        ip=opts.get('ip',None)
        port=opts.get('port',None)
        bmc=opts.get('bmc',False)
        mode=opts.get('mode',opts.get('method','get'))
        max_try=opts.get('max_try',opts.get('retry',opts.get('loop',opts.get('try',3)))) # Retry max number
        auth=opts.get('auth',None)
        user=opts.get('user',None)
        passwd=opts.get('passwd',None)
        data=opts.get('data',None) # dictionary format
        json_data=opts.get('json',None) # dictionary format
        files=opts.get('files',None) # dictionary format
        request_url=opts.get('request_url',None)
        dbg=opts.get('dbg',False)  # show debugging log
        log=opts.get('log') 
        chk_ping=opts.get('ping',False) # check ping to IP
        timeout=opts.get('timeout',None) # request timeout
        command_timeout=opts.get('command_timeout',None)
        ping_good=Int(opts.get('ping_good'),10)
        if IsInt(command_timeout): chk_ping=True
        req_data={}
        chk_dest=None
        if isinstance(timeout,int): req_data['timeout']=timeout
        if opts.get('https'): req_data['verify']=False
        if Type(auth,'tuple',data=True):
            req_data['auth']=opts.get('auth')
        elif Type(user,'str',data=True) and Type(passwd,'str',data=True):
            req_data['auth']=(user,passwd)
        if Type(data,'dict',data=True): req_data['data']=opts.get('data')
        if Type(json_data,'dict',data=True): req_data['json']=json_data
            
        if Type(files,'dict',data=True): req_data['files']=opts.get('files')
        headers=opts.get('headers') # dictionary format
        if Type(headers,'str',data=True):
            if headers == 'json':
                headers={ "Content-Type": "application/json"}
                if data:
                    data=json.dumps(data)
                    req_data['data']=data
                elif json_data:
                    data=json.dumps(json_data)
                    if 'json' in req_data: req_data.pop('json')
                    req_data['data']=data
        elif Type(headers,'dict',data=True):
            req_data['headers']=headers
        if not IsNone(ip):
            ip=IpV4(ip,out=str,support_hostname=True)
            chk_dest='{}'.format(ip)
            if req_data.get('verify',True):
                host_url='http://{}'.format(ip)
            else:
                host_url='https://{}'.format(ip)
            if not IsNone(port): host_url='{}:{}'.format(host_url,port)
            if not IsNone(request_url): host_url='{}/{}'.format(host_url,request_url)
        elif Type(host_url,'str',data=True) and host_url.startswith('http'):
            chk_dest=re.compile('(http|https)://([a-zA-Z0-9.]*)[:/]').findall(host_url)
            if len(chk_dest)==0:
                chk_dest=re.compile('(http|https)://([a-zA-Z0-9.]*)').findall(host_url)
            if len(chk_dest):
                chk_dest=chk_dest[0][1]
                if host_url.find('https://') == 0:
                    req_data['verify']=False
        if IsNone(chk_dest):
            return False,'host_url or ip not found'
        if chk_ping and chk_dest:
            ping_rc=ping(chk_dest,timeout=3,support_hostname=True,log_format='i')
            if not isinstance(ping_rc,bool) and ping_rc==0:
                return 0,'Canceled'
            elif not ping_rc:
                if IsInt(command_timeout):
                    Time=TIME()
                    Time.Reset(name='good')
                    while True:
                        if Time.Out(command_timeout):
                            return False,'Can not access to destination({}) over {} sec'.format(chk_dest,command_timeout)
                        ping_rc=ping(chk_dest,count=1,support_hostname=True,log_format='i')
                        if not isinstance(ping_rc,bool) and ping_rc==0:
                            return 0,'Canceled'
                        if ping_rc:
                            if Time.Out(ping_good,name='good'):
                                printf('\n',direct=True,log=log)
                                break
                            printf('.',direct=True,log=log)
                        else:
                            Time.Reset(name='good')
                            printf('x',direct=True,log=log)
                        time.sleep(2)
                else:
                    return False,'Can not access to destination({})'.format(chk_dest)
        if bmc:
            if IpV4(chk_dest,bmc=True,support_hostname=True) is False:
                return False,'The IP({}) is not BMC IP'.format(chk_dest)
        ss = self.requests.Session()
        err_msg=''
        for j in range(0,max_try):
            try:
                if IsSame(mode,'post'):
                    r =ss.post(host_url,**req_data)
                elif IsSame(mode,'patch'):
                    r =ss.patch(host_url,**req_data)
                else:
                    r =ss.get(host_url,**req_data)
                return True,r
            except:
                pass
            #except requests.exceptions.RequestException as e:
            err_msg='Server({}) has no response'.format(chk_dest)
            if dbg:
                printf('Server({}) has no response (wait {}/{} (10s))'.format(chk_dest,j,max_try),log=log,mode='s')
            else:
                printf('.',direct=True,log=log)
                printf('Server({}) has no response (wait {}/{} (10s))'.format(chk_dest,j,max_try),log=log,mode='d')
            time.sleep(10)
        return False,'TimeOut: {}'.format(err_msg) if err_msg else 'TimeOut'

    def str2url(self,string):
        if IsNone(string): return ''
        if isinstance(string,str):
            return string.replace('+','%2B').replace('?','%3F').replace('/','%2F').replace(':','%3A').replace('=','%3D').replace(' ','+')
        return string

    def form2dict(self,src=None):
        if IsNone(src): src=self.requests.form
        return Dict(src)

    def highlight(self,strings,find,color='#ffff42'):
        if isinstance(strings,str):
            ff=re.compile(find,re.I)
            all_ff=ff.findall(strings)
            if len(all_ff) >0:
                for mm in all_ff:
                    strings=strings.replace(mm,'''<font style="background-color:{1}">{0}</font>'''.format(mm,color))
        return strings


class TIME:
    def __init__(self,src=None,timezone=None):
        self.stopwatch={}
        self.timezone=timezone
        self.stopwatch['init']=self.Now(timezone=self.timezone)
        self.stopwatch['lifetime']=self.stopwatch['init']
        self.src=src

    def Spend(self,life_time=False,unit=None,integer=True,human_unit=True,name=''):
        rt=None
        if name and isinstance(name,str):
            name=name.split(',')
        if isinstance(name,list) and 1 <= len(name) <= 2:
            if len(name) == 1 and name[0] in self.stopwatch:
                rt=self.Now() - self.stopwatch[name[0]]
            elif len(name) == 2 and name[0] in self.stopwatch and name[1] in self.stopwatch:
                if self.stopwatch[name[0]] < self.stopwatch[name[1]]:
                    rt=self.stopwatch[name[1]]-self.stopwatch[name[0]]
                else:
                    rt=self.stopwatch[name[0]]-self.stopwatch[name[1]]
        if rt is None:
            if life_time:
                rt=self.Now() - self.stopwatch['lifetime']
            else:
                rt=self.Now() - self.stopwatch['init']
        # Convert integer value to human readable time
        # unit: None , integer: output : seconds (int)
        # Unit: None , not integer: output : Human readable passed time string (automatically calculate)
        # Unit: unit , integer: output : the unit's number (int)
        # Unit: unit , not integer: output : Human readable passed time string (max is defined unit)
        rt=int(rt.total_seconds())
        if human_unit:
            return Human_Unit(rt,unit='S',want_unit=unit,int_out=integer)
        return rt

    def Reset(self,name=None,timezone=None):
        if name:
            self.stopwatch[name]=self.Now(timezone=timezone if timezone else self.timezone)
        else:
            self.stopwatch['init']=self.Now(timezone=timezone if timezone else self.timezone)

    def Sleep(self,try_wait=None,default=1):
        if isinstance(try_wait,(int,str)): try_wait=(try_wait,)
        if isinstance(try_wait,(list,tuple)) and len(try_wait):
            if len(try_wait) == 2:
                try:
                    time.sleep(random.randint(int(try_wait[0]),int(try_wait[1])))
                except:
                    pass
            else:
                try:
                    time.sleep(int(try_wait[0]))
                except:
                    pass
        else:
            time.sleep(default)
    def Rand(self,try_wait=None,default=1):
        if isinstance(try_wait,(int,str)): try_wait=(try_wait,)
        if isinstance(try_wait,(list,tuple)) and len(try_wait):
            if len(try_wait) == 2:
                try:
                    return random.randint(int(try_wait[0]),int(try_wait[1]))
                except:
                    pass
            else:
                try:
                    return int(try_wait[0])
                except:
                    pass
        return default

    def Get(self,name=None,mode=None,timezone=None,default=False):
        # Get name's time or initial time's 
        # mode = int then return to int, not than return datetime 
        if IsIn(name,['all']):
            return self.stopwatch
        elif IsIn(name,['now']):
            timedata=self.Now(timezone=timezone)
        else:
            if IsIn(default,['now']):
                default=self.Now(timezone=timezone)
            elif IsIn(default,[False,'False','fail','error']):
                default=False
            else:
                default=self.stopwatch['init']
            timedata=self.stopwatch.get(name,default)
        if isinstance(timedata,self.Datetime()) and IsIn(mode,[int,'int','integer','sec']):
            return int(timedata.timestamp())
        else:
            return timedata

    def Now(self,mode=None,timezone=None,timedata=None):
        # Now time, mode:int than return int, not than return datetime
        if timezone is None: timezone=self.timezone
        if isinstance(timezone,str) and timezone:
            Import('import pytz')
            try:
                timezone=pytz.timezone(timezone)
            except:
                printf('Unknown current timezone ({})'.format(timezone),mode='e')
                return False
            timedata=self.Datetime().now(timezone)
        else:
            timedata=self.Datetime().now()
        if isinstance(timedata,self.Datetime()) and IsIn(mode,[int,'int','integer','sec']):
            #return int(timedata.strftime('%s'))
            return int(timedata.timestamp())
        else:
            return timedata

    def Int(self,name=None,timezone=None):
        # Now time to int, same as Now or Get
        #return self.Now(int,timezone=timezone if timezone else self.timezone)
        return self.Get(name,mode=int,timezone=timezone if timezone else self.timezone,default='now')

    def Out(self,timeout_sec,default=(24*3600),name='init'):
        #Check Timeout
        timeout_sec=Int(timeout_sec,default)
        if timeout_sec == 0:
            return False
        if self.Now() - self.Get(name,default='init') >  datetime.timedelta(seconds=timeout_sec):
            return True
        return False

    def Format(self,tformat='%s',read_format='%S',time='_#_'):
        #convert time to format
        if IsNone(time,chk_val=['_#_'],chk_only=True): time=self.src
        if IsNone(time,chk_val=[None,'',0,'0']):
            return self.Now().strftime(tformat)
        elif read_format == '%S' or read_format == '%s':
            if isinstance(time,int) or (isinstance(time,str) and time.isdigit()):
                return self.Datetime().fromtimestamp(int(time)).strftime(tformat)
        elif isinstance(time,str):
            return self.Datetime().strptime(time,read_format).strftime(tformat)
        elif isinstance(time,self.Datetime()):
            return time.strftime(tformat)

    def Init(self,mode=None):
        return self.Get(name='init',mode=mode)

    def Time(self):
        return time.time()

    def Datetime(self):
        return datetime.datetime

    def Print(self,timedata=None,time_format='%Y-%m-%d %H:%M:%S'):
        if not timedata: timedata=self.stopwatch['init']
        if isinstance(timedata,self.Datetime()):
            return timedata.strftime('%Y-%m-%d %H:%M:%S')
        return ''

    def ReadStr(self,timedata,time_format='%Y-%m-%d %H:%M:%S'):
        if isinstance(timedata,str):
            return self.Datetime().strptime(timedata,time_format)
        return ''

    def TimeZone(self,setzone=None,want=None,name=None,timedata=None):
        '''set timezone at timedata or convert to want timezone'''
        if isinstance(timedata,str):
            timedata=self.ReadStr(timedata,time_format=time_format)
        elif timedata is None:
            timedata=self.Get(name=name if name else 'now')
        if isinstance(timedata,self.Datetime()):
            Import('import pytz')
            if isinstance(setzone,str) and setzone:
                if setzone in ['local','localtime','localzone','localtimezone']:
                    setzone=None # set to local timezone
                elif setzone in ['utc','UTC']:
                    setzone=pytz.utc  # set to UTC timezone
                else:
                    try:
                        setzone=pytz.timezone(setzone) # set to setzone
                    except:
                        printf('Unknown current timezone ({})'.format(setzone),mode='e')
                        return False
            if setzone != timedata.tzinfo: # if different timezone between source time and setzone
                timedata=timedata.replace(tzinfo=setzone) # set to setzone
            if isinstance(want,str) and want:
                if want in ['local','localtime','localzone','localtimezone']:
                    want=None # convert to local timezone
                elif want in ['utc','UTC']:
                    want=pytz.utc # convert  to utc timezone
                else:
                    try:
                        want=pytz.timezone(want) # convert to want timezone
                    except:
                        printf('Unknown current timezone ({})'.format(want),mode='e')
                        return False
                if setzone != want: # if different timezone between source time and want zone
                    localtime=timedata.astimezone(tz=want)
                    return localtime
            return timedata
        return False

    def TimeZoneName(self,name=None,timedata=None):
        if isinstance(timedata,str):
            timedata=self.ReadStr(timedata,time_format=time_format)
        elif timedata is None:
            timedata=self.Get(name=name if name else 'now')
        if isinstance(timedata,self.Datetime()):
            tzname=timedata.tzname()
            return tzname if tzname else timedata.astimezone().tzname()

    def Utc2Local(self,time_format='%Y-%m-%d %H:%M:%S',mode='str',name=None,timedata=None):
        if isinstance(timedata,str):
            timedata=self.ReadStr(timedata,time_format=time_format)
        elif timedata is None:
            timedata=self.Get(name=name if name else 'now')
        if isinstance(timedata,self.Datetime()):
            timedata=self.TimeZone(setzone='UTC',want='local',timedata=timedata)
            return self.Print(timedata=timedata) if IsIn(mode,[str,'str','string']) else int(timedata.timestamp()) if IsIn(mode[int,'int','integer']) else timedata
        return False

def rshell(cmd,dbg=False,timeout=0,ansi=False,interactive=False,executable='/bin/bash',path=None,progress=False,progress_pre_new_line=False,progress_post_new_line=True,log=None,env={},full_path=None,remove_path=None,remove_all_path=None,default_timeout=3600,env_out=False,cd=False,keep_cwd=False,decode=None,interactive_background_stderr_log=True):
    '''
    Interactive shell
    path: append the path to existing system path
    full_path: exchange the full_path to system path
    remove_path: remove front remove_path at full_path
    remove_all_path: remove remove_all_path in full_path
    decode: character decoding (default : ISO-8859-1), it changed to Str() default
    interactive_background_stderr_log:default True,interactive case, print Standard Error log in background
    '''
    # OS environments
    os_env=dict(os.environ)
    if env and isinstance(env,dict):
        for ii in env:
            if ii in os_env:
                os_env[ii]=env[ii]

    def cmd_form(cmd):
        cmd_a=cmd.split()
        cmd_file=cmd_a[0]
        if cmd_file[0] != '/' and cmd_file == os.path.basename(cmd_file) and os.path.isfile(cmd_file):
            return './'+cmd
        return cmd

    def pprog(stop,progress_pre_new_line=False,progress_post_new_line=True,log=None,progress_interval=5):
        for i in range(0,progress_interval*10):
            time.sleep(0.1)
            if stop():
                return
        local_printed=False
#        if progress_pre_new_line:
#            printf('',ignore_empty=False,start_newline=True,log=log,end='',log_level=1)
        i=0
        while True:
            if stop(): break
            if i > progress_interval*10:
                i=0
                printf('>',direct=True,log=log,log_level=1)
                local_printed=True
            i+=1
            time.sleep(0.1)
        if progress_post_new_line and local_printed:
            printf('',ignore_empty=False,caller_parent=1,no_intro=True,log=log,log_level=1)
    start_time=TIME()
    if not Type(cmd,'str',data=True):
        return -1,'wrong command information :{0}'.format(cmd),'',start_time.Int('init'),start_time.Now(int),cmd,path

    #ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    Popen=subprocess.Popen
    PIPE=subprocess.PIPE
    STDOUT=subprocess.PIPE
    out,err='',''
    exe_name=os.path.basename(executable) if executable else os.path.basename(os_env.get('SHELL','bash'))
    if dbg:
        if exec_name in ['bash','sh']:
            cmd='set -x\n' + cmd
    if isinstance(remove_path,str) and len(remove_path) > 0 :
        if not full_path: full_path=os.environ['PATH']
        full_path_a=full_path.split(':')
        for ii in remove_path.split(':'):
            if ii in full_path_a:
                full_path_a.remove(ii)
        full_path=':'.join(full_path_a)
    elif isinstance(remove_all_path,str) and len(remove_all_path) > 0 :
        if not full_path: full_path=os.environ['PATH']
        full_path_a=full_path.split(':')
        for ii in remove_all_path.split(':'):
            full_path_a=[i for i in full_path_a if i != ii]
        full_path=':'.join(full_path_)
    if executable:
        if not os.path.isfile(executable):
            executable=find_executable(exe_name)
    #################################
    # Run Command
    #################################
    if full_path:
        if exe_name in ['csh','tcsh']:
            p = Popen('''setenv PATH "%s"; %s'''%(full_path,cmd) , shell=True, stdout=PIPE, stderr=STDOUT,executable=executable, env=os_env)
        else:
            p = Popen('''export PATH=%s; %s'''%(full_path,cmd) , shell=True, stdout=PIPE, stderr=STDOUT,executable=executable, env=os_env)
    elif isinstance(path,str) and len(path) > 0:
        if cd:
            if os.path.isdir(path):
                #p = Popen(cmd_form(cmd) , shell=True, stdout=PIPE, stderr=STDOUT,executable=executable, env=os_env, cwd=path)
                pwd=os.getcwd()
                os.chdir(path) # for cmd_form()
                p = Popen(cmd_form(cmd) , shell=True, stdout=PIPE, stderr=STDOUT,executable=executable, env=os_env)
                if keep_cwd:
                    os.chdir(pwd)
            else:
                return 1, '{} not found'.format(path), '{} not found'.format(path),start_time.Int('init'),start_time.Now(int),cmd,path
        else:
            if exe_name in ['csh','tcsh']:
                p = Popen('''setenv PATH "%s:${PATH}"; %s'''%(path,cmd) , shell=True, stdout=PIPE, stderr=STDOUT,executable=executable, env=os_env)
            else:
                p = Popen('''export PATH=%s:${PATH}; %s'''%(path,cmd) , shell=True, stdout=PIPE, stderr=STDOUT,executable=executable, env=os_env)
    else:
        p = Popen(cmd_form(cmd) , shell=True, stdout=PIPE, stderr=STDOUT,executable=executable, env=os_env)

    if interactive:
       #################################
       #Need error log out from thread to output
       #################################
       def write_err(stop,p,err,interactive_background_stderr_log=True,decode=None):
          _t_=[]
          while True:
              ee=p.stderr.read(1)
              if stop(): break
              if not ee:
                  if interactive_background_stderr_log:
                      sys.stderr.write(''.join(_t_)) # write bytes data to stdout
                      sys.stderr.flush()
                  _t_=[]
              if ee:
                  ees=Str(ee,encode=decode)
                  _t_.append(ees)
                  err.append(ees)
          p.stderr.close()

       ########### STD Error
       err=[]
       stop_err_threads=False
       err_t = Thread(target=write_err, args=(lambda:stop_err_threads,p,err,interactive_background_stderr_log,decode,))
       err_t.start()
       ########### STD Out
       while True:
          d=p.stdout.read(1)
          if not d: break
          if isinstance(d,bytes):
              sys.stdout.buffer.write(d) # write bytes data to stdout
              #out+=d.decode('utf-8').replace('\r','')
              out+=Str(d).replace('\r','')
          else:
              sys.stdout.write(d) # write str data to stdout
              out+=d.replace('\r','')
          sys.stdout.flush()
       p.wait()
       stop_err_threads=True
       p.stdout.close()
       err=''.join(err) if err else ''
    else:
       if progress:
           stop_threads=False
           ppth=Thread(target=pprog,args=(lambda:stop_threads,progress_pre_new_line,progress_post_new_line,log,))
           ppth.start()

       timeout=Int(timeout,default_timeout)
       if timeout > 0:
          if PyVer(3):
             try:
                out, err = p.communicate(timeout=timeout)
             except subprocess.TimeoutExpired:
                p.kill()
                p.returncode=999
                err='Error: Kill process after Timeout {0}'.format(timeout)
          else:
              otimeout='{}'.format(timeout)
              while p.poll() is None and timeout > 0:
                  time.sleep(0.1)
                  timeout = timeout - 0.1
              if p.poll() is None and timeout < 0:
                  p.kill()
                  p.returncode=999
                  err='Error: Kill process after Timeout {0}'.format(otimeout)
              if len(out) == 0 and len(err) == 0:
                  out, err = p.communicate()
       else:
          out, err = p.communicate()
       if progress:
          stop_threads=True
          ppth.join()
    #if PyVer(3):
    #    if Type(out,'bytes'): out=out.decode("ISO-8859-1").rstrip()
    #    if Type(err,'bytes'): err=err.decode("ISO-8859-1").rstrip()
    out=Str(out,encode=decode).rstrip()
    err=Str(err,encode=decode).rstrip()
    if ansi:
        out=CleanAnsi(out)
        err=CleanAnsi(err)
    if env_out:
        return p.returncode, out, err,start_time.Int('init'),start_time.Now(int),cmd,path,os_env
    return p.returncode, out, err,start_time.Int('init'),start_time.Now(int),cmd,path

def IsCancel(func,**opts):
    return IsTrue(func,requirements=['cancel','canceling','REVD','stop','break'],**opts)

def IsBreak(func,**opts):
    return IsTrue(func,requirements=['cancel','canceling','REVD','stop','break'],**opts)

def FixApostrophe(string):
    if isinstance(string,str):
        if "'" in string:
            return '''"{}"'''.format(string)
        return """'{}'""".format(string)
    return string

def sprintf(string,*inps,**opts):
    '''
    """ipmitool -H %(ipmi_ip)s -U %(ipmi_user)s -P '%(ipmi_pass)s' """%(**opts)
    """{app} -H {ipmi_ip} -U {ipmi_user} -P '{ipmi_pass}' """.format(**opts)
    """{} -H {} -U {} -P '{}' """.format(*inps)
    """{0} -H {1} -U {2} -P '{3}' """.format(*inps)
    _err_ : True: missing parameter then return False, False(default): convert just possible things, others just keep return original form
    apostrophe : True: automatically change and add when input value having apostrophe
                 None : automatically change apostrophe when input value having same apostrophe, but not automatically adding apostrophe when format string having no apostrophe(default)
                 False: do not change any parameter
    '''
    def _replace_format_to_value_(i,tmp,string,val,apostrophe=True):
        missing=[]
        string_a=string.split()
        oidx=0
        tuple_val=isinstance(val,(tuple,list))
        for ii in tmp:
            if tuple_val: ii=int(ii)
            idx=None
            #input location format
            if i < 2:
                # list,tuple,parameter
                #print('{}'.format(1))
                #print('{0}'.format(1))
                #print('{a}'.format(**{'a':1}))
                #print('{a}'.format(a=1))
                if '''{%s}'''%(ii) in string_a:
                    idx=string_a.index('''{%s}'''%(ii))
                elif """'{%s}'"""%(ii) in string_a:
                    idx=string_a.index("""'{%s}'"""%(ii))
                elif '''"{%s}"'''%(ii) in string_a:
                    idx=string_a.index('''"{%s}"'''%(ii))
            elif i == 2:
                # dictionary input 
                # print('%(a)s'%({'a':'a'}))
                if '''%({})s'''.format(ii) in string_a:
                    idx=string_a.index('''%({})s'''.format(ii))
                elif """'%({})s'""".format(ii) in string_a:
                    idx=string_a.index("""'%({})s'""".format(ii))
                elif '''"%({})s"'''.format(ii) in string_a:
                    idx=string_a.index('''"%({})s"'''.format(ii))
            #Found format location
            if isinstance(idx,int):
                # if input data is string
                if (tuple_val and len(val) > ii) or (not tuple_val and ii in val):
                    if isinstance(val[ii],str):
                        if (string_a[idx][0] == "'" and string_a[idx][-1] == "'") \
                           or (string_a[idx][0] == '"' and string_a[idx][-1] == '"'):
                            if apostrophe \
                               and ((val[ii][0] == "'" and val[ii][-1] == "'")\
                               or (val[ii][0] == '"' and val[ii][-1] == '"')):
                                string_a[idx]=val[ii]
                            elif apostrophe is not False:
                                if string_a[idx][0] == "'" and "'" in val[ii]:
                                    string_a[idx]='''"'''+val[ii]+'''"'''
                                elif string_a[idx][0] == '"' and '"' in val[ii]:
                                    string_a[idx]="""'"""+val[ii]+"""'"""
                                else:
                                    string_a[idx]=string_a[idx].format(**val)
                        else:
                            if apostrophe:
                                if "'" in val[ii]:
                                    string_a[idx]='''"'''+val[ii]+'''"'''
                                elif '"' in val[ii]: 
                                    string_a[idx]="""'"""+val[ii]+"""'"""
                            else:
                                string_a[idx]=val[ii]
                    else:
                        if tuple_val:
                            string_a[idx]=string_a[idx].format(*val)
                        else:
                            string_a[idx]=string_a[idx].format(**val)
                else:
                    missing.append(ii)
                # if not string input data then skip here
        return Join(string_a,symbol=' '),missing

    if not isinstance(string,str): return False,string
    ffall=[re.compile('\{(\d*)\}').findall(string),re.compile('\{(\w*)\}').findall(string),re.compile('\%\((\w*)\)s').findall(string),re.compile('\{\}').findall(string),re.compile('\%[-0-9.]*[s|c|d|f]').findall(string)]
    i=0
    apostrophe=opts.pop('apostrophe') if 'apostrophe' in opts else None
    error=opts.pop('_err_') if '_err_' in opts else False
    for tmp in ffall:
        if i in [0,1]: tmp=[ j  for j in tmp if len(j) ]
        if tmp:
            if i == 0:
                mx=0
                for z in tmp:
                    if int(z) > mx: mx=int(z)
                if len(inps) > mx:
                    string,m=_replace_format_to_value_(i,tmp,string,inps,apostrophe)
                    if error and m : return False,'missing parameters {}'.format(m)
                elif len(opts) > mx:
                    string,m=_replace_format_to_value_(i,tmp,string,list(opts.values()),apostrophe)
                    if error and m : return False,'missing parameters {}'.format(m)
                else:
                    return False,"""Need more input (tuple/list) parameters(require {})""".format(mx)
            elif 0< i < 2:
                string,m=_replace_format_to_value_(i,tmp,string,opts,apostrophe)
                if error and m : return False,'missing parameters {}'.format(m)
            elif i == 2:
                for tt in inps:
                    if isinstance(tt,dict):
                        opts.update(tt)
                string,m=_replace_format_to_value_(i,tmp,string,opts,apostrophe)
                if error and m : return False,'missing parameters {}'.format(m)
            elif i == 3:
                if inps:
                    if len(tmp) == len(inps):
                        string=string.format(*inps)
                    elif error:
                        return False,"""Mismatched input (tuple/list) number (require:{}, input:{})""".format(len(tmp),len(inps))
                elif opts:
                    if len(tmp) == len(opts):
                        try:
                            string=string.format(*opts.values())
                        except:
                            return False,"""STRING FORMAT ISSUE:\n{}""".format(string)
                    elif error:
                        return False,"""Mismatched input (tuple/list) number (require:{}, input:{})""".format(len(tmp),len(opts))
            elif i >= 4:
                if inps:
                    if len(tmp) == len(inps):
                        string=string%(inps)
                    elif error:
                        return False,"""Mismatched input (tuple/list) number (require:{}, input:{})""".format(len(tmp),len(inps))
                elif opts:
                    if len(tmp) == len(opts):
                        string=string%(opts.values())
                    elif error:
                        return False,"""Mismatched input (tuple/list) number (require:{}, input:{})""".format(len(tmp),len(opts))
        i+=1
    if inps:
        try:
            return True,string.format(*inps)
        except:
            try:
                return True,string%(inps)
            except:
                pass
    if opts:
        try:
            return True,string.format(**opts)
        except:
            try:
                return True,string%(opts)
            except:
                pass
    return True,string

def Sort(src,reverse=False,func=None,order=None,field=None,base='key',sym=None):
    '''
    Sorting data
    support list,tuple,dict format
    reverse : reverse sort
    func    : sorting key function (default None)
    order   : sorting order method
        None: default with sort() function
        int : sort with integer
        str : sort with ascii code
        len : sort with data length
    field   
        None : default
        <int>: sort with list's index number
    base
        key  : default, sort with key of dict 
        value: Sort with value of dict
    sym      : None (default)
        <symbol> : if src is string then split with the sym
    '''
    if isinstance(src,str) and not IsNone(sym): src=src.split(sym)
    if isinstance(src,dict) and base in ['data','value']:
        field=1
    def _clen_(e):
        try:
            if isinstance(field,int):
                if isinstance(e,(list,tuple)) and len(e) > field:
                    return len('{}'.format(Str(e[field])))
                else:
                    return 9999999
            return len('{}'.format(Str(e)))
        except:
            return e
    def _cint_(e):
        try:
            if isinstance(field,int):
                if isinstance(e,(list,tuple)) and len(e) > field:
                    return int(e[field])
                else:
                    return 9999999
            return int(e)
        except:
            return e
    def _cstr_(e):
        if isinstance(field,int):
            if isinstance(e,(list,tuple)) and len(e) > field:
                return '''{}'''.format(e[field])
            else:
                return 'zzzzzzzzz'
        return '''{}'''.format(e)
    if isinstance(src,(list,tuple)):
        src=list(src)
        if order in [int,'int','digit','number']:
            src.sort(reverse=reverse,key=_cint_)
        elif order in ['len','length']:
            src.sort(reverse=reverse,key=_clen_)
        elif order in [str,'str']:
            src.sort(reverse=reverse,key=_cstr_)
        else:
            if isinstance(field,int):
                src.sort(reverse=reverse,key=_cint_)
            else:
                src.sort(reverse=reverse,key=func)
        return src
    elif isinstance(src,dict):
        lst=list(src.items())
        if base == 'key':
            field=0
            if order in [int,'int','digit','number']:
                lst.sort(reverse=reverse,key=_cint_)
            elif order in ['len','length']:
                lst.sort(reverse=reverse,key=_clen_)
            elif order in [str,'str']:
                lst.sort(reverse=reverse,key=_cstr_)
            else:
                lst.sort(reverse=reverse,func=func)
        else: # value / data case
            field=1
            if order in [int,'int','digit','number']:
                lst.sort(reverse=reverse,key=_cint_)
            elif order in ['len','length']:
                return lst.sort(reverse=reverse,key=_clen_)
            elif order in [str,'str']:
                lst.sort(reverse=reverse,key=_cstr_)
            else:
                lst.sort(reverse=reverse,func=func)
        return lst
        #return [i[0] for i in lst]

def VersionSort(data,sym=',',rev=False):
    def DictKeysToList(data,ver='',out=[]):
        if isinstance(data,dict):
            for i in data:
                if not isinstance(data[i],dict) or data[i] in ['',None,{}]:
                    #out.append(ver+'.{}'.format(i)) #Use key (changed format)
                    out.append(data[i]) # Use original Data
                else:
                    DictKeysToList(data[i],ver+'.{}'.format(i) if ver else '{}'.format(i),out=out)
        return ver
    if isinstance(data,str): data=data.split(sym)
    if not isinstance(data,(list,tuple)): return False
    data=list(data)
    if len(data) < 2: return data
    sort_data={}
    out=[]
    #convert list to dict format
    for i in data:
        if not i: continue
        tt=sort_data
        j_a=Split(i,'.|-|:|_')
        j_m=len(j_a)-1
        for j in range(0,j_m+1):
            j_a[j]=Int(j_a[j])
            if j == j_m:
                tt[j_a[j]]=i
            else:
                if j_a[j] not in tt: tt[j_a[j]]={}
                tt=tt[j_a[j]]

    #dict data to auto sorting (like as python2.x style sorting)
    new_data_str=pprint.pformat(sort_data)
    new_data=ast.literal_eval(new_data_str)
    #Get sorted data from dict sorting
    DictKeysToList(new_data,out=out)
    if rev: out.reverse() #reverse data
    return out

def MacV4(src,**opts):
    '''
    Check Mac address format and convert
    Hex to Int
    Hex to Mac string
    Mac string to Int
    symbol : default ':' mac address spliter symbol
    out :
      str : default : XX:XX:XX:XX:XX format
      int : integer format
    default : False
    case : 
      upper : upper case output
      lower : lower case output
    ifname :
      True : src is Network interface Name
    '''
    symbol=opts.get('symbol',opts.get('sym',':'))
    default=opts.get('default',False)
    out=opts.get('out','str')
    case=opts.get('case','lower')
    # From ifname (network device name)
    ifname=opts.get('ifname',False)
    if ifname is True and isinstance(src,str):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            if PyVer(3):
                info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', Bytes(src[:15],encode='utf-8')))
                return ':'.join(['%02x' % char for char in info[18:24]])
            else:
                info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', src[:15]))
                return ':'.join(['%02x' % ord(char) for char in info[18:24]])
        except:
            return default

    def int2str(src,sym):
        return ':'.join(['{}{}'.format(a, b) for a, b in zip(*[iter('{:012x}'.format(src))]*2)])
    def str2int(src):
        return int(src.lower().replace('-','').replace(':',''), 16)
    if Type(src,'bytes'): 
        if len(src) == 6: # format b'\x00\xde4\xef.\xf4'
            src=codecs.encode(src,'hex')  # format b'00de34ef2ef4'
        src=Str(src)
    if isinstance(src,str):
        src=src.strip()
        # make sure the format
        if 12 <= len(src) <= 17:
            for i in [':','-']:
                src=src.replace(i,'')
            src=Join([src[i:i+2] for i in range(0,12,2)],symbol=':')
        # Check the normal mac format
        octets = src.split(':')
        if len(octets) != 6: return default
        for i in octets:
            try:
               if len(i) != 2 or int(i, 16) > 255:
                   return default
            except:
               return default
        if out in [int,'int','number']: return str2int(src)
        if symbol != ':': src=src.replace(':',symbol)
        if case == 'upper': return src.upper()
        return src.lower()
    elif isinstance(src,int) and not isinstance(src,bool):
        if out in [int,'int','number']: return src
        src=int2str(src,symbol)
        if case == 'upper': return src.upper()
        return src.lower()
    return default

def GetIfname(mac):
    net_dir='/sys/class/net'
    if os.path.isdir(net_dir):
        dirpath,dirnames,filenames = list(os.walk(net_dir))[0]
        for dev in dirnames:
            fmac=cat('{}/{}/address'.format(dirpath,dev),no_end_newline=True)
            if type(fmac) is str and fmac.strip().lower() == mac.lower():
                return dev

def Path(*inp,**opts):
    '''
    Get Path of input
    inputs)
       ~       : home path
       ~<user> : user's home path
       None    : current path
       __file__: current python script file path
       __mod__ : This python script file path
       file    : the file's path
       [list]  : convert to path rule 
       obj     : support function, module, class, instance

    remove_dot : 
      True : (default) /a/b/./../c => /a/c
      False: /a/b/./../c => /a/b/./../c
    error : 
      False: default, if path issue then return error
      True : if path issue then ignore
    out :
     str : default: return path string
     list: return list format
       - force_root : default False, True: ['','a','b'] or ['a','b'] => '/a/b'

     '/a/b/c' => ['','a','b','c'] (out=list)
     'a/b/c'  => ['a','b','c']    (out=list)
     ['','a','b','c']  => '/a/b/c'(out=str)
     ['a','b','c']     => 'a/b/c' (out=str)
    '''
    sym=opts.get('sym','/')
    out=opts.get('out','str')
    exist=opts.get('exist',False)
    default=opts.get('default',False)
    remove_dot=opts.get('remove_dot',True)
    err=opts.get('err',opts.get('error',False))
    default=opts.get('default',False)
    base_dir=None
    if not inp:
        try:
            base_dir=os.environ['PWD']
        except:
            base_dir=os.path.dirname(os.path.realpath((inspect.stack()[-1])[1]))
    elif inp:
        if isinstance(inp[0],str):
            if os.path.isfile(inp[0]):
                base_dir=os.path.dirname(os.path.abspath(inp[0]))
            elif inp[0] == '__mod__':
                #This module path
                base_dir=os.path.dirname(os.path.abspath(__file__)) # Not input then get current path
            elif inp[0] == '__file__':
                #Get Caller function's Filename
                my_file=inspect.getfile(FunctionName(parent=1,obj=True)[1]) 
                base_dir=os.path.dirname(os.path.abspath(my_file)) # Get filename path
            else:
                base_dir=inp[0]
        elif Type(inp[0],('function','module','classobj','instance')):
            my_file=inspect.getfile(inp[0]) # Get obj's filename
            base_dir=os.path.dirname(os.path.abspath(my_file))  
    full_path=[]
    if isinstance(base_dir,str):
        full_path=base_dir.split(sym)
    elif isinstance(inp[0],(list,tuple)):
        full_path=list(inp[0])
    if full_path:
        if full_path[0] == '~' or (full_path[0] and full_path[0][0] == '~'):      # ~ or ~<user> style
            #full_path=os.environ['HOME'].split(sym)+full_path[1:]
            full_path=os.path.expanduser(full_path[0]).split(sym)+full_path[1:]
#        elif full_path[0] and full_path[0][0] == '~': # ~<user> style
#            full_path=os.path.expanduser(full_path[0]).split(sym)+full_path[1:]
    if remove_dot:
        nfp=[]
        for i in full_path:
            if i == '..': #remove '..'
                if nfp:
                    #keep root path ('/')
                    if len(nfp)==1:
                        if nfp[0]:
                            del nfp[-1]
                        elif err:
                            return default
                    else:
                        del nfp[-1]
                elif err:
                    return default
            else:
                if i != '.': #remove '.'
                    nfp.append(i)
        full_path=nfp
    for ii in inp[1:]: # add extra input
        if isinstance(ii,str):
            for zz in ii.split(sym):
                if remove_dot:
                    if zz == '.' or not Type(zz,'str',data=True): continue
                    if zz == '..':
                        if full_path:
                            #keep root path ('/')
                            if len(full_path)==1:
                                if full_path[0]:
                                    del full_path[-1]
                                elif err:
                                    return default
                            else:
                                del full_path[-1]
                            continue
                        elif err:
                            return default
                full_path.append(zz)
    if out in [str,'str']:
        if not full_path: return ''
        rt=Join(full_path,symbol=sym)
        if opts.get('force_root',opts.get('root',False)):
            if rt[0] != '/': return '/'+rt
        return rt
    else:
        return full_path

def MergeStr(a,b,_type=None):
    if a is None and b is None:
        if _type == 'bytes':
            return b''
        else:
            return ''
    if _type is None:
        if a is None:
            return b
        elif b is None:
            return a
        elif Type(a) == Type(b):
            return a + b
        elif Type(a) == 'bytes':
            return  a+Bytes(b)
        else:
            return  a+Str(b)
    else:
        if _type in [str,'str']:
            if a is None: return Str(b)
            elif b is None: return Str(a)
            return Str(a)+Str(b)
        else:
            if a is None: return Bytes(b)
            elif b is None: return Bytes(a)
            return Bytes(a)+Bytes(b)

def Cut(src,head_len=None,body_len=None,new_line='\n',out=str,front_space=None,newline_head=False):
    '''
    Cut string with length
    head_len : int : first line length (default None)
               if body_len is None then everything cut same length with head_len
    body_len : int : line length after head_len (default None)
               without head_len(None) then swap between head_len and body_len
    new_line : default linux new line
    front_space: 
        True : fill out space to gap between head_len  and body_len (same as 0)
        False/None : No space
        #    : fill out space of # at front of all strings (head and body)
        '  ' : same as number(#)
    newline_head:
        True : each first line has head condition
        False: first line has head condition of entire source (src)
    out=
        str  : output to string with new_line (default)
        list : output to list instead new_line
    '''
    if not Type(src,('str','bytes')): return False
    source=Split(src,new_line)
    # swap head_len and body_len when head_len is None
    if IsNone(head_len) and isinstance(body_len,int):
        head_len=body_len
        body_len=None

    if not isinstance(head_len,int) or head_len >= len(src):
       if src and out in ['str',str,'string']: return src
       return source # split with new line

    rt=[]
    if isinstance(front_space,bool):
        front_space=0 if front_space is True else None
    elif isinstance(front_space,int):
        front_space=Space(front_space)
    if not isinstance(front_space,str) and front_space is not None:
        front_space=None
    front_space_head=front_space
    front_space_body=front_space
    if front_space is not None:
        if head_len and body_len:
            if head_len > body_len:
                front_space_body=Space(len(front_space)+(head_len-body_len))
            elif head_len < body_len:
                front_space_head=Space(len(front_space)+(body_len-head_len))
    _type=type(src)
    for src_idx in range(0,len(source)):
        str_len=len(source[src_idx])
        if head_len == 0: head_len=str_len
        if IsNone(body_len):
            rt=rt+[MergeStr(front_space,source[src_idx][i:i + head_len],_type=_type) for i in range(0, str_len, head_len)]
        else:
            if src_idx == 0 or newline_head is True:
                rt.append(MergeStr(front_space_head,source[src_idx][0:head_len],_type=_type)) # Take head
                if str_len > head_len:
                    rt=rt+[MergeStr(front_space_body,source[src_idx][head_len:][i:i + body_len],_type=_type) for i in range(0, str_len-head_len, body_len)]
            else:
                rt=rt+[MergeStr(front_space_body,source[src_idx][i:i + body_len],_type=_type) for i in range(0, str_len, body_len)]
    if out in ['str',str,'string']:
        if rt: return Join(rt,symbol=new_line)
        return ''
    return rt

def Space(num=4,fill=None,mode='space',tap=''):
    '''
    make a charactor(space, tap) group
    num: default 4, how many fill out <fill>
    mode:
      space : default: ' '
      tap   : \\t
    fill:
      None : default: following mode information
      <special charactor> : fill out the charactor
    tap:
      ''   : default
      <spcial inital chractor>: pre-fillout with this chractor
    '''
    mode=mode.lower()
    if mode =='tap':
        fill='\t'
    elif mode == 'space' or fill is None:
        fill=' '
    for i in range(0,num):
        tap=tap+fill
    return tap

def WrapString(string,fspace=0,nspace=0,new_line='\n',flength=0,nlength=0,ntap=0,NFLT=False,mode='space',default='',out='str',ignore_empty_endline=True):
    #string : printing data
    #fspace : pre space(space before string, before first line)
    #nspace : space for body area
    #new_line: new_line symbol
    #flength : first line ( head line ) print-string length
    #nlength : body area print-string length
    #mode    : space: white space to space area
    #out     : output to string or list
    #ntap    : not used (removed parameter)
    #NFLT    : same as fspace=0
    #ignore_empty_endline: True: if endline have no data then ignore making space for wrap.  False: making space to wrap for next attaching string
    if IsNone(string): return default
    if not Type(string,'str'):string='''{}'''.format(string)
    rc_str=[]
    string_a=string.split(new_line)
    #First line design
    if NFLT: fspace=0
    rc_str.append(Space(fspace,mode=mode)+Join(Cut(string_a[0],head_len=flength,body_len=nlength,new_line=new_line,out=list),'\n',append_front=Space(nspace,mode=mode)))
    #Body line design
    #for ii in string_a[1:]:
    mx=len(string_a)-1
    for ii in range(1,mx+1):
        if ignore_empty_endline is True and ii == mx and not string_a[ii]: break
        rc_str.append(Space(nspace,mode=mode)+Join(Cut(string_a[ii],head_len=nlength,new_line=new_line,out=list),'\n',append_front=Space(nspace,mode=mode)))
    #return new_line.join(rc_str)
    if out in [list,'list']: return rc_str
    elif out in [tuple,'tuple']: return tuple(rc_str)
    return Join(rc_str,new_line)

def GetKey(src,find=None,default=None,mode='first',root=None):
    '''
    Get key from dict,list,tuple,str
    find : if matched value then return the key/index of the data
    mode :
      first : default: return first find
      all   : return found all
    default : return when not found
    '''
    rt=[]
    if isinstance(src,dict):
        if IsNone(find):
            return list(src.keys())
        else:
            for key,val in src.items():
                if isinstance(val,dict):
                    a=GetKey(val,find,default,mode,key)
                    if a:
                        if isinstance(a,str):
                            if root is None:
                                return '/{}/{}'.format(key,a)
                            else:
                                return '{}/{}'.format(key,a)
                        elif isinstance(a,list):
                            for i in a:
                                if root is None:
                                    rt.append('/{}/{}'.format(key,i))
                                else:
                                    rt.append('{}/{}'.format(key,i))
                elif val == find:
                    if mode == 'first': return key
                    rt.append(key)
            if rt: return rt
    elif isinstance(src,(list,tuple,str)):
        if IsNone(find):
            return len(src)
        else:
            for i in range(0,len(src)):
                if find == src[i]:
                    if mode == 'first': return i
                    rt.append(i)
        if rt: return rt
    return default

def rm(*args,**opts):
    '''
    delete local file with option like as CLI
       [<opt>] <files>/<directory>
       -f    : don't ask delete
       -r    : <directory> or recurring delete
    delete local file with option like as Function
       <files>/<directory>,...
       force=True    : don't ask delete, default False
       recurring=True: <directory> or recurring delete
    delete list/tuple
       <list,tuple>,<del items>,...
       option)
         data
           True : delete data like as <del items>
           False: (default) delete index (<del items> are int)
    delete dict
       <dict>,<del items>,...
       option)
         data
           True : delete data like as <del items>
           False: (default) delete key like as <del items>
         recurring 
           False: searching data in first level
           True : keep searching inside dictionary 
    '''
    if len(args) <= 0: return opts.get('default')
    #List/Tuple
    if Type(args[0],('LIST','list','tuple')):
        rt=list(args[0])
        LIST(rt).Delete(*args[1:],find='data' if opts.get('value',opts.get('data',False)) else 'index')
        return rt
        #del_data=opts.get('value',opts.get('data',False))
        #if del_data:
        #    for i in args[1:]:
        #        if i in rt: rt.remove(i)
        #    if Type(args[0],'tuple'): return tuple(rt)
        #    return rt
        #else:
        #    tmp=[]
        #    for i in range(0,len(rt)):
        #        if i in args[1:]: continue
        #        tmp.append(rt[i])
        #    if Type(args[0],'tuple'): return tuple(tmp)
        #    return tmp
    #Dict
    elif Type(args[0],dict):
        rt=args[0]
        del_data=opts.get('value',opts.get('data',False))
        # Del Data
        if del_data: 
            tmp=[]
            rt_items=list(rt.items())
            for i in range(0,len(rt_items)):
                #Recurring check
                if opts.get('recurring',False) and Type(rt_items[i][1],dict):
                    a=list(rt_items[i])
                    a[1]=rm(rt_items[i][1],*args[1:],data=del_data)
                    tmp.append(tuple(a))
                elif rt_items[i][1] not in args[1:]:
                    tmp.append(rt_items[i])
            return dict(tmp)
        # Del key
        else:
            # Recurring checking
            if opts.get('recurring',False):
                tmp=[]
                rt_items=list(rt.items())
                for i in range(0,len(rt_items)):
                    if rt_items[i][0] not in args[1:]:
                        if Type(rt_items[i][1],dict):
                            a=list(rt_items[i])
                            a[1]=rm(rt_items[i][1],*args[1:],data=del_data)
                            tmp.append(tuple(a))
                        else:
                            tmp.append(rt_items[i])
                return dict(tmp)
            else:
                for i in args[1:]:
                    #Path key
                    if '/' in i and i[0] == '/':
                        i_a=i.split('/')
                        tmp=rt
                        brk=False
                        for z in i_a[1:-1]:
                            if z in tmp:
                                tmp=tmp[z]
                            else:
                                brk=True
                                break
                        if not brk and i_a[-1] in tmp: tmp.pop(i_a[-1])
                        continue
                    elif i in rt:
                        rt.pop(i)
        return rt
    else:
        #File/Directory
        sub_dir=opts.get('recurring',False)
        force=opts.get('force',False)
        if find_executable('rm'):
            sub_opt=''
            if sub_dir: sub_opt='-r'
            if force:
                if sub_opt: sub_opt=sub_opt+'f'
                else: sub_opt='-f'
            rshell('rm -i {}'.format(sub_opt)+Join(args,' '),interactive=True)
        else:
            for arg in args:
                if arg[0] == '-':
                   if 'r' in arg:
                      sub_dir=True
                   if 'f' in arg:
                      force=True
                else:
                    if os.isfile(arg):
                        if not force:
                            yn=cli_input('Delete {} (Y/N)?')
                            if not isinstance(yn,str) or yn.lower() not in ['y','yes']: continue
                        #os.remove(arg)
                        os.unlink(arg)
                    elif os.isdir(arg):
                        if sub_dir:
                            if not force:
                                yn=cli_input('Delete {} (Y/N)?')
                                if not isinstance(yn,str) or yn.lower() not in ['y','yes']: continue
                            shutil.rmtree(arg)
                        else:
                            print('''can't delete directory:{}'''.format(arg))
                    else:
                        print('''can't delete {}'''.format(arg))
    return opts.get('default')

#New CLASS
#class NAME():
#    def __init__(self,...): #Initialize data
#        self.data=....
#    def __new__(cls,*inps): ???
#        ....
#    def __repr__(self): # reply self.data back to the Class's output a=<NAME>(['a']), return the data to a
#        return repr(self.data)
#    def <new func>(self,xxx):
#        data=self # get original data to data variable
#        super().<original func name>(xxxx) # using original function

class LIST(list):
    def __init__(self,*inps,merge=False,uniq=False):
        if len(inps) == 1 and isinstance(inps[0],(list,tuple)):
            super().__init__(i for i in inps[0])
        else:
            if merge:
                for i in inps:
                    if isinstance(i,(type(self),list)):
                        super().extend(i)
                    else:
                        super().append(i)
            else:
                super().__init__(i for i in inps)
        if uniq:
            self.Uniq()

    def Append(self,*inps,**opts):
        uniq=opts.get('uniq',False)
        symbol=opts.get('symbol',':white_space:')
        path=opts.get('path',False)
        default=opts.get('default',False)
        for pp in inps:
            if Type(pp,('bytes','str')):
                if symbol == ':white_space:':
                    pp=pp.strip()
                    symbol=' '
                if path: symbol='/'
                for rp in Split(pp,symbol):
                    if rp == default: continue
                    if uniq and rp in self: continue
                    if path:
                        if rp == '.': continue
                        if rp == '..' and len(self):
                            del self[-1]
                            continue
                    self.append(rp)
            else:
                if uniq and pp in self: continue
                self.append(pp)
        return self

    def Uniq(self,*inps,**opts):
        symbol=opts.get('symbol',opts.get('split',opts.get('split_symbol')))
        path=opts.get('path',False)
        if path: symbol='/'
        default=opts.get('default',False)
        rt=[]
        for pp in self + list(inps):
            if Type(pp,('bytes','str')):
                if symbol or path:
                    for rp in Split(Strip(pp) if symbol == ':white_space:' else pp,' ' if symbol==':white_space:' else symbol):
                        if rp not in rt and rp != default:
                            if path:
                                if rp == '.': continue
                                if rp == '..' and len(rt):
                                    del rt[-1]
                                    continue
                            rt.append(rp)
                    continue
            if pp not in rt: rt.append(pp)
        super().__init__(i for i in rt)
        return self

    def Delete(self,*inps,**opts):
        find=opts.get('find','index')
        all_data=opts.get('all',opts.get('all_data',opts.get('del_all')))
        default=opts.get('default',False)
        if find in ['index','id']: # for keep original index
            tmp=[]
            for i in range(0,len(self)):
                if i in inps: continue
                tmp.append(self[i])
            super().__init__(i for i in tmp)
        else: # Data
            for i in inps:
                if all_data:
                    while i in self:
                        super().remove(i)
                elif i in self:
                    super().remove(i)

    def Get(self,*inps,**opts):
        if not inps: return self
        find=opts.get('find','data')
        default=opts.get('default',None)
        out=opts.get('out',list)
        err=opts.get('err',False)
        if len(self) == 0 and err:
            return default
        rt=[]
        if find in ['index','idx']:
            rt=self.Index(*inps,default=default,out=out)
        else:
            rt=List(*self,idx=inps,mode='err' if err else 'auto',default=default)
        if rt:
            if out in [tuple,'tuple']:
                return tuple(rt)
            elif IsNone(out,chk_val=[None,'','raw']):
                if len(rt) == 1: return rt[0]
            return rt
        return default

    def Index(self,*inps,**opts):
        mixed=opts.get('any',opts.get('mixed',opts.get('OR',True)))
        all_data=opts.get('all',opts.get('ALL',opts.get('everything')))
        out=opts.get('out')
        peel=opts.get('peel',True)
        default=opts.get('default',False)
        rt=[]
        for i in inps:
            tt=[]
            for z in range(0,len(self)):
                if Type(i,('str','bytes')):
                    j=i.replace('*','.+').replace('?','.')
                    mm=re.compile(j)
                    if bool(re.match(mm,self[z])):
                        tt.append(z)
                        if not all_data: break
                elif self[z] == i:
                    tt.append(z)
                    if not all_data: break
            if mixed:
                rt=rt+tt
            else:
                rt.append(tuple(tt))
        return OutFormat(rt,out=out,peel=peel,org=self,default=default)

    def Insert(self,*inps,**opts):
        at=opts.get('at',-1)
        default=opts.get('default',False)
        err=opts.get('err',False)
        if isinstance(at,str):
            if at in ['start','first']: root=list(inps)+self
            elif at in ['end','last']: root=self+list(inps)
        elif len(self) == 0:
            root=list(inps)
        elif isinstance(at,int):
            if len(self) >= abs(at):
                if at == -1 or len(self) == at:
                    root=self+list(inps)
                else:
                    if at < -1: at=at+1
                    root=self[:at]+list(inps)+self[at:]
            elif len(self) < abs(at):
                if at > 0:
                    root=self+list(inps)
                else:
                    root=list(inps)+self
        else:
            if err:
                return default
            root=self+list(inps)
        super().__init__(i for i in root)

    def Update(self,*inps,**opts):
        at=opts.get('at',0)
        err=opts.get('err',False)
        default=opts.get('default',False)
        n=len(self)
        if n == 0:
            if err is True:
                return default
            else:
                super().__init__(i for i in inps)
        elif isinstance(at,int) and n > at:
            for i in range(0,len(inps)):
                if n > at+i:
                    super().insert(at+i,inps[i])
                elif err is True:
                    return default
                else:
                    super().__init__(i for i in self+list(inps)[i:])
                    break
        elif isinstance(at,(tuple,list)):
            if len(inps) == len(at):
                for i in range(0,len(at)):
                    if isinstance(at[i],int) and n > at[i]:
                        super().insert(at[i],inps[i])
                    elif err is True:
                        return default
                    else:
                        super().append(inps[i])

    def Find(self,*inps,**opts):
        find=opts.get('find','index')
        default=opts.get('default',[])
        rt=[]
        for i in range(0,len(self)):
            for j in inps:
                j=j.replace('*','.+').replace('?','.')
                mm=re.compile(j)
                if bool(re.match(mm,self[i])):
                    if find in ['index','idx']:
                        rt.append(i)
                    else:
                        rt.append(self[i])
        if len(rt):
            return rt
        return default

    def Move2first(self,find):
        if Type(find,('LIST','list','tuple')):
            self.Delete(*find,find='data')
            super().__init__(i for i in list(find)+self)
        else:
            self.Delete(*(find,),find='data')
            super().__init__(i for i in [find]+self)
        return self

    def Move2end(self,find):
        if isinstance(find,(list,tuple)):
            self.Delete(*find,find='data')
            super().__init__(i for i in self+list(find))
        else:
            self.Delete(*(find,),find='data')
            super().__init__(i for i in self+[find])
        return self

    def Sort(self,reverse=False,func=None,order=None,field=None,base='key',sym=None):
        try:
            super().__init__(i for i in Sort(self,reverse=reverse,func=func,order=order,field=field,base=base,sym=sym))
            return self
        except:
            print('Not support mixed string and int')

def Iterable(inp,default=[],split=None):
    if isinstance(inp,(list,tuple,dict)):
        return inp
    elif isinstance(inp,str) and isinstance(split,str) and split:
        return inp.split(split)
    return default

def List(*inps,**opts):
    '''
    tuple2list: 
        True : convert tuple data to list data
        False: append tuple into list
    <dict input>
     items : <dict>.items()
     data  : <dict>.value()
     path  : convert <dict> to path like list ([('/a/b',1),('/a/c',2),...])
     (default): <dict>.keys()
    <option>
     ignores=[]   : ignore group(default: made to list, all)
     idx=<int>    : get <idx> data
     del=<int>    : delete <idx>
     first=<data> : move <data> to first
     end=<data>   : move <data> to end
     find=<data>  : get Index list
     uniq=False   : Make to Uniq data
     strip=False  : remove white space
     default      : False
     mode 
        auto      : auto fixing index
        err       : not found then return default(False)
        ignore    : not found then ignore the data
    '''
    def DD(s):
        rt=[]
        for i in s:
            if Type(s[i],dict):
                for z in DD(s[i]):
                    rt.append((i+'/'+z[0],z[1]))
            else:
                rt.append((i,s[i]))
        return rt

    tuple2list=opts.get('tuple2list',True)
    mode=opts.get('mode','auto')
    ignores=opts.get('ignores')
    if isinstance(ignores,str):
        ignores=tuple(ignores.split(','))
    if isinstance(ignores,(list,tuple)):
        ignores=tuple(ignores)
    rt=[]
    if len(inps) == 0 : return rt
    if Type(inps[0],('list','LIST')):
        rt=inps[0]
    elif Type(inps[0],tuple):
        if tuple2list:
            rt=list(inps[0])
        else:
            rt.append(inps[0])
    elif Type(inps[0],dict):
        if opts.get('data'):
            rt=list(inps[0].values())
        elif opts.get('all',opts.get('whole',opts.get('items'))):
            rt=list(inps[0].items())
        elif opts.get('path'):
            tmp=[]
            for k in inps[0]:
                if Type(inps[0][k],dict):
                    for d in DD(inps[0][k]):
                        tmp.append(('/'+k+'/'+d[0],d[1]))
                else:
                    tmp.append(('/'+k,inps[0][k]))
            rt=rt+tmp
        else:
            rt=list(inps[0])
    else:
        if isinstance(ignores,tuple) and (Type(inps[0],ignores) or IsIn(inps[0],ignores)):
            pass
        else:
            rt=[inps[0]]
    for i in inps[1:]:
        if Type(i,list):
            rt=rt+i
        else:
            if Type(i,tuple):
                if tuple2list:
                    rt=rt+list(i)
                    continue
            elif Type(i,dict):
                rt=rt+List(rt,i,**opts)
                continue
            if isinstance(ignores,tuple) and (Type(i,ignores) or IsIn(i,ignores)):
                continue
            rt.append(i)
    if opts.get('strip'):
        rt=[i.strip() if isinstance(i,(str,bytes)) else i for i in rt]
    if opts.get('uniq'):
        return Uniq(rt)
    idx=opts.get('idx')
    if not IsNone(idx):
        ok,idx=IndexForm(idx,idx_only=True,symbol=',')
        if ok is False: return opts.get('default',False)
        if isinstance(idx,tuple) and len(idx) == 2:
            idx=range(idx[0],idx[1]+1)
        if not Type(idx,(list,tuple,'range')): idx=[idx]
        tt=[]
        for i in idx:
            if mode == 'auto':
                i=FixIndex(rt,i,default=False,err=False)
            elif mode in ['err','ignore']:
                i=FixIndex(rt,i,default=False,err=True)
            if i is False:
                if mode == 'err': return opts.get('default',False)
            else:
                tt.append(rt[i])
        return tt
    if not IsNone(opts.get('rm')):
        return rm(rt,*opts.get('rm') if Type(opts.get('rm'),(list,tuple)) else opts.get('rm'))
    first=opts.get('first')
    if not IsNone(first) and first in rt:
        return [first]+[i for i in rt if i != first]
    end=opts.get('end')
    if not IsNone(end) and end in rt:
        return [i for i in rt if i != end]+[end]
    find=opts.get('find')
    if not IsNone(find):
        if not Type(find,(list,tuple)): find=[find]
        tt=[]
        for i in find:
            for z in range(0,len(rt)):
                if Type(i,('str','bytes')):
                    j=i.replace('*','.+').replace('?','.')
                    mm=re.compile(j)
                    if bool(re.match(mm,rt[z])):
                        tt.append(z)
                elif rt[z] == i: tt.append(z)
        return tt
    return rt

def Replace(src,replace_what,replace_to,default=None,newline='\n'):
    '''
    replace string (src, from, to)
    if not string then return default
    default: return defined value when not string
      'org': return src
      ...  : return defined default
    '''
    def _S_(src,p):
        if isinstance(p,list):
            t=[]
            m=len(p)-1
            for i in range(0,m+1):
                if i == 0:
                    t.append(src[:p[i][0]])
                    if i==m:
                        t.append(src[p[i][1]:])
                elif i < m:
                    t.append(src[p[i-1][1]:p[i][0]])
                elif i == m:
                    t.append(src[p[i-1][1]:p[i][0]])
                    t.append(src[p[i][1]:])
            return t

    if not Type(src,('str','bytes')):
        return Default(src,default)
    if Type(src,'bytes'):
        replace_what=Bytes(replace_what)
        replace_to=Bytes(replace_to)
        newline=Bytes(newline)
    else:
        replace_what=Str(replace_what)
        replace_to=Str(replace_to)
        newline=Str(newline)
    tmp=[]
    for ii in src.split(newline):
        tt=_S_(ii,Found(ii,replace_what,location=True))
        tmp.append(Join(tt,replace_to) if tt else ii)
    return Join(tmp,newline)

def SehllToPythonRC(rc):
    rc=Int(rc,default='org')
    if type(rc).__ == 'int':
        if rc == 0: return 1
        elif rc == 1: return 0
        return rc
    return rc

#def krc(rt=None,chk='_',rtd=None,default=False,mode=None,ext='shell'):
def krc(rt=None,ext=None,chk='_',rtd=None,default=False,mode=None):
    global krc_define
    global krc_ext
    if not ext: ext=krc_ext
    nrtd=Copy(krc_define,deep=True) if rtd is None else Copy(rtd,deep=True)
    if ext == 'shell': # python
        if not IsIn(0,nrtd['GOOD']): nrtd['GOOD'].append(0)
        if not IsIn(1,nrtd['ERRO']): nrtd['ERRO']=nrtd['ERRO']+[1,126,128,130,255]
        if not IsIn(127,nrtd['NFND']): nrtd['NFND'].append(127)
    #elif ext == 'python': # python
    else: # python
        if not IsIn(1,nrtd['GOOD']): nrtd['GOOD'].append(1)# Python's True level
        if not IsIn(0,nrtd['FAIL']): nrtd['FAIL'].append(0)# Python's False level
    '''
    Shell exit code:
      1   - Catchall for general errors
      2   - Misuse of shell builtins (according to Bash documentation)
    126   - Command invoked cannot execute
    127   - “command not found”
    128   - Invalid argument to exit
    128+n - Fatal error signal “n”
    130   - Script terminated by Control-C
    255\* - Exit status out of range
    '''
    if mode == 'get':
        return nrtd
    elif mode == 'keys':
        if isinstance(nrtd,dict):
            return nrtd.keys()
    def trans(irt):
        #type_irt=str(irt) if isinstance(irt,kRT) else type(irt)
        type_irt=type(irt)
        for ii in nrtd:
            for jj in nrtd[ii]:
                if type(jj) == type_irt and ((type_irt is str and jj.lower() == irt.lower()) or jj == irt):
                    return ii
        return 'UNKN'
    rtc=Get(rt,'0|rc',err=True,default='org',type=(bool,int,list,tuple,dict))
    a=Peel(rtc,err=False,default='unknown') #If Get() got multi data then use first data
    if isinstance(a,kRT): a=FormData(str(a)) # convert kRT()'s rc to rc data
    #nrtc=trans(Peel(rtc,err=False,default='unknown')) #If Get() got multi data then use first data
    nrtc=trans(a) #If Get() got multi data then use first data
    if chk != '_':
        if not isinstance(chk,list): chk=[chk]
        for cc in chk:
            if trans(cc) == nrtc:
                return True
            if nrtc == 'UNKN' and default == 'org':
                return rtc
        return Default(rt,default)
    return nrtc

def OutFormat(data,out=None,strip=False,peel=None,org=None,default=None):
    '''
    Output Format maker
    <option>
      out
        None: Not convert
        str,int,list,dict : convert data to want format
        raw : Peeled data when single data(['a'],('a'),{'a':'abc'}) others then return orignal
      peel
        None : automatically working according to out
        True : Peeling data
        False: Not Peeling
      strip 
        False: not remove white space
        True : remove white space
    '''
    out_data=None
    if IsIn(data,[[],{}]) and IsIn(default,['org','original']):
        #If no data and default is original then convert original to out
        data=org
    if IsIn(out,[tuple,'tuple',list,'list']):
        if not isinstance(data,(tuple,list)):
            out_data=[data]
        else:
            out_data=list(data)
        if out in [tuple,'tuple']:
            if out_data:
                return tuple(out_data)
            elif isinstance(default,tuple):
                return default
            else:
                return (Default(org,default))
        if out_data:
            return out_data
        elif isinstance(default,list):
            return default
        else:
            return [Default(org,default)]
    elif IsIn(out,[dict,'dict']):
        if data:
            return Dict(data)
        elif isinstance(default,dict):
            return default
        else:
            return Default(org,default)
    elif IsIn(out,['str',str,'string','text']):
        out_data=WhiteStrip(Peel(Str(data),peel),strip)
    elif IsIn(out,['int',int,'integer','number','numeric']):
        out_data=Int(WhiteStrip(Peel(data,peel),strip))
    if out_data is False: #if str or int got False then 
        return Default(org,default)
    if IsNone(peel): peel=True
    out_data=WhiteStrip(Peel(data,peel),strip)
    if out_data: return out_data
    return Default(org,default)

def FeedFunc(obj,*inps,**opts):
    '''
    Automatically Feed matched variables to function
    FeedFunc(<func>,<function's arguments>,<function's variables>)
    if something wrong then return False
    if correct then return output of ran the Function with inputs
    '''
    #Block Infinity Loop
    loop_history=FunctionName(parent=10,obj=obj,history=True,line_number=True,filename=True)
    if len(loop_history) > 1 and loop_history[0] in loop_history[1:]:
        loop_history_chain='{}({} in {})'.format(loop_history[0][0],loop_history[0][2],loop_history[0][3])
        for i in loop_history[1:]:
            if i == loop_history[0]:
                loop_history_chain=loop_history_chain+'->{}({} in {})'.format(i[0],i[2],i[3])
                break
            else:
                loop_history_chain=loop_history_chain+'->{}'.format(i[0])
        StdErr('ERROR: Infinity Loop Call in 10 depth: {}\n'.format(loop_history_chain))
        return False,'Infinity Loop Call in 10 depth: {}'.format(loop_history_chain)
    if Type(obj,'str') and not inspect.isclass(obj): # for str class
        mymod=MyModule(default=False,parent=1)
        if mymod is False:
            mymod=MyModule(default=False,parent=0)
        if mymod is False:
            mymod=MyModule(default=False,parent=-1)
        if Type(mymod,'module'):
            try:
                obj=getattr(mymod,obj,None)
            except:
#                StdErr('Function name "{}" not found in the module\n'.format(obj))
                return False,'Function name "{}" not found in the module\n'.format(obj)
    e='Wrong Object type'
    if Type(obj,('function','method','builtin_function_or_method','type','int','str','list','dict')):
        fcargs=FunctionArgs(obj,mode='detail',default={})
        ninps=[]
        nopts={}
        #Special case int,str,list,dict
        if Type(obj, ('int','str','list','dict')):
            if inps: ninps.append(inps[0])
            if 'base' in opts: #int()
                nopts['base']=opts['base']
            if 'encoding' in opts: # str()
                nopts['encoding']=opts['encoding']
            elif Type(obj,'str') and ninps and Type(ninps[0],'bytes') and 'encoding' not in opts: # str()
                nopts['encoding']='ascii'
        idx=0
        if 'args' in fcargs:
            for i in fcargs['args']:
                if len(inps) > idx:
                    ninps.append(inps[idx])
                    idx+=1
                else:
                    if i in opts:
                        ninps.append(opts.pop(i))
                    else:
#                        StdErr('input parameter "{}" not found\n'.format(i))
                        return False,'input parameter "{}" not found\n'.format(i)
        if 'varargs' in fcargs:
            ninps=ninps+list(inps[idx:])
        if 'defaults' in fcargs:
            for i in fcargs['defaults']:
                if i in opts:
                    nopts[i]=opts.pop(i) #make with input value
                else:
                    nopts[i]=fcargs['defaults'][i] # make with default value
        if 'keywords' in fcargs:
            nopts.update(opts)
        #Run function with found arguments
        if ninps and nopts:
            if Type(obj,('int','str')):
                return True,obj(ninps[0],**nopts)
            else:
                return True,obj(*ninps,**nopts)
        elif ninps:
            if Type(obj,('int','str','list','dict')):
                return True,obj(ninps[0])
            else:
                return True,obj(*ninps)
        elif nopts:
            return True,obj(**nopts)
        else:
            try:
                return True,obj()
            except:
                e=ExceptMessage()
                #StdErr(e)
    return False,e

def printf(*msg,**opts):
    '''
    Similar as print()
    date=True/False              : (True) print date initial line
    date_format                  : if defined date_format then print date with date_format
    direct=False/True            : (True) print without newline and any intro information
    logfile=                     : saveing log to logfile
    caller_detail=False/True     : print caller information
       True:
                                 - line number, filename, args, optional caller_full_filename
       False: (detail selection)
          caller_args=False/True : (False) print args of function
          caller_filename=False/True : (False) print filename
          caller_full_filename=False/True : (False) print full path filename
          caller_line_number=False/True : (False) print line number 
    caller_tree=False/True       : print tree of caller history
       True:
          - tree and history
       False:
          caller_history=False/True : return history without tree
    syslogd=                     : logging to syslogd daemon
    end_newline=True/False       : mark new line at end of the line
    start_newline=False/True     : mark new line at start of the line
    intro=<str>                  : log intro string before log data
    no_intro                     : True: temporary remove intro , False(default): Intro when exist intro, None: space instead intro string
    log_level=<int>              : make log-level
        printf_log_base=6
        printf('aaaaa',log_level=3) -> this will print
        printf('bbbbb',log_level=8) -> this not print. but if change printf_log_base to 9 then it will print
    log=<func>                   : put logging data to log function
    dsp or mode =                : Display format/mode
        a      : auto
        s      : screen
        f or d : save to file only
        n      : ignore save to file only for duplicated message (special case, want don't print at debug file)
        e      : log to standard error 
        c      : console
        i      : ignore print (all of printing (file,debug,screen,....))
        r      : return the log message
                 rt=printf('xxxx',dsp='r')
                 print(rt)
    '''
    global printf_caller_detail
    global printf_caller_tree
    global printf_log_base
    global printf_caller_name
    global printf_newline_info
    global printf_ignore_empty
    global printf_dbg_empty
    global printf_scr_dbg
    direct=opts.get('direct',False)
    dsp=opts.get('dsp',opts.get('mode','a'))
    if not dsp: dsp='a'
    if dsp == 'i': return # ignore print
    log=opts.get('log',None)
    log_level=opts.get('log_level',None)
    parent_n=opts.get('caller_parent',1)
    caller_detail=opts.get('caller',opts.get('caller_detail',printf_caller_detail))
    caller_tree=opts.get('caller_tree',printf_caller_tree)
    caller_history=opts.get('caller_history',False)
    caller_ignore=opts.get('caller_ignore',opts.get('caller_upper',[]))
    caller_full_filename=opts.get('caller_full_filename',False)
    caller_filename=opts.get('caller_filename',False)
    caller_line_number=opts.get('caller_line_number',False)
    caller_args=opts.get('caller_args',False)
    caller_name=opts.get('caller_name',printf_caller_name)
    syslogd=opts.get('syslogd',None)
    scr_dbg=opts.get('scr_dbg',printf_scr_dbg)
    scr_dbg_condition=opts.get('scr_dbg_condition')
    no_intro=opts.get('no_intro',False)
    ignore_empty=opts.get('ignore_empty',printf_ignore_empty)
    dbg_empty=opts.get('dbg_empty',printf_dbg_empty)
    msg_split=opts.get('msg_split',' ')
    msg=list(msg)
    if no_intro is True or direct:
        date_format=None
    else:
        date_format=opts.get('date_format','%m/%d/%Y %H:%M:%S' if opts.get('date') else None)
    # end newline design
    new_line='' if direct else opts.get('new_line',opts.get('newline',opts.get('end',opts.get('end_newline',opts.get('post_newline','\n')))))
    if new_line not in ['','\n']:new_line='\n' if new_line and not direct else ''
    # start newline design
    no_start_newline=opts.get('no_start_newline')
    start_newline='' if no_start_newline is True else opts.get('start_newline',opts.get('start',opts.get('pre_newline')))
    if no_start_newline:
        start_newline=''
    else:
        if start_newline is True:
            start_newline='\n'
        elif IsIn(start_newline,['A','Auto']):
            start_newline='auto'
        else:
            start_newline=''

    if no_intro is True: # if no_intro then ignore start_newline mark
        start_newline=''

    intro=opts.get('intro',None)
    logfile=opts.get('logfile',opts.get('log_file',[]))
    ignore_myself=opts.get('ignore_myself',True)
    def msg_maker(*msg,msg_split=' ',intro_len=0,intro_msg=''):
        # Make input data to a string msg 
        msg_str=''
        TT=0  # For '\n' or '\n\n' ...
        for ii in msg:
            if not isinstance(ii,str):
                if intro_len:
                    a=ColorStr(WrapString(Str(pprint.pformat(ii),default='org'),fspace=0 if not msg_str or msg_split != '\n' or TT else intro_len, nspace=intro_len,mode='space'),**opts)
                else:
                    a=ColorStr(Str(pprint.pformat(ii),default='org'),**opts)
            else:
                if '\n' in ii and not ii.replace('\n',''): #convert \n or \n\n .... to wrapping format
                    TT+=1
                    ii=ii+'T'
                if intro_len:
                    a=ColorStr(WrapString(Str(ii,default='org'),fspace=0 if not msg_str or msg_split != '\n' or TT else intro_len, nspace=intro_len,mode='space'),**opts)
                else:
                    a=ColorStr(Str(ii,default='org'),**opts)
                #Recover added T for wrapping format to original
                if TT and '\n' in ii and ii.replace('\n','') == 'T': a=a[:-1]
            if msg_str:
                if TT:
                    #if message spliter exist and fix to first character
                    if TT == 1 and not ii.replace('\n',''):
                        msg_str=msg_str + msg_split + a
                    else:
                        msg_str=msg_str + a
                    if ii.replace('\n',''): TT=0 # remove special format tag
                else:
                    msg_str=msg_str + msg_split + a
            else:
                if intro_msg:
                    msg_str=intro_msg + a 
                elif intro_len:
                    msg_str= Space(num=intro_len) + a
                else:
                    msg_str=a 
            # if end of the line has extra '\n' then recover the losted '\n' by WrapString()
            if isinstance(ii,str) and len(ii) > 1 and ii[-1] == '\n':
                msg_str=msg_str + ii[-1]
        return msg_str

    #Get Logfile information for OLD version and remove the Logfile information in the messages
    if isinstance(logfile,str):
        logfile=logfile.split(',')
    elif isinstance(logfile,tuple):
        logfile=list(tuple)
    if not isinstance(logfile,list):
        logfile=[]
    for ii in msg:
        if isinstance(ii,str) and ':' in ii:
            logfile_list=ii.split(':')
            if logfile_list[0] in ['log_file','logfile']:
                if len(logfile_list) > 2:
                    for jj in logfile_list[1:]:
                        logfile.append(jj)
                else:
                    logfile=logfile+logfile_list[1].split(',')
                if isinstance(msg,tuple):
                    msg=list(msg)
                    msg.remove(ii)
                    msg=tuple(msg)
                else:
                    msg.remove(ii)
    
    # save msg(removed log_file information) to syslogd 
    if syslogd:
        # Make a message to single line
        tmp_str=msg_maker(*msg,msg_split=msg_split)
        if syslogd in ['INFO','info']:
            syslog.syslog(syslog.LOG_INFO,tmp_str)
        elif syslogd in ['KERN','kern']:
            syslog.syslog(syslog.LOG_KERN,tmp_str)
        elif syslogd in ['ERR','err']:
            syslog.syslog(syslog.LOG_ERR,tmp_str)
        elif syslogd in ['CRIT','crit']:
            syslog.syslog(syslog.LOG_CRIT,tmp_str)
        elif syslogd in ['WARN','warn']:
            syslog.syslog(syslog.LOG_WARNING,tmp_str)
        elif syslogd in ['DBG','DEBUG','dbg','debug']:
            syslog.syslog(syslog.LOG_DEBUG,tmp_str)
        else:
            syslog.syslog(tmp_str)

    #When having Log function then give the data to log function
    log_p=False
    if IsFunction(log): # Log function( debug mode log function too )
        try:
            if ('d' in dsp or 'f' in dsp) and logfile and 'n' not in dsp:
                if 'caller_parent' in opts:
                    if isinstance(opts['caller_parent'],int):
                        opts['caller_parent']=opts['caller_parent']+1
                    else:
                        opts['caller_parent']=2
                else:
                    opts['caller_parent']=2
            FeedFunc(log,*msg,**opts)
            # If log function take over the log then no more print to others
            return
        except:
            pass

    # Make a Intro
    intro_len=0
    intro_msg=''
    if not direct and not no_intro:
        intro_msg='{0} '.format(TIME().Now().strftime(date_format)) if date_format and not syslogd else ''
        intro_len=len(intro_msg)
        if caller_detail or caller_tree or caller_history or caller_ignore:
            if ignore_myself:
                if not isinstance(caller_ignore,list): caller_ignore=[]
                if 'FeedFunc' not in caller_ignore: caller_ignore.append('FeedFunc')
                if 'printf' not in caller_ignore: caller_ignore.append('printf')
        if caller_ignore and isinstance(caller_ignore,list):
            arg={'parent':parent_n,'args':False,'history':True,'tree':False}
            call_name=FunctionName(**arg)
            new_p=0
            for i in range(len(call_name)-1,0,-1):
                if call_name[i][0] in caller_ignore:
                    new_p+=1
                    continue
                break
            if isinstance(parent_n,str):
                parent_n_a=parent_n.split('-')
                if parent_n_a[0]:
                    parent_n_a[0]='{}'.format(int(parent_n_a[0])+new_p)
                else:
                    parent_n_a[0]='{}'.format(new_p)
                if len(parent_n_a) == 2 and parent_n_a[1]:
                    parent_n_a[1]='{}'.format(int(parent_n_a[1])+new_p)
                parent_n='-'.join(parent_n_a)
            elif isinstance(parent_n,int):
                parent_n=parent_n+new_p
        if caller_name or caller_ignore:
            arg={'parent':parent_n}
            if caller_detail:
                arg.update({'line_number':True,'full_filename':caller_full_filename,'filename':True,'args':True})
            else:
                arg['line_number']=caller_line_number
                arg['full_filename']=caller_full_filename
                arg['args']=caller_args
                arg['filename']=caller_filename
            if caller_tree:
                arg.update({'history':True,'tree':True})
            else:
                arg['history']=caller_history
            call_name=FunctionName(**arg)
            if call_name:
                # if line_number and filename then print logging at next line
                # if date_format then logging's intro length will be date format
                # if not date_format then loggin's intro length will be stepping length
                if isinstance(call_name,str): call_name=[call_name]
                if caller_tree or caller_history: call_name=call_name+[''] if date_format else call_name+[' ']
                intro_msg=intro_msg+WrapString(Join(call_name,'\n'),fspace=0, nspace=len(intro_msg),mode='space',ignore_empty_endline=False) + ': '
                intro_len=intro_len+len(call_name[-1])+2
        if Type(intro,'str') and intro:
            intro_msg=intro_msg+intro+': '
            intro_len=intro_len+len(intro)+2

    # Make input data to a string msg 
    if start_newline:
        if len(msg) and isinstance(msg[0],str) and len(msg[0]) and msg[0][0] == '\n': msg[0]=msg[0][1:]
        if start_newline == 'auto':
            if printf_newline_info.Get(dsp):
                start_newline='\n'
            else:
                start_newline=''
    msg_str=msg_maker(*msg,msg_split=msg_split,intro_len=intro_len,intro_msg='' if no_intro is None else intro_msg)
# DOn't need below code
#    if new_line:
#        if msg_str and msg_str[-1] == '\n': msg_str=msg_str[:-1]

    ## if end of line have no newline, but it has intro then adding start_newline
    #if intro_msg and not no_start_newline:
    #    if printf_newline_info.Get(dsp): 
    #        start_newline='\n'

    #DBG MODE for printing
    scr_dbg_print=False
    if scr_dbg is True:
        if scr_dbg_condition is None or msg_str == scr_dbg_condition:
            scr_dbg_print=True
            arg={'parent':'1-9','line_number':True,'filename':True,'args':False,'history':True,'tree':True}
            call_name=FunctionName(**arg)
            print('-------------FUNCTION--------------------')
            print(Join(call_name,'\n'))
            print('-----------------------------------------')
            print('log                   :{} (function:{}:{})'.format(log,IsFunction(log),opts))
            print('logfile               :{}'.format(logfile))
            print('newline info          :{}'.format(printf_newline_info.data))
            print('force no start newline:{}'.format(no_start_newline))
            print('newline               :(direct:{},start:{},end:{})'.format(direct,True if start_newline else False,True if new_line else False))
            print('ignore_empty          :{}'.format(ignore_empty))
            print('message               :[{}]'.format(msg))
            print('intro                 :[{}]'.format(intro_msg))
            print('log level             :{} < {} (print:{})'.format(printf_log_base,log_level, printf_log_base < log_level if IsInt(printf_log_base) and IsInt(log_level) else True))
            print('before mode print     :[{}]'.format(start_newline+msg_str+new_line))

    # Save to file or print to screen filter with log_level and already logging with log function or not.
    if 'd' in dsp and IsInt(printf_log_base) and IsInt(log_level):
        if printf_log_base < log_level:
            return
    # if just whitespace then not newline, something else with data then what ever
    # Save msg to logfile when defined logfile
    if logfile: # all mode can (even if d, f, i) just loging to file.
        for ii in logfile:
            if isinstance(ii,str) and ii:
                ii_d=os.path.dirname(ii)
                ii_d=ii_d if ii_d else '.' # If just filename then directory to .(current directory)
                if ii and os.path.isdir(ii_d):
                    if not msg_str:
                        if dbg_empty and not ignore_empty:   # Ignore empty data on screen w/o debugging 
                            parent_n=opts.get('caller_parent') if isinstance(opts.get('caller_parent'),int) else 1
                            arg={'parent':parent_n,'line_number':True,'filename':True,'args':False,'history':False,'tree':False}
                            call_name=FunctionName(**arg)
                            msg_str=intro_msg + ColorStr(WrapString('[** Empty-Data **] ({})'.format(call_name),fspace=intro_len, nspace=intro_len,mode='space'),**opts)
                    if not msg_str: return

                    # if end of line have no newline, but it has intro then adding start_newline
                    if intro_msg and not no_start_newline:
                        if printf_newline_info.Get(Bytes(ii)): 
                            start_newline='\n'
                    if scr_dbg_print:
                        print('mode                  :{} (before no newline:{})'.format(ii,True if printf_newline_info.Get(Bytes(ii)) else False))
                        print('updated start newline :{}'.format(True if start_newline else False))
                        print('print                 :[{}]'.format(start_newline+msg_str+new_line))
                        print('-----------------------------------------')
                    log_p=True  # writing to log_file
                    try:
                        with open(ii,'a+') as f:
                            f.write(start_newline+msg_str+new_line)
                    except FileNotFoundError:
                        err_msg="Error: Directory '{os.path.basedir(ii)}' not found"
                        StdErr(err_msg)
                        if 'r' in dsp:
                            return err_msg
                        return
                    except PermissionError:
                        err_msg="Error: Permission denied for '{ii}'"
                        StdErr(err_msg)
                        if 'r' in dsp:
                            return err_msg
                        return
                    except Exception as e: 
                        StdErr(e)
                        if 'r' in dsp:
                            return e
                        return
                    if new_line:
                        printf_newline_info.Del(Bytes(ii))
                    else:
                        printf_newline_info.Put(Bytes(ii),True)
    if ignore_empty is True and not msg_str: return # Ignore empty data on screen
    # print msg to screen when did not done with logfile or log function
    if 'e' in dsp:
        # if end of line have no newline, but it has intro then adding start_newline
        if intro_msg and not no_start_newline:
            if printf_newline_info.Get('e'): 
                start_newline='\n'
        if scr_dbg_print:
            print('mode                  :{} (before no newline:{})'.format('e',True if printf_newline_info.Get('e') else False))
            print('updated start newline :{}'.format(True if start_newline else False))
            print('print                 :[{}]'.format(start_newline+msg_str+new_line))
            print('-----------------------------------------')
        StdErr(start_newline+msg_str+new_line)
        printf_newline_info.Put('e',False if new_line else True)
    elif 'c' in dsp: #Display to console (it also work with Robot Framework)
        print(start_newline+msg_str+new_line,end='',file=sys.__stdout__)
    elif 's' in dsp or 'a' in dsp or 'n' in dsp: # Print out on screen
        if intro_msg and not no_start_newline:
            if printf_newline_info.Get('a' if 'a' in dsp else 's'): 
                start_newline='\n'
        if scr_dbg_print:
            print('mode                  :{} (before no newline:{})'.format('a',True if printf_newline_info.Get('a' if 'a' in dsp else 's') else False))
            print('updated start newline :{}'.format(True if start_newline else False))
            print('print                 :[{}]'.format(start_newline+msg_str+new_line))
            print('-----------------------------------------')
        # if end of line have no newline, but it has intro then adding start_newline
        StdOut(start_newline+msg_str+new_line)
        printf_newline_info.Put('a' if 'a' in dsp else 's',False if new_line else True)
    # return msg when required return whatever condition
    if 'r' in dsp:
        return msg_str

def ColorStr(msg,**opts):
    color=opts.get('color',None)
    color_db=opts.get('color_db',{'blue': 34, 'grey': 30, 'yellow': 33, 'green': 32, 'cyan': 36, 'magenta': 35, 'white': 37, 'red': 31})
    bg_color=opts.get('bg_color',None)
    bg_color_db=opts.get('bg_color_db',{'cyan': 46, 'white': 47, 'grey': 40, 'yellow': 43, 'blue': 44, 'magenta': 45, 'red': 41, 'green': 42})
    attr=opts.get('attr',None)
    attr_db=opts.get('attr_db',{'reverse': 7, 'blink': 5,'concealed': 8, 'underline': 4, 'bold': 1})
    if IsNone(os.getenv('ANSI_COLORS_DISABLED')) and (color or bg_color or attr):
        reset='''\033[0m'''
        fmt_msg='''\033[%dm%s'''
        if color and color in color_db:
            msg=fmt_msg % (color_db[color],msg)
        if bg_color and bg_color in bg_color_db:
            msg=fmt_msg % (color_db[bg_color],msg)
        if attr and attr in attr_db:
            msg=fmt_msg % (attr_db[attr],msg)
        return msg+reset #Support Color
    return msg #Not support color

def CleanAnsi(data):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    if Type(data,('str','bytes')):
        return ansi_escape.sub('',Str(data))
    elif isinstance(data,(list,tuple)):
        return [CleanAnsi(ii) for ii in data]
    elif isinstance(data,dict):
        for i in data:
            data[i]=CleanAnsi(data[i])
    return data

def cli_input(msg,**opts):
    '''
    CLI Input command
    hidden or passwd = True : input as password, False: (default) normal text input
    '''
    hidden=opts.get('hidden',opts.get('passwd',opts.get('password',False)))
    if hidden:
        if sys.stdin.isatty():
            p = getpass.getpass(msg)
        else:
            printf(msg,end_line='')
            p = sys.stdin.readline().rstrip()
    else:
        if PyVer(2):
            p=raw_input(msg)
        else:
            p=input(msg)
    return p

def TypeData(src,want_type=None,default='org',spliter=None):
    '''Convert (input)data to want type (ex: str -> list, int, ...), can not convert to type then return False'''
    if Type(want_type,'str'):
        if isinstance(src,(list,tuple)):
            if not isinstance(spliter,str): spliter=' '
            return Join(Str(src),Str(spliter))
        else:
            return Str(src,mode='force')
    elif Type(want_type,'bytes'):
        if isinstance(src,(list,tuple)):
            if not isinstance(spliter,str): spliter=b' '
            return Join(Bytes(src),Bytes(spliter))
        else:
            return Bytes(src)
    elif Type(want_type,'int'):
        return Int(src,err=True)
    elif Type(want_type,('list','tuple')) and isinstance(src,str) and isinstance(spliter,str):
        if Type(want_type,'tuple'):
            return tuple(Split(src,spliter))
        return Split(src,spliter)
    elif Type(want_type,'tuple') and isinstance(src,(list,dict)):
        if isinstance(src,dict):
            if spliter == 'key':
                return tuple(src.keys())
            elif spliter == 'value':
                return tuple(src.values())
            else:
                return tuple(src.items())
        return tuple(src)
    elif Type(want_type,'list') and isinstance(src,(tuple,dict)):
        if isinstance(src,dict):
            if spliter == 'key':
                return list(src.keys())
            elif spliter == 'value':
                return list(src.values())
            else:
                return list(src.items())
        return list(src)
    elif Type(src,want_type):
        return src
    if Type(src,('str','bytes')):
        return FormData(src,default='org')
    return Default(src,default)

def MoveData(src,data=None,to=None,from_idx=None,force=False,default='org'):
    '''
    support src type is list,str,(tuple)
    moving format : data(data) or from_idx(int)
      - data : if src has many same data then just keep single data at moved
    moving dest   : to(int)
    move data or index(from_idx) to want index(to)
      force=True: even tuple to move
    if not support then return default
    default : org
    '''
    _tuple=False
    src_type=TypeName(src)
    if src_type == 'tuple':
        if not force: return Default(src,default)
        _tuple=True
        src_type='list'
    if src_type in ['list','str'] and src:
        src=list(src)
        if to == 'last': to=-1
        elif to == 'first': to=0
        if isinstance(from_idx,int) and isinstance(to,int):
            if len(src) > abs(from_idx):
                to=FixIndex(src,to)
                if from_idx!=to:
                    if to == -1:
                        src.append(src[from_idx])
                    elif to == 0:
                        src=[src[from_idx]]+src
                    else:
                        src=src[:to]+[src[from_idx]]+src[to:]
                    src[to]=src[from_idx]
                    del src[from_idx]
        elif not IsNone(data) and isinstance(to,int):
            to=FixIndex(src,to)
            src=[i for i in src if i!=data]
            if to == -1:
                src.append(data)
            elif to == 0:
                src=[data]+src
            else:
                src=src[:to]+[data]+src[to:]
        if _tuple: return tuple(src)
        elif src_type == 'str': return Join(src,'')
        return src
    return Default(src,default)

def Random(length=8,mode=None,strs=None,**opts):
    '''
    make random number/string/characters
    length   : random string length (default: 8)
    mode (default: Alphanum)
     - alpha : lower alphabet
     - ALPHA : upper alphabet
     - Alpha : lower + upper alphabet
     - num   : number
     - char  : linux console usable symbol characters
     - sym   : all symbol characters
     - combin above modes (ex: Alphanum)
    strs     : if you want make a random string with your own special characters
    '''
    alpha='abcdefghijklmnopqrstuvwxyz'
    Alpha='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    num='0123456789'
    symbol='''~!@#$%^_+-={}[]:,.'''
    Symbol='''`*()&|\\';"/i<>?'''
    space=' '
    if not isinstance(strs,str) or not strs:
        strs=''
        if mode in ['all','*']:
            strs=alpha+Alpha+num+symbol+Symbol+space
        elif isinstance(mode,str):
            if 'alpha' in mode: strs=alpha
            if 'Alpha' in mode: strs=alpha+Alpha
            if 'ALPHA' in mode: strs=Alpha
            if 'num' in mode: strs=strs+num
            if 'char' in mode: strs=strs+symbol
            elif 'sym' in mode: strs=strs+symbol+Symbol+space
    if not strs: strs=alpha+Alpha+num
    strn=len(strs)-1
    stra=list(strs)
    out=[]
    for i in range(0,length):
        random.shuffle(stra)
        out.append(stra[random.randint(0,strn)])
    return int(''.join(out)) if mode == 'num' else ''.join(out)

def IsAllSameStr(src,find):
    '''Check input string is All same string or not'''
    if isinstance(src,str) and isinstance(find,str):
        if src.count(find) == len(src)/len(find):
            return True
    return False

def MkTemp(filename=None,suffix=None,split='-',opt='dry',base_dir=None,uniq=False,default_length=8,mode=None,**opts):
    '''
    make a random string
    filename: 
      None  : generate random string
      abc-XXXXX.log : abc-<random 5 characters>.log
      abc-NNN-abcd.log   : abc-<random 3 numbers>-abcd.log
      abc.log-XXXX  : abc.log-<random 4 characters>
    suffix  : if you need adding file extand(suffix) (ex: suffix='log' => XXXXX.log)
    split   : default -, split symbol for the filename
    opt
      - dry : dry run (return string)(default)
      - file: make a file
      - dir : make a directory
    base_dir: if you want a string under base_dir
    uniq    : if you want make a uniq string (not existing filename in the (base_dir)directory)
      seirial increase number
        if exist abc.log then abc.log-00000000
        if exist abc.log,abc.log-00000000 then abc.log-00000001
      filename='abc',suffix='log',uniq=True
        if exist abc.log then abc-00000000.log
        if exist abc.log,abc-00000000.log then abc-00000001.log
    default_length: random string length
    mode    : random string mode (same as Random()'s mode)
    custom  : custom random string source (same as Random()'s strs parameter)
    '''
    #Support OLD MkTemp() 
    if isinstance(suffix,str) and isinstance(filename,str):
        if suffix[0]=='-':
            if IsAllSameStr(suffix[1:],'X') or IsAllSameStr(suffix[1:],'N') or IsAllSameStr(suffix[1:],'x') or IsAllSameStr(suffix[1:],'n'):
                default_length=len(suffix)-1
                filename=filename+suffix.upper()
    # New design
    def outfile(filename,opt):
        if opt in ['file','f']:
           os.mknode(filename)
        elif opt in ['dir','d','directory']:
           os.mkdir(filename)
        else:
           return filename

    def mk_filename(filename,split):
        filename_a=filename.split(split)
        filename_n=len(filename_a)
        sss=None
        for ff in range(0,filename_n):
            for ss in ['N','X']:
                if IsAllSameStr(filename_a[ff],ss):
                    sss=ss
                    if ff < filename_n-1:
                        aa=Random(length=len(filename_a[ff]),mode='num' if sss == 'N' else mode,strs=opts.get('custom'))
                        if isinstance(aa,int):
                            filename_a[ff]='%0{}d'.format(len(filename_a[ff]))%aa
                        else:
                            filename_a[ff]='{}'.format(aa)
        filename_last_suffix=filename_a[-1].split('.')[0]
        filename_last_ext='.'.join(filename_a[-1].split('.')[1:])
        if sss is None: sss=['N','X']
        for ss in sss:
            if IsAllSameStr(filename_last_suffix,ss):
                aa=Random(length=len(filename_last_suffix),mode='num' if ss == 'N' else mode,strs=opts.get('custom'))
                if isinstance(aa,int):
                    filename_a[-1]='%0{}d'.format(len(filename_last_suffix))%aa
                else:
                    filename_a[-1]='{}'.format(aa)
                if filename_last_ext:
                    filename_a[-1]=filename_a[-1]+'.{}'.format(filename_last_ext)
        return split.join(filename_a)

    if IsNone(filename) or not isinstance(filename,str):
        rfilename=Random(length=default_length,mode='num' if suffix in ['n','N'] else mode,strs=opts.get('custom'))
        base_dir='.' if not base_dir else base_dir
    else:
        base_dir=os.path.dirname(filename)
        base_dir='.' if not base_dir else base_dir
        rfilename=mk_filename(os.path.basename(filename),split)
    if uniq:
        if isinstance(base_dir,str) and os.path.isdir(base_dir):
            inc=False
            for i in range(0,1000):
                if inc:
                    new_filename=rfilename+'{}%0{}d'.format(split,default_length)%(i-1)
                    if suffix:
                        new_filename=new_filename+'.{}'.format(suffix)
                    new_file=os.path.join(base_dir,new_filename)
                    if not os.path.exists(new_file):
                        return outfile(new_file,opt)
                else:
                    new_filename=mk_filename(rfilename,split)
                    if new_filename == rfilename:
                        inc=True
                    if suffix:
                        new_filename=new_filename+'.{}'.format(suffix)
                    new_file=os.path.join(base_dir,new_filename)
                    if not os.path.exists(new_file):
                        return outfile(new_file,opt)
    else:
        if base_dir == '.':
            if suffix:
                return rfilename+'.{}'.format(suffix)
            return rfilename
        return outfile(os.path.join(base_dir,rfilename),opt)

def osversion(mode='upper'):
    _p_system=platform.system()
    _p_machine=platform.machine()
    if IsSame(_p_machine,'aarch64'): _p_machine='arm'
    #64bit: platform.architecture()[0]
    mode='l' if IsSame(mode,'lower') else 'u'

    out={
       'platform':_p_system.lower() if mode == 'l' else _p_system.upper(),
       'arch':_p_machine.lower() if mode == 'l' else _p_machine.upper(),
       'name':None,
       'version':None,
       'ext':None,
       '64bit':sys.maxsize > 2**32,
       'code':None
    }
    if IsSame(_p_system,'Linux'):
        rt=rshell('''[ -f /etc/os-release ] && ( . /etc/os-release ; echo $ID)''')
        out['name']=rt[1].lower() if mode == 'l' else rt[1].upper()
        if IsIn(out['name'],('ubuntu','Raspbian','Fedora')):
            rt=rshell('''[ -f /etc/os-release ] && ( . /etc/os-release ; echo $VERSION)''')
            out['version']=rt[1].split()[0]
            out['ext']=' '.join(rt[1].split()[1:])
            rt=rshell('''[ -f /etc/os-release ] && ( . /etc/os-release ; echo $VERSION_CODENAME)''')
            out['code']=rt[1]
        else: #Centos, Rocky, Redhat,
            rt=rshell('''[ -f /etc/redhat-release ] && cat /etc/redhat-release''')
            if rt[0] == 0:
                for ii in rt[1].split():
                    if '.' in ii and ii.split('.')[0].isdigit():
                        ii_a=ii.split('.')
                        out['version']='{}.{}'.format(ii_a[0],ii_a[1])
                        out['ext']=ii_a[-1]
                        break
    elif IsSame(_p_system,'FreeBSD'):
        out['name']=_p_system.lower() if mode == 'l' else _p_system.upper()
        aa=platform.version()
        out['version']=aa.split()[1].split('-')[0]
        out['ext']=aa.split()[2]
    elif IsSame(_p_system,'Darwin'):
        out['name']='osx' if mode == 'l' else 'OSX'
        out['version']=platform.mac_ver()
    elif IsSame(_p_system,'Windows'):
        out['name']=_p_system.lower() if mode == 'l' else _p_system.upper()
        out['version']=platform.win32_ver()()
    else:
        out['name']=_p_system.lower() if mode == 'l' else _p_system.upper()
    return out

def Strip(src,mode='all',sym='whitespace'):
    if isinstance(src,str):
        if mode in ['start','left','begin']:
            if sym=='whitespace':
                return src.lstrip()
            else:
                return src.lstrip(sym)
        elif mode in ['end','right','last']:
            if sym=='whitespace':
                return src.rstrip()
            else:
                return src.rstrip(sym)
        elif mode in ['both','edge','outside']:
            if sym=='whitespace':
                return src.strip()
            else:
                return src.strip(sym)
        elif mode in ['inside']:
            for s in range(0,len(src)):
                if sym=='whitespace':
                    if src[s] != ' ': break
                else:
                    if src[s] != sym: break
            for e in range(len(src)-1,0,-1):
                if sym=='whitespace':
                    if src[e] != ' ': break
                else:
                    if src[e] != sym: break
            if sym=='whitespace':
                return src[:s]+' '.join(src[s:e+1].split())+src[e+1:]
            else:
                return src[:s]+sym.join(src[s:e+1].split(sym))+src[e+1:]
        else:
            if sym=='whitespace':
                return ' '.join(src.split())
            else:
                return sym.join(src.split(sym))
    return src

def Pop(src,key,default=None):
    if isinstance(src,dict):
        if key in src:
            return src.pop(key)
    elif isinstance(src,list):
        if isinstance(key,int) and not isinstance(key,bool):
            if len(src) > abs(key):
                return src.pop(key)
    if not IsNone(default):
        return default

def IsTrue(condition,requirements=None,shell=False,**opts):
    condition_type=type(condition).__name__
    if IsFunction(condition,builtin=False):
        opts['parent']=3 if 'parent' not in opts else opts['parent']+2
        ok,condout=FeedFunc(condition,**opts)
        if ok and condout:
            return True
    elif condition_type == 'str':
        try:
            return eval(condition)
        except:
            if isinstance(requirements,(tuple,list)):
                if IsIn(condition ,requirements): return True
            elif requirements is not None:
                if condition == requirements : return True
    elif condition_type == 'bool':
        return condition
    elif condition_type == 'int':
        if shell:
            if condition==0: return True
            return False
        else:
            if condition>0: return True
            return False
    return False

def Append(*a,symbol='',at=-1,want=None): # Append data according to source type
    if a:                    # list + list
        s=a[0]               # other => put to list
        if isinstance(s,bytes): s=Str(s)
        if want:
            if want in [list,'list']:
                if isinstance(s,tuple):
                    s=list(s)
                elif not isinstance(s,list):
                    s=[s]
                elif isinstance(s,str) and symbol:
                    s=s.split(symbol)
            elif want in [str,'str']:
                if isinstance(s,(list,tuple)):
                    s=Join(s,symbol=symbol)
                else:
                    s='{}'.format(s)
        sn=type(s).__name__
        for i in a[1:]:
            if sn == 'str':
                if isinstance(i,(list,tuple)):
                    for x in i:
                        if at == -1:
                            s=Join(s,'{}'.format(x),symbol=symbol)
                        elif at == 0:
                            s=Join('{}'.format(x),s,symbol=symbol)
                        else:
                            if len(s) > at:
                                s=Join(Join(s[:at],'{}'.format(x),symbol=symbol),s[at:],symbol=symbol)
                elif isinstance(i,(int,str,bytes)):
                    if at == -1:
                        s=Join(s,'{}'.format(Str(i)),symbol=symbol)
                    elif at == 0:
                        s=Join('{}'.format(Str(i)),s,symbol=symbol)
                    else:
                        if len(s) > at:
                            s=Join(Join(s[:at],'{}'.format(Str(i)),symbol=symbol),s[at:],symbol=symbol)
            elif sn == 'list':
                if isinstance(i,str) and symbol:
                    i=i.split(symbol)
                if at == -1 or at == len(s)-1:
                    if isinstance(i,list):
                        s=s+i
                    else:
                        s.append(i)
                elif at == 0 or len(s)+at == 0:
                    if isinstance(i,list):
                        s=i+s
                    else:
                        s=[i]+s
                elif at >0 and at < len(s):
                    if isinstance(i,list):
                        s=s[:at]+i+s[at:]
                    else:
                        s=s[:at]+[i]+s[at:]
        return s
    return False

def packet_receive_all(sock,count,progress=False,progress_msg=None,log=None,retry=0,retry_timeout=5,err_scr=False): # Packet
    if type(sock).__name__ not in ['socket','_socketobject','SSLSocket']:
        return False,'Is not network socket'
    buf = b''
    file_size_d=int('{0}'.format(count))
    tn=0
    newbuf=None
    while count:
        if progress:
            if progress_msg:
                printf('\r{} [ {} % ]'.format(progress_msg,int((file_size_d-count) / file_size_d * 100)),log=log,direct=True)
            else:
                printf('\rDownloading... [ {} % ]'.format(int((file_size_d-count) / file_size_d * 100)),log=log,direct=True)
        try:
            newbuf = sock.recv(count)
            tn=0 # reset try
        except socket.error as e:
            if tn < retry:
                printf("[ERROR] timeout value:{} retry: {}/{}\n{}".format(sock.gettimeout(),tn,retry,e),log=log,dsp='e' if err_scr else 'd')
                tn+=1
                TIME().Sleep(1)
                sock.settimeout(retry_timeout)
                continue
            return 'error',e
        if not newbuf: return True,None #maybe something socket issue.
        buf += newbuf
        count -= len(newbuf)
    if progress:
        if progress_msg:
            printf('\r{} [ 100 % ]\n'.format(progress_msg),log=log,direct=True)
        else:
            printf('\rDownloading... [ 100 % ]\n',log=log,direct=True)
    return True,buf

def Data2ByteString(data,protocol=2):
    try:
        return True,pickle.dumps(data,protocol=protocol) # common 2.x & 3.x version : protocol=2
    except:
        try:
            # <class 'KeyError'> then try again after filter out python default engine
            # maybe unknown character in the data
            return True,pickle.dumps(eval(str(data)),protocol=protocol) # common 2.x & 3.x version : protocol=2
        except:
            return False,sys.exc_info()[0]

def ByteString2Data(data):
    # If not pickle data then return original data, that is real data
    # if pickle data then convert to data
    try:
        return pickle.loads(data)
    except:
        return data

def packet_enc(data,key='kg',enc=False):
    nkey=Bytes2Int(key,encode='utf-8',default='org')
    ok,pdata=Data2ByteString(data)
    if not ok: return False,pdata
    data_type=Bytes(type(data).__name__[0])
    if enc and key:
        # encode code here
        #enc_tf=Bytes('t') # Now not code here. So, everything to 'f'
        #pdata=encode(key,pdata)
        enc_tf=Bytes('f')
    else:
        enc_tf=Bytes('f')
    ndata=struct.pack('>IssI',len(pdata),data_type,enc_tf,nkey)+pdata
    return True,ndata
        
def packet_head(sock,key='kg',retry=0,retry_timeout=5,keep_retry=False,timeout=1):
    #Get Header
    #keep_retry :True: if clased socket but wait
    ph=TIME()
    if (retry * retry_timeout) > timeout:
        timeout=retry * retry_timeout
    else:
        if retry_timeout <= 0: retry_timeout=5
        retry=(timeout//retry_timeout)+1
    while True:
        if ClosedSocket(sock):
            if retry <= 0:
                return False,'Already closed the socket',None,None
            retry-=1
            time.sleep(retry_timeout)
            continue
        ok,head=packet_receive_all(sock,10,retry=retry,retry_timeout=retry_timeout)
        if krc(ok,chk=True):
            try:
                st_head=struct.unpack('>IssI',Bytes(head))
                if st_head[3] == Bytes2Int(key,encode='utf-8',default='org'):
                    return True,st_head[0],st_head[1],st_head[2]
            except:
                pass
        if ph.Out(timeout): break
        time.sleep(1)
    return False,'Fail for read header({})'.format(head),None,None

def packet_dec(data,enc,key='kg'):
    #ok,size,data_type,enc=packet_head(sock)
    #ok,data=packet_receive_all(sock,size,....)
    #real_data=packet_dec(data,enc)
    if enc == 't':
        # decode code here
        # data=decode(data)
        pass
    return ByteString2Data(data)

def ClosedSocket(sock):
    try:
        # this will try to read bytes without blocking
        # and also without removing them from buffer (peek only)
        data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:
        return True  # socket was closed for some other reason
    except Exception as e: #unexpected exception when checking if a socket is closed
        return False
    return False

def RemoveNewline(src,mode='edge',newline='\n',byte=None):
    if isinstance(byte,bool):
        if byte:
            src=Bytes(src)
        else:
            src=Str(src)
    src_a=Split(src,newline,default=False,listonly=False)
    if src_a is False:
        return src
    if mode in ['edge','both']:
        if not src_a[0].strip() and not src_a[-1].strip():
            return Join(src_a[1:-1],symbol=newline)
        elif not src_a[0].strip():
            return Join(src_a[1:],symbol=newline)
        elif not src_a[-1].strip():
            return Join(src_a[:-1],symbol=newline)
    elif mode in ['first','start',0]:
        if not src_a[0].strip():
            return Join(src_a[1:],symbol=newline)
    elif mode in ['end','last',-1]:
        if not src_a[-1].strip():
            return Join(src_a[:-1],symbol=newline)
    elif mode in ['*','all','everything']:
        return Join(src_a,symbol='')
    return src

def ls(dirname,opt=''):
    if not IsNone(dirname) and os.path.isdir(dirname):
        dirlist=[]
        dirinfo_a=list(os.walk(dirname))
        if not IsNone(dirinfo_a):
            dirinfo=dirinfo_a[0]
            if opt == 'd':
                dirlist=Get(dirinfo,1)
            elif opt == 'f':
                dirlist=Get(dirinfo,2)
            else:
                dirlist=Get(dirinfo,1)+Get(dirinfo,2)
            return dirlist
    return False

def cat(filename,**opts):
    byte=opts.get('byte',False)
    newline=opts.get('newline','\n')
    read_firstline=opts.get('read_firstline',opts.get('head',opts.get('head_line',False)))
    default=opts.get('default',False)
    no_edge=opts.get('no_edge',False)
    no_end_newline=opts.get('no_end_newline',False)
    file_only=opts.get('file_only',opts.get('fileonly',True))
    no_all_newline=opts.get('no_all_newline',False)
    no_first_newline=opts.get('no_first_newline',False)
    log=opts.get('log')

    if IsNone(filename):
        printf('Filename is None',log=log,mode='d')
        return default
    if os.path.isdir(filename):
        printf('{} is a directory'.format(filename),log=log,mode='d')
        return default
    if not os.path.exists(filename):
        printf('{} not found'.format(filename),log=log,mode='d')
        return default
    try:
        if read_firstline:  # Readline
            with open(filename,'rb') as f:
                data=f.readline()
        elif not file_only: # Read special file
            data=os.open(filename,os.O_RDONLY)
            os.close(data)
        else: # Read normal file
            with open(filename,'rb') as f:
                data=f.read()
        if not byte:
           data=Str(data)
    except:
        printf(sys.exc_info()[0],log=log,mode='d')
        return default
    return RemoveNewline(data,mode='edge' if no_edge else 'end' if no_end_newline else 'first' if no_first_newline else 'all' if no_all_newline else None,newline=newline,byte=byte)

def Compress(data,mode='gzip'):
    try:
        if isinstance(data,str) and os.path.isfile(data):
            with open(data,'rb') as f:
                data=f.read()
        if mode == 'lz4':
            Import('from lz4 import frame')
            return frame.compress(data)
        elif mode == 'bz2':
            return bz2.compress(data)
        elif mode == 'gzip':
            return gzip.compress(data,compresslevel=9) #decompress(data)
        else: #zlib
            return zlib.compress(data) # decompress(data)
    except:
        return False

def Decompress(data,mode='gzip'):
    try:
        if isinstance(data,str) and os.path.isfile(data):
            with open(data,'rb') as f:
                data=f.read()
        if mode == 'lz4':
            Import('from lz4 import frame')
            return frame.decompress(data)
        elif mode == 'bz2':
            return bz2.BZ2Decompressor().decompress(data)
        elif mode == 'gzip':
            return gzip.decompress(data)
        else:
            return zlib.decompress(data)
    except:
        return False

def sizeof(obj):
    msize = 0
    ids = set()
    objects = [obj]
    while objects:
        new = []
        for i in objects:
            if id(i) not in ids:
                ids.add(id(i))
                msize += sys.getsizeof(i)
                new.append(i)
        objects = gc.get_referents(*new)
    return msize

def human_byte(num, unit="K", wunit=None,int_out=False):
    units = ["B","K","M","G","T","P"]
    if wunit is None:
        unit=unit.upper()
        if num >= 1000:
            while num >= 1000:
               sui=units.index(unit)
               if len(units) <= sui+1:
                   break
               num /= 1024.0
               unit = units[sui+1]
        elif num < 1:
            while num < 1: #0.XXX digits
               sui=units.index(unit)
               if sui-1 < 0:
                   break
               num *= 1024.0
               unit = units[sui-1]
    else:
        wunit=wunit.upper()
        eui=units.index(wunit)
        if sui < eui:
            for i in range(sui,eui):
                num /= 1024.0
        elif sui > eui:
            for i in range(sui,eui,-1):
                num *= 1024.0
        unit=wunit
    if int_out:
        return float("%.1f"%(num))
    else:
        if unit == "B":
            return "%.1f %s" % (num,unit)
        else:
            return "%.1f %sB" % (num,unit)

def Human_Unit(num,unit='S',want_unit=None,int_out=False):
    def convert_sec_to_format(num,want_format="%Y %m %d %H:%M:%S"):
        return datetime.datetime.fromtimestamp(num).strftime(want_format)
    def convert_int_time_to_yhms(num,unit='S',want=None):
        c=[31536000,86400,3600,60,1] # yy,dd,hh,mm,ss
        cu=['Y','D','H','M','S']     # yy,dd,hh,mm,ss
        if isinstance(want,str) and want and want in cu:
            start_i=cu.index(want)
        else:
            start_i=0
        if isinstance(unit,str) and unit and unit in cu:
            mx=cu.index(unit)
        else:
            mx=len(c)-1
        if mx == len(c)-1: # sec -> want
            o={}
            for i in range(start_i,mx+1):
                if (mx == i and num >= c[i]) or num > c[i]:
                    o[cu[i]]=num//c[i]
                    num=num%(c[i]*o[cu[i]])
            return o
        else:  # unit -> sec and calculate sec to want
            num = num * c[mx] # convert to unit to seconds
            return convert_int_time_to_yhms(num,unit='S',want=want)
    if isinstance(unit,str) and unit and (want_unit is None or isinstance(want_unit,str)):
        if unit.upper() in ['MM','MIN','Y','YY','YEAR','HH','H','HOUR','S','SEC','SS']:
            mode='time'
            if isinstance(want_unit,str):
                up_want_unit=want_unit.upper()
                if up_want_unit in ['HOUR','HH','HOURS','H']: want_unit='H'
                elif up_want_unit in ['MIN','MM','MINUTE','MINUTES','M']: want_unit='M'
                elif up_want_unit in ['DAY','DD','DAYS','D']: want_unit='D'
                elif up_want_unit in ['YEAR','YY','YEARS','Y']: want_unit='Y'
                elif up_want_unit in ['SEC','SS','SECOND','SECONDS','S']: want_unit='S'
        else:
            mode='byte'
        num_unit=unit[0].upper()
        #TIME
        if num_unit == 'S' and (isinstance(want_unit,str) and want_unit and want_unit[0] == '%'):
            if len(want_unit) == 1:
                return convert_sec_to_format(num,want_format="%Y %m %d %H:%M:%S")
            else:
                return convert_sec_to_format(num,want_format=want_unit)
        #TIME
        elif (mode == 'time' and want_unit in ['Y','D','H','M','S',None]) or (num_unit in ['Y','D','H','M','S'] and want_unit in ['Y','D','H','M','S']):
            oo=convert_int_time_to_yhms(num,unit=num_unit,want=want_unit)
            if int_out:
                if want_unit:# and want_unit in oo:
                    return oo.get(want_unit,0)
                else: # if want unit is None then return num
                    return num
            else:
                o=''
                for i in ['Y','D','H','M','S']:
                    if i in oo:
                        if o: o=o+' {}{}'.format(oo[i],i)
                        else: o='{}{}'.format(oo[i],i)
                return o
        #Byte
        elif num_unit in ["B","K","M","G","T","P"] and want_unit in ["B","K","M","G","T","P",None]:
            return human_byte(num, unit=num_unit, wunit=want_unit, int_out=int_out)
    return 'Unknown Unit({} -> {})'.format(unit,want_unit)

class FILE_W:
    '''
    New design to simple
    sub_dir  : True (Get files in recuring directory)
    data     : True (Get File Data)
    md5sum   : True (Get File's MD5 SUM)
    link2file: True (Make a real file instead sym-link file)
    file format : size (13)+head({})+data([,,,,,])
    head: {info{},data_id:x}
    '''
    def __init__(self,*inp,**opts):
        self.root_path=opts.get('root_path',None)
        if IsNone(self.root_path): self.root_path=Path()
        self.info=opts.get('info',opts.get('data',{}))

    def List(self,name,sub_dir=False,dirname=False,default=[]):
        #get directory and each directories' file list
        if isinstance(name,str):
            if name[0] == '/':  # Start from root path
                if os.path.isfile(name) or os.path.islink(name): return os.path.dirname(name),[os.path.basename(name)]
                if os.path.isdir(name):
                    if sub_dir:
                        rt = []
                        pwd=os.getcwd()
                        os.chdir(name)
                        for base, dirs, files in os.walk('.'):
                            if dirname: rt.extend(os.path.join(base[2:], d) for d in dirs)
                            rt.extend(os.path.join(base[2:], f) for f in files)
                        os.chdir(pwd)
                        return Path(name),rt
                    else:
                        return Path(name),[f for f in os.listdir(name)]
            elif self.root_path: # start from defined root path
                chk_path=Path(self.root_path,name)
                if os.path.isfile(chk_path) or os.path.islink(chk_path): return Path(self.root_path),[name]
                if os.path.isdir(chk_path):
                    if sub_dir:
                        rt = []
                        pwd=os.getcwd()
                        os.chdir(self.root_path) # Going to defined root path
                        # Get recuring file list of the name (when current dir then '.')
                        for base, dirs, files in os.walk(name):
                            if dirname: rt.extend(os.path.join(base[2:], d) for d in dirs)
                            rt.extend(os.path.join(base[2:], f) for f in files)
                        os.chdir(pwd) # recover to the original path
                        return Path(self.root_path),rt
                    else:
                        if name == '.': name=''
                        return Path(self.root_path),[os.path.join(name,f) for f in os.listdir('{}/{}'.format(self.root_path,name))]
        return default,[]

    def FileName(self,filename):
        if isinstance(filename,str):
            filename_info=os.path.basename(filename).split('.')
            if 'tar' in filename_info:
                idx=filename_info.index('tar')
            else:
                idx=-1
            return Join(filename_info[:idx],symbol='.'),Join(filename_info[idx:],symbol='.')
        return None,None

    def FileType(self,filename,default=False):
        if not isinstance(filename,str) or not os.path.isfile(filename): return default
        Import('import magic',install_name='python-magic')
        f=open(filename,'rb')
        aa=magic.from_buffer(f.read(2048))
        f.close()
        if isinstance(aa,str): return aa.split()[0].lower()
        return 'unknown'

    def FileInfo(self,filename,roots=None,_type=None,exist=None):
        if self.info: # from inside data
            if IsNone(roots): roots=self.FindRP()
            if not isinstance(filename,str) or IsNone(filename): return False
            for root in roots:
                rt=self.info.get(root,{})
                for ii in filename.split('/'):
                    if ii not in rt: return False
                    rt=rt[ii]
                return rt.get(' i ',False)

        # from real file
        rt={}
        if exist is False: return {'exist':False}
        rt['name'],rt['ext']=self.FileName(filename)
        if os.path.exists(filename):
            state=os.stat(filename)
            rt['exist']=True
            rt['size']=state.st_size
            rt['mode']=oct(state.st_mode)[-4:]
            rt['atime']=state.st_atime
            rt['mtime']=state.st_mtime
            rt['ctime']=state.st_ctime
            rt['gid']=state.st_gid
            rt['uid']=state.st_uid
            if IsNone(_type):
                rt['type']=_type
            else:
                if os.path.islink(filename):
                    rt['type']='link'
                elif os.path.isdir(filename):
                    rt['type']='dir'
                else:
                    rt['type']=self.FileType(filename)
        else:
            rt['exist']=False
        return rt

    def CdPath(self,base,path):
        rt=base
        for ii in path.split('/'):
            if ii not in rt: return False
            rt=rt[ii]
        return rt

    def MkInfo(self,rt,filename=None,**opts):
        if ' i ' not in rt: rt[' i ']={}
        rt[' i ']=self.FileInfo(filename,_type=opts.get('type'),exist=opts.get('exist'))
        if opts: rt[' i '].update(opts)

    def Get(self,*filenames,**opts):
        base={}
        filelist={}
        def MkPath(base,path,root_path):
            rt=base
            chk_dir='{}'.format(root_path)
            for ii in path.split('/'):
                if ii:
                    chk_dir=Path(chk_dir,ii)
                    if ii not in rt:
                        rt[ii]={}
                        if os.path.isdir(chk_dir): self.MkInfo(rt[ii],chk_dir,type='dir')
                    rt=rt[ii]
            return rt

        def _Get_(root_path,*filenames,**opts):
            data=opts.get('data',False)
            md5sum=opts.get('md5sum',False)
            link2file=opts.get('link2file',False)

            for filename in filenames:
                tfilename=Path(root_path,filename)
                if os.path.exists(tfilename):
                    rt=MkPath(base,filename,root_path)
                    if os.path.islink(tfilename): # it is a Link File
                        if os.path.isfile(filename): # it is a File
                            if link2file:
                                _md5=None
                                if data or md5sum: # MD5SUM or Data
                                    filedata=self.Rw(tfilename,out='byte')
                                    if filedata[0]:
                                        if data: rt['data']=filedata[1]
                                        if md5sum: _md5=md5(filedata[1])
                                self.MkInfo(rt,filename=tfilename,type=self.FileType(tfilename),md5=_md5)
                        else:
                            self.MkInfo(rt,filename=tfilename,type='link',dest=os.readlink(tfilename))
                    elif os.path.isdir(tfilename): # it is a directory
                        self.MkInfo(rt,tfilename,type='dir')
                    elif os.path.isfile(tfilename): # it is a File
                        _md5=None
                        if data or md5sum: # MD5SUM or Data
                            filedata=self.Rw(tfilename,out='byte')
                            if filedata[0]:
                                if data: rt['data']=filedata[1]
                                if md5sum: _md5=md5(filedata[1])
                        self.MkInfo(rt,filename=tfilename,type=self.FileType(tfilename),md5=_md5)
                else:
                    self.MkInfo(rt,filename,exist=False)
            if base:
                return {root_path:base}
            return {}

        if not filenames: filenames=['.']
        for filename in filenames:
            root_path,flist=self.List(filename,sub_dir=opts.get('sub_dir',False),dirname=True)
            if root_path not in filelist: filelist[root_path]=[]
            filelist[root_path]=filelist[root_path]+flist

        for ff in filelist:
            self.info.update(_Get_(ff,*filelist[ff],**opts))
        return self


    def GetList(self,dirname=None,roots=None,file_only=False,dir_only=False,sub_dir=False,include_path=False,detail=False): #get file info dict from Filename path
        if IsNone(roots): roots=self.FindRP()
        for root in roots:
            if isinstance(root,str):
                rt=self.info.get(root,{})
                if dirname and dirname != root:
                    rt=self.CdPath(rt,dirname)
                if isinstance(rt,dict):
                    for ii in rt:
                        file_info=rt[ii].get(' i ',{})
                        dinfo=''
                        if detail:
                            dinfo='{} {} {} {} {} {} '.format(file_info.get('mode'),
                                      1 if file_info.get('type') != 'dir' else len(rt[ii])-1,
                                      file_info.get('uid'),
                                      file_info.get('gid'),
                                      file_info.get('size'),
                                      file_info.get('mtime'),
                                      )
                        if ii == ' i ': continue
                        if file_info.get('type') == 'dir':
                            if file_only: continue
                            print('{}{}/'.format(dinfo,ii))
                            if sub_dir:
                                self.GetList(dirname=ii,roots=[root],sub_dir=sub_dir,include_path=True,detail=detail)
                        elif not dir_only:
                            if include_path:
                                print('{}{}/{}'.format(dinfo,dirname,ii))
                            else:
                                print('{}{}'.format(dinfo,ii))
        return False

    def ExecFile(self,filename,bin_name=None,default=None,work_path='/tmp'):
        # check the filename is excutable in the system bin file then return the file name
        # if compressed file then extract the file and find bin_name file in the extracted directory
        #   and found binary file then return then binary file path
        # if filename is excutable file then return the file path
        # if not found then return default value
        exist=self.FileInfo(filename)
        if exist:
            if exist['type'] in ['elf'] and exist['mode'] == 33261:return filename
            if self.Extract(filename,work_path=work_path):
                if bin_name:
                    rt=[]
                    for ff in self.Find(work_path,filename=bin_name):
                        if self.Info(ff).get('mode') == 33261:
                            rt.append(ff)
                    return rt
        else:
            if find_executable(filename): return filename
        return default

    def Basename(self,filename,default=False):
        if isinstance(filename,str):return os.path.basename(filename)
        return default

    def Dirname(self,filename,bin_name=None,default=False):
        if not isinstance(filename,str): return default
        if IsNone(bin_name): return os.path.dirname(filename)
        if not isinstance(bin_name,str): return default
        bin_info=bin_name.split('/')
        bin_n=len(bin_info)
        filename_info=filename.split('/')
        filename_n=len(filename_info)
        for ii in range(0,bin_n):
            if filename_info[filename_n-1-ii] != bin_info[bin_n-1-ii]: return default
        return Join(filename_info[:-bin_n],symbol='/')

    def Find(self,filename,default=[]):
        if not isinstance(filename,str): return default
        filename=os.path.basename(filename)
        if os.path.isdir(self.root_path):
            rt = []
            for base, dirs, files in os.walk(self.root_path):
                found = fnmatch.filter(files, filename)
                rt.extend(os.path.join(base, f) for f in found)
            return rt
        return default

    def Rw(self,name,data=None,out='byte',append=False,read=None,overwrite=True,finfo={},file_only=True,default=False):
        if isinstance(name,str):
            #if data is None: # Read from file
            if IsNone(data): # Read from file
                data=cat(name,file_only=file_only,byte=out,head=read,default=default)
                if data is False:
                    return False,default
                return True,data
            else: # Write to file
                file_path=os.path.dirname(name)
                if not file_path or os.path.isdir(file_path): # current dir or correct directory
                    if append:
                        with open(name,'ab') as f:
                            f.write(Bytes(data))
                    elif not file_only:
                        try:
                            f=os.open(name,os.O_RDWR)
                            os.write(f,data)
                            os.close(f)
                        except:
                            return False,None
                    else:
                        with open(name,'wb') as f:
                            f.write(Bytes(data))
                        if isinstance(finfo,dict) and finfo: self.SetIdentity(name,**finfo)
                        #mode=self.Mode(mode)
                        #if mode: os.chmod(name,int(mode,base=8))
                        #if uid and gid: os.chown(name,uid,gid)
                        #if mtime and atime: os.utime(name,(atime,mtime))# Time update must be at last order
                    return True,None
                if default == {'err'}:
                    return False,'Directory({}) not found'.format(file_path)
                return False,default
        if default == {'err'}:
            return False,'Unknown type({}) filename'.format(name)
        return False,default

    def Mode(self,val,mode='chmod',default=False):
        '''
        convert File Mode to mask
        mode 
           'chmod' : default, convert to mask (os.chmod(<file>,<mask>))
           'int'   : return to int number of oct( ex: 755 )
           'oct'   : return oct number (string)
           'str'   : return string (-rwxr--r--)
        default: False
        '''
        def _mode_(oct_data,mode='chmod'):
            #convert to octal to 8bit mask, int, string
            if mode == 'chmod':
                return int(oct_data,base=8)
            elif mode in ['int',int]:
                return int(oct_data.replace('o',''),base=10)
            elif mode in ['str',str]:
                m=[]
                #for i in list(str(int(oct_data,base=10))):
                t=False
                for n,i in enumerate(str(int(oct_data.replace('o',''),base=10))):
                    if n == 0:
                        if i == '1': t=True
                    if n > 0:
                        if i == '7':
                            m.append('rwx')
                        elif i == '6':
                            m.append('rw-')
                        elif i == '5':
                            m.append('r-x')
                        elif i == '4':
                            m.append('r--')
                        elif i == '3':
                            m.append('-wx')
                        elif i == '2':
                            m.append('-w-')
                        elif i == '1':
                            m.append('--x')
                str_mod=Join(m,'')
                if t: return str_mod[:-1]+'t'
                return str_mod
            return oct_data
        if isinstance(val,int):
            #if val > 511:       #stat.st_mode (32768 ~ 33279)
            #stat.st_mode (file: 32768~36863, directory: 16384 ~ 20479)
            if 32768 <= val <= 36863 or 16384 <= val <= 20479:   #stat.st_mode
                #return _mode_(oct(val)[-4:],mode) # to octal number (oct(val)[-4:])
                return _mode_(oct(val & 0o777),mode) # to octal number (oct(val)[-4:])
            elif 511 >= val > 63:      #mask
                return _mode_(oct(val),mode)      # to ocal number(oct(val))
            else:
                return _mode_('%04d'%(val),mode)      # to ocal number(oct(val))
        else:
            val=Str(val,default=None)
            if isinstance(val,str):
                val_len=len(val)
                num=Int(val,default=None)
                if isinstance(num,int):
                    if 3 <= len(val) <=4 and 100 <= num <= 777: #string type of permission number(octal number)
                        return _mode_('%04d'%(num),mode)
                else:
                    val_len=len(val)
                    if 9<= val_len <=10:
                        if val_len == 10 and val[0] in ['-','d','s']:
                            val=val[1:]
                    else:
                        StdErr('Bad permission length')
                        return default
                    if not all(val[k] in 'rw-' for k in [0,1,3,4,6,7]):
                        StdErr('Bad permission format (read-write)')
                        return default
                    if not all(val[k] in 'xs-' for k in [2,5]):
                        StdErr('Bad permission format (execute)')
                        return default
                    if val[8] not in 'xt-':
                        StdErr( 'Bad permission format (execute other)')
                        return default
                    m = 0
                    if val[0] == 'r': m |= stat.S_IRUSR
                    if val[1] == 'w': m |= stat.S_IWUSR
                    if val[2] == 'x': m |= stat.S_IXUSR
                    if val[2] == 's': m |= stat.S_IXUSR | stat.S_ISUID

                    if val[3] == 'r': m |= stat.S_IRGRP
                    if val[4] == 'w': m |= stat.S_IWGRP
        if isinstance(val,int):
            #if val > 511:       #stat.st_mode (32768 ~ 33279)
            #stat.st_mode (file: 32768~36863, directory: 16384 ~ 20479)
            if 32768 <= val <= 36863 or 16384 <= val <= 20479:   #stat.st_mode
                #return _mode_(oct(val)[-4:],mode) # to octal number (oct(val)[-4:])
                return _mode_(oct(val & 0o777),mode) # to octal number (oct(val)[-4:])
            elif 511 >= val > 63:      #mask
                return _mode_(oct(val),mode)      # to ocal number(oct(val))
            else:
                return _mode_('%04d'%(val),mode)      # to ocal number(oct(val))
        else:
            val=Str(val,default=None)
            if isinstance(val,str):
                val_len=len(val)
                num=Int(val,default=None)
                if isinstance(num,int):
                    if 3 <= len(val) <=4 and 100 <= num <= 777: #string type of permission number(octal number)
                        return _mode_('%04d'%(num),mode)
                else:
                    val_len=len(val)
                    if 9<= val_len <=10:
                        if val_len == 10 and val[0] in ['-','d','s']:
                            val=val[1:]
                    else:
                        StdErr('Bad permission length')
                        return default
                    if not all(val[k] in 'rw-' for k in [0,1,3,4,6,7]):
                        StdErr('Bad permission format (read-write)')
                        return default
                    if not all(val[k] in 'xs-' for k in [2,5]):
                        StdErr('Bad permission format (execute)')
                        return default
                    if val[8] not in 'xt-':
                        StdErr( 'Bad permission format (execute other)')
                        return default
                    m = 0
                    if val[0] == 'r': m |= stat.S_IRUSR
                    if val[1] == 'w': m |= stat.S_IWUSR
                    if val[2] == 'x': m |= stat.S_IXUSR
                    if val[2] == 's': m |= stat.S_IXUSR | stat.S_ISUID

                    if val[3] == 'r': m |= stat.S_IRGRP
                    if val[4] == 'w': m |= stat.S_IWGRP
        if isinstance(val,int):
            #if val > 511:       #stat.st_mode (32768 ~ 33279)
            #stat.st_mode (file: 32768~36863, directory: 16384 ~ 20479)
            if 32768 <= val <= 36863 or 16384 <= val <= 20479:   #stat.st_mode
                #return _mode_(oct(val)[-4:],mode) # to octal number (oct(val)[-4:])
                return _mode_(oct(val & 0o777),mode) # to octal number (oct(val)[-4:])
            elif 511 >= val > 63:      #mask
                return _mode_(oct(val),mode)      # to ocal number(oct(val))
            else:
                return _mode_('%04d'%(val),mode)      # to ocal number(oct(val))
        else:
            val=Str(val,default=None)
            if isinstance(val,str):
                val_len=len(val)
                num=Int(val,default=None)
                if isinstance(num,int):
                    if 3 <= len(val) <=4 and 100 <= num <= 777: #string type of permission number(octal number)
                        return _mode_('%04d'%(num),mode)
                else:
                    val_len=len(val)
                    if 9<= val_len <=10:
                        if val_len == 10 and val[0] in ['-','d','s']:
                            val=val[1:]
                    else:
                        StdErr('Bad permission length')
                        return default
                    if not all(val[k] in 'rw-' for k in [0,1,3,4,6,7]):
                        StdErr('Bad permission format (read-write)')
                        return default
                    if not all(val[k] in 'xs-' for k in [2,5]):
                        StdErr('Bad permission format (execute)')
                        return default
                    if val[8] not in 'xt-':
                        StdErr( 'Bad permission format (execute other)')
                        return default
                    m = 0
                    if val[0] == 'r': m |= stat.S_IRUSR
                    if val[1] == 'w': m |= stat.S_IWUSR
                    if val[2] == 'x': m |= stat.S_IXUSR
                    if val[2] == 's': m |= stat.S_IXUSR | stat.S_ISUID

                    if val[3] == 'r': m |= stat.S_IRGRP
                    if val[4] == 'w': m |= stat.S_IWGRP
                    if val[5] == 'x': m |= stat.S_IXGRP
                    if val[5] == 's': m |= stat.S_IXGRP | stat.S_ISGID

                    if val[6] == 'r': m |= stat.S_IROTH
                    if val[7] == 'w': m |= stat.S_IWOTH
                    if val[8] == 'x': m |= stat.S_IXOTH
                    if val[8] == 't': m |= stat.S_IXOTH | stat.S_ISVTX
                    return _mode_(oct(m),mode)
        return default

    # Find filename's root path and filename according to the db
    def FindRP(self,filename=None,default=None):
        if isinstance(filename,str) and self.info:
            info_keys=list(self.info.keys())
            info_num=len(info_keys)
            if filename[0] != '/':
                if info_num == 1: return info_keys[0]
                return self.root_path
            aa='/'
            filename_a=filename.split('/')
            for ii in range(1,len(filename_a)):
                aa=Path(aa,filename_a[ii])
                if aa in info_keys:
                    #remain_path='/'.join(filename_a[ii+1:])
                    remain_path=Join(filename_a[ii+1:],symbol='/')
                    if info_num == 1: return aa,remain_path
                    # if info has multi root path then check filename in the db of each root_path
                    if self.FileInfo(remain_path,aa): return aa,remain_path
        elif self.info:
            return list(self.info.keys())
        return default

    def ExtractRoot(self,**opts):
        root_path=opts.get('root_path',[])
        dirpath=opts.get('dirpath')
        sub_dir=opts.get('sub_dir',False)
        if isinstance(root_path,str):
            root_path=[root_path]
        #if not os.path.isdir(opts.get('dest')): os.makedirs(opts.get('dest'))
        if self.Mkdir(opts.get('dest'),force=True) is False: return False
        for rp in root_path:
            new_dest=opts.get('dest')
            if dirpath:
                rt=self.CdPath(self.info[rp],dirpath)
                if rt is False:
                    print('{} not found'.format(dirpath))
                    return
            else:
                dirpath=''
                rt=self.info[rp]

            rinfo=rt.get(' i ',{})
            rtype=rinfo.get('type')
            #dir:directory,None:root directory
            if not IsNone(rtype,chk_val=['dir',None,'']): # File / Link
                mydest=os.path.dirname(dirpath)
                myname=os.path.basename(dirpath)
                if mydest:
                    mydest=os.path.join(new_dest,mydest)
                else:
                    mydest=new_dest
                #if not os.path.isdir(mydest): os.makedirs(mydest)
                if self.Mkdir(mydest,force=True,info=rinfo) is False: return False
                if rtype == 'link':
                    os.symlink(rinfo['dest'],os.path.join(mydest,myname))
                    self.SetIdentity(os.path.join(mydest,myname),**rinfo)
                else: # File
                    if 'data' in rt: self.Rw(Path(mydest,myname),data=rt['data'],finfo=rinfo)
                    else: print('{} file have no data'.format(dirpath))
#                self.SetIdentity(os.path.join(mydest,myname),**rinfo)
            else: # directory or root DB
                for ii in rt:
                    if ii == ' i ': continue
                    finfo=rt[ii].get(' i ',{})
                    ftype=finfo.get('type')
                    if ftype == 'dir':
                        mydir=os.path.join(new_dest,ii)
                        self.Mkdir(mydir,force=True,info=finfo)
                        #self.SetIdentity(mydir,**finfo)
                        # Sub directory
                        if sub_dir: self.ExtractRoot(dirpath=os.path.join(dirpath,ii),root_path=rp,dest=os.path.join(new_dest,ii),sub_dir=sub_dir)
                        #if dmtime and datime: os.utime(mydir,(datime,dmtime)) # Time update must be at last order
                    elif ftype == 'link':
                        iimm=os.path.join(new_dest,ii)
                        if not os.path.exists(iimm):
                            os.symlink(finfo['dest'],iimm)
                            self.SetIdentity(iimm,**finfo)
                    else: # File
                        if 'data' in rt[ii]: self.Rw(os.path.join(new_dest,ii),data=rt[ii]['data'],finfo=finfo)
                        else: print('{} file have no data'.format(ii))

    def Mkdir(self,path,force=False,info={}):
        if not isinstance(path,str): return None
        if os.path.exists(path): return None
        if force:
            try:
                os.makedirs(path)
                if isinstance(info,dict) and info: self.SetIdentity(path,**info)
            except:
                return False
        else:
            try:
                os.mkdir(path)
                if isinstance(info,dict) and info: self.SetIdentity(path,**info)
            except:
                return False
        return True

    def SetIdentity(self,path,**opts):
        if os.path.exists(path):
            chmod=self.Mode(opts.get('mode',None))
            uid=opts.get('uid',None)
            gid=opts.get('gid',None)
            atime=opts.get('atime',None)
            mtime=opts.get('mtime',None)
            try:
                if chmod: os.chmod(path,int(chmod,base=8))
                if uid and gid: os.chown(path,uid,gid)
                if mtime and atime: os.utime(path,(atime,mtime)) # Time update must be at last order
            except:
                pass

    def Extract(self,*path,**opts):
        dest=opts.get('dest',None)
        root_path=opts.get('root_path',None)
        sub_dir=opts.get('sub_dir',False)
        if IsNone(dest): return False
        if not path:
            self.ExtractRoot(root_path=self.FindRP(),dest=dest,sub_dir=sub_dir)
        else:
            for filepath in path:
                fileRF=self.FindRP(filepath)
                if isinstance(fileRF,tuple):
                    root_path=[fileRF[0]]
                    filename=fileRF[1]
                    self.ExtractRoot(root_path=root_path,dirpath=filename,dest=dest,sub_dir=sub_dir)
                elif isinstance(fileRF,list):
                    self.ExtractRoot(root_path=fileRF,dest=dest,sub_dir=sub_dir)

    def Save(self,filename):
        pv=b'3'
        if PyVer(2): pv=b'2'
        self.Rw(filename,data=pv+Compress(pickle.dumps(self.info,protocol=2),mode='bz2'))

    def Open(self,filename):
        if not os.path.isfile(filename):
            print('{} not found'.format(filename))
            return False
        data=self.Rw(filename)
        if data[0]:
            pv=data[1][0]
            if pv == '3' and PyVer(2):
                print('The data version is not matched. Please use Python3')
                return False
            # decompress data
            try:
                dcdata=Decompress(data[1][1:],mode='bz2')
            except:
                print('This is not KFILE format')
                return False
            try:
                self.info=pickle.loads(dcdata) # Load data
            except:
                try:
                    self.info=pickle.loads(dcdata,encoding='latin1') # Convert 2 to 3 format
                except:
                    print('This is not KFILE format')
                    return False
        else:
            print('Can not read {}'.format(filename))
            return False

class TRY:
    def __init__(self,auto=None,logfile=None,log_all=False,err_screen=False,err_exit=False,default=None,log=None):
        self.auto=auto #True: All auto, None: defaults auto, False: not use
        self.logfile=logfile
        self.log_all=log_all
        self.log=log
        self.err_exit=err_exit
        self.err_screen=True if err_exit else err_screen
        
        self.rc=None #None: not run, False: something error, True: run function
        self.result=default
        self.error=None

    def __repr__(self):
        if self.result:
            return Str(self.result)
        return ''

    def run(self,func,*inps,**opts):
        #if Type(func,'function'):
        if IsFunction(func,builtin=True):
            arg=Args(func)
            if self.log_all:
                printf('Try Function: {}{}\nRecived: {}, {}'.format(func.__name__,FunctionArgs(func,mode='string'),inps,opts),date=True,caller_tree=True,caller_parent='1-5',caller_filename=True,caller_line_number=True,logfile=self.logfile,log=self.log,dsp='f' if self.logfile else 'a')

            ninps=[]
            nopts={}
            if self.auto is not False:
                ninps_n=0
                ninps_o=0
                opts_i=list(opts.items())
                while len(arg.get('args',[])) > ninps_n:
                    if ninps_n < len(inps):
                        ninps.append(inps[ninps_n])
                    elif self.auto is True and ninps_n < len(inps)+len(opts):
                        if opts_i[ninps_o][0] not in arg.get('defaults',{}):
                            ninps.append(opts_i[ninps_o][1])
                            ninps_o+=1
                    else:
                        break
                    ninps_n+=1
                if arg.get('varargs'):
                    ninps=ninps+inps[ninps_n:]
                    ninps_n=len(inps)
                no_inps=False
                if ninps_o > 0 : opts=dict(opts_i[ninps_o:])
                for k in arg.get('defaults',{}):
                    if k in opts:
                        nopts[k]=opts.pop(k)
                        no_inps=True
                    else:
                        # Fill in to inps for default with extra remained inps
                        if not no_inps and ninps_n < len(inps):
                            ninps.append(inps[ninps_n])
                            ninps_n+=1
                        else:
                            nopts[k]=arg.get('defaults').get(k)
                            no_inps=True
                if arg.get('keywords') and opts:
                    nopts.update(opts)
                if self.log_all:
                    printf('New Inputs: {} {}'.format(ninps,nopts),date=True,logfile=self.logfile,log=self.log,dsp='f' if self.logfile else 'a')
            try:
                self.rc=True
                if self.auto is False:
                    self.result=func(*inps,**opts)
                else:
                    if not arg and type(func).__name__ == 'builtin_function_or_method':
                        try:
                            self.result=func(*inps,**opts)
                        except:
                            e=ExceptMessage()
                            self.error=e+'(function name: {})'.format(func.__name__)
                            self.rc=False
                    else:
                        self.result=func(*ninps,**nopts)
                if self.log_all:
                    printf('RC:{}\nResult:{}'.format(self.rc,self.result),date=True,logfile=self.logfile,log=self.log,dsp='f' if self.logfile else 'a')
                return self
            except:
                e=ExceptMessage()
                if self.logfile or self.log:
                    printf(e,date=True,caller_tree=True,caller_parent='1-5',caller_filename=True,caller_line_number=True,logfile=self.logfile,log=self.log,dsp='f')
                if self.err_screen:
                    printf(e,mode='e')
                if self.err_exit:
                    os._exit(1)
                self.rc=False
                self.error=e
                return self
        elif isinstance(func,str):
            self.rc,self.result,self.error=TryCode(func,default=False,_return_=True)
            return self
        self.rc=False
        self.error='Not [support] function'
        if self.log_all:
            printf('RC:{}\nResult:{}\nError:{}'.format(self.rc,self.result,self.error),date=True,logfile=self.logfile,log=self.log,dsp='f' if self.logfile else 'a')
        return self

    def Result(self):
        return self.result

    def Rc(self):
        return self.rc

    def Error(self):
        return self.error

class RETURN:
    '''Temporary try to RETURN value define'''
    def __init__(self,*data,**opts):
        self.rc=opts.get('rc',opts.get('RC',None))
        if len(data) == 1:
            self.data=data[0]
        else:
            self.data=data
        self.info={}
        if opts.get('info',True) is True:
            self.info['time']=TIME().Int()
            if opts.get('function',True) is True:
                self.info['function']=FunctionName(**{'parent':1,'args':True,'line_number':True,'filename':True})
            if opts.get('parent') is True:
                self.info['parent']=FunctionName(**{'parent':2,'line_number':True,'filename':True})
            if 'msg' in opts: self.info['msg']=opts.get('msg')
            if 'network' in opts: self.info['network']=opts.get('network')

    def Get(self,*o,**opts):
        if not o: opts['default']='org'
        return Get(self.data,*o,**opts)

class kThread(Thread):
    '''
    t = kThread(target=foo, args=('world!',)) # define
    t.start() # start
    print(t.get())  # get result
    '''
    def __init__(self, group=None, target=None, name=None,
            args=(), kwargs={}, Verbose=None, default=None):
        if PyVer(3):
            Thread.__init__(self, group, target, name, args, kwargs)
        else:
            Thread.__init__(self, group, target, name, args, kwargs, Verbose)
        self._return = default

    def run(self):
        if PyVer(3):
            if self._target is not None:
                self._return = self._target(*self._args,**self._kwargs)
        else:
            if self._Thread__target is not None:
                self._return = self._Thread__target(*self._Thread__args,
                                                **self._Thread__kwargs)
    def get(self):
        if self._tstate_lock:
            Thread.join(self)
            return self._return
        return None

    def stop(self,retry_num=10):
        def _async_raise(th_id,exe_type):
            th_id=ctypes.c_long(th_id)
            if not inspect.isclass(exe_type):
                exe_type=type(exe_type)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(th_id, ctypes.py_object(exe_type))
            if res == 0:
                #print("Invalid thread id({})".format(th_id))
                return -1
            elif res != 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(th_id, None)
                raise SystemError("ThreadStop failed")
            # stopped thread
            return 0
        for i in range(retry_num):
            exit_id=_async_raise(self.ident, SystemExit)
            if exit_id == 0:
                self._is_stopped=True
                return True # stopped
            elif exit_id == -1: #No thread
                self._is_stopped=True
                return None
        return False # stop Fail

    def isAlive(self):
        #if not self._tstate_lock and not self._is_stopped: return None # Not started
        if not self._tstate_lock and not self._ident: return None # Not started
        if not self._tstate_lock or self._is_stopped: return False #Stopped
        return True #Running

    def Name(self):
        return self._name
    def Args(self):
        return self._args,self._kwargs
    def Id(self):
        if isinstance(self.ident,int):
            return self.ident
        return None # not started
    def PPID(self):
        return os.getpid()

def Progress(symbol='.',**opts):
    start_newline=opts.get('start_newline',False)
    end_newline=opts.get('end_newline',opts.get('newline',True))
    log=opts.get('log',None)
    interval=Int(opts.get('interval'),5)
    timeout=Int(opts.get('timeout'),3600*100)
    mode=opts.get('mode','s')
    stop=opts['stop'] if 'stop' in opts else False
    delay=opts['delay'] if 'delay' in opts else False
    local_printed=False
    if start_newline:
        printf('',ignore_empty=False,caller_parent=1,start_newline='auto',log=log,end='',mode=mode)
    Time=TIME()
    while True:
        if IsTrue(stop) or (timeout > 0 and Time.Out(timeout)): break
        if delay:
            if (isinstance(delay,int) and not  Time.Out(delay)) or not IsTrue(delay): #less delay time then skip progress log
                time.sleep(0.3)
                continue
        printf(symbol,direct=True,log=log,log_level=1,mode=mode)
        local_printed=True
        time.sleep(interval)
    if end_newline and local_printed:
        printf('',ignore_empty=False,caller_parent=1,no_intro=True,log=log,mode=mode)

def GetOptValue(data,key,default=None,data_type=None,default_with_none=False):
    # get key value in a dictionary 
    if isinstance(data,dict):
        if isinstance(key,str): key=[key]
        for k in key: # Check all want keys in the dictionary
            if k in data:
                if default_with_none: # if None data then pass to next check
                    if IsNone(data[k]): continue
                if data_type: # if different type of data then pass to next check
                    if not Type(data[k],data_type): continue
                return data[k]
    return default # not meet then default

def fprintf(src,fmt,fmt_key=0,default=None,err=True,new_line='\n',location=True,cli=False,simple=False):
    '''
    require: copy, re
    #Output : [[{data},line numver,original string],...]
    #{data} : {'parameter':{'type':...,'opt':...,'exist':True/False,'data':...},...}
    #fmt    :   {[:[:]]} ....
    #fmt_key:
    #   : 's key/location number
    #   : type {KEY} instead  in fmt.
    #  re    : fmt string is re's expression string
    #  word  : fmt string is re's expression string and finding unit is word
    #  : NONE => No data, just check that prameter only(exist or not)
    #         : take data of index() starting from KEY (-n,-1,KEY,1,2,...)
    #          0 : whole data (forward then forwared to new line, backward then backward to new line)
    #         FIX: same as . but automatically indexing from KEY(fw:1,2,...,n, bw:-1,-2,...,-n)
    #         IP : check data format to IP
    #         MAC: check data format to MAC
    #         INT: convert data to Int
    #         Float: convert data to Float
    #         BYTES: convert data to Bytes
    #         BOOL: convert data to BOOL
    #         STR: default (String data)
    #   : how many taken data (>=2, default=1)
    #location: True then show line number, False then always 0
    #cli     : True then string convert to standard SHELL's to list, False then space will seperator
    #ex) 
    #   src="~]$ ENV ipmitool -I lanplug -H 192.168.3.100 -U ADMIN -P 'AD M  IN' chassis power status"
    #   fmt="{ENV:FIX} ipmitool -H {IP:IP} -U {User} -P {User}"
    #   fprintf(src,fmt,fmt_key=1,cli=True)
    #   =>  [[{'ENV': {'data': 'ENV', 'idx': -1, 'num': None, 'opt': None, 'type': 'FIX'},
               'IP': {'data': '192.168.3.100',
                      'exist': True,
                      'idx': None,
                      'num': None,
                      'opt': '-H',
                      'type': 'IP'},
               'Passwd': {'data': 'AD M  IN',
                          'exist': True,
                          'idx': None,
                          'num': None,
                          'opt': '-P',
                          'type': 'STR'},
               'User': {'data': 'ADMIN',
                        'exist': True,
                        'idx': None,
                        'num': None,
                        'opt': '-U',
                        'type': 'STR'}},
            0,
            "~]$ ENV ipmitool -I lanplug -H 192.168.3.100 -U ADMIN -P 'AD M  IN' chassis "
            'power status']]
    '''
    def finding(ll,fmt_v,backward=False,cli=False):
        src_i=ll.index(fmt_v['E']['key']['string'])
        src_len=fmt_v['E']['key']['length']
        if backward:
            if cli:
                new_src_a=Str2Args(ll[:src_i])
            else:
                new_src_a=ll[:src_i].split()
            keys=fmt_v['E']['bw']
        else:
            if cli:
                new_src_a=[ll[src_i:src_i+src_len]]+Str2Args(ll[src_i+src_len:])
            else:
                new_src_a=[ll[src_i:src_i+src_len]]+ll[src_i+src_len:].split()
            keys=fmt_v['E']['fw']
        rt={}
        for ii in keys:
            rt[ii]=fmt_v['V'][ii]
            opt_idx=fmt_v['V'][ii].get('idx') # if fixed location number
            starts=fmt_v['V'][ii].get('starts')
            ends=fmt_v['V'][ii].get('ends') 
            if isinstance(opt_idx,int): # find fixed location data
                if opt_idx == 0:
                    if backward:
                        data=piller(' '.join(new_src_a[:-1]))
                    else:
                        data=piller(' '.join(new_src_a[1:]))
                    if starts and ends:
                        if data.startswith(starts) and data.endswith(ends):
                            rt[ii]['data']=data[len(starts):len(ends)]
                    elif starts:
                        if data.startswith(starts): rt[ii]['data']=data[len(starts):]
                    elif ends:
                        if data.endswith(ends): rt[ii]['data']=data[:-len(ends)]
                    else:
                        rt[ii]['data']=data
                elif (opt_idx > 0 and len(new_src_a) > opt_idx) or (opt_idx < 0 and len(new_src_a) >= abs(opt_idx)):
                    data=piller(new_src_a[opt_idx])
                    if starts and ends:
                        if data.startswith(starts) and data.endswith(ends):
                            rt[ii]['data']=data[len(starts):len(ends)]
                    elif starts:
                        if data.startswith(starts): rt[ii]['data']=data[len(starts):]
                    elif ends:
                        if data.endswith(ends): rt[ii]['data']=data[:-len(ends)]
                    else:
                        rt[ii]['data']=data
            else:
                # find by option character
                opt_g=rt[ii].get('opt')
                if opt_g not in new_src_a: continue
                rt[ii]['exist']=True
                opt_t=rt[ii].get('type','STR')
                #if opt_t in ['NONE','None',None]: continue
                if IsNone(opt_t,chk_val=['NONE','None',None,'']): continue
                opt_i=new_src_a.index(opt_g)
                opt_n=rt[ii].get('num')
                if opt_n is None: opt_n=0
                if len(new_src_a) > opt_i+opt_n+1:
                    if opt_n:
                        found_data=piller(' '.join(new_src_a[opt_i+1:opt_i+opt_n+1]))
                    else:
                        found_data=piller(new_src_a[opt_i+1])
                    if starts and ends:
                        if found_data.startswith(starts) and found_data.endswith(ends):
                            found_data=found_data[len(starts):len(ends)]
                    elif starts:
                        if found_data.startswith(starts): found_data=found_data[len(starts):]
                    elif ends:
                        if found_data.endswith(ends): found_data=found_data[:-len(ends)]
                    if IsIn(opt_t,['ip','ipaddress']):
                        if IpV4(found_data):
                            rt[ii]['data']=found_data
                    elif IsIn(opt_t,['mac','macaddress']):
                        if MacV4(found_data):
                            rt[ii]['data']=found_data
                    elif IsIn(opt_t,[bytes,'byte','bytes']):
                        try:
                            rt[ii]['data']=bytes(found_data)
                        except:
                            if err:
                                rt[ii]['data']=default
                            else:
                                rt[ii]['data']=found_data
                    elif IsIn(opt_t,[bool,'bool']):
                        try:
                            rt[ii]['data']=bool(found_data)
                        except:
                            if err:
                                rt[ii]['data']=default
                            else:
                                rt[ii]['data']=found_data
                    elif IsIn(opt_t,[int,'int','integer']):
                        try:
                            rt[ii]['data']=int(found_data)
                        except:
                            if err:
                                rt[ii]['data']=default
                            else:
                                rt[ii]['data']=found_data
                    elif IsIn(opt_t,[float,'float']):
                        try:
                            rt[ii]['data']=int(found_data)
                        except:
                            if err:
                                rt[ii]['data']=default
                            else:
                                rt[ii]['data']=found_data
                    else:
                        rt[ii]['data']=found_data
                else:
                    rt[ii]['data']=default
        return copy.deepcopy(rt)
    if not isinstance(src,str): return default
    src_l_a=src.split(new_line)
    # re Search
    if fmt_key == 're':
        rt=[]
        fmt=fmt.replace('*','.+').replace('?','.')
        find_form=re.compile(fmt,flags=re.IGNORECASE)
        for src_ln in range(0,len(src_l_a)):
            # Search line by line for key
            if isinstance(src_l_a[src_ln],str):
                aa=find_form.findall(src_l_a[src_ln])
                if aa:
                    rt.append([aa,src_ln,src_l_a[src_ln]])
        return rt
    elif fmt_key == 'word':
        rt=[]
        fmt=fmt.replace('*','.+').replace('?','.')
        find_form=re.compile(r'\b({0})\b'.format(fmt),flags=re.IGNORECASE)
        for src_ln in range(0,len(src_l_a)):
            # Search line by line for key
            if isinstance(src_l_a[src_ln],str):
                aa=find_form.findall(src_l_a[src_ln])
                if aa:
                    rt.append([aa,src_ln,src_l_a[src_ln]])
        return rt
    elif isinstance(fmt,set):
        for src_ln in range(0,len(src_l_a)):
            src_a=src_l_a[src_ln].split()
            for ii in src_a:
                found_data=piller(ii)
                if fmt == {'IP'}:
                    if IpV4(found_data):
                        rt.append([found_data,src_ln,src_l_a[src_ln]])
                elif fmt == {'MAC'}:
                    if MacV4(found_data):
                        rt.append([found_data,src_ln,src_l_a[src_ln]])
        return rt
    
    # CLI Search
    new_src=None
    # make fmt_v
    fmt_v={'E':{},'V':{}}
    fmt_a=fmt.split()
    if isinstance(fmt_key,str):
        found_key=re.search(fmt_key,src)
        if found_key is None: return [] #not found
        loc=found_key.span()
        #fmt_v['E']['key']={'string':found_key.group(),'str_idx':loc[0],'length':(loc[1]-loc[0])}
        fmt_v['E']['key']={'string':fmt_key,'str_idx':loc[0],'length':(loc[1]-loc[0])}
        if '{KEY}' in fmt_a:
            fmt_key=fmt_a.index('{KEY}')
        else:
            print('missing {KEY} in fmt')
            return False
    elif isinstance(fmt_key,int):
        if len(fmt_a) <= fmt_key: 
            print('out of fmt_key in fmt')
            return False
        if fmt_a[fmt_key] not in src: return [] # Not found
        loc=src.index(fmt_a[fmt_key])
        fmt_v['E']['key']={'string':fmt_a[fmt_key],'str_idx':loc,'length':len(fmt_a[fmt_key])}
    fmt_v['E']['bw']=[]
    fmt_v['E']['fw']=[]
    for ii in range(0,len(fmt_a)):
        if fmt_key == ii: continue
        if fmt_a[ii] == '{KEY}':
            fmt_key=ii
            continue
        fmt_p=piller(fmt_a[ii])
        bsc=fmt_p.count('{')
        bec=fmt_p.count('}')
        if bsc > 0 and bsc == bec:
            ps=fmt_p.index('{')
            pe=fmt_p.index('}')
            ps_r=None
            pe_r=None
            if ps > 0: ps_r=fmt_p[:ps]
            if len(fmt_p) > pe+1: pe_r=fmt_p[pe+1:]
            var=fmt_p[ps+1:pe].split(':')
            if var[0] in fmt_v['V']:
                return False,'Duplicated variable name({})'.format(var[0])
            idx=None
            num=None
            opt=None
            _type='STR'
            len_var=len(var)
            if ii < fmt_key:
                fmt_v['E']['bw'].append(var[0])
            else:
                fmt_v['E']['fw'].append(var[0])
            if len_var > 2: #take number of data
                if var[2]:
                    try:
                        num=int(var[2])
                        if num < 2: num=None
                    except:
                        print('{} has wrong define. it should be int at  in ::'.format(var[0]))
                        continue
            if len_var > 1: #Data Type
                _type=var[1]
                if isinstance(_type,str):
                    try:
                        _type=int(_type)
                        if _type == 0:
                            idx=0
                        elif _type > 0:
                            idx=_type-fmt_key
                        elif _type < 0:
                            idx=_type+1-fmt_key
                        _type='FIX'
                    except:
                        if _type == 'FIX':
                            idx=ii-fmt_key
                        elif not _type:
                            _type='STR'
                # Set OPT
            if _type != 'FIX': opt=fmt_a[ii-1]
            # Make Variable
            fmt_v['V'][var[0]]={'type':_type,'opt':opt,'num':num,'idx':idx,'starts':ps_r,'ends':pe_r,'form':fmt_a[ii]}
    # Location data
    if not location:
        if new_line:
            new_src=''
            if fmt_v['E']['bw']:
                new_src=src[:fmt_v['E']['key']['str_idx']].split(new_line)[-1]
            if fmt_v['E']['fw']:
                new_src=new_src+src[fmt_v['E']['key']['str_idx']:].split(new_line)[0]
            src=new_src
        else:
            if fmt_v['E']['bw'] and not fmt_v['E']['fw']:
                src=src[:fmt_v['E']['key']['str_idx']]
            elif not fmt_v['E']['bw'] and fmt_v['E']['fw']:
                src=src[fmt_v['E']['key']['str_idx']:]
            #else: all string
        
    if not new_line:
        src_l=[src]
    else:
        src_l=src.split(new_line)
    # Find data
    rt=[]
    for src_ln in range(0,len(src_l)):
        fv={}
        # Search line by line for key
        if fmt_v['E']['key']['string'] not in src_l[src_ln]: continue
        if fmt_key >= 0:
            aa=finding(src_l[src_ln],fmt_v,cli=cli)
            if aa: fv.update(aa)
        if fmt_key > 0:
            aa=finding(src_l[src_ln],fmt_v,backward=True,cli=cli)
            if aa: fv.update(aa)
        if fv: rt.append([fv,src_ln,src_l[src_ln]])
    if simple and rt:
        nrt={}
        for ii in rt[0][0]:
            if rt[0][0][ii].get('data'):
                nrt[ii]=rt[0][0][ii].get('data')
            else:
                nrt[ii]=rt[0][0][ii].get('exist')
        return nrt
    return rt

def piller(data,mode='cli',pill_list={'python':["'''",'"""','"',"'"],'cli':['"',"'"],'bracket':['{','[']}):
    if mode in ['cli','shell','list','console']: mode='cli'
    for ii in pill_list.get(mode,[]):
        if isinstance(data,str) and len(data) > len(ii) * 2:
            if mode == 'bracket':
                if data[:1] == ii:
                    if ii == '{' and data[-1:] == '}':
                        return data[1:-1]
                    elif ii == '[' and data[-1:] == ']':
                        return data[1:-1]
                    elif ii == '(' and data[-1:] == ')':
                        return data[1:-1]
                    elif ii == '<' and data[-1:] == '>':
                        return data[1:-1]
            else:
                if data[:len(ii)] == ii and data[-len(ii):] == ii:
                    return data[len(ii):-len(ii)]
    return data


def Str2Args(data,breaking='-'):
    '''Convert String to Standard SHELL/CLI/SYS Args data(list)'''
    def inside_data(rt,breaking,data_a,ii,symbol):
        tt=data_a[ii][1:]
        if len(data_a) > ii:
            for jj in range(ii+1,len(data_a)):
                if data_a[jj] and data_a[jj].startswith(breaking):
                    for tt in range(ii,jj+1):
                        rt.append(data_a[tt])
                    return jj
                if (data_a[jj] and data_a[jj][0] != symbol and data_a[jj][-1] == symbol) or (data_a[jj] and data_a[jj][0] == symbol):
                    tt=tt+""" {}""".format(data_a[jj][:-1])
                    rt.append(tt)
                    tt=''
                    return jj
                else:
                    tt=tt+""" {}""".format(data_a[jj])
        return None
 
 
    data_a=data.split(' ')
    rt=[]
    ii=0
    while ii < len(data_a):
        if not data_a[ii]:
            ii+=1
            continue
        if data_a[ii][0] == '"' and data_a[ii][-1] == '"':
            rt.append(data_a[ii][1:-1])
        elif data_a[ii][0] == "'" and data_a[ii][-1] == "'":
            rt.append(data_a[ii][1:-1])
        elif data_a[ii][0] == "'" and data[ii][-1] != "'":
            a=inside_data(rt,breaking,data_a,ii,"'")
            if isinstance(a,int): ii=a
        elif data_a[ii][0] == '"' and data[ii][-1] != '"':
            a=inside_data(rt,breaking,data_a,ii,'"')
            if isinstance(a,int): ii=a
        else:
            rt.append(data_a[ii])
        ii+=1
    return rt

def IsFloat(a):
    try:
        float(a)
        return True
    except:
        return False

def IsBool(a):
    try:
        if isinstance(a,str): a=eval(a)
        if isinstance(a,bool) and not isinstance(a,int):
            return True
    except:
         pass
    return False


def scanf(string,fmt,**opts):
    '''
    a=scanf('<any string>',<format of finding value>,<options>)
    <format of finding value> : {<parameter name>} or {<parameter name>:<format>}
      - format : IP, MAC, INT, Float, BOOL, STR(default)
    scanf("ipmitool -H 192.168.1.3 -U ADMIN -P 'ADMIN 123' chassis power status","ipmitool -H {ip:ip} -U {user} -P {passwd} chassis")
    => {'ip': '192.168.1.3', 'user': 'ADMIN', 'passwd': 'ADMIN 123'}
    '''
    err=opts.get('err',opts.get('error',False))
    new_line=opts.get('newline',opts.get('new_line'))
    # Exact same format
    if opts.get('fix',opts.get('fixed',opts.get('fixed_form',opts.get('same',opts.get('exact_same',opts.get('sameform',opts.get('space',opts.get('whitespace',opts.get('white_space',False))))))))) is True:
        regex = re.sub(r'{(.+?)}', r'(?P<_\1>.+)', fmt)
        found=re.search(regex, string)
        if found:
            values = list(found.groups())
            keys = re.findall(r'{(.+?)}', fmt)
            _dict = dict(zip(keys, values))
            return _dict
        return {}
    #Similar format
    fmt_d=[]
    fmt_a=fmt.split()
    for i,f in enumerate(fmt_a):
        if f and f[0] == '{' and f[-1] == '}':
            f_a=f[1:-1].split(':')
            if len(f_a) == 2:
                fmt_d.append({'id':i,'name':f_a[0],'type':'parameter','form':f_a[1]})
            else:
                fmt_d.append({'id':i,'name':f[1:-1],'type':'parameter'})
        else:
            fmt_d.append({'id':i,'name':f,'type':'string'})
    def find_in_line(line_string,fmt_d):
        out={}
        foundstarts=0
        nextfoundstarts=0
            
        for s in Str2Args(line_string):
            if foundstarts >= len(fmt_d): break
            if fmt_d[foundstarts].get('type') == 'string':
                if s == fmt_d[foundstarts].get('name'):
                    foundstarts+=1
                else:
                    foundstarts=nextfoundstarts
                continue
            elif fmt_d[foundstarts].get('type') == 'parameter':
                if fmt_d[foundstarts].get('form','_N.A_') != '_N.A_':
                    if IsIn(fmt_d[foundstarts].get('form'),['ip','ipaddress']):
                        if IpV4(s):
                            nextfoundstarts=foundstarts
                            out[fmt_d[foundstarts].get('name')]=s
                            foundstarts+=1
                    elif IsIn(fmt_d[foundstarts].get('form'),['mac','macaddress']):
                        if MacV4(s):
                            nextfoundstarts=foundstarts
                            out[fmt_d[foundstarts].get('name')]=s
                            foundstarts+=1
                    elif IsIn(fmt_d[foundstarts].get('form'),[int,'int','integer']):
                        if IsInt(s):
                            nextfoundstarts=foundstarts
                            out[fmt_d[foundstarts].get('name')]=eval(s)
                            foundstarts+=1
                    elif IsIn(fmt_d[foundstarts].get('form'),[float,'float']):
                        if IsInt(s) or IsFloat(s):
                            nextfoundstarts=foundstarts
                            out[fmt_d[foundstarts].get('name')]=eval(s)
                            foundstarts+=1
                    elif IsIn(fmt_d[foundstarts].get('form'),[bool,'bool']):
                        if IsBool(s):
                            nextfoundstarts=foundstarts
                            out[fmt_d[foundstarts].get('name')]=eval(s)
                            foundstarts+=1
                else:
                    nextfoundstarts=foundstarts
                    out[fmt_d[foundstarts].get('name')]=s
                    foundstarts+=1
        return out
    if new_line:
        for ll in string.split(new_line):
            out=find_in_line(ll,fmt_d)
            if out: return out
    elif isinstance(string,str):
        string.replace('\n',' ')
        return find_in_line(string.replace('\n',' '),fmt_d)
    return {}

class kRT:
    __name__='kRT'
    def __init__(self,*args,_history_='1-5',_merge_=False,**kwargs):
        # default : dictionary, optional : tuple
        # _merge_ : merge between input kRT data's kwargs and my kwargs
        #  True   : merge mine to old data (mine is new)
        #  False  : None (only keep mine)
        # X_merge_ : merge between kwargs's args and *args when kwargs has args parameter
        # X True : merge kwargs's args to args
        # X False: error
        # X None : keep kwargs's args
        if isinstance(_history_,str):
            history_a=_history_.split('-')
            if len(history_a) == 2:
                if not history_a[0]:
                    history_a[0]=['1']
            else:
                history_a=['1','5']
            historyrange='-'.join(history_a)
        else:
            historyrange='1-5'
        self.__info__={'history':FunctionName(parent=historyrange,history=True,tree=True,line_number=True,filename=True,args=True),'parent':None,'time':TIME().Int()}
        if 'args' in kwargs:
            if arg:
                raise IndexError('duplicated args parameter')
            else:
                if isinstance(kwargs['args'],list):
                    self.arg=tuple(kwargs['args'])
                elif not isinstance(kwargs['args'],tuple):
                    self.arg=tuple([kwargs['args']])
                else:
                    self.arg=kwargs['args']
            #if _merge_:
            #    if isinstance(kwargs['args'],tuple):
            #        self.args=args+kwargs['args']
            #    elif isinstance(kwargs['args'],list):
            #        self.args=args+tuple(kwargs['args'])
            #    else:
            #        self.args=args+tuple([kwargs['args']])
            #elif _merge_ is False:
            #    raise IndexError('duplicated args parameter')
            #else: #merge is None
            #    if isinstance(kwargs['args'],tuple):
            #        self.args=kwargs['args']
            #    elif isinstance(kwargs['args'],list):
            #        self.args=tuple(kwargs['args'])
            #    else:
            #        self.args=tuple([kwargs['args']])
        else:
            self.arg=args
        if 'parent' in kwargs:
            if type(kwargs['parent']) == type(self):
                self.__info__['parent']=kwargs.pop('parent')
        if not self.__info__['parent'] and self.arg: 
            for i in self.arg:
                if type(i) == type(self):
                    # if following old kRT data then just update history for checking following history
                    self.__info__['parent']=i
                    ##remove old return value? or keep it in args ?
                    #if _merge_:
                    #    #merge old input kRT's kwargs value to my kwargs when not exist data in mine for reference
                    #    # mine data must be mine data
                    #    _a_=self.arg[0].get(mode=dict)
                    #    for i in _a_:
                    #        if i not in kwargs:
                    #            kwargs[i]=_a_[i]
        if 'rc' in kwargs:
            self.rc=kwargs['rc']
        elif self.arg: #
            if type(self.arg[0]) == type(self): # ignore return code for my self OBJ
                if len(self.arg) > 1:
                    self.rc=self.arg[1]
                else:
                    self.rc=None
            else:
                self.rc=self.arg[0]
        else:
            self.rc=None
        for key, value in kwargs.items():
            setattr(self,key,value)

    #def __setattr__(self,key,value):
    #    # Not support this function when __init__ has *args
    #    #Handle dot notation access
    #    # Put data: obj.key=value
    #    if key == 'kwargs':
    #        super().__setattr__(name,value)
    #    else:
    #        self.kwargs[key]=value

    def __setitem__(self,key,value):
        #for obj[key]=value
        if isinstance(key,int): 
            if len(self.arg) > abs(key): # replace
                self.arg=list(self.arg)
                self.arg[key]=value
                self.arg=tuple(self.arg)
            elif key < 0: # insert at first
                self.arg=tuple([value])+self.arg
            else: #key > 0
                self.arg=self.arg+tuple([value]) # append
        else: # update/add self dict
            setattr(self,key,value)

    def __getitem__(self,key):
        #Get data : obj[key]
        if isinstance(key,int):
            if len(self.arg) > abs(key):
                return self.arg[key]
            else:
                raise IndexError('Out of index')
        else:
            if key != '__info__' and key in self.__dict__:
                return self.__dict__[key]
            elif key == '__history__':
                return self.__info__['history']
            elif key == '__parent__':
                return self.__info__['parent']
            elif key == '__time__':
                return self.__info__['time']
            elif key in ['__full__','__dict__']:
                return self.__dict__
            elif key == '__list__':
                return self.arg
            raise IndexError('Not found the key({})'.format(key))

    def __getattr__(self,key):
        #Handle dot notation access
        # Get data: obj.key (can not put int at key (obj.2)
        #if isinstance(key,int):
        #    if len(self.arg) > abs(key):
        #        return self.arg[key]
        #    else:
        #        raise IndexError('Out of index')
        #elif key in self.__dict__:
        if key != '__info__' and key in self.__dict__:
            return self.__dict__[key]
        elif key == '__history__':
            return self.__info__['history']
        elif key == '__parent__':
            return self.__info__['parent']
        elif key == '__time__':
            return self.__info__['time']
        elif key == '__full__':
            return self.__dict__
        elif key == '__list__':
            return self.arg
        else:
            raise IndexError(f'Not found the key({key})')

    def __bool__(self):
        # for if command
        # if 0 then False, if # then True, if others then True, if bool then return bool
        if isinstance(self.rc,bool):
            return self.rc
        elif isinstance(self.rc,int):
            return False if self.rc == 0 else True
        elif self.rc:
            return True
        return False

    def __str__(self):
        # in print(), str()
        return str(self.rc)

    def __int__(self):
        # in int()
        try:
            return int(self.rc)
        except:
            raise ValueError(f"{self.rc} is not numberable")

    def __delitem__(self,key):
        if isinstance(key,int):
            if len(self.arg) > abs(key):
                del self.arg[key]
            else:
                raise IndexError('Out of index')
        elif key in self.get():
            del self.__dict__[key]
        else:
            raise KeyError(f"Key {key} not found")

    def __contain__(self,key):
        #key is in the data ( 3 in data )
        #return key in self.get()
        if key in self.__dict__:
            return True
        elif key in self.arg:
            return True
        return False

    def __len__(self):
        # in len()
        return len(self.get())

    def __iter__(self):
        # in iter()
        return iter(self.get())

    def __eq__(self,other):
        # for a == b
        if isinstance(other,kRT):
            return self.rc==other.rc
        return self.rc==other

    def __add__(self,other):
        # for a + b
        if isinstance(other,kRT): other=other.rc
        if isinstance(self.rc,int) and isinstance(other,int):
            return self.rc+other

    def __sub__(self,other):
        # for a - b
        if isinstance(other,kRT): other=other.rc
        if isinstance(self.rc,int) and isinstance(other,int):
            return self.rc-other

    def get(self,key=None,default=None,mode='arg-dict',err=False,parent=None):
        # Get data: obj.get(key)
        def arg_data(a,key,err=False):
            if isinstance(key,int):
                if len(a.arg) > abs(key):
                    return a.arg[key]
                else:
                    if err:
                        raise KeyError(f"Key {key} out of range")
                    else:
                        if key < 0:
                            return a.arg[0]
                        else:
                            return a.arg[-1]
            if key is None: return a.arg
        # if being parent
        if isinstance(parent,int) and parent > 0 and self.__info__['parent']:
            a=self.__info__['parent']
            for i in range(1,parent):
                a=a.__info_['parent']
                if not a.__info__['parent']: break
        else:
            a=self

        if mode is list:
            return arg_data(a,key,err=err)
        elif isinstance(mode,str):
            mode_a=mode.lower().split('-')
            if mode_a[0] in ['list','args','arg','opt','opts']:
                _tmp_=arg_data(a,key,err=err)
                if len(mode_a) == 1:
                    return _tmp_
                elif _tmp_: #if multi (arg-dict) and no data of arg then get dict
                    return _tmp_
        if key in ['__history__']:
            return '\n'.join(a.__info__['history'])
        elif key in ['__time__']:
            return a.__info__['time']
        elif key in ['__parent__']:
            return a.__info__['parent']
        elif key in ['__full__','__dict__']: 
            return a.__dict__
        elif key in ['rc','RC','Rc']:
            return a.rc
        elif key:
            return a.__dict__.get(key,default)
        else:
            return {key:value for key, value in a.__dict__.items() if key not in ['__info__']}

    def put(self,key,value,mode=dict,err=False,**opts):
        if mode is list or (isinstance(mode,str) and mode.lower() in ['list','args','arg','opt','opts']):
            if isinstance(key,int):
                add=opts.get('add',opts.get('append',False))
                if add:
                    if key == -1:
                        self.arg=self.arg+tuple([value])
                    elif len(self.arg) > abs(key):
                        self.arg=self.arg[:key]+tuple([value])+self.arg[key:]
                    else:
                        if err:
                            raise KeyError(f"Key {key} out of range")
                        else:
                            if key < 0:
                                self.arg=tuple([value])+self.arg
                            else:
                                self.arg=self.arg+tuple([value])
                else:
                    if len(self.arg) > abs(key):
                        self.arg=list(self.arg)
                        self.arg[key]=value
                        self.arg=tuple(self.arg)
                    else:
                        if err:
                            raise KeyError(f"Key {key} out of range")
                        else:
                            if key < 0:
                                self.arg=list(self.arg)
                                self.arg[0]=value
                                self.arg=tuple(self.arg)
                            else:
                                self.arg=list(self.arg)
                                self.arg[-1]=value
                                self.arg=tuple(self.arg)
        if key in ['rc','RC','Rc']:
            self.rc=value
        else:
            self.__dict__[key]=value

    #Dict case
    def items(self):
        return self.get().items()

    def keys(self):
        return self.get().keys()

    def values(self):
        return self.get().values()

    def args(self):
        return self.get(mode=list)

    def opts(self):
        return self.get()

    def code(self):
        return self.rc

    def status(self):
        return self.rc

class kCursor:
    def __init__(self,log=None,log_level=0):
        self.log=log
        self.log_level=log_level

    def MoveLeft(self,cnt=0):
        #sys.stdout.write(f'\033[{cnt}D')
        printf(f'\033[{cnt}D',direct=True,log=self.log,log_level=self.log_level)

    def MoveFirst(self):
        #sys.stdout.write('\r')
        printf('\r',direct=True,log=self.log,log_level=self.log_level)

    def MoveHome(self):
        #sys.stdout.write('\033[H')
        printf('\033[H',direct=True,log=self.log,log_level=self.log_level)

    def MoveStart(self):
        #sys.stdout.write('\033[0G')
        printf('\033[0G',direct=True,log=self.log,log_level=self.log_level)

    def DelLeft(self,cnt=0):
        for _ in range(cnt):
            #sys.stdout.write('\033[1D \033[1D')
            printf('\033[1D \033[1D',direct=True,log=self.log,log_level=self.log_level)

    def DelLineAfter(self):
        #sys.stdout.write("\033[K")
        printf('\033[K',direct=True,log=self.log,log_level=self.log_level)

    def DelCurrentLine(self):
        self.MoveStart()
        self.DelLineAfter()

def Bracket(msg,bracket=None):
    if bracket:
        if isinstance(bracket,str) and len(bracket) == 2:
            return f'{bracket[0]}{msg}{bracket[1]}'
    return msg

class kProgress:
    def __init__(self,msg=None,bracket=None,rotates=['|','/','-','\\'],log=None,log_level=0):
        self.rotates=rotates
        self.rotate_num=len(self.rotates)
        self.rr=0 #Rotate number
        self.msg=msg
        self.old_len=0
        self.bracket=bracket
        self.stop=False
        self.log=log
        self.log_level=log_level

    def Ing(self,symbol='.',loop=False,interval=1):
        if loop:
            while True:
                printf(symbol,direct=True,log=self.log,log_level=self.log_level)
                time.sleep(interval)
        else:
            printf(symbol,direct=True,log=self.log,log_level=self.log_level)
#        sys.stdout.write(symbol)
#        sys.stdout.flush()

    def Percent(self,percent,msg=None):
        if not msg: msg=self.msg
        if msg:
            kCursor().DelCurrentLine()
            msg = f'{msg} : {Bracket("%3.2f%%"%(percent),self.bracket)}'
            printf(msg,direct=True,log=self.log,log_level=self.log_level)
            #sys.stdout.write(msg)
            #sys.stdout.flush()
        else:
            kCursor().DelLeft(self.old_len)
            msg=f'{Bracket("%3.2f%%"%(percent),self.bracket)}'
            printf(msg,direct=True,log=self.log,log_level=self.log_level)
            #sys.stdout.write(msg)
            #sys.stdout.flush()
            self.old_len=len(msg)

    def Rotate(self,msg=None,loop=False,interval=1):
        if not msg: msg=self.msg
        if msg:
            kCursor().DelCurrentLine()
            msg = f'{msg} : {Bracket(self.rotates[self.rr%self.rotate_num],self.bracket)}'
            printf(msg,direct=True,log=self.log,log_level=self.log_level)
            #sys.stdout.write(msg)
            #sys.stdout.flush()
            self.rr+=1
        else:
            if loop:
                while True:
                    kCursor().DelLeft(self.old_len)
                    msg=f'{Bracket(self.rotates[self.rr%self.rotate_num],self.bracket)}'
                    printf(msg,direct=True,log=self.log,log_level=self.log_level)
                    self.old_len=len(msg)
                    self.rr+=1
                    time.sleep(interval)
            else:
                kCursor().DelLeft(self.old_len)
                msg=f'{Bracket(self.rotates[self.rr%self.rotate_num],self.bracket)}'
                printf(msg,direct=True,log=self.log,log_level=self.log_level)
                #sys.stdout.write(msg)
                #sys.stdout.flush()
                self.old_len=len(msg)
                self.rr+=1

    def Threads(self,mode='ing',symbol='.',interval=1):
        if mode=='rotate':
            t=kThread(target=self.Rotate,args=(None,True,interval,))
        else:
            t=kThread(target=self.Ing,args=(symbol,True,interval,))
        t.start()
        return t
#        self.stop=False
#        ppth=Thread(target=self.Ing,args=(lambda:self.stop,))
#        ppth.start()
#        return self


#if __name__ == "__main__":
#    # Integer
#    print("Get(12345):",Get(12345))
#    print("Get(12345,1):",Get(12345,1))

Open Kage's useful tools and class to public.
(Long time used and upgraded)
But, this is develope version.
So, suddenly it will be big change when I got some more good idea.
make to seperate to Import from kmisc

# Install
```javascript
pip3 install kmport
```

# Functions

## Global()
    Method's global variables

## StdOut(msg)
    Standard Output Print without new line symbol

## def StdErr(msg)
    Standard Error Print without new line symbol

## PyVer(main=None,miner=None,msym=None)
    python version check
    ```
    ex)
    if PyVer(3): # If Python version 3 then ...
       ~~~
    ```

## find_executable(executable,path=None)
    Find Excuatable command location
    ```
    ex)
    if find_executable('ping'): # if ping command is in the system
       ~~~
    
    ping_path=find_executable('ping') # Get ping command full path
    ```

## ByteName(src)
    Get Byte type name

## Bytes(src,**opts)
    Convert data to bytes data

## Str(src,**opts)
    Convert data to String data

## Int(i,default='org',sym=None,err=False):
    Convert data to Int data when possible. if not then return default (original data)
    support data type: int,float,digit number,list,tuple
    default: (default org)
        org : fail then return or keeping the input data
        True,False,None: fail then return default value in single data or ignore the item in list
    sym     : split symbol when input is string
    err     : 
        False: replace data for possible positions
        True : if convert error in list/tuple then return default

## Join(*inps,symbol='_-_',byte=None,ignore_data=(),append_front='',append_end='')
    Similar as join function.
    ```
    ex)
    Join(['a','b','c'],' ') same as ' '.join(['a','b','c'])

    Join(['a','b','c'],'\n',append_front='  ') 
    Output:
    a
      b
      c

    Join(['a','b','c'],'\n',append_end='  ') 
    Output:
    a<newline>
    b   <newline>
    c   <newline>

    Join(['a','b','c'],'\n',append_front='  ',ignore_data=['b']) # Ignore 'b' data
    Output:
    a
      c
    ```

## FixIndex(src,idx,default=False,err=False):
    Find Index number in the list,tuple,str,dict
    default   : if wrong or error then return default
    err : default False
        False: fixing index to correcting index without error
        True: if wrong index then return default value

## Next(src,step=0,out=None,default='org')
    Get Next data or first key of the dict 
    ```
    ex) get send data in the list
    Next([1,2,3,4],step=1)
    Output:
    2

    ex) get dictionary key
    Next({'a':1})
    Output:
    a

    Next({'a':1,'b':2},step=2)
    Output:
    b
    ```

## Copy(src)
    Copy data
    ```
    a={'a':1,'b':2}
    b=Copy(a)
    ```

## TypeName(obj)
    Get input's Type,Instance's name
    ```
    TypeName(1)     # int
    TypeName('1')   # str
    TypeName(int)   # int
    TypeName('int') # int
    TypeName(str)   # str
    TypeName('str') # str

    def abc(): pass
    TypeName(abc)   # function

    class cc:
        def AA(): pass
    TypeName(cc)    # classobj

    import os
    TypeName(os)    # module

    ...
    ```

## Type(*inps,**opts): 
    Similar as isinstance(A,())
    support : basic type and ('byte','bytes'),('obj','object'),('func','unboundmethod','function'),('classobj','class'),'generator','method','long',....

## FIND(src).Find(find,src='_#_',sym='\n',default=[],out=None,findall=True,word=False,mode='value',prs=None,line_num=False,peel=None,idx=None)
    Searching regular expression form data and return the data

## Found(data,find,digitstring=False,word=False,white_space=True,sense=True,location=False):
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

## IsSame(src,dest,sense=False,order=False,Type=False,digitstring=True,white_space=False,**opts):
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

## IsIn(find,dest,idx=False,default=False,sense=False,startswith=True,endswith=True,Type=False,digitstring=True,word=True,white_space=False,order=False)
    Check key or value in the dict, list or tuple then True, not then False
    <find> can use IsSame's <dest> rule
    ```
    IsIn('abc',['AC','abc','uuu']): True ('abc' in the list['AC','abc','uuu'])
    IsIn('a*c',['AC','abc','uuu']): True ('a*c' in the list['AC','abc','uuu'])
    ```

## WhiteStrip(src,mode=True):
    remove multi space to single space, remove first and end space
    others return original

## IsNone(src,**opts):
    Check the SRC is similar None type data('',None) or not
    -check_type=<type> : include above and if different type then the return True
    -list_none :
      - False: check index item in the source (default)
      - True : check all list of source
    -index   : if source is list then just want check index item
    -space   :
      - True : aprove space to data in source
      - False: ignore space data in source
   ```
   IsNone('')   : True
   IsNone(None) : True
   IsNone([])   : True
   IsNone({})   : True
   IsNone(0)    : False
   IsNone(False): False
   ```

## IsVar(src,obj=None,default=False,mode='all',parent=0)
    Check the input(src) is Variable name or not (in OBJ or in my function)
    ```
    g=9
    def abc(c=5):
       b=3
       IsVar('b') : True
       IsVar('c') : True
       IsVar('g') : True
       IsVar('m') : False

    class AA:
        def __init__(self):
            self.abc=1111
    IsVar('abc',AA()) : True ('abc' is a variable in the AA class)
    ```

## IsFunction(src,find='_#_')
    Check the find is a Function in the src object(module,class)
    ```
    def abc(): pass
    IsFunction('abc')             : False ('abc' is not a function)
    IsFunction(abc)               : True (abc is a function)
    IsFunction(MyModule(),'abc')  : True ('abc' is a function in my module)
    IsFunction(MyModule(),abc)    : True (abc is a function in my module)
    IsFunction(MyModule(),'abcd') : False (not found 'abcd' in my module)
    ```

## IsBytes(src)
    Check data is Bytes or not

## IsInt(src,mode='all'):
    Check data is Int or not
    - mode : int => check only int
             str => int type string only
             all => Int and int type string

## Dict(*inp,**opt):
    Dictionary
    - Define
    - marge
    - Update
    - Append
    support : Dict, list or tuple with 2 data, dict_items, Django request.data, request data, like path type list([('/a/b',2),('/a/c',3),...]), kDict

## CompVersion(*inp,**opts):
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

## ModVersion(mod)
    Find Module Version

## Install(module,install_account='',mode=None,upgrade=False,version=None,force=False,pkg_map=None,err=False):
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

## Import(*inps,**opts):
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

## MethodInClass(class_name)
    Get Method list in Class

## ObjInfo(obj)
    Get object information
    type, name, method list, path, module_name, module_version, module
    ```
    import requests
    ObjInfo(requests)
    Output:
    {'type': 'module', 'name': 'requests', 'methods': ['ConnectTimeout', 'ConnectionError', 'DependencyWarning', 'FileModeWarning', 'HTTPError', 'JSONDecodeError', 'NullHandler', 'PreparedRequest', 'ReadTimeout', 'Request', 'RequestException', 'RequestsDependencyWarning', 'Response', 'Session', 'Timeout', 'TooManyRedirects', 'URLRequired', '__author__', '__author_email__', '__build__', '__builtins__', '__cached__', '__cake__', '__copyright__', '__description__', '__doc__', '__file__', '__license__', '__loader__', '__name__', '__package__', '__path__', '__spec__', '__title__', '__url__', '__version__', '_check_cryptography', '_internal_utils', 'adapters', 'api', 'auth', 'certs', 'chardet_version', 'charset_normalizer_version', 'check_compatibility', 'codes', 'compat', 'cookies', 'delete', 'exceptions', 'get', 'head', 'hooks', 'logging', 'models', 'options', 'packages', 'patch', 'post', 'put', 'request', 'session', 'sessions', 'ssl', 'status_codes', 'structures', 'urllib3', 'utils', 'warnings'], 'path': ['/usr/lib/python3.10/site-packages/requests'], 'version': '2.27.1', 'module_name': 'requests', 'module': <module 'requests' from '/usr/lib/python3.10/site-packages/requests/__init__.py'>}
    ```
## MyModule(default=False,parent=-1): 
    Get current module 
    - parent
      -1 : my current python page's module
      0  : my function's module
      1  : my parent's module

## CallerName(default=False,detail=False):
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

## Frame2Function(obj,default=False):
    Get Function Object from frame or frame info

## FunctionName(parent=0,default=False,history=0,tree=False,args=False,line_number=False,filename=False,obj=False,show=False):
    Get function name
     - parent
       0            : my name (default)
       1            : my parent function
       ...          : going top parent function
     - history      : Getting history (return list)
     - tree         : tree  (return list)
       - show       : show tree on screen
     - args         : show arguments
     - line_number  : show line number
     - filename     : show filename
     - obj          : Get OBJ (return list)

## FunctionList(obj=None)
    Get function list in this object

## GetClass(obj,default=None)
    Get Class object from instance,method,function

## FunctionArgs(func,**opts):
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

## Args(src,field='all',default={}):
    Get Class, instance's global arguments
    Get Function input parameters

## Variable(src=None,obj=None,parent=0,history=False,default=False,mode='local',VarType=None,alltype=True):
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

## Uniq(src,default='org'):
    make to uniq data

## Split(src,sym,default=None,sym_spliter='|'):
    multipul split then 'a|b|...'
    without "|" then same as string split function

## FormData(src,default=None,want_type=None):
    convert string data to format
    '1' => 1
    json string to json format
    "{'a':1}" => {'a':1}
    "[1,2,3]" => [1,2,3]
    ....

## IndexForm(idx,idx_only=False,symbol=None):
    return : <True/False>, Index Data
     - False: not found Index form from input idx 
     - True : found Index
    Index Data
     - tuple(A,B) : Range Index (A~B)
     - list [A,B] : OR Index or keys A or B
     - Single     : int: Index, others: key
    - idx_only    : only return integer index
    - symbol   : default None, if idx is string and want split with symbol

## Get(*inps,**opts):
    Get (Any) something
    Get('whoami')  : return my function name
    Get('funclist'): return my module's function list
     - parent=1    : my parent's function list
    Get(<list|string|dict|int|...>,<index|key|keypath>): Get data at the <index|key|keypath>
     - keypath : '/a/b/c' => {'a':{'b':{'c':1,'d'}}} => return c's 1
    Get('_this_',<key>): my functions's <key>
    Get('<var name>')  : return variable data
    Get('_this_','args')  : return my functions Arguments
    Get(<function>,'args')  : return the functions Arguments
    <option>
    default : None, any issue

## ExceptMessage(msg='',default=None):
    Try:
       AAA
    Except:
       err=ExceptMessage() => If excepting then taken error or traceback code and return it

## IpV4(ip,out='str',default=False,port=None,bmc=False,used=False,pool=None):
    check/convert IP
    ip : int, str, ...
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
    pool: if give IP Pool(tuple) then check the IP is in the POOL or not.
## ping(host,**opts)
    same as ping command
    log_format='ping' : print ping output on screen
    ping('<IP>',log_format='ping') : print ping output
    ping('<IP>',count=5) : 5 times pinging then return True not then return False
    ping('<IP>',timeout=50) : pinging then return True and passing 50 seconds then return False
    ping('<IP>',keep_good=50,timeout=3600) : if keep pinging 50 seconds then return True in the 1hour.

## WEB
    import requests
    Web=WEB(requests)
    Web.GetIP() : get my web server IP
    Web.GetIP(mode='client') : get client IP 
    Web.Method() : return method name(get,post,...)
    Web.Method(mode='upper') : return method name (GET,POST,...)
    Web.Method('GET') : if requests' method is GET then return True, not then False
    Web.Request('<host_url>') : return requests' output
    WEB().str2url(<string>): if some special character then convert to URL
    WEB().form2dict(<request.form>) : return form data to dictionary.

## TIME()
    TIME().Int()     : Now second time 
    TIME().Rset()    : Reset initial Time
    TIME().Format('<time format>')            : return format time current time
    TIME().Format('<time format>',time=<int>) : return format time from time
    TIME().Format('<time format>',read_format='<time format>',time='<format time>'): Read time using read_format and return want time format (covert time format)
    TIME().Time()    : Same as time.time()
    TIME().Datetime(): Sameas datetime.datetime()
    Timeout example)
    ```
    timeout=30
    Time=TIME()
    while True:
        if Time.Out(timeout): break
        ~~~ 
        Time.Sleep(1)
    ```
## rshell(cmd,timeout=None,ansi=True,path=None,progress=False,progress_pre_new_line=False,progress_post_new_line=False,log=None,progress_interval=5,cd=False,default_timeout=3600):
    Run a shell command

## sprintf(string,*inps,**opts):
    """ipmitool -H %(ipmi_ip)s -U %(ipmi_user)s -P '%(ipmi_pass)s' """%(**opts)
    """{app} -H {ipmi_ip} -U {ipmi_user} -P '{ipmi_pass}' """.format(**opts)
    """{} -H {} -U {} -P '{}' """.format(*inps)
    """{0} -H {1} -U {2} -P '{3}' """.format(*inps)

## Sort(src,reverse=False,func=None,order=None,field=None,base='key',sym=None):
    Sorting data
    reverse=True: reverse sort
    field=<num> : Sorting by tuple's index number(field) data in list
    order
        int   : sorting by integer style
        str   : sorting by string style
        len   : sorting by string's length
    base='key': (default), sort by key, 'value': sort by data  for dictionary case
    sym=<split symbol>: if src is string with symbol then automatically split with that symbol and sorting.
    
## MacV4(src,**opts):
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

## Path(*inp,**opts):
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

## Cut(src,head_len=None,body_len=None,new_line='\n',out=str):
    Cut string
    head_len : int : first line length (default None)
               if body_len is None then everything cut same length with head_len
    body_len : int : line length after head_len (default None)
    new_line : default linux new line
    out=
        str  : output to string with new_line (default)
        list : output to list instead new_line

## Space(num=4,fill=None,mode='space',tap=''):
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

## WrapString(string,fspace=0,nspace=0,new_line='\n',flength=0,nlength=0,ntap=0,NFLT=False,mode='space',default=''):

## GetKey(src,find=None,default=None,mode='first',root=None):
    Get key from dict,list,tuple,str
    find : if matched value then return the key/index of the data
    mode :
      first : default: return first find
      all   : return found all
    default : return when not found

## rm(*args,**opts):
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

## List(*inps,**opts):
    tuple2list: 
        True : convert tuple data to list data
        False: append tuple into list
    <dict input>
     items : <dict>.items()
     data  : <dict>.value()
     path  : convert <dict> to path like list ([('/a/b',1),('/a/c',2),...])
     (default): <dict>.keys()
    <option>
     idx=<int>    : get <idx> data
     del=<int>    : delete <idx>
     first=<data> : move <data> to first
     end=<data>   : move <data> to end
     find=<data>  : get Index list
     default      : False
     mode 
        auto      : auto fixing index
        err       : not found then return default(False)
        ignore    : not found then ignore the data

## Replace(src,replace_what,replace_to,default=None,newline='\n'):
    replace string (src, from, to)
    if not string then return default
    default: return defined value when not string
      'org': return src
      ...  : return defined default

## OutFormat(data,out=None,strip=False,peel=None):
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

## FeedFunc(obj,*inps,**opts):
    Automatically Feed matched variables to function
    FeedFunc(<func>,<function's arguments>,<function's variables>)
    if something wrong then return False
    if correct then return output of ran the Function with inputs

## printf(*msg,**opts):

## ColorStr(msg,**opts):

## CleanAnsi(data):

## cli_input(msg,**opts):

## TypeData(src,want_type=None,default='org',spliter=None)
    Convert (input)data to want type (ex: str -> list, int, ...), can not convert to type then return False

## MoveData(src,data=None,to=None,from_idx=None,force=False,default='org'):
    support src type is list,str,(tuple)
    moving format : data(data) or from_idx(int)
      - data : if src has many same data then just keep single data at moved
    moving dest   : to(int)
    move data or index(from_idx) to want index(to)
      force=True: even tuple to move
    if not support then return default
    default : org

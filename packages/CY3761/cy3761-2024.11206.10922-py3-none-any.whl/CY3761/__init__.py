# ----------------------------------------------------------------------------------------------------
# import requests | pip install -U requests
# from fake_useragent import UserAgent | pip install -U fake_useragent
# from execjs import get, runtime_names, compile | pip install -U PyExecJS2
# ----------------------------------------------------------------------------------------------------
"""
/__init__.py
/string/config.py
/string/ascii.py
/string/helper.py

/storage/open.py

/py/helper.py
/js/helper.py
/js/npm.py

/js/0/ | CJS (CommonJS) [require]
/js/0/helper.js

/js/1/ | MJS (ES Modules) [import]
/js/1/helper.js
/js/1/curlconverter.js
/js/1/package.json | {"type": "module"}

/send/config.py
/send/req.py | 请求 (request)
/send/res.py | 响应 (response)

/build/
/build/template | 模板
/build/res.py | 生成请求相关文件
/build/string.py | 生成字符串相关文件


"""

# ----------------------------------------------------------------------------------------------------
from pathlib import Path

# ----------------------------------------------------------------------------------------------------
root_00 = Path(__file__).parent


# ----------------------------------------------------------------------------------------------------
def switch(v: bool | int, a: any, b: any):
    return [a, b][int(v)]


# ----------------------------------------------------------------------------------------------------
from CY3761.string.config import *
from CY3761.string.ascii import *
from CY3761.string.helper import *

from CY3761.storage.open import *

from CY3761.py.helper import *
from CY3761.js.helper import *
from CY3761.js.npm import *

from CY3761.send.req import *
from CY3761.send.res import *

from CY3761.build.res import *

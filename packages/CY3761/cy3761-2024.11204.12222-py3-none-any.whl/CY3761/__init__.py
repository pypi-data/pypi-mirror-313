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

/py/helper.py
/js/helper.py
/js/node.js

/send/config.py
/send/req.py
/send/res.py

/storage/open.py



这里需要做更改
/string/build.py -> /build/string.py
/send/res/build.py -> /build/res.py
/build/template/res/main.py
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

from CY3761.storage.open import *

from CY3761.py.helper import *
from CY3761.js.helper import *
from CY3761.js.npm import *

from CY3761.send.req import *
from CY3761.send.res import *

from CY3761.build.res import *

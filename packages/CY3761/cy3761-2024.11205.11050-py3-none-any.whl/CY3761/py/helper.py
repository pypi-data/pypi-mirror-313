# CY3761 | fb764bc@outlook.com | 2024-11-25 11:23:25 | helper.py
# ----------------------------------------------------------------------------------------------------
from datetime import datetime
from json import dumps
# ----------------------------------------------------------------------------------------------------
from CY3761 import *


# ----------------------------------------------------------------------------------------------------
def format_datetime(dt: datetime = None) -> str:
    return switch(isinstance(dt, datetime), datetime.now(), dt).isoformat()


# ----------------------------------------------------------------------------------------------------
def format_dumps(v: dict | list):
    return dumps(v, indent=4, ensure_ascii=False, sort_keys=True)


# ----------------------------------------------------------------------------------------------------
def timestamp_10():  # s | 秒
    from time import time
    return int(time())


# ----------------------------------------------------------------------------------------------------
cwd_00 = './'


# ----------------------------------------------------------------------------------------------------
def cmd(code: str | list, cwd=cwd_00):
    from subprocess import run, PIPE

    ret = run(code, encoding=encoding, shell=True, cwd=cwd, text=True, stdout=PIPE, stderr=PIPE)

    print(code, cwd)

    ret.stderr and storage('./cmd-error.log', ret.stderr) and print(repr(ret.stderr))

    return ret.stdout.strip()


# ----------------------------------------------------------------------------------------------------
def env(k, v=None):
    from os import environ

    if v is not None:
        environ[k] = '%s' % v

    return environ.get(k)


# ----------------------------------------------------------------------------------------------------
def main_00():
    print(switch(0, 'r', 'w'))


# ----------------------------------------------------------------------------------------------------
def main_01():
    print(format_dumps([1, 2, 3, 4, 5]))
    print(format_dumps(dict(a=1, b=2)))


# ----------------------------------------------------------------------------------------------------
def main_02():
    v = timestamp_10()

    print(type(v), repr(v), len(str(v)))

    print(format_datetime())


# ----------------------------------------------------------------------------------------------------
def main_03():
    print(repr(cmd('npm list')))
    # print(repr(cmd('npm i curlconverter')))


# ----------------------------------------------------------------------------------------------------
def main():
    main_00()
    main_01()
    main_02()
    main_03()


# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

# CY3761 | fb764bc@outlook.com | 2024-11-25 13:06:33 | helper.py
# ----------------------------------------------------------------------------------------------------

from execjs import get, runtime_names, compile  # pip install -U PyExecJS2
# ----------------------------------------------------------------------------------------------------
from CY3761 import *

# ----------------------------------------------------------------------------------------------------
get(runtime_names.Node)

root_02 = Path(__file__).parent
# https://zhuanlan.zhihu.com/p/669242181
root_03 = root_02 / '0'  # CJS (CommonJS)   | 同步加载 | const fs = require('fs')   | module.exports = {}
root_04 = root_02 / '1'  # MJS (ES Modules) | 异步加载 | import fs from 'fs'        | export {}
root_03_k = 'root_03'
root_04_k = 'root_04'


# ----------------------------------------------------------------------------------------------------
# 脚本读取并运行
# 这个并不支持 import 语法
def require(src='', cwd=cwd_00):
    return compile(source=storage(src), cwd=cwd)


# ----------------------------------------------------------------------------------------------------
# 通过 py 运行 js 表达式, 表达式会包含在函数中执行并返回
# 执行 execute
def execute(code: str, *args) -> str:
    from string import ascii_lowercase

    return compile('const _ = ({0}) => {1}'.format(
        ', '.join([ascii_lowercase[i] for i, v in enumerate(args)]),
        code,
    )).call('_', *args)


# ----------------------------------------------------------------------------------------------------
def timestamp_13():  # ms | 毫秒
    return int(execute('+new Date()'))


# ----------------------------------------------------------------------------------------------------
def json_stringify(o: dict | list):
    return execute('JSON.stringify(a)', o)


def atob(v: str):
    return execute('atob(a)', v)


def btoa(v: str):
    return execute('btoa(a)', v)


# ----------------------------------------------------------------------------------------------------
def np(v: str, *args, cwd=cwd_00):
    return cmd('np{0} '.format(v) + ' '.join([str(v) for v in args]), cwd=cwd)


# ----------------------------------------------------------------------------------------------------
# 这个可能有问题
def npx(*args, cwd=cwd_00):
    return np('x', *args, cwd=cwd)


# ----------------------------------------------------------------------------------------------------
def npm(*args, cwd=cwd_00):
    return np('m', *args, cwd=cwd)


# ----------------------------------------------------------------------------------------------------
# 这个是利用命令行 node 脚本 并传参, 但如果参数比较特殊, 建议保存成文件, 直接js读文件内容, 而非直接命令行传参
# 这里的 func 可以是对象.静态方法
def node(src: str | Path, func: str, *args):
    temp = args
    args = [Path(src).absolute(), func]
    args.extend(temp)

    return cmd('node.exe ' + ' '.join([str(v) for v in args]))


# ----------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------
def main_00():
    # 任何正常结果返回都是字符串类型的值
    print(repr(node(root_03 / 'test.js', 'sum', 8, 9)))
    print('-' * 100)
    print(repr(execute('+new Date()')))
    print('-' * 100)


# ----------------------------------------------------------------------------------------------------
def main_01():
    v = timestamp_13()

    print(type(v), repr(v), len(str(v)))
    print('-' * 100)

    print(json_stringify({'a': 1, 'b': 2}))
    print('-' * 100)

    v = 'https://xy123x138x84x34xy.mcdn.bilivideo.cn:4483/upgcxcode/09/07/364170709/364170709-1-100023.m4s'
    e = btoa(v)
    d = atob(e)

    print(v, e, d, sep=a_010)


# ----------------------------------------------------------------------------------------------------
def main():
    main_00()
    main_01()


# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

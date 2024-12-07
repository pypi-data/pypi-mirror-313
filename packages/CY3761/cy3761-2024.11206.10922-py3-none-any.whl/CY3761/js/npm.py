# CY3761 | fb764bc@outlook.com | 2024-12-02 12:23:27 | npm.py
# ----------------------------------------------------------------------------------------------------
from CY3761 import *


# ----------------------------------------------------------------------------------------------------
# 软件包是否已经在 指定目录安装
def installed(kpg: str, cwd: str):
    ret = npm('list', cwd=cwd)

    if ret.count(kpg) == 0:
        return False

    # 有可能 package.json 存在关键字, 但实际未安装
    if ret.count('UNMET DEPENDENCY') >= 0:
        return False

    return True


# ----------------------------------------------------------------------------------------------------
def installed_code(pkg: str, cwd: str, code: str, is_installed: bool):
    if installed(pkg, cwd=cwd) == is_installed:
        return

    # 类似命令均加上国内镜像源
    ret = npm(code, pkg, '--registry', 'https://registry.npmmirror.com/', cwd=cwd)

    return ret


# ----------------------------------------------------------------------------------------------------
# 安装/删除 都需要目录参数, 否则无法 安装/删除 到 指定目录
def install(pkg: str, cwd: str):
    return installed_code(pkg, cwd, 'install', True)


# ----------------------------------------------------------------------------------------------------
def remove(pkg: str, cwd: str):
    return installed_code(pkg, cwd, 'remove', False)


# ----------------------------------------------------------------------------------------------------
def main_00(v='curlconverter', cwd=root_04):
    print(remove(v, cwd=cwd))
    print(install(v, cwd=cwd))


# ----------------------------------------------------------------------------------------------------
def main():
    main_00()


# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

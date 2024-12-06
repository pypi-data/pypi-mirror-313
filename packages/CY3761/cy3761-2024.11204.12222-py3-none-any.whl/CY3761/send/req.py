# CY3761 | fb764bc@outlook.com | 2024-11-25 13:06:58 | req.py
# ----------------------------------------------------------------------------------------------------
from fake_useragent import UserAgent  # pip install -U fake_useragent
import requests # pip install -U requests
# ----------------------------------------------------------------------------------------------------
from CY3761.send.config import *

# ----------------------------------------------------------------------------------------------------
ua = UserAgent(platforms='pc')


# ----------------------------------------------------------------------------------------------------
def set_headers(headers: dict[str, str], refresh_useragent=False):  # 刷新
    # 检查是否具有 'User-Agent', 是否更新 'User-Agent'

    # 在HTTP协议中, 请求头字段的名称通常是不区分大小写的.
    # 这意味着无论请求头中的键是以大写、小写还是混合形式出现, 它们通常都被认为是等效的.
    # 这种设计有助于简化HTTP协议的处理, 并允许客户端和服务器在实现时有更多的灵活性

    headers = {k: v for k, v in headers.items() if not k == useragent_k1}

    # print(headers.get(useragent_k0))

    if not headers.get(useragent_k0):
        headers[useragent_k0] = useragent

    if refresh_useragent:
        headers[useragent_k0] = ua.random

    return headers


# ---------------------------------------------------------------------------------------------------
def main_00():
    # [print(ua.random) for v in range(10)]
    headers = {}

    print(set_headers(headers))  # 没有改变原来的 headers


# ----------------------------------------------------------------------------------------------------
def main():
    pass
    main_00()


# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

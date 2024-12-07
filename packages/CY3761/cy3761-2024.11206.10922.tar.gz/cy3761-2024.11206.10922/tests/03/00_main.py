# CY3761 | fb764bc@outlook.com | 2024-12-05T12:12:08.656754 | 00_main.py
# ----------------------------------------------------------------------------------------------------
from CY3761 import *

# ----------------------------------------------------------------------------------------------------
src = './00_main.js'
req = require(src)


# ----------------------------------------------------------------------------------------------------
def main_00():
    print(req.call('sum', 5, 7))  # 12
    print(node(src, 'sum', 8, 9))  # 17


# ----------------------------------------------------------------------------------------------------
def main_01():
    cookies = headers = params = data = {}
    # 'getCookies', 'getHeaders', 'getParams', 'getData'
    # * = req.call('get*', *)
    # print(dumps(*))

    # https://clogin.ke.com/authentication/initialize | POST
    # application/json;charset=UTF-8
    # {"service":"https://ajax.api.ke.com/login/login/getuserinfo","mainAuthMethodName":"username-password","accountSystem":"customer","credential":{"username":"13802973761","password":"Nadi1dJeAzK2B3YuXFl3O3STuzmXseXsXJDSzl0gEOeQh992YVB1bGm1ZbVGFgw6S4OoN/pEmO5dbgQEbvmBbtj1aaGwh+Evqgikq66bl1+eYV4xFHgQhGB/8kfGh6mFe8uBSNcp+mj/9yBumgkRB93cthls+BveCnKY5W6c/FA=","encodeVersion":"2"},"context":{"ua":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36","clientSource":"pc","os":"Windows","osVersion":"10","registerPosLx":643.5,"registerPosLy":485,"registerPosRx":923.5,"registerPosRy":529,"clickPosX":818,"clickPosY":500,"screen":"1328_917","dataId":"2MrTQAGTZfB41AoQZ5SHAl86G7IDw7lLRccgMUifh+Jv0Ywj9iN6ckzyf/UNTzKQ"},"loginTicketId":"anGN8Fd2bmcasR6Szxg8kSP4TANkiyl5","version":"2.0","srcId":"eyJ0Ijoie1wiZGF0YVwiOlwiYmQ3MDg4MmVmNGQ4YjU1NjA0NTVmNGU4MmExYzkzZGQzZTMyZjhmZTY3MzJkYTAzMjgzY2EwZWEyNGZkMjNlNTczMjBmM2Y2MmU5OTljOTk3NGY3MzhjNTQ4MDA3NGJkZmJiMjg3MzBmZTc2NDA5YjhhMDg5NDJmOGM3M2Q0YmY0ZmVmZTdlMTJkYTYyZTlmNTNjMjEwNWEwYTg0N2JhNjc4Njc0ODMzZjEwMzAyMTM4YTBmODIxNWExYzU4NjRkMmIxODQ3YjU2ZTE4ZjNhMWEzNjRmNmQ3NjUxNDcxZWZmYzE5NWRlYzYyYzc4YmNkN2IxNjgwMmFkNWM4NzFmY1wiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJmOTdkZGMyZVwifSIsInIiOiJodHRwczovL2JqLmtlLmNvbS8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ=="}
    # lianjia_ssid
    # 响应
    # {
    #     "exception": {
    #         "code": "auth.incorrect.credential",
    #         "identities": {},
    #         "message": "用户名或密码不正确"
    #     },
    #     "message": "用户名或密码不正确",
    #     "success": false
    # }

    # 请求 | application/json;charset=UTF-8 | {"service":"https://ajax.api.ke.com/login/login/getuserinfo","version":"2.0"}
    # https://dig.lianjia.com/fee.gif | 获取 cookie
    # lianjia_ssid | lianjia_uuid
    # arguments[0]
    # '{"service":"https://ajax.api.ke.com/login/login/getuserinfo","mainAuthMethodName":"username-password","accountSystem":"customer","credential":{"username":"13802973761","password":"Nadi1dJeAzK2B3YuXFl3O3STuzmXseXsXJDSzl0gEOeQh992YVB1bGm1ZbVGFgw6S4OoN/pEmO5dbgQEbvmBbtj1aaGwh+Evqgikq66bl1+eYV4xFHgQhGB/8kfGh6mFe8uBSNcp+mj/9yBumgkRB93cthls+BveCnKY5W6c/FA=","encodeVersion":"2"},"context":{"ua":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36","clientSource":"pc","os":"Windows","osVersion":"10","registerPosLx":643.5,"registerPosLy":485,"registerPosRx":923.5,"registerPosRy":529,"clickPosX":818,"clickPosY":500,"screen":"1328_917","dataId":"2MrTQAGTZfB41AoQZ5SHAl86G7IDw7lLRccgMUifh+Jv0Ywj9iN6ckzyf/UNTzKQ"},"loginTicketId":"anGN8Fd2bmcasR6Szxg8kSP4TANkiyl5","version":"2.0","srcId":"eyJ0Ijoie1wiZGF0YVwiOlwiYmQ3MDg4MmVmNGQ4YjU1NjA0NTVmNGU4MmExYzkzZGQzZTMyZjhmZTY3MzJkYTAzMjgzY2EwZWEyNGZkMjNlNTczMjBmM2Y2MmU5OTljOTk3NGY3MzhjNTQ4MDA3NGJkZmJiMjg3MzBmZTc2NDA5YjhhMDg5NDJmOGM3M2Q0YmY0ZmVmZTdlMTJkYTYyZTlmNTNjMjEwNWEwYTg0N2JhNjc4Njc0ODMzZjEwMzAyMTM4YTBmODIxNWExYzU4NjRkMmIxODQ3YjU2ZTE4ZjNhMWEzNjRmNmQ3NjUxNDcxZWZmYzE5NWRlYzYyYzc4YmNkN2IxNjgwMmFkNWM4NzFmY1wiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJmOTdkZGMyZVwifSIsInIiOiJodHRwczovL2JqLmtlLmNvbS8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ=="}'
    # https://clogin.ke.com/authentication/initialize | POST |
    # 请求 | application/json;charset=UTF-8 | {"service":"https://ajax.api.ke.com/login/login/getuserinfo","version":"2.0"}

    # 这个登录需要手机号验证 | 这个算成功的响应
    # {"extraData":{"userTag":"0"},"loginTicket":{"id":"rJCz5ep3B9erBM71RvsrGLw3A7LxIdEv","createdAt":"2024-12-05T09:12:46Z"},"needMethodsNames":["security-code"],"status":"WARN","success":true}

    response = requests.get('')

    res_00(response)

    text = req.call('getResponseBody', response.text)
    print(text)


# ----------------------------------------------------------------------------------------------------
def main():
    build_config_js()
    main_00()
    # main_01()


# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

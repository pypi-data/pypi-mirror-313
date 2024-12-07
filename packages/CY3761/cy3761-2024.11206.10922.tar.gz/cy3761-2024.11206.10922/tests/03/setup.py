# CY3761 | fb764bc@outlook.com | 2024-12-05T12:11:11.213054 | setup.py
# ----------------------------------------------------------------------------------------------------
from CY3761 import *


# ----------------------------------------------------------------------------------------------------
def main_00():
    build_base64([
        # https://bj.ke.com/ | 北京房产网_北京二手房|租房|新房|房地产信息网【北京贝壳找房】
        'aHR0cHM6Ly9iai5rZS5jb20v'
    ])
    build_config_js()

    [
        [v0(pad_zero(i)) for v0 in (build_main_js, build_main_py)] for i in range(1)
    ]


# ----------------------------------------------------------------------------------------------------
def main_01():
    [build_test_py(pad_zero(i), v) for i, v in enumerate([
        """
        curl 'https://clogin.ke.com/authentication/authenticate' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: select_city=110000; lianjia_uuid=7e790768-7ef4-41a5-994e-b1477677e4ed; Hm_lvt_b160d5571570fd63c347b9d4ab5ca610=1733385135; HMACCOUNT=801D86F051673852; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219395ce23894fb-01bc8025f69551-26011851-2073600-19395ce238a67c%22%2C%22%24device_id%22%3A%2219395ce23894fb-01bc8025f69551-26011851-2073600-19395ce238a67c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; ftkrc_=35de58d1-db04-40d0-8930-8aaac26fa1d3; lfrc_=7849210b-86b1-4342-8a2b-fa8a91be1be3; JSESSIONID=F462D2AF38019C58CA66F347FD5647A5; lianjia_ssid=4842078c-4236-4370-9fba-07546a35ef8c; Hm_lpvt_b160d5571570fd63c347b9d4ab5ca610=1733389962' \
  -H 'Origin: https://bj.ke.com' \
  -H 'Referer: https://bj.ke.com/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  --data-raw '{"service":"https://ajax.api.ke.com/login/login/getuserinfo","mainAuthMethodName":"username-password","accountSystem":"customer","credential":{"username":"13802973761","password":"WVsPBM2bRznoy2WBs75SxmgerIxDmiD+Rd+1mF61RV+PoGefH25wZeOWR4z7T36hL2nOP1+yPO+w3RKiwTrpzFuHZWuF+lQrO5tfNBOiw7m06zD4NsmiskvoLNVaybYP+lK5S+H0irtlxLcgQj2ZpBo5FQrA8nwo+bTwPUTxg6o=","encodeVersion":"2"},"context":{"ua":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36","clientSource":"pc","os":"Windows","osVersion":"10","registerPosLx":407,"registerPosLy":476.5,"registerPosRx":687,"registerPosRy":520.5,"clickPosX":569,"clickPosY":493,"screen":"855_900","dataId":"2CzARphZ37LkTo1A6ztcQ24ufFf/lvHS52aGEVCnroJv0Ywj9iN6ckzyf/UNTzKQ"},"loginTicketId":"rJCz5ep3B9erBM71RvsrGLw3A7LxIdEv","version":"2.0","srcId":"eyJ0Ijoie1wiZGF0YVwiOlwiYmQ3MDg4MmVmNGQ4YjU1NjA0NTVmNGU4MmExYzkzZGQzZTMyZjhmZTY3MzJkYTAzMjgzY2EwZWEyNGZkMjNlNTczMjBmM2Y2MmU5OTljOTk3NGY3MzhjNTQ4MDA3NGJkZmJiMjg3MzBmZTc2NDA5YjhhMDg5NDJmOGM3M2Q0YmY0ZmVmZTdlMTJkYTYyZTlmNTNjMjEwNWEwYTg0N2JhNjY4ZmNhZGVkZjQ4MzRjNjYwMDc4MzNjNjg4MDJhZGEwNzllNDI4NjBkNjYwMTBhYzM1ZWJjMjQ0ZDc4NTk2OTBhMDVjYmZmYTBkNjE5YjdjNmNiMDMyYjM0NTUwM2I2NVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI4NmNlODA3ZVwifSIsInIiOiJodHRwczovL2JqLmtlLmNvbS8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ=="}'
        """  ])]


# ----------------------------------------------------------------------------------------------------
def main():
    # main_00()
    main_01()


# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

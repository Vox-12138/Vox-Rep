# 这个程序每卵用，我还不知道怎么改
import requests
import re

log_url = 'http://hall-dlmu-edu-cn-s.svpn.dlmu.edu.cn:8118'
post_url = 'http://id-dlmu-edu-cn-s.svpn.dlmu.edu.cn:8118/cas/login'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}
post_data = {
    'username': '2220194003',
    'type': 'UsernamePassword',
    '_eventId': 'submit',
    'geolocation': '',
    'execution': 'c1263d31-81e8-4ce0-bdfd-45678dca61b7_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',
    'captcha_code': '',
    'croypto': 'Ub+XeZ4ls0w=',
    'password': 'FMNhShV1J9+kBFQ3P/gkJA=='
}
session = requests.session()

session.post(url=post_url, data=post_data, headers=headers)
response = session.get(url=log_url, headers=headers).text

url = re.findall('url:.*?,right:0', response)
url = url[1]
url = re.findall('".*"', url)[0]
url = url.split('"')[1]

response = session.get(url=url, headers=headers).text
print(response)

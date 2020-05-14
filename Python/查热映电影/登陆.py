# 我没法解决验证码，登录次数过多会出现验证码。
import requests

#print('这个可爱的程序可以登陆豆瓣:)')
#name = input('请输入你的账号：')
#password = input('和密码：')

log_url = 'https://www.douban.com/'  # 登陆后的网址
post_url = 'https://accounts.douban.com/j/mobile/login/basic'  # 登陆时POST的网址，抓包得到
post_data = {
    'ck': '',
    'name': '17713590325',
    'password': 'GD200104183',
    'remember': 'false',
    'ticket': ''
}  # POST的数据，抓包得到
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
           }
session = requests.session()  # 要用session方法来get和post，我也不知道为什么
session.post(url=post_url, data=post_data, headers=headers)  # 向登陆时POST的网址post登陆数据
response = session.get(url=log_url, headers=headers).text  # 再获取登陆后页面的源代码

print(response)

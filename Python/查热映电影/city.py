import re
import requests

url = 'https://movie.douban.com/cinema/nowplaying/dalian'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                        '537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}
response = requests.get(url=url, headers=header)
data = response.text
# 在豆瓣网上得到数据

city_dic = {}  # 以中文城市名为键，以对应部分网址为值

city_data = re.findall('<span><a class="city-item" href="javascript:;" id="'
                       '.*?</a></span>', data)
for one_city_data in city_data:
    one_city_data = str(re.findall('uid.*?<', one_city_data))
    C_city = str(re.findall('[\u4E00-\u9FA5\\s]+', one_city_data))
    C_city = C_city[2:-2]
    E_city = str(re.findall('\".*?\"', one_city_data))
    E_city = E_city[3:-3]

    city_dic[C_city] = E_city
# 处理数据


import requests


def weather(id):
    params = {'appid': '5234888', 'appsecret': 'tFfGJa5X', 'version': 'v6', 'id': str(id)}
    web = requests.get('http://www.tianqiapi.com/api/', params=params)

    data = web.json()
    print('现在%s的天气是:' % data['city'])
    print('温度：%s 摄氏度' % data['tem'])
    print('风向和风速：%s%s' % (data['win'], data['win_speed']))
    print('空气质量:%s , ' % data['air_level']+'PM2.5: %s    ' % data['air_pm25'])
    print('湿度：%s' % data['humidity'])
    print('能见度：%s' % data['visibility'])
    print('\n地区：%s , 日期：%s ,更新时间：%s' % (data['city'], data['date'], data['update_time']))
# 这个函数咨询并显示天气


f_ID_data = open('城市ID.txt', encoding='UTF-8')
ID_data = f_ID_data.readlines()  # "\t('101010100','beijing','北京','beijing','北京','China','中国','beijing','北京','39.904989','116.405285'),\n"
f_ID_data.close()
l_ID_data = []  # ["'101010100'", "'beijing'", "'北京'", "'beijing'", "'北京'", "'China'", "'中国'", "'beijing'", "'北京'", "'39.904989'", "'116.405285')"]
for city_data in ID_data:
    city_data = city_data[2:-2]
    l_ID_data.append(city_data.split(','))
new_l_ID_data = []
for city_data in l_ID_data:
    new_city_data = []
    for inside_city_data in city_data:
        inside_city_data = inside_city_data[1:-1]
        new_city_data.append(inside_city_data)
    del new_city_data[-1]
    del new_city_data[-1]
    del new_city_data[1]
    del new_city_data[2]
    del new_city_data[3]
    del new_city_data[3]
    del new_city_data[3]
    new_l_ID_data.append(new_city_data)
l_ID_data = new_l_ID_data  # ['ID', '区', '省', '市'], [.....]
d_ditrict_id = {}  # '朝阳': '101071201'
for id_data in l_ID_data:
    d_ditrict_id[id_data[1]] = id_data[0]
d_city_ditrict = {}  # '北京': ['北京', '海淀', '朝阳', '顺义', '怀柔', '通州', '昌平', '延庆', '丰台', '石景山', '大兴', '房山', '密云', '门头沟', '平谷']
for id_data in l_ID_data:
    city = id_data[3]
    ditrict = id_data[1]
    l_ditrict = d_city_ditrict.get(city)
    if None == l_ditrict:
        d_city_ditrict[city] = []
        l_ditrict = d_city_ditrict.get(city)
    l_ditrict.append(ditrict)
    d_city_ditrict[city] = l_ditrict
# 这部分代码将城市ID整理为字典


print('你想查哪个城市的天气啊？')
query = str(input())
query_city = d_city_ditrict.get(query)
if None == query_city:
    ditrict_id = d_ditrict_id.get(query)
    city_or_ditrict = 'ditrict'
    if None == ditrict_id:
        print('找不到这个城市欸 :(')
else:
    ditrict_id = d_ditrict_id.get(query_city[0])
    city_or_ditrict = 'city'
if None != ditrict_id:
    weather(ditrict_id)
# 这部分代码得到地区的ID，输出天气


if city_or_ditrict == 'city':
    print('\n\n\n%s有以下地区:' % query_city[0])
    for ditricts in query_city:
        print(ditricts, end='  ')
    print('\n你可以进一步查询，请输入你想查询的地区')
    query_ditrict = input()
    if query_ditrict in query_city:
        ditrict_id = d_ditrict_id.get(query_ditrict)
        weather(ditrict_id)
    else:
        print('？？？\n没有这个地区 :o')
# 进一步查询天气

import re
import requests

print('你想查哪个城市的热映电影啊?')
import city  # 引入city.py中的城市数据
input_city = str(input())
city_dic = city.city_dic
city_idu = city_dic.get(input_city)
# 根据城市名得到部分网址

if None == city_idu:
    print('找不到这个城市欸:(')
else:
    url = 'https://movie.douban.com/cinema/nowplaying/' + city_idu
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                            '537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}
    response = requests.get(url=url, headers=header)
    response.encoding = 'utf-8'
    data = response.text
    # 从豆瓣网上获取热映电影数据

    data = data.split('正在上映')
    del data[0]
    data = str(data)
    # 去掉数据中“即将上映”部分


    class Movie:
        def __init__(self, the_target):
            self.target = str(the_target)
        # 设置要查找的目标

        def process(self):
            movies = re.findall('%s.*?n' % self.target, data)
            the_list = []
            for movie in movies:
                movie = movie.split('\"')
                movie = str(movie[1])
                the_list.append(movie)
            return the_list
        # 查找该目标，将结果写进一个list
    # 进一步处理数据

    targets_list = ['data-score', 'data-release', 'data-duration',
                    'data-region', 'data-director', 'data-actors']  # 要查找的目标list
    result_dic = {}  # 最终结果字典 以电影名为键，以名为movie_info_list的list为值
    title_class = Movie('data-title')
    title_list = title_class.process()  # 得到电影名list
    for title in title_list:
        result_dic[title] = []  # 将电影名list作为结果字典的键

    for target in targets_list:
        target_class = Movie(target)
        result_list = target_class.process()
        # 将得到的信息写入result_list

        rank = 0
        for result in result_list:
            title = title_list[rank]
            movie_info_list = result_dic.get(title)
            movie_info_list.append(result)
            result_dic[title] = movie_info_list
            rank = rank + 1  # 将result_list的内容写入result_dic的值
    # 将处理后的数据写入结果字典

    print('\n正在热映的电影有这些喔:)\n')
    for title in title_list:
        print(title)
        movie_info_list = result_dic.get(title)
        print('  得分：' + movie_info_list[0] + '分')
        print('  年份：' + movie_info_list[1])
        print('  时长：' + movie_info_list[2])
        print('  地区：' + movie_info_list[3])
        print('  导演：' + movie_info_list[4])
        print('  主演：' + movie_info_list[5])
    # 输出结果

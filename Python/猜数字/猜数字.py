from random import randint
import pickle

f_players = open('players.txt', 'rb')
name_grade_d = pickle.load(f_players)
f_players.close()
name = input('你的名字是：')
grade_list = name_grade_d.get(name)
if None == grade_list:
    grade_list = []
    name_grade_d[name] = grade_list
else:
    print('欢迎回来，' + name)
# 读取玩家的成绩数据到字典中，并为新玩家创建数据

while True:
    num = randint(1, 100)
    print('请猜一个1-100的数字')
    times = 1
    while True:
        guess = int(input())
        if guess < num:
            print(str(guess)+'太小了，再猜一次吧 :(')
            times = times+1
        elif guess > num:
            print(str(guess)+'太大了，再猜一次吧 :(')
            times = times + 1
        else:
            print('哇你猜对了，你只猜了'+str(times)+'次!')
            grade_list.append(str(times))
            break
    print('想再玩一次，请输入\"继续\",想退出请输入其它任意字符')
    choice = input()
    if choice != '继续':
        break
name_grade_d[name] = grade_list  # {'戴林均': ['10', '9'], '泰勒斯威夫特': ['7', '6']}
# 进行游戏，并将成绩存入字典中

new_grade_list = list(map(int, grade_list))  # [10, 9, 1]
new_grade_list.sort()  # [1, 9, 10]
t = 0
sum_grade = 0
for grades in new_grade_list:
    t = t+1
    sum_grade = sum_grade+grades
print('你总共玩了%d把，平均每把猜了%d次，最好的成绩是猜了%d次' % (t, sum_grade/t, new_grade_list[0]))
# 显示玩家的成绩

f_players = open('players.txt', 'wb')
pickle.dump(name_grade_d, f_players)
f_players.close()

input()  # 输入任意字符后程序关闭






















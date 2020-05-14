import pygame
from sys import exit
from math import sqrt
from random import randint
from random import uniform

print('忽略上面这句话 :) ')

pygame.init()  # 初始化

pygame.display.set_caption('Game')  # 标题
size = w, h = 600, 780
window = pygame.display.set_mode(size)  # 屏幕大小

background_image = pygame.image.load('背景.jpg').convert()
player_image = pygame.image.load('玩家战机.png').convert_alpha()
enemy_image = pygame.image.load('小敌机.png').convert_alpha()
big_enemy_image = pygame.image.load('大敌机.png').convert_alpha()
bullet_image = pygame.image.load('子弹.png').convert_alpha()
# 加载一大坨图片


class Key:  # Key用来处理按键
    key_left = False
    key_right = False
    key_up = False
    key_down = False  # 为上、下、左、右四个按键设置标签，该标签标志按键是否被按下

    key_pressed = pygame.key.get_pressed()  # 按下的按键

    def key_flag(self):
        self.key_left = False
        self.key_right = False
        self.key_up = False
        self.key_down = False

        self.key_pressed = pygame.key.get_pressed()  # 获取被按下的按键

        if self.key_pressed[pygame.K_LEFT]:  # 若左键被按下
            self.key_left = True             # 将左键的标签设为True

        if self.key_pressed[pygame.K_RIGHT]:
            self.key_right = True

        if self.key_pressed[pygame.K_UP]:
            self.key_up = True

        if self.key_pressed[pygame.K_DOWN]:
            self.key_down = True
key = Key()


class Player:  # Player用来控制玩家战机
    player_pos_x = w / 2  # 玩家战机的横坐标
    player_pos_x -= player_image.get_width() / 2
    player_pos_y = h * 0.9  # 玩家战机的纵坐标
    player_pos_y -= player_image.get_height() / 2  # 这四句话设置玩家战机的初始位置

    player_speed = 0.5  # 玩家战机的速度；单位：像素/毫秒

    clock = pygame.time.Clock()
    time_passed = clock.tick()  # time_passed 是从上一帧到这一帧的历时；单位：毫秒

    def player_move(self):
        window.blit(player_image, (self.player_pos_x, self.player_pos_y))  # 显示玩家战机

        self.time_passed = self.clock.tick()

        self.player_speed = 0.5

        if key.key_left and self.player_pos_x > player_image.get_width() / 2 - 50:  # 如果按下了左键而且玩家战机不在屏幕的左边缘
            if not key.key_up and not key.key_down:  # 如果没有按下上键或下键
                self.player_pos_x -= self.player_speed * self.time_passed  # 每一帧中玩家战机移动的距离=速度*每一帧历时
            else:  # 如果同时按下了上键或下键，即在玩家战机斜着运动时
                self.player_speed = self.player_speed * sqrt(0.5)          # 因为玩家战机在斜着运动时速度会变为2^0.5倍
                self.player_pos_x -= self.player_speed * self.time_passed  # 所以把速度调为原来的2^(-0.5)倍

        if key.key_right and self.player_pos_x < w - player_image.get_width() / 2 - 50:
            if not key.key_up and not key.key_down:
                self.player_pos_x += self.player_speed * self.time_passed
            else:
                self.player_speed = self.player_speed * sqrt(0.5)
                self.player_pos_x += self.player_speed * self.time_passed

        if key.key_up and self.player_pos_y > player_image.get_height() / 2 - 50:
            if not key.key_left and not key.key_right:
                self.player_pos_y -= self.player_speed * self.time_passed
            else:
                self.player_speed = self.player_speed * sqrt(0.5)
                self.player_pos_y -= self.player_speed * self.time_passed

        if key.key_down and self.player_pos_y < w - player_image.get_height() / 2 + 100:
            if not key.key_left and not key.key_right:
                self.player_pos_y += self.player_speed * self.time_passed
            else:
                self.player_speed = self.player_speed * sqrt(0.5)
                self.player_pos_y += self.player_speed * self.time_passed
player = Player()


class OneBullet:  # OneBullet用来控制一颗子弹
    bullets_shoot_flag = False  # 这是子弹的发射标签，该标签标志这颗子弹是否需要被发射
    bullets_fly_flag = False  # 这是子弹的飞行标签，该标签标志子弹是否在飞行状态

    start_bullet_pos_x = player.player_pos_x + 38
    start_bullet_pos_y = player.player_pos_y + 9  # 子弹射出时的位置，即玩家战机机头位置

    stop_bullet_pos_x = -10
    stop_bullet_pos_y = -10  # 子弹不在飞行时的位置

    bullet_pos_x = stop_bullet_pos_x
    bullet_pos_y = stop_bullet_pos_y

    bullet_speed = 1.5  # 子弹速度；单位：像素/毫秒

    time_passed = player.time_passed  # 从上一帧到这一帧的历时

    def one_bullet(self):
        self.time_passed = player.time_passed

        self.start_bullet_pos_x = player.player_pos_x + 38
        self.start_bullet_pos_y = player.player_pos_y + 9  # 设置子弹发射的初始位置为机头位置

        if self.bullets_shoot_flag and not self.bullets_fly_flag:  # 判断这颗子弹的发射标签和飞行标签
            self.bullet_pos_x = self.start_bullet_pos_x
            self.bullet_pos_y = self.start_bullet_pos_y

            self.bullets_shoot_flag = False  # 发射这颗子弹后，将其发射标签改为否

        if self.bullet_pos_y > self.stop_bullet_pos_y + 10:  # 判断这颗子弹是否在屏幕中
            self.bullet_pos_y -= self.time_passed * self.bullet_speed  # 若在屏幕中，则继续飞行

            self.bullets_fly_flag = True  # 将子弹飞行标签设置为是

            window.blit(bullet_image, (self.bullet_pos_x, self.bullet_pos_y))  # 显示子弹
        else:  # 若子弹已飞出屏幕
            self.bullets_fly_flag = False  # 将子弹飞行标签设置为否

            self.bullet_pos_x = self.stop_bullet_pos_x
            self.bullet_pos_y = self.stop_bullet_pos_y  # 将其位置设置为不在飞行时的位置


class Bullets:  # Bullets用来控制所有子弹
    bullets_num = 10  # bullets_num 是子弹的总数量
    bullets_interval_time = 300  # interval_time 是从上一颗子弹发射到现在的历时；单位：毫秒
    bullets_hz = 300  # bullets_hz 每经过这么多时间，发射一颗子弹；单位：毫秒

    def __init__(self):
        self.bullets_dict = {}  # 该字典容纳所有的子弹
        for i in range(1, self.bullets_num + 1):
            self.bullets_dict[i] = OneBullet()  # 该字典的键为1开始的自然数，值为一个OneBullets的实例


    def shoot_bullets(self):
        self.bullets_interval_time += player.time_passed

        if self.bullets_interval_time > self.bullets_hz:  # 每过一段时间，发射一颗子弹
            self.bullets_interval_time = 0  # 将 interval_time 重置

            i = 1
            while self.bullets_dict[i].bullets_fly_flag and i < self.bullets_num:
                i += 1  # 检索哪颗子弹的飞行标签为否

            self.bullets_dict[i].bullets_shoot_flag = True
            self.bullets_dict[i].bullets_fly_flag = True  # 将这颗子弹的发射标签和飞行标签改为是

        for i in range(1, self.bullets_num + 1):
            self.bullets_dict[i].one_bullet()  # 运行每颗子弹的控制程序
bullets = Bullets()


class OneEnemy:  # OneEnemy用来控制一个小敌机
    enemy_shoot_flag = False  # 这是敌机的发射标签，该标签标志这个敌机是否需要被发射
    enemy_fly_flag = False  # 这是敌机的飞行标签， 该标签标志这个敌机是否在飞行状态

    start_enemy_pos_x = randint(0, w - enemy_image.get_width())
    start_enemy_pos_y = -enemy_image.get_height()  # 敌机的初始位置

    stop_enemy_pos_x = -10
    stop_enemy_pos_y = -enemy_image.get_height() - 20  # 敌机不在飞行时的位置

    enemy_pos_x = stop_enemy_pos_x
    enemy_pos_y = stop_enemy_pos_y

    enemy_speed_x = uniform(0.03, 0.2)
    enemy_speed_y = uniform(0.03, 0.15)  # 敌机的速度，以后可以把速度做成随机的

    enemy_direction = randint(1, 2)  # 敌机的飞行方向，奇数代表左，偶数代表右
    enemy_move_time = randint(1000, 5000)  # 向一个方向飞行的时间，每过这么多时间，改变飞行方向；单位：毫秒
    enemy_has_moved_time = 0  # 朝某方向已经飞行的时；单位：毫秒

    time_passed = player.time_passed

    def one_enemy(self):
        self.time_passed = player.time_passed  # 从上一帧到这一帧的历时

        if self.enemy_shoot_flag and not self.enemy_fly_flag:  # 判断这个敌机的发射标签和飞行标签
            self.enemy_shoot_flag = False  # 将发射标签改为否

            self.enemy_speed_x = uniform(0.03, 0.2)
            self.enemy_speed_y = uniform(0.03, 0.13)

            self.start_enemy_pos_x = randint(0, w - enemy_image.get_width())
            self.enemy_pos_x = self.start_enemy_pos_x
            self.enemy_pos_y = self.start_enemy_pos_y  # 设置敌机的初始位置

        if self.stop_enemy_pos_y + 10 < self.enemy_pos_y < h:  # 判断这个敌机是否在屏幕中
            window.blit(enemy_image, (self.enemy_pos_x, self.enemy_pos_y))  # 显示敌机

            self.enemy_fly_flag = True  # 将飞行标签改为是

            self.enemy_has_moved_time += self.time_passed

            self.enemy_pos_y += self.time_passed * self.enemy_speed_y  # y方向匀速向下飞行

            if self.enemy_pos_x < 10:  # 若敌机到达了屏幕左边缘
                self.enemy_direction = 2  # 将飞行方向改为向右
                self.enemy_move_time = randint(500, 2000)
                self.enemy_has_moved_time = 0  # 重置飞行时间

            elif self.enemy_pos_x > w - enemy_image.get_width() - 10:  # 若敌机到达右边缘
                self.enemy_direction = 1
                self.enemy_move_time = randint(500, 2000)
                self.enemy_has_moved_time = 0

            if self.enemy_has_moved_time > self.enemy_move_time:  # 到需要改变飞行方向时
                self.enemy_direction += 1
                self.enemy_move_time = randint(500, 2000)
                self.enemy_has_moved_time = 0

            if self.enemy_direction % 2 == 1:  # 判断飞行方向
                self.enemy_pos_x -= self.time_passed*self.enemy_speed_x  # 向左飞
            else:
                self.enemy_pos_x += self.time_passed*self.enemy_speed_x  # 向右飞
        else:  # 若这个敌机飞出屏幕
            self.enemy_fly_flag = False  # 将敌机飞行标签改为否

            self.enemy_pos_x = self.stop_enemy_pos_x
            self.enemy_pos_y = self.stop_enemy_pos_y  # 将其位置设置为不在飞行时的位置


class Enemies:  # Enemies用来控制所有的敌机
    enemies_num = 35  # 敌机总数量
    enemies_now_num = 1  # 当前难度敌机的数量

    difficulty_interval_time = 0  # 从上次难度增加到现在的历时；单位：毫秒
    difficulty_hz = 10000  # 每经过这么多时间，就增加一次难度，即增加敌机数量并加快敌机频率；单位：毫秒

    enemies_interval_time = 3700  # 从上一次发射敌机到现在的时间；单位：毫秒
    enemies_hz = 3700  # 每经过这么多时间，发射一波敌机，该变量随难度增加而变小；单位：毫秒

    def __init__(self):
        self.enemies_dict = {}  # 该字典用来容纳所有的敌机
        for i in range(1, self.enemies_num + 1):
            self.enemies_dict[i] = OneEnemy()  # 该字典的键为从1开始的自然数，值为OneEnemy的一个实例

    def shoot_enemies(self):
        self.difficulty_interval_time += player.time_passed

        if self.difficulty_interval_time > self.difficulty_hz:  # 随时间增加难度，即增加每一波发射敌机的数量
            self.difficulty_interval_time = 0  # 重置时间

            self.enemies_now_num += 1

            self.enemies_hz -= 30



        self.enemies_interval_time += player.time_passed
        if self.enemies_interval_time > self.enemies_hz:  # 每过一段时间，发射一波敌机
            self.enemies_interval_time = 0  # 重置时间

            for k in range(1, self.enemies_now_num + 1):  # 根据当前难度增加一波发射的敌机数量
                i = 1
                while self.enemies_dict[i].enemy_fly_flag and i < self.enemies_num:
                    i += 1  # 检索哪个敌机不在飞行状态

                self.enemies_dict[i].enemy_shoot_flag = True
                self.enemies_dict[i].enemy_fly_flag = True  # 将这个敌机的发射标签和飞行标签改为是

        for i in range(1, self.enemies_num + 1):
            self.enemies_dict[i].one_enemy()  # 运行每个敌机的控制程序
enemies = Enemies()


class Damage:  # Damage用来使子弹能击毁敌机，并计分
    hit = False  # 标志子弹是否击中敌机
    score = 0  # 得分

    def check(self, bullet_x, bullet_y, enemy_x, enemy_y):  # 该方法用来检测子弹是否击中
        if enemy_x < bullet_x < enemy_x + enemy_image.get_width():
            if enemy_y < bullet_y < enemy_y + enemy_image.get_height():  # 若子弹和敌机位置重合，则记为击中
                self.hit = True
        else:
            self.hit = False

    def damage(self):
        for i in range(1, bullets.bullets_num + 1):
            for k in range(1, enemies.enemies_num + 1):  # 检测每一个子弹和敌机
                self.check(bullets.bullets_dict[i].bullet_pos_x, bullets.bullets_dict[i].bullet_pos_y,
                           enemies.enemies_dict[k].enemy_pos_x, enemies.enemies_dict[k].enemy_pos_y)

                if self.hit:  # 若击中
                    bullets.bullets_dict[i].bullets_fly_flag = False  # 将子弹飞行标签设置为否
                    bullets.bullets_dict[i].bullet_pos_x = bullets.bullets_dict[i].stop_bullet_pos_x
                    bullets.bullets_dict[i].bullet_pos_y = bullets.bullets_dict[i].stop_bullet_pos_y
                    # 将其位置设置为不在飞行时的位置

                    enemies.enemies_dict[k].enemy_fly_flag = False  # 将敌机飞行标签改为否
                    enemies.enemies_dict[k].enemy_pos_x = enemies.enemies_dict[k].stop_enemy_pos_x
                    enemies.enemies_dict[k].enemy_pos_y = enemies.enemies_dict[k].stop_enemy_pos_y
                    # 将其位置设置为不在飞行时的位置

                    self.score += 1
damage = Damage()


class Game:  # 游戏主程序
    gameover = False  # 标志游戏是否结束

    def check(self, enemy_x, enemy_y, player_x, player_y):  # 检测游戏是否结束
        if player_x < enemy_x < player_x + player_image.get_width() or player_x < enemy_x + enemy_image.get_width() < player_x + player_image.get_width():
            if player_y < enemy_y < player_y + player_image.get_height() or player_y < enemy_y + enemy_image.get_height() < player_y + player_image.get_height():
                self.gameover = True  # 检测敌机是否和玩家战机相撞

        if enemy_y > h:
            self.gameover = True  # 检测敌机是否飞出屏幕


    @staticmethod
    def run():  # 运行游戏
        key.key_flag()
        player.player_move()
        bullets.shoot_bullets()
        enemies.shoot_enemies()
        damage.damage()


    @staticmethod
    def end():  # 结束游戏
        font_big = pygame.font.Font('字体.ttf', 40)
        font_small = pygame.font.Font('字体.ttf', 32)
        gameover_text = font_big.render('Game Over :(', 1, (0, 0, 0))
        score_text = font_small.render('Your score:%d' % damage.score, 1, (0, 0, 0))

        window.blit(gameover_text, (w / 2 - 115, 0))
        window.blit(score_text, (w / 2 - 105, h / 2 - 300))  # 显示Game Over和得分


    def game(self):
        if self.gameover:
            self.end()
        else:
            self.run()

        for i in range(1, enemies.enemies_num + 1):
            self.check(enemies.enemies_dict[i].enemy_pos_x, enemies.enemies_dict[i].enemy_pos_y,
                       player.player_pos_x, player.player_pos_y)
game = Game()



while True:  # 主循环
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  # 得到退出命令时结束程序

    pygame.event.pump()  # 我不知道这句话什么意思，但是没有它就没法获取键盘事件
    pygame.display.update()  # 刷新屏幕

    window.blit(background_image, (0, 0))  # 显示背景
    game.game()  # 运行游戏






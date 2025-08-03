import sys

from symbol import yield_arg

import pygame

from button import Button

from setting import Setting

from time import sleep

from game_stats import GameStats

from random import randint

from bullet import Bullet

from ship import Ship

from scoreboard import Scoreboard

from alien import Alien

class AlienInvasion:
    """管理游戏资源和行为"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()#这个东东用来初始化背景的
        self.clock = pygame.time.Clock()
        self.setting = Setting()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.setting.screen_width = self.screen.get_rect().width
        self.setting.screen_height = self.screen.get_rect().height
        self.screen = pygame.display.set_mode((self.setting.screen_width, self.setting.screen_height))
        self.random_number = randint(2, 10)
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption('小曼波打飞机')#这里是定义窗口左上角的名称的

        #创建存储游戏统计信息的实例，并创建记分牌
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)


        self.bullets = pygame.sprite.Group()#Group()这个类类似于列表
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.ship = Ship(self)

        #让游戏在一开始处于非活动状态
        self.game_active = False


        #按钮系统
        self._create_menu_buttons()
        self.difficulty = "normal"

    def _create_menu_buttons(self):
        """创建所有菜单按钮"""
        # Play按钮（）
        self.play_button = Button(self, "Play", y_offset=100)
        # 新增难度按钮
        self.easy_button = Button(self, "Easy", y_offset=-60)
        self.normal_button = Button(self, "Normal", y_offset=0)
        self.hard_button = Button(self, "Hard", y_offset=60)

        # 设置不同颜色
        self.easy_button.button_color = (0, 200, 0)  # 绿色
        self.normal_button.button_color = (0, 100, 200)  # 蓝色
        self.hard_button.button_color = (200, 0, 0)  # 红色


    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()#放在self._update_bullets()后面才行
            self.clock.tick(60)
            self.update_screen()
    def _check_events(self):
        """响应按键和鼠标实践"""
        for event in pygame.event.get():#在同一帧内，if-elif 会按顺序检查事件，但 Pygame 的事件队列（pygame.event.get()）会一次性返回所有未处理的事件（包括同时触发的按键）。例如：同时按住 左键+上键 时，Pygame 会生成两个独立的 KEYDOWN 事件（一个左键，一个上键），并在同一帧内依次处理：pygame.event.get() 会一次性处理当前帧中所
            # 有待处理的事件，并且每个事件都是独立检测和执行的。这是 Pygame 事件系统的核心机制。以下是详细解释
            if event.type == pygame.QUIT:
                sys.exit()


            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)#这里的event从第42行那里得的
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_play_button(self, mouse_pos):
        """选择难度和在玩家单击play按钮时开始新游戏"""
        if not self.game_active:
            # 检测难度选择
            if self.easy_button.rect.collidepoint(mouse_pos):
                self.difficulty = "easy"
            elif self.normal_button.rect.collidepoint(mouse_pos):
                self.difficulty = "normal"
            elif self.hard_button.rect.collidepoint(mouse_pos):
                self.difficulty = "hard"
            # 原书Play按钮检测
            elif self.play_button.rect.collidepoint(mouse_pos):
                self._start_game()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
    def _start_game(self):
        """根据难度设置并启动游戏"""
        if self.difficulty == "easy":
            self.setting.bullet_speed = 10
            self.setting.alien_speed = 3
            self.setting.ship_speed = 10
        elif self.difficulty == "normal":
            self.setting.bullet_speed = 6
            self.setting.alien_speed = 6
            self.setting.ship_speed = 7
        elif self.difficulty == "hard":
            self.setting.bullet_speed = 61
            self.setting.alien_speed = 10
            self.setting.ship_speed = 5


        self.stats.reset_stats()#检测还有多少飞船（就是说还有多少条命）
        self.game_active = True
        self.bullets.empty()
        self.aliens.empty()
        self._create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)#用来在游戏开始时隐藏光标


    def _check_keydown_events(self, event):
        """响应按下"""
        if event.key == pygame.K_KP1:
            self._fire_bullet()

        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
                # 向右移动飞船
            self.ship.rect.x += 1
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
            # 向左移动飞船
            self.ship.rect.x -= 1

        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
            # 向上移动飞船
            self.ship.rect.y -= 1

        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
            # 向下移动飞船
            self.ship.rect.y += 1
        elif event.key == pygame.K_q:#注意要开大写打，不然人物会停，英文模式
            sys.exit()

    def _check_keyup_events(self, event):
        """响应释放"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False


    def _fire_bullet(self):
        """创建一颗子弹，并将其加如编组bullets"""
        if len(self.bullets) < self.setting.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """更新子弹的位置并删除已消失的子弹"""
        #更新子弹的位置
        self.bullets.update()

        #删除已消失的子弹
        for bullet in self.bullets.copy():  # 在使用for循坏遍历列表（或pygame编组）时2，python要求该列表长度在整个循坏中保持不变，这意味着不能从for循坏遍历的列表或编组中删除元素，因此必须遍历编组的副本，用copy()方法来实现
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()


    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left > 0:
            #将ships_left 减1并更新在飞船与外星人碰撞后还剩多少条命
            self.stats.ships_left -= 1
            self.sb.prep_ships()
        #清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()

        #创建一个新的外星舰队，并将飞船放在屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()

            #暂停
            sleep(1)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕的下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.setting.screen_height:
                #像飞船被撞到一样进行处理
                self._ship_hit()
                break

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞"""
        #删除发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)#True和False值会使对应的对象在双方触碰时决定是否消失，True是消失，False相反
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.setting.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            #删除现有的子弹并创建一个新的外星舰队和将飞船位置重置为屏幕中底部
            self.bullets.empty()
            self._create_fleet()
            self.setting.increase_speed()
            self.ship.center_ship()

            #提高等级
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """ 检查是否有外星人位于屏幕边缘，并更新整个外形舰队的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        #检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollide(self.ship, self.aliens, False):#spritecollide()函数接收两个实参，一个精灵和一个编组，它检查编组是否有成员与精灵发生了碰撞，并在找到与精灵发生碰撞的成员后停止遍历编组，这里，它遍历aliens编组，并返回找到的第一个与飞船发生碰撞的外星人
            self._ship_hit()

        #检查是否有外星人到达了屏幕的下边缘
        self._check_aliens_bottom()

    def _create_fleet(self):
        """创建一个外星舰队"""
        #创建一个外星人，再不断添加，直到没有空间添加外星人为止
        #外星人的间距为外星人的宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.setting.screen_height - 3 * alien_height):
            while current_x < (self.setting.screen_width - 10 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            #添加一行外星人后，重置x值并递增y值
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self,x_position,y_position):
        """创建一个外星人并将其放在当前行中"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


    def _check_fleet_edges(self):
        """在有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """将整个外星舰队向下移动，并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.setting.fleet_drop_speed
        self.setting.fleet_direction *= -1




    def update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.setting.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.game_active:
            # 绘制标题
            title_font = pygame.font.SysFont(None, 72)#pygame.font.SysFont() 是 Pygame 中用于加载系统字体的函数，主要作用是在游戏中创建文本渲染所需的字体对象。
            title = title_font.render("SIMPLE  INTRUSION", True, (255, 255, 255))#font.render() 是 Pygame 中用于将文字转换为可显示的图像表面（Surface）的核心方法。它的作用可以类比为"文字打印机"——把字符串转换成带有视觉样式的像素图像。
            title_rect = title.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery - 150))#center=(x,y) 参数
            self.screen.blit(title, title_rect)

            # 绘制所有按钮
            self.easy_button.draw_button()
            self.normal_button.draw_button()
            self.hard_button.draw_button()
            self.play_button.draw_button()

            # 显示当前难度
            hint_font = pygame.font.SysFont(None, 36)
            hint = hint_font.render(f"DIFFICULTY: {self.difficulty.upper()}", True, (255, 255, 255))
            hint_rect = hint.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery + 180))
            self.screen.blit(hint, hint_rect)

        pygame.display.flip()

if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()







#千磨万击还坚韧，一朝登上九冲天！————————记录我的第一个python项目，完成于2025年8月3日19时05分！





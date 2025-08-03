import pygame.font

from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """显示得分信息的类"""

    def __init__(self, ai_game):
        """初始化显示得分涉及的属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.setting = ai_game.setting
        self.stats = ai_game.stats

        #显示得分信息时使用的字体设置
        self.text_color = (230, 230, 220)
        self.font = pygame.font.SysFont(None, 48)#实例化字体对象

        #准备包含最高分和当前得分的图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将得分渲染为图像"""
        rounded_score = round(self.stats.score, -1)#round()函数通常让浮点数（第一个实参）精确到小数点后某一位，其中的小数位数由第二个实参指定。如果第二个实参是负数，round()会将第一个实参舍入到最近的10的整数倍，如10，100，1000等，这里是10

        score_str = f'{rounded_score:,}'#这里的：，使python在数值的合适位置插入逗号，生成如1，000，000（而不是1000000），但这里rounded_score是字符串，不是数值，所以不会有效果
        score_str = 'score:  ' + str(self.stats.score)#方法str()使数值转化为字符串,self.stats.score初始为零的
        self.score_image = self.font.render(score_str, True,
                                            self.text_color,self.setting.bg_color)

        #在屏幕右上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def prep_high_score(self):
        """将最高得分渲染为图像"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f'Highest score in history:  {high_score:,}'
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color,self.setting.bg_color)

        #将最高分放在屏幕顶部的中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top



    def check_high_score(self):
        """检查是否诞生了新的最高分"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
            self.save_high_score()



    def save_high_score(self):
        """将最高分保存到文件"""
        high_score_file = 'high_score.txt'
        with open(high_score_file, 'w') as f:
            f.write(str(self.stats.high_score))

    def load_high_score(self):
        """从文件加载最高分"""
        high_score_file = 'high_score.txt'
        try:
            with open(high_score_file, 'r') as f:
                return int(f.read())
        except (FileNotFoundError, ValueError):
            # 如果文件不存在或内容无效，返回0
            return 0


    def prep_level(self):
        """将等级渲染为图像"""
        level_str = "Current game progress:  " + str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                                            self.text_color,self.setting.bg_color)

        #将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10


    def prep_ships(self):
        """显示还余下多少飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)


    def show_score(self):
        """在屏幕上绘制得分，等级和余下的飞船数"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)




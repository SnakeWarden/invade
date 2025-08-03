import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """表示外星人的类"""

    def __init__(self, ai_game):
        """初始化外星人并设置其起始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        #加载外星人图像并设置其rect属性
        self.image = pygame.image.load('images/simple.bmp')
        self.rect = self.image.get_rect()

        #每个外星人最初都在屏幕的左上角附近
        self.rect.x = self.rect.width#在PyGame中，rect.x和rect.y表示矩形（这里是外星人图像）左上角的坐标
        self.rect.y = self.rect.height#self.rect.width和self.rect.height是外星人图像的宽度和高度

        #存储外星人的精确位置
        self.x = float(self.rect.x)


    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """向右或向左移动外星人"""
        self.x += self.setting.alien_speed * self.setting.fleet_direction

        self.rect.x = self.x












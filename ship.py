import pygame

from pygame.sprite import Sprite

class Ship(Sprite):
    """管理飞船的类"""
    def __init__(self,ai_game):
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        self.screen_rect = ai_game.screen.get_rect()

        #加载飞船图像并获取其外接矩形/s
        self.image = pygame.image.load('images/manbo.bmp')
        self.rect = self.image.get_rect()

        #每艘新飞船都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        #在飞船的属性x中存储一个浮点数
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # 移动标志 （飞船一开始不移动）
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    def update(self):
        """根据移动标志调整飞船的位置"""
        #更新飞船而不是rect对象的x值

        if  self.moving_right and self.rect.right < self.screen_rect.right:#这里如果self.moving_right的值为False的话也无法满足条件从而不运行下面的代码
            self.x += self.setting.ship_speed #如果想让向某一方向移动的更快的用+10这种来实现
        if self.moving_left and self.rect.left > 0:
            self.x -= self.setting.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.setting.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.setting.ship_speed
        self.rect.x = self.x
        self.rect.y = self.y
    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)


    def center_ship(self):
        """将飞船放在屏幕底部的中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
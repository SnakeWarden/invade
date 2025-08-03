import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """管理飞船所发射的子弹的类"""
    def __init__(self,ai_game):
        """在飞船的当前位置创建一个子弹对象"""
        super().__init__()#super是一个特殊的函数，让你能够调用父类的方法这里调用了父类Sprite的__init__方法，从而让Bullet包含这个方法定义的所有属性值，父类也叫作超类
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        self.color = self.setting.bullet_color

        #在（0，0）处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, self.setting.bullet_width,
                                self.setting.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        #存储用浮点数表示的子弹位置
        self.y = float(self.rect.y)
        self.width = self.setting.bullet_line_width#在pygame中，线框只能是整数而不能是浮点数
    def update(self):
        """向上更新移动子弹"""
        #更新子弹的准确位置
        self.y -= self.setting.bullet_speed
        #更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color,self.rect,self.width)#pygame.draw.rect(主屏幕, 颜色, 填充区域, 线宽=0)如果 线宽=0（默认），矩形会被完全填充
                                                                # 如果 线宽>0（如 1），矩形会以指定线宽绘制边框（不填充内部）。













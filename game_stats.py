
class GameStats:

    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.setting = ai_game.setting
        self.reset_stats()
        #在任何情况下都不应该重置最高分
        try:
            with open('high_score.txt', 'r') as f:  # 打开文件
                self.high_score = int(f.read())  # 读取内容并转为整数
        except (FileNotFoundError, ValueError):  # 处理文件不存在或内容非法的情况
            self.high_score = 0

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.setting.ship_limit
        self.score = 0
        self.level = 1


    def prep_high_score(self):
        """将最高分渲染为图像"""
        high_score = round(self.high_score, -1)
        high_score_str = f'{high_score:,}'





























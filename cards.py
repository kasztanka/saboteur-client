import os
from PyQt5.QtGui import QPixmap


class Card:

    WIDTH = 66
    HEIGHT = 104

    def __init__(self, filename, is_hand):
        self.filename = filename
        self.pixmap = QPixmap(filename)
        self.is_hand = is_hand

    def paint(self, painter, x, y=0):
        painter.drawPixmap(
            x * self.WIDTH,
            y * self.HEIGHT,
            self.WIDTH,
            self.HEIGHT,
            self.pixmap
        )


class TunnelCard(Card):

    def __init__(self, *args, x=None, y=None, **kwargs):
        super(TunnelCard, self).__init__(*args, **kwargs)
        ways = os.path.basename(self.filename).split('.')[0]
        self.up = 'U' in ways
        self.down = 'D' in ways
        self.left = 'L' in ways
        self.right = 'R' in ways
        self.mid = 'M' in ways
        self.x = x
        self.y = y
        self.is_rotated = False

    def rotate(self):
        self.up, self.down = self.down, self.up
        self.right, self.left = self.left, self.right
        self.is_rotated = not self.is_rotated

    def paint(self, painter, x, y):
        painter.save()
        if self.is_rotated:
            x_offset = self.WIDTH * x + self.WIDTH / 2
            y_offset = self.HEIGHT * y + self.HEIGHT / 2
            painter.translate(x_offset, y_offset)
            painter.rotate(180)
            painter.translate(-x_offset, -y_offset)
        super(TunnelCard, self).paint(painter, x, y)
        painter.restore()


class ActionCard(Card):
    pass


class GoalCard(TunnelCard):
    pass


class HealCard(ActionCard):
    pass


class BlockCard(ActionCard):
    pass


class DestroyCard(ActionCard):
    pass


class MapCard(ActionCard):
    pass

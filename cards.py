import os
from PyQt5.QtGui import QPixmap, QTransform


class Card:

    WIDTH = 66
    HEIGHT = 103

    def __init__(self, filename, is_hand):
        self.filename = filename
        self.pixmap = QPixmap(filename)
        self.is_hand = is_hand

    def paint(self, painter, x, y):
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

    def paint_tunnel(self, painter):
        if self.is_rotated:
            rotation = QTransform()
            rotation.rotate(180)
            painter.setTransform(rotation)
        super(TunnelCard, self).paint(painter, self.x, self.y)


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

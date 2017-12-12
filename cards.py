import os
from PyQt5.QtGui import QPixmap, QPen, QColor

from blockade import Blockade


class Card:

    WIDTH = 66
    HEIGHT = 104
    SELECTION_BORDER_WIDTH = 2

    def __init__(self, filename):
        self.filename = filename
        self.pixmap = QPixmap(filename)
        self.is_selected = False

    def paint(self, painter, x, y=0):
        painter.drawPixmap(
            x * self.WIDTH,
            y * self.HEIGHT,
            self.WIDTH,
            self.HEIGHT,
            self.pixmap
        )
        if self.is_selected:
            pen = QPen(QColor(0,255,0))
            pen.setWidth(5)
            painter.setPen(pen)
            painter.drawRect(
                x * self.WIDTH + self.SELECTION_BORDER_WIDTH,
                y * self.HEIGHT + self.SELECTION_BORDER_WIDTH,
                self.WIDTH - 2 * self.SELECTION_BORDER_WIDTH,
                self.HEIGHT - 2 * self.SELECTION_BORDER_WIDTH
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


class GoalCard(TunnelCard):
    def __init__(self, *args, **kwargs):
        super(GoalCard, self).__init__(*args, **kwargs)
        self.is_gold = 'gold' in self.filename


class ActionCard(Card):
    def __init__(self, *args, **kwargs):
        super(ActionCard, self).__init__(*args, **kwargs)
        filename = os.path.basename(self.filename).split('.')[0]
        self.blockade = Blockade[filename]


class HealCard(ActionCard):
    pass


class BlockCard(ActionCard):
    pass

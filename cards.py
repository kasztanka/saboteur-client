import os
from enum import Enum

from PyQt5.QtGui import QPixmap, QPen, QColor

from blockade import Blockade


class CardType(Enum):
    TUNNEL = 0
    BLOCK = 1
    HEAL = 2
    GOAL = 3


class Card:
    WIDTH = 66
    HEIGHT = 104
    SELECTION_BORDER_WIDTH = 2
    DIR_NAME = ''
    IMAGE_TYPE = '.jpg'

    def __init__(self, filename):
        self.filename = filename
        self.pixmap = QPixmap(
            os.path.join(self.DIR_NAME, filename) + self.IMAGE_TYPE
        )
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

    @classmethod
    def create_card(cls, name, card_type, x=None, y=None):
        card_mapping = {
            CardType.TUNNEL: TunnelCard,
            CardType.BLOCK: BlockCard,
            CardType.HEAL: HealCard,
            CardType.GOAL: GoalCard
        }
        card_class = card_mapping[card_type]
        return card_class(name, x=x, y=y)


class TunnelCard(Card):
    DIR_NAME = os.path.join('images', 'tunnels')

    def __init__(self, *args, x=None, y=None, **kwargs):
        super(TunnelCard, self).__init__(*args, **kwargs)
        self.up = 'U' in self.filename
        self.down = 'D' in self.filename
        self.left = 'L' in self.filename
        self.right = 'R' in self.filename
        self.mid = 'M' in self.filename
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
    DIR_NAME = os.path.join('images', 'goals')

    def __init__(self, *args, **kwargs):
        super(GoalCard, self).__init__(*args, **kwargs)
        self.is_gold = 'gold' in self.filename


class ActionCard(Card):
    def __init__(self, *args, **kwargs):
        super(ActionCard, self).__init__(*args, **kwargs)
        filename = os.path.basename(self.filename).split('.')[0]
        self.blockade = Blockade[filename]


class HealCard(ActionCard):
    DIR_NAME = os.path.join('images', 'heal')


class BlockCard(ActionCard):
    DIR_NAME = os.path.join('images', 'block')

from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsItem
from qtconsole.qt import QtCore

from cards import TunnelCard, Card


class Board(QGraphicsItem):

    ROWS = None
    COLS = None

    def __init__(self, window):
        super(Board, self).__init__()
        self.window = window
        self.cards = []

    def boundingRect(self):
        return QRectF(
            0, 0,
            Card.WIDTH * self.COLS,
            Card.HEIGHT * self.ROWS
        )

    def mousePressEvent(self, event):
        pos = event.pos()
        self.tile_clicked(
            event.button(),
            int(pos.x() / Card.WIDTH),
            int(pos.y() / Card.HEIGHT)
        )
        self.update()
        super(Board, self).mousePressEvent(event)

    def tile_clicked(self, button, x, y):
        if 0 <= x < self.COLS and 0 <= y < self.ROWS:
            self.cards.append(TunnelCard('images/tunnels/DL.jpg', False, x=x, y=y))


class GameBoard(Board):

    ROWS = 4
    COLS = 6

    def __init__(self, window):
        super(GameBoard, self).__init__(window)
        self.add_initial_cards()

    def add_initial_cards(self):
        self.cards.append(TunnelCard('images/tunnels/UDL.jpg', is_hand=False, x=0, y=3))
        self.cards.append(TunnelCard('images/tunnels/UDM.jpg', is_hand=False, x=0, y=2))
        self.cards.append(TunnelCard('images/tunnels/LRM.jpg', is_hand=False, x=1, y=1))

    def reset_cards(self):
        self.cards = []

    def paint(self, painter, option, widget):
        for card in self.cards:
            card.paint(painter, card.x, card.y)



class HandBoard(Board):

    ROWS = 1
    COLS = 6

    def paint(self, painter, option, widget):
        for i, card in enumerate(self.cards):
            card.paint(painter, x=i, y=0)

    def add_card(self, card):
        self.cards.append(card)

    def tile_clicked(self, button, x, y):
        if button == QtCore.Qt.RightButton:
            if x < len(self.cards):
                self.cards[x].rotate()
        else:
            super(HandBoard, self).tile_clicked(button, x, y)
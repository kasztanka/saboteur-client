from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsItem

from cards import TunnelCard, Card


class GameBoard(QGraphicsItem):

    ROWS = 4
    COLS = 6

    def __init__(self, main_window):
        super(GameBoard, self).__init__()
        self.main_window = main_window
        self.cards = []

        self.cards.append(TunnelCard('images/tunnels/UDL.jpg', is_hand=False, x=0, y=3))
        self.cards.append(TunnelCard('images/tunnels/UDM.jpg', is_hand=False, x=0, y=2))
        self.cards.append(TunnelCard('images/tunnels/LRM.jpg', is_hand=False, x=1, y=1))

    def reset_cards(self):
        self.cards = []

    def boundingRect(self):
        return QRectF(
            0, 0,
            Card.WIDTH * GameBoard.COLS,
            Card.HEIGHT * GameBoard.ROWS
        )

    def select(self, x, y):
        if 0 <= x < self.COLS and 0 <= y < self.ROWS:
            self.cards.append(TunnelCard('images/tunnels/DL.jpg', False, x=x, y=y))

    def paint(self, painter, option, widget):
        for card in self.cards:
            card.paint_tunnel(painter)

    def mousePressEvent(self, event):
        pos = event.pos()
        self.select(
            int(pos.x() / Card.WIDTH),
            int(pos.y() / Card.HEIGHT)
        )
        self.update()
        super(GameBoard, self).mousePressEvent(event)
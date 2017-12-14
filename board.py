from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsScene, QGraphicsView
from qtconsole.qt import QtCore

from cards import Card, GoalCard, TunnelCard, BlockCard, HealCard


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
            self.window.play_tunnel_card(x, y)

    def add_card(self, card):
        self.cards.append(card)

    def remove_selected_card(self):
        self.cards = list(filter(lambda c: not c.is_selected, self.cards))
        self.update()

    def setup(self, ui_board):
        board_scene = QGraphicsScene(ui_board)
        board_scene.addItem(self)
        board_scene.setSceneRect(
            0, 0,
            Card.WIDTH * self.COLS,
            Card.HEIGHT * self.ROWS
        )
        ui_board.setScene(board_scene)
        ui_board.setCacheMode(QGraphicsView.CacheBackground)


class GameBoard(Board):
    ROWS = 5
    COLS = 10

    def reset_cards(self):
        self.cards = [
            TunnelCard('UDLRM1', x=0, y=2),
            GoalCard('UDLRM_gold', x=9, y=0),
            GoalCard('ULM_coal', x=9, y=2),
            GoalCard('URM_coal', x=9, y=4)
        ]

    def paint(self, painter, option, widget):
        for card in self.cards:
            card.paint(painter, card.x, card.y)


class HandBoard(Board):
    ROWS = 1
    COLS = 10

    def __init__(self, window):
        super(HandBoard, self).__init__(window)
        self.cards.append(TunnelCard('UDL'))
        self.cards.append(TunnelCard('LRM'))
        self.cards.append(TunnelCard('DRM'))
        self.cards.append(BlockCard('LAMP'))
        self.cards.append(BlockCard('TRUCK'))
        self.cards.append(HealCard('LAMP_TRUCK'))

    def paint(self, painter, option, widget):
        for i, card in enumerate(self.cards):
            card.paint(painter, x=i, y=0)

    def tile_clicked(self, button, x, y):
        if x < len(self.cards):
            if button == QtCore.Qt.RightButton:
                if isinstance(self.cards[x], TunnelCard):
                    self.cards[x].rotate()
            else:
                for card in self.cards:
                    card.is_selected = False
                self.cards[x].is_selected = True
                self.window.selected_card = self.cards[x]

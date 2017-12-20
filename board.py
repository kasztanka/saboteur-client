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
        self.cards = None
        self.reset_cards()

    def reset_cards(self):
        self.cards = [[None for _ in range(self.COLS)] for _ in range(self.ROWS)]

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

    def paint(self, painter, option, widget):
        for y, row in enumerate(self.cards):
            for x, col in enumerate(row):
                if self.cards[y][x]:
                    self.cards[y][x].paint(painter, x, y)

    def tile_clicked(self, button, x, y):
        raise NotImplementedError()


class GameBoard(Board):
    ROWS = 5
    COLS = 10

    def reset_cards(self):
        super(GameBoard, self).reset_cards()
        self.add_card(TunnelCard('UDLRM1'), x=0, y=2)
        self.add_card(GoalCard('UDLRM_gold'), x=9, y=0)
        self.add_card(GoalCard('ULM_coal'), x=9, y=2)
        self.add_card(GoalCard('URM_coal'), x=9, y=4)

    def add_card(self, card, x, y):
        self.cards[y][x] = card
        self.update()

    def remove_card(self, x, y):
        self.cards[y][x] = None
        self.update()

    def tile_clicked(self, button, x, y):
        if 0 <= x < self.COLS and 0 <= y < self.ROWS:
            self.window.play_tunnel_card(x, y)


class HandBoard(Board):
    ROWS = 1
    COLS = 10

    def __init__(self, window):
        super(HandBoard, self).__init__(window)
        self.cards[0] = []
        self.hand_cards = self.cards[0]

    def tile_clicked(self, button, x, y):
        if x < len(self.hand_cards):
            if button == QtCore.Qt.RightButton:
                if isinstance(self.hand_cards[x], TunnelCard):
                    self.hand_cards[x].rotate()
            else:
                for card in self.hand_cards:
                    card.is_selected = False
                self.hand_cards[x].is_selected = True
                self.window.selected_card = self.hand_cards[x]

    def add_card(self, card):
        self.hand_cards.append(card)
        self.update()

    def remove_card(self, x):
        self.hand_cards.pop(x)
        self.update()



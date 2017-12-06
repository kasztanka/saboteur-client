from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsItem


class GameBoard(QGraphicsItem):

    CARD_WIDTH = 66
    CARD_HEIGHT = 103
    ROWS = 4
    COLS = 6

    def __init__(self, main_window):
        super(GameBoard, self).__init__()
        self.main_window = main_window
        self.cards = None
        self.reset_cards()
        self.cards[2][5] = QPixmap('images/1.jpg')
        self.cards[1][0] = QPixmap('images/2.jpg')
        self.cards[1][1] = QPixmap('images/2.jpg')

    def reset_cards(self):
        self.cards = [
            [0 for _ in range(GameBoard.COLS)]
                for _ in range(GameBoard.ROWS)
        ]

    def boundingRect(self):
        return QRectF(
            0, 0,
            GameBoard.CARD_WIDTH * GameBoard.COLS,
            GameBoard.CARD_HEIGHT * GameBoard.ROWS
        )

    def select(self, x, y):
        self.cards[y][x] = QPixmap('images/2.jpg')

    def paint(self, painter, option, widget):
        for y in range(GameBoard.ROWS):
            for x in range(GameBoard.COLS):
                if self.cards[y][x]:
                    painter.drawPixmap(
                        x * GameBoard.CARD_WIDTH,
                        y * GameBoard.CARD_HEIGHT,
                        GameBoard.CARD_WIDTH,
                        GameBoard.CARD_HEIGHT,
                        self.cards[y][x]
                    )

    def mousePressEvent(self, event):
        pos = event.pos()
        self.select(
            int(pos.x() / GameBoard.CARD_WIDTH),
            int(pos.y() / GameBoard.CARD_HEIGHT)
        )
        self.update()
        super(GameBoard, self).mousePressEvent(event)
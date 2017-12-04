# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'saboteur.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.game_board = QtWidgets.QGraphicsView(self.centralwidget)
        self.game_board.setMinimumSize(QtCore.QSize(550, 400))
        self.game_board.setObjectName("game_board")
        self.verticalLayout_4.addWidget(self.game_board)
        self.cards_in_hand = QtWidgets.QGraphicsView(self.centralwidget)
        self.cards_in_hand.setMinimumSize(QtCore.QSize(550, 0))
        self.cards_in_hand.setObjectName("cards_in_hand")
        self.verticalLayout_4.addWidget(self.cards_in_hand)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.join_room = QtWidgets.QPushButton(self.centralwidget)
        self.join_room.setObjectName("join_room")
        self.gridLayout.addWidget(self.join_room, 1, 1, 1, 1)
        self.create_room = QtWidgets.QPushButton(self.centralwidget)
        self.create_room.setObjectName("create_room")
        self.gridLayout.addWidget(self.create_room, 0, 1, 1, 1)
        self.room_name = QtWidgets.QTextEdit(self.centralwidget)
        self.room_name.setMaximumSize(QtCore.QSize(16777215, 30))
        self.room_name.setObjectName("room_name")
        self.gridLayout.addWidget(self.room_name, 0, 0, 1, 1)
        self.available_rooms = QtWidgets.QComboBox(self.centralwidget)
        self.available_rooms.setObjectName("available_rooms")
        self.gridLayout.addWidget(self.available_rooms, 1, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.players_list = QtWidgets.QListView(self.centralwidget)
        self.players_list.setObjectName("players_list")
        self.verticalLayout_3.addWidget(self.players_list)
        self.chat = QtWidgets.QTextEdit(self.centralwidget)
        self.chat.setMinimumSize(QtCore.QSize(0, 200))
        self.chat.setMaximumSize(QtCore.QSize(16777215, 200))
        self.chat.setObjectName("chat")
        self.verticalLayout_3.addWidget(self.chat)
        self.send_message = QtWidgets.QPushButton(self.centralwidget)
        self.send_message.setObjectName("send_message")
        self.verticalLayout_3.addWidget(self.send_message)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Sabotazysta"))
        self.join_room.setText(_translate("MainWindow", "Dolacz"))
        self.create_room.setText(_translate("MainWindow", "Stworz pokoj"))
        self.send_message.setText(_translate("MainWindow", "Wyslij"))


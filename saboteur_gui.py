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
        MainWindow.resize(1028, 709)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.game_board = QtWidgets.QGraphicsView(self.centralwidget)
        self.game_board.setMinimumSize(QtCore.QSize(800, 550))
        self.game_board.setObjectName("game_board")
        self.verticalLayout_4.addWidget(self.game_board)
        self.hand_board = QtWidgets.QGraphicsView(self.centralwidget)
        self.hand_board.setMinimumSize(QtCore.QSize(800, 105))
        self.hand_board.setObjectName("hand_board")
        self.verticalLayout_4.addWidget(self.hand_board)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.player_name = QtWidgets.QLineEdit(self.centralwidget)
        self.player_name.setObjectName("player_name")
        self.verticalLayout_3.addWidget(self.player_name)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.join_room = QtWidgets.QPushButton(self.centralwidget)
        self.join_room.setObjectName("join_room")
        self.gridLayout.addWidget(self.join_room, 3, 1, 1, 1)
        self.create_room = QtWidgets.QPushButton(self.centralwidget)
        self.create_room.setObjectName("create_room")
        self.gridLayout.addWidget(self.create_room, 2, 1, 1, 1)
        self.available_rooms = QtWidgets.QComboBox(self.centralwidget)
        self.available_rooms.setObjectName("available_rooms")
        self.gridLayout.addWidget(self.available_rooms, 3, 0, 1, 1)
        self.room_name = QtWidgets.QLineEdit(self.centralwidget)
        self.room_name.setObjectName("room_name")
        self.gridLayout.addWidget(self.room_name, 2, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.players_list = QtWidgets.QListWidget(self.centralwidget)
        self.players_list.setObjectName("players_list")
        self.verticalLayout_3.addWidget(self.players_list)
        self.draw_card = QtWidgets.QPushButton(self.centralwidget)
        self.draw_card.setObjectName("draw_card")
        self.verticalLayout_3.addWidget(self.draw_card)
        self.chat = QtWidgets.QTextEdit(self.centralwidget)
        self.chat.setMinimumSize(QtCore.QSize(0, 200))
        self.chat.setMaximumSize(QtCore.QSize(16777215, 200))
        self.chat.setReadOnly(True)
        self.chat.setObjectName("chat")
        self.verticalLayout_3.addWidget(self.chat)
        self.new_message = QtWidgets.QLineEdit(self.centralwidget)
        self.new_message.setObjectName("new_message")
        self.verticalLayout_3.addWidget(self.new_message)
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
        self.label.setText(_translate("MainWindow", "Sabotażysta"))
        self.player_name.setPlaceholderText(_translate("MainWindow", "Twój nick"))
        self.join_room.setText(_translate("MainWindow", "Dołącz"))
        self.create_room.setText(_translate("MainWindow", "Stwórz pokój"))
        self.draw_card.setText(_translate("MainWindow", "Dobierz kartę"))
        self.send_message.setText(_translate("MainWindow", "Wyślij"))


from PyQt5.QtWidgets import QMessageBox

from saboteur_client import IncorrectActionError


def validate_action(func):
    def safe_action(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except IncorrectActionError as e:
            print(e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText('Ta akcja jest niedozwolona')
            msg.setWindowTitle('Niepoprawna akcja')
            msg.exec_()

    return safe_action


def active_player_required(func):
    def func_for_active_player(self, *args, **kwargs):
        if self.local_player and self.local_player.is_active:
            func(self, *args, **kwargs)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText('Poczekaj na swoją turę')
            msg.setWindowTitle('Błędny ruch')
            msg.exec_()

    return func_for_active_player


def selected_card_required(func):
    def func_with_selected_card(self, *args, **kwargs):
        if self.selected_card:
            func(self, *args, **kwargs)
            self.hand_board.remove_selected_card()

    return func_with_selected_card

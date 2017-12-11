from PyQt5.QtWidgets import QMessageBox

from blockade import Blockade


class IncorrectActionError(Exception):
    pass


def validate_action(func):
    def safe_action(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except IncorrectActionError as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(str(e))
            msg.setWindowTitle('Niepoprawna akcja')
            msg.exec_()
    return safe_action


def active_player_required(func):
    def func_for_active_player(self, *args, **kwargs):
        if self.local_player and self.local_player.is_active:
            func(self, *args, **kwargs)
        else:
            raise IncorrectActionError('Poczekaj na swoją turę')
    return func_for_active_player


def selected_card_required(func):
    def func_with_selected_card(self, *args, **kwargs):
        if self.selected_card:
            func(self, *args, **kwargs)
            self.hand_board.remove_selected_card()
            self.selected_card.is_selected = False
            self.selected_card = None
    return func_with_selected_card


def validate_blockade(func):
    def func_with_blockade_validated(self, blockade, *args):
        if isinstance(blockade, Blockade):
            func(self, blockade, *args)
        else:
            raise IncorrectActionError('Niepoprawna wartość blokady')
    return func_with_blockade_validated

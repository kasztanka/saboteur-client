def active_player_required(func):
    def func_for_active_player(self, *args, **kwargs):
        if self.local_player and self.local_player.is_active:
            func(self, *args, **kwargs)
    return func_for_active_player


def selected_card_required(func):
    def func_with_selected_card(self, *args, **kwargs):
        if self.selected_card:
            func(self, *args, **kwargs)
    return func_with_selected_card


def player_name_required(func):
    def func_with_player_name_required(self, *args, **kwargs):
        if self.player_name:
            func(self, *args, **kwargs)
        else:
            self.show_warning('Wprowadź swoją nazwę')
    return func_with_player_name_required
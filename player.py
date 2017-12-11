from blockade import Blockade


class Player:

    def __init__(self, name, num_of_cards):
        self.name = name
        self.blockades = set()
        self.num_of_cards = num_of_cards
        self.is_active = False

    def get_blockades_str(self):
        return ''.join(map(lambda b: b.name[0], self.blockades))

    def add_blockade(self, blockade):
        self.blockades.add(blockade)

    def remove_blockade(self, blockade):
        for b in Blockade.get_matching_blockades(blockade):
            self.blockades.discard(b)

    def __str__(self):
        blockades_str = self.get_blockades_str()
        if blockades_str:
            result = result = '{} ({}) - blokady: {}'.format(
                self.name, self.num_of_cards, blockades_str
            )
        else:
            result = result = '{} ({})'.format(self.name, self.num_of_cards)
        result = result + ' <<' if self.is_active else result
        return result


class LocalPlayer(Player):

    def __init__(self, *args, **kwargs):
        super(LocalPlayer, self).__init__(*args, **kwargs)
        self.cards = []
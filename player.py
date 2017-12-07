from blockades import Blockades


class Player:

    def __init__(self, name, num_of_cards):
        self.name = name
        self.blockades = set()
        self.num_of_cards = num_of_cards

    def get_blockades_str(self):
        print(self.blockades)
        blockades_str = ''
        if Blockades.PICKAXE in self.blockades:
            blockades_str += 'P'
        if Blockades.LAMP in self.blockades:
            blockades_str += 'L'
        return blockades_str

    def __str__(self):
        blockades_str = self.get_blockades_str()
        if blockades_str:
            result = result = '{} ({}) - blokady: {}'.format(
                self.name, self.num_of_cards, blockades_str
            )
        else:
            result = result = '{} ({})'.format(self.name, self.num_of_cards)
        return result


class LocalPlayer(Player):

    def __init__(self, *args, cards, **kwargs):
        super(LocalPlayer, self).__init__(self, *args, **kwargs)
        self.cards = cards
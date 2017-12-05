class IncorrectActionError(Exception):
    pass

class SaboteurClient:

    def get_available_rooms(self):
        return ['Pokój Piotrka', 'Room 2']

    def create_room(self, room_name):
        pass

    def join_room(self, room_name):
        raise IncorrectActionError()
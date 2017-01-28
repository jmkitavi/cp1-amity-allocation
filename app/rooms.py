"""app/rooms"""


class Rooms(object):
    """ Rppms class """
    def __init__(self, room_name, room_type, max_occupants):
        self.room_name = room_name
        self.room_type = room_type
        self.max_occupants = max_occupants


class Living(Rooms):
    """ Living space class inheriting from Room class """
    def __init__(self, room_name, room_type, max_occupants=4):
        super().__init__(room_name, room_type="LIVING")


class Office(Rooms):
    """ Office class inheriting from Room class """
    def __init__(self, room_name, room_type, max_occupants=6):
        super().__init__(room_name, room_type="OFFICE")

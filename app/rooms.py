"""app/rooms"""


class Rooms(object):
    def __init__(self, room_name="", room_type="", max_occupants=""):
        self.room_name = room_name
        self.room_type = room_type
        self.max_occupants = max_occupants


class Living(Rooms):
    def __init__(self, room_name, room_type):
        super().__init__(room_name, room_type="LIVING", max_occupants=4)


class Office(Rooms):
    def __init__(self, room_name, room_type):
        super().__init__(room_name, room_type="OFFICE", max_occupants=6)

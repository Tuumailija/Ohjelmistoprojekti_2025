import projekti.RoomGeneration

class Main:
    def __init__(self):
        self.room = projekti.RoomGeneration.RoomGeneration()

    def generate(self):
        self.room.generate()
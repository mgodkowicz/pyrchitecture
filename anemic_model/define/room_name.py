class RoomName:
    def __init__(self, name: str):
        if len(name) > 100:
            raise ValueError(f"Illegal room name {name}")
        self.name = name

    def __str__(self):
        return self.name
APPLE_NORMAL = "normal"
APPLE_GOLD = "gold"
APPLE_SPOILED = "spoiled"

class Apple:
    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind

    def position(self):
        return (self.x, self.y)



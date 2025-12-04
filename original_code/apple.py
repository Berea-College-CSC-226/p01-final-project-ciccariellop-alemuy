APPLE_NORMAL = "normal"
APPLE_GOLD = "gold"
APPLE_SPOILED = "spoiled"

# Subtask I.D.2: Set point values

APPLE_NORMAL_POINTS = 1
APPLE_GOLD_POINTS = 2
APPLE_SPOILED_POINTS = -1

class Apple:
    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind

    def position(self):
        return (self.x, self.y)



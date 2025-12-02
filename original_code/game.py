import random
from apple import Apple, APPLE_NORMAL, APPLE_GOLD, APPLE_SPOILED
from snake import Snake

CELL_SIZE = 24
GRID_WIDTH = 20
GRID_HEIGHT = 20

class Game:
    def __init__(self):
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT
        self.snake = None
        self.apples = []
        self.score = 0
        self.state = "playing"
        self.spawn_apple()

        start_x = self.width // 2
        start_y = self.height // 2
        self.snake = Snake(start_x, start_y, length=3, direction="RIGHT")

    def spawn_apple(self):
        """Create a new Apple at a random position with a random type"""
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)

        r = random.random()
        if r < 0.8:
            kind = APPLE_NORMAL
        elif r < 0.95:
            kind = APPLE_GOLD
        else:
            kind = APPLE_SPOILED

        new_apple = Apple(x, y, kind)
        self.apples.append(new_apple)

    def handle_input(self):
        # read pygame events
        # if arrow key pressed: change snake direction
        pass

    def check_wall_collision(self, x, y):
        """Checks if the snake has collided with a wall"""
        if x < 0:
            return True
        if x >= self.width:
            return True
        if y < 0:
            return True
        if y >= self.height:
            return True
        return False

    def check_apple_collision(self, x, y):
        """Checks if the snake has collided with an apple"""
        index = 0
        while index < len(self.apples):
            apple = self.apples[index]
            if apple.x == x and apple.y == y:
                return apple, index
            index = index + 1
        return None, None
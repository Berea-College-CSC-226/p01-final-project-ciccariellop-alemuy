import random
import pygame as pg
from apple import Apple, APPLE_NORMAL, APPLE_GOLD, APPLE_SPOILED, APPLE_GOLD_POINTS, APPLE_NORMAL_POINTS, APPLE_SPOILED_POINTS
from snake import Snake

CELL_SIZE = 24
GRID_WIDTH = 20
GRID_HEIGHT = 20

BG_COLOR = (17,17,17)


class Game:
    def __init__(self):
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT
        self.running = True

        # Subtask I.D.1: Set score
        self.score = 0

        # Subtask I.B.1, I.B.2, and I.B.3: Snake position, initial length, and direction
        start_x = self.width // 2
        start_y = self.height // 2
        self.snake = Snake(start_x, start_y, 3, "RIGHT")

        self.apples = []

        self.state = "playing"

        self.spawn_apple() # Spawn first apple

    def spawn_apple(self):
        """Create a new Apple at a random position with a random type"""
        # Makes sure an apple doesn't spawn on a snake
        occupied = self.snake.occupies()

        # Subtask I.C.1 and I.C.2: Set the x and y position to a randomly generated integer, corresponding to a position on the window. Also assigned apple types

        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) in occupied:
                break

        r = random.random()
        if r < 0.8:
            kind = APPLE_NORMAL
        elif r < 0.95:
            kind = APPLE_GOLD
        else:
            kind = APPLE_SPOILED

        new_apple = Apple(x, y, kind)
        self.apples.append(new_apple)

    def handle_input(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.running = False

            elif event.type == pg.KEYDOWN: ## Subtask II.B: Interpret arrow keys
                if event.key == pg.K_UP or event.key == pg.K_w:
                    self.snake.set_direction("UP")
                elif event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.snake.set_direction("DOWN")
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.snake.set_direction("RIGHT")
                elif event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.snake.set_direction("LEFT")

    def tick(self):
        """
        One game step:
          - figure out where snake will go
          - check for wall, self, and apple collisions
          - move snake, possibly growing
        """
        if self.state != "playing":
            return

        # compute next head position based on current direction
        head_x, head_y = self.snake.head()

        dx = 0
        dy = 0
        if self.snake.direction == "UP":
            dx = 0
            dy = -1
        elif self.snake.direction == "DOWN":
            dx = 0
            dy = 1
        elif self.snake.direction == "LEFT":
            dx = -1
            dy = 0
        elif self.snake.direction == "RIGHT":
            dx = 1
            dy = 0

        new_x = head_x + dx
        new_y = head_y + dy

        # wall collision (III.B)
        if self.check_wall_collision(new_x, new_y):
            self.state = "game_over"
            return

        # self-collision (III.C)
        if self.snake.hits_self(new_x, new_y):
            self.state = "game_over"
            return

        # apple collision (III.A)
        eaten_apple, eaten_index = self.check_apple_collision(new_x, new_y)
        grow = False
        if eaten_apple is not None:
            grow = True

            # basic scoring – your partner can adjust this later (V.A, IV effects, etc.)
            if eaten_apple.kind == APPLE_NORMAL:
                self.score = self.score + APPLE_NORMAL_POINTS
            elif eaten_apple.kind == APPLE_GOLD:
                self.score = self.score + APPLE_GOLD_POINTS
            elif eaten_apple.kind == APPLE_SPOILED:
                self.score = self.score - APPLE_SPOILED_POINTS

            # remove eaten apple and spawn a new one (IV.B.3, IV.C)
            self.apples.pop(eaten_index)
            self.spawn_apple()

        # finally move the snake
        self.snake.step(grow)

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

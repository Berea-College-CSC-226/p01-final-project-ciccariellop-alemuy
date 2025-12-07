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

        # Subtask IV.B.2: Base game speed
        # This will change when we eat certain apple types.
        self.current_speed = 10
        self.speed = self.current_speed # normal speed

        self.slow_until = None  # time when slow effect ends

        # Spoiled apple timing (Subtask IV.B.2 / IV.C)
        # A spoiled apple lives 5 seconds, then reappears after 3–6 seconds.
        self.spoiled_lifetime_ms = 5000
        self.next_spoiled_at_ms = pg.time.get_ticks() + random.randint(3000, 6000)

        # Golden apple timing (Subtask IV.B.2 / IV.C)
        # A golden apple lives 5 seconds, then reappears after 10–20 seconds.
        self.gold_lifetime_ms = 5000
        self.next_gold_at_ms = pg.time.get_ticks() + random.randint(10000, 20000)

        # Ghost mode from golden apple (Subtask IV.B.2)
        # When active, snake can pass through its own body.
        self.ghost_until = None

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
            # only accept positions that are NOT on the snake
            if (x, y) not in occupied:
                break

        r = random.random()
        # NOTE: golden apples now use their own timing logic.
        # Here we only spawn normal or spoiled apples.
        if r < 0.75: #75%
            kind = APPLE_NORMAL
        else:         #25%
            kind = APPLE_SPOILED

        new_apple = Apple(x, y, kind)
        self.apples.append(new_apple)

    #NEW HELPERS FOR SPOILED / NORMAL APPLES

    def spawn_normal_apple(self):
        """Return a random (x, y) that is not on the snake and not on any apple."""
        occupied = set(self.snake.occupies())
        for apple in self.apples:
            occupied.add((apple.x, apple.y))

        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in occupied:
                return x, y

    def random_empty_position(self):
        """Spawn a guaranteed normal (red) apple at an empty position."""
        x, y = self.spawn_normal_apple()
        new_apple = Apple(x, y, APPLE_NORMAL)
        self.apples.append(new_apple)

    def spawn_spoiled_apple(self):
        """Spawn a spoiled apple at an empty position and remember when it appeared."""
        x, y = self.spawn_normal_apple()
        spoiled = Apple(x, y, APPLE_SPOILED)
        spoiled.spawn_time_ms = pg.time.get_ticks()
        self.apples.append(spoiled)

    def spawn_gold_apple(self):
        """Spawn a golden apple at an empty position and remember when it appeared."""
        x, y = self.spawn_normal_apple()
        gold = Apple(x, y, APPLE_GOLD)
        gold.spawn_time_ms = pg.time.get_ticks()
        self.apples.append(gold)

    def ensure_spoiled_has_normal(self):
        """
        Subtask IV.A / IV.C:
        If there is a spoiled apple, make sure there is at least one normal (red) apple.
        """
        has_spoiled = any(a.kind == APPLE_SPOILED for a in self.apples)
        if not has_spoiled:
            return

        has_normal = any(a.kind == APPLE_NORMAL for a in self.apples)
        if not has_normal:
            self.random_empty_position()

    def ensure_gold_has_normal(self):
        """
        Subtask IV.A / IV.C:
        If there is a golden apple, make sure there is at least one normal (red) apple.
        """
        has_gold = any(a.kind == APPLE_GOLD for a in self.apples)
        if not has_gold:
            return

        has_normal = any(a.kind == APPLE_NORMAL for a in self.apples)
        if not has_normal:
            self.random_empty_position()

    def update_spoiled_apples(self):
        """
        Handle spoiled apple lifetime and reappearance timing.

        Subtask IV.B.2 / IV.C:
        - A spoiled apple should appear together with a red apple.
        - It should remain on the screen for 5 seconds if not eaten.
        - After disappearing, it should reappear again after a random delay
          between 3 and 6 seconds.
        """
        now = pg.time.get_ticks()

        # 1) Remove any spoiled apples that have "expired" (older than 5s)
        i = 0
        while i < len(self.apples):
            apple = self.apples[i]
            if apple.kind == APPLE_SPOILED:
                # give it a timestamp if it doesn't have one yet
                if not hasattr(apple, "spawn_time_ms"):
                    apple.spawn_time_ms = now

                age = now - apple.spawn_time_ms
                if age >= self.spoiled_lifetime_ms:
                    # This spoiled apple timed out remove it and schedule the next one
                    self.apples.pop(i)
                    self.next_spoiled_at_ms = now + random.randint(3000, 6000)
                    # don't increment i because list shrank
                    continue
            i += 1

        #If there is no spoiled apple right now, see if it's time to spawn one
        if not any(a.kind == APPLE_SPOILED for a in self.apples):
            if self.next_spoiled_at_ms is not None and now >= self.next_spoiled_at_ms:
                self.spawn_spoiled_apple()
                # Once spawned, clear the timer until it either expires or is eaten
                self.next_spoiled_at_ms = None

        #Making sure any spoiled apple on screen has a normal red apple with it
        self.ensure_spoiled_has_normal()

    def update_gold_apples(self):
        """
        Handle golden apple lifetime & ghost mode timing.

        Subtask IV.B.2 / IV.C:
        - A golden apple should appear together with a red apple.
        - It should remain on the screen for 5 seconds if not eaten.
        - After disappearing, it should reappear again after a random delay
          between 10 and 20 seconds
        """
        now = pg.time.get_ticks()

        #Remove any golden apples that have "expired" (older than 5s)
        i = 0
        while i < len(self.apples):
            apple = self.apples[i]
            if apple.kind == APPLE_GOLD:
                # give it a timestamp if it doesn't have one yet
                if not hasattr(apple, "spawn_time_ms"):
                    apple.spawn_time_ms = now

                age = now - apple.spawn_time_ms
                if age >= self.gold_lifetime_ms:
                    # This golden apple timed out: remove it and schedule the next one
                    self.apples.pop(i)
                    self.next_gold_at_ms = now + random.randint(3000, 6000)
                    # don't increment i because list shrank
                    continue
            i += 1

        #If there is no golden apple right now, see if it's time to spawn one
        if not any(a.kind == APPLE_GOLD for a in self.apples):
            if self.next_gold_at_ms is not None and now >= self.next_gold_at_ms:
                self.spawn_gold_apple()
                # Once spawned, clear the timer until it either expires or is eaten
                self.next_gold_at_ms = None

        #Make sure any golden apple on screen has a normal red apple with it
        self.ensure_gold_has_normal()

    def ghost_active(self):
        """Return True if ghost mode (from golden apple) is currently active."""
        if self.ghost_until is None:
            return False
        return pg.time.get_ticks() < self.ghost_until

    def ghost_time_remaining_seconds(self):
        """
        Helper for how many seconds of Ghost Mode are left.
        Returns an integer number of seconds (0 if not active).
        """
        if not self.ghost_active():
            return 0
        remaining_ms = self.ghost_until - pg.time.get_ticks()
        if remaining_ms <= 0:
            return 0
        # Round up a bit so "1s" doesn't instantly disappear
        return remaining_ms // 1000 + 1

    def handle_input(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.running = False

            elif event.type == pg.KEYDOWN: #Subtask II.B: Interpret arrow keys
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
          - update spoiled/golden apple timers
          - figure out where snake will go
          - check for wall, self, and apple collisions
          - move snake, possibly growing
        """
        if self.state != "playing":
            return
        # Restore speed after spoiled apple effect ends
        if self.slow_until is not None:
            if pg.time.get_ticks() >= self.slow_until:
                self.speed = self.current_speed
                self.slow_until = None
        # Update spoiled and golden apple logic (Subtask IV.B.2 / IV.C)
        self.update_spoiled_apples()
        self.update_gold_apples()
        # compute next head position based on the SAME logic the snake uses
        # (Subtask IV.A: Identify apple type eaten on the correct tile)
        new_x, new_y = self.snake.peek_next_head()

        # wall collision (III.B)
        if self.check_wall_collision(new_x, new_y):
            self.state = "game_over"
            return

        # self-collision (III.C)
        # NOTE: Ghost mode from golden apple disables self-collision temporarily.
        if (not self.ghost_active()) and self.snake.hits_self(new_x, new_y):
            self.state = "game_over"
            return

        # apple collision (III.A + IV.A)
        eaten_apple, eaten_index = self.check_apple_collision(new_x, new_y)
        grow = False
        if eaten_apple is not None:
            grow = True

            # basic scoring – your partner can adjust this later (V.A, IV effects, etc.)
            if eaten_apple.kind == APPLE_NORMAL:
                self.score = self.score + APPLE_NORMAL_POINTS
            elif eaten_apple.kind == APPLE_GOLD:
                # Increase speed
                self.current_speed = min(self.speed + 1, 24)
                self.speed = self.current_speed
                print(self.speed)
                self.score = self.score + APPLE_GOLD_POINTS
                print(self.speed)
                # Ghost mode: snake can pass through its own body
                # for a fixed duration (5 seconds)
                self.ghost_until = pg.time.get_ticks() + 5000

                # Schedule next golden apple after a cooldown
                self.next_gold_at_ms = pg.time.get_ticks() + random.randint(10000, 20000)

            elif eaten_apple.kind == APPLE_SPOILED:
                #spoiled apples subtract points
                self.score = self.score + APPLE_SPOILED_POINTS
                # Subtask IV.B.2: Temporary slow effect (4 seconds)
                self.speed = 4
                self.slow_until = pg.time.get_ticks() + 4000
                print(self.speed)

            # remove eaten apple and spawn a new one (IV.B.3, IV.C)
            self.apples.pop(eaten_index)
            self.spawn_apple()

        # finally move the snake
        self.snake.step(grow)

    def check_wall_collision(self, x, y):
        """Checks if the snake has collided with a wall"""
        # Subtask III.B: Check wall collisions
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
        # Subtask III.A: Check snake-apple collisions
        index = 0
        while index < len(self.apples):
            apple = self.apples[index]
            if apple.x == x and apple.y == y:
                return apple, index
            index = index + 1
        return None, None

    def draw(self, screen, font):
        """Draw the snake, apples, and score."""
        screen.fill(BG_COLOR)

        # ----- Draw apples -----
        i = 0
        while i < len(self.apples):
            apple = self.apples[i]

            if apple.kind == APPLE_NORMAL:
                color = (220, 60, 60)  # red
            elif apple.kind == APPLE_GOLD:
                color = (255, 210, 80)  # gold/yellow
            else:
                color = (140, 140, 140)  # gray for spoiled

            rect = pg.Rect(
                apple.x * CELL_SIZE,
                apple.y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pg.draw.rect(screen, color, rect)
            i = i + 1

        # ----- Draw snake -----
        ghost_on = self.ghost_active()
        body = self.snake.occupies()
        i = 0
        while i < len(body):
            x, y = body[i]

            if ghost_on:
                # Ghost Mode colors – more "spectral"
                if i == 0:
                    color = (180, 220, 255)  # ghost head – light blue
                else:
                    color = (120, 170, 230)  # ghost body – softer blue
            else:
                # Normal colors
                if i == 0:
                    color = (80, 220, 120)  # head – brighter
                else:
                    color = (40, 160, 100)  # body – darker

            rect = pg.Rect(
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pg.draw.rect(screen, color, rect)
            i = i + 1

        # ----- Draw score -----
        text_surface = font.render("Score: " + str(self.score), True, (255, 255, 255))
        screen.blit(text_surface, (5, 5))

        # ----- Draw Ghost Mode timer (when it's active) -----
        remaining = self.ghost_time_remaining_seconds()
        if remaining > 0:
            ghost_text = f"Ghost: {remaining}s"
            ghost_surface = font.render(ghost_text, True, (180, 220, 255))
            screen.blit(ghost_surface, (5, 25))

        # Optional: simple game over text
        if self.state == "game_over":
            over_surface = font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(over_surface, (5, 45))

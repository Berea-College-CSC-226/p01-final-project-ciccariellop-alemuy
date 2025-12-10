import random
import pygame as pg
from apple import (
    Apple,
    APPLE_NORMAL,
    APPLE_GOLD,
    APPLE_SPOILED,
    APPLE_GOLD_POINTS,
    APPLE_NORMAL_POINTS,
    APPLE_SPOILED_POINTS,
)
from snake import Snake
from sprites import AppleSpriteManager

CELL_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 20

BG_COLOR = (17, 17, 17)


class Game:
    def __init__(self):
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT
        self.running = True

        #NEW: game state and player name (start screen)
        self.state = "menu"
        self.player_name_input = ""  # text the user is typing
        self.player_name = ""        # confirmed name after pressing Enter

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
        # Sprite manager for apples
        self.apple_sprites = AppleSpriteManager(CELL_SIZE)
        # Start screen will show first; apples will spawn once we start playing
        self.spawn_apple() # Spawn first apple

    #reset game for restart
    def start_new_game(self):
        """
        Reset all gameplay-related state for a fresh run.
        Keeps the current player_name.
        """
        self.score = 0

        # Reset speeds and timers
        self.current_speed = 10
        self.speed = self.current_speed
        self.slow_until = None

        self.spoiled_lifetime_ms = 5000
        self.next_spoiled_at_ms = pg.time.get_ticks() + random.randint(3000, 6000)

        self.gold_lifetime_ms = 5000
        self.next_gold_at_ms = pg.time.get_ticks() + random.randint(3000, 6000)

        self.ghost_until = None

        # Reset snake and apples
        start_x = self.width // 2
        start_y = self.height // 2
        self.snake = Snake(start_x, start_y, 3, "RIGHT")
        self.apples = []
        self.spawn_apple()

        # Back to gameplay
        self.state = "playing"

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
        if r < 0.75:  # 75%
            kind = APPLE_NORMAL
        else:         # 25%
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

    def handle_input(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.running = False

            elif event.type == pg.KEYDOWN:
                #MENU INPUT: typing the player name
                if self.state == "menu":
                    if event.key == pg.K_RETURN:
                        # Confirm name if empty, default to "Player"
                        if self.player_name_input.strip() == "":
                            self.player_name = "Player"
                        else:
                            self.player_name = self.player_name_input.strip()
                        # Move to gameplay
                        self.state = "playing"
                    elif event.key == pg.K_BACKSPACE:
                        # Remove last character
                        self.player_name_input = self.player_name_input[:-1]
                    else:
                        # Append printable characters
                        if event.unicode.isprintable() and len(self.player_name_input) < 16:
                            self.player_name_input += event.unicode

                # -------- GAMEPLAY INPUT: move snake --------
                elif self.state == "playing":
                    # Subtask II.B: Interpret arrow keys
                    if event.key == pg.K_UP or event.key == pg.K_w:
                        self.snake.set_direction("UP")
                    elif event.key == pg.K_DOWN or event.key == pg.K_s:
                        self.snake.set_direction("DOWN")
                    elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                        self.snake.set_direction("RIGHT")
                    elif event.key == pg.K_LEFT or event.key == pg.K_a:
                        self.snake.set_direction("LEFT")

                #GAME OVER INPUT: end game menu
                elif self.state == "game_over":
                    # 1 = restart game
                    if event.key == pg.K_1 or event.key == pg.K_KP1:
                        self.start_new_game()

                    # 2 = back to main menu
                    elif event.key == pg.K_2 or event.key == pg.K_KP2:
                        # Reset game world but go to menu; keep the typed/confirmed name
                        self.start_new_game()
                        self.state = "menu"

                    # 3 = quit game entirely
                    elif event.key == pg.K_3 or event.key == pg.K_KP3:
                        self.running = False

    def tick(self):
        """
        One game step:
          -if playing update spoiled/golden apple timers
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
                self.score = self.score + APPLE_GOLD_POINTS
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

        # ---------- MENU: start screen with name entry ----------
        if self.state == "menu":
            title = font.render("Welcome to Snake++", True, (255, 255, 255))
            prompt = font.render("Enter your name:", True, (200, 200, 200))
            name_text = font.render(self.player_name_input + "|", True, (80, 220, 120))
            hint = font.render("Press Enter to start", True, (200, 200, 200))

            screen.blit(title, (40, 40))
            screen.blit(prompt, (40, 80))
            screen.blit(name_text, (40, 110))
            screen.blit(hint, (40, 150))
            return
        # ----- Draw apples -----
        i = 0
        while i < len(self.apples):
            apple = self.apples[i]

            # Try to use a sprite image for this apple kind
            sprite = self.apple_sprites.get_surface(apple.kind)

            if sprite is not None:
                screen.blit(
                    sprite,
                    (apple.x * CELL_SIZE, apple.y * CELL_SIZE),
                )
            else:
                # Fallback: old rectangle drawing
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
                    CELL_SIZE,
                )
                pg.draw.rect(screen, color, rect)
            i = i + 1

        # ----- Draw snake -----
        body = self.snake.occupies()
        ghost = self.ghost_active()
        i = 0
        while i < len(body):
            x, y = body[i]
            if i == 0:
                # head – brighter; change slightly if ghost mode
                color = (80, 220, 120) if not ghost else (120, 220, 255)
            else:
                color = (40, 160, 100) if not ghost else (80, 180, 220)

            rect = pg.Rect(
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )
            pg.draw.rect(screen, color, rect)
            i = i + 1

        #Draw score and player name
        player_text = font.render(f"Player: {self.player_name or '???'}", True, (255, 255, 255))
        screen.blit(player_text, (5, 15))

        # Draw score on the right
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (screen.get_width() - score_text.get_width() - 5, 15))  # right-aligned

        if ghost:
            remaining_ms = self.ghost_until - pg.time.get_ticks()
            if remaining_ms < 0:
                remaining_ms = 0
            remaining_sec = remaining_ms // 1000
            ghost_text = font.render(f"Ghost: {remaining_sec}s", True, (180, 220, 255))
            screen.blit(ghost_text, (5, 55))

        # ---------- END GAME SCREEN ----------
        if self.state == "game_over":
            overlay = pg.Surface(screen.get_size(), pg.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            screen.blit(overlay, (0, 0))

            line1 = font.render(
                "Game Over. What would you like to do?", True, (255, 255, 255)
            )
            line2 = font.render("1 - Restart game", True, (200, 200, 200))
            line3 = font.render("2 - Main menu", True, (200, 200, 200))
            line4 = font.render("3 - Quit", True, (200, 200, 200))

            center_x = screen.get_width() // 2
            center_y = screen.get_height() // 2
            screen.blit(line1, (center_x - line1.get_width() // 2, center_y - 40))
            print()
            # Align all options using the same X as "Main menu" (line3)
            option_x = center_x - line3.get_width() // 2
            screen.blit(line2, (option_x, center_y - 10))  # Restart
            screen.blit(line3, (option_x, center_y + 20))  # Main menu
            screen.blit(line4, (option_x, center_y + 50))  # Quit

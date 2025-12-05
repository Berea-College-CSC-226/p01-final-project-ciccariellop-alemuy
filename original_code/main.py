import pygame as pg
from game import Game, GRID_WIDTH, GRID_HEIGHT, CELL_SIZE, BG_COLOR

def main():
    pg.init()

    # Subtask I.A.1: Set window size
    width = GRID_WIDTH * CELL_SIZE
    height = GRID_HEIGHT * CELL_SIZE
    screen = pg.display.set_mode((width, height))

    # Subtask I.A.3: Set game title
    pg.display.set_caption("Snake Game with Apples")

    font = pg.font.SysFont(None, 24)
    clock = pg.time.Clock()

    game = Game()

    while game.running:
        events = pg.event.get() # Subtask II.A: Handle keyboard input

        game.handle_input(events)
        game.tick()

        game.draw(screen,font)
        pg.display.flip()

        clock.tick(10)

        keys = pg.key.get_pressed() # Quit on press of escape key
        if keys[pg.K_ESCAPE]:
            game.running = False

    pg.quit()


if __name__ == "__main__":
    main()
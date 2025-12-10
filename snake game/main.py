#################################################################################
# Author: Yoseph Alemu, Pier Ciccariello
#
# Assignment: P01 Final Project – Snake Game
# Course: CSC 226
#
# Purpose:
# This project implements an interactive Snake game using Pygame.
# The game demonstrates object-oriented programming, event-driven design,
# collision detection, game state management, and sprite-ready rendering.
#################################################################################
# Acknowledgements:
# - Original concepts inspired by classic Snake games.
# - Boustrophedon Turtle Drawing assignment (earlier coursework reference).
# - Icons and images sourced from https://www.flaticon.com
# - ChatGPT (OpenAI) was used as a programming assistant to help with:
#   refactoring logic, documenting code, and understanding
#   design tradeoffs. All code was reviewed, modified, and integrated
#   by the authors.
#################################################################################

import pygame as pg
from game import Game, GRID_WIDTH, GRID_HEIGHT, CELL_SIZE, BG_COLOR

def main():
    pg.init()

    # Subtask I.A.1: Set window size
    width = GRID_WIDTH * CELL_SIZE
    height = GRID_HEIGHT * CELL_SIZE
    screen = pg.display.set_mode((width, height))

    # Subtask I.A.3: Set game title
    pg.display.set_caption("Snake++")

    font = pg.font.SysFont(None, 24)
    clock = pg.time.Clock()

    game = Game()

    while game.running:
        events = pg.event.get() # Subtask II.A: Handle keyboard input

        game.handle_input(events)
        game.tick()

        game.draw(screen,font)
        pg.display.flip()

        clock.tick(game.speed)

        keys = pg.key.get_pressed() # Quit on press of escape key
        if keys[pg.K_ESCAPE]:
            game.running = False

    pg.quit()


if __name__ == "__main__":
    main()
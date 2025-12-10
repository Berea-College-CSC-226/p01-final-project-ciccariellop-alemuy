# Test Suite for Snake Game
from snake import Snake
from apple import Apple, APPLE_NORMAL
from game import Game


def test_snake_movement():
    snake = Snake(5, 5, 3, "RIGHT")
    snake.step(False)
    assert snake.head() == (6, 5)

def test_snake_growth():
    snake = Snake(8, 8, 3, "RIGHT")
    before_len = len(snake.occupies())
    snake.step(True)
    assert len(snake.occupies()) == before_len + 1

def test_apple_collision():
    game = Game()
    apple = Apple(4, 7, APPLE_NORMAL)
    game.apples = [apple]
    apple, index = game.check_apple_collision(4, 7)
    assert apple is game.apples[0]

def test_wall_collision():
    game = Game()
    assert game.check_wall_collision(-1, 5) == True
    assert game.check_wall_collision(0, 0) == False

def main():
    test_snake_movement()
    test_snake_growth()
    test_apple_collision()
    test_wall_collision()
    print("Minimal tests passed!")

if __name__ == "__main__":
    main()
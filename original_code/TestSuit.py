# Subtask I – Initialization tests


def test_game_window_methods_exist():
    gw = GameWindow()
    gw.set_window_size()
    gw.set_background_color()
    gw.set_game_title()


def test_snake_initialization_methods_exist():
    s = Snake()
    s.set_starting_position()
    s.set_starting_length()
    s.set_initial_direction()


def test_apple_manager_methods_exist():
    am = AppleManager()
    am.generate_apple_positions()
    am.assign_apple_types()


def test_score_system_methods_exist():
    ss = ScoreSystem()
    ss.initialize_score()
    ss.set_point_values()

# Subtask II – Input handling tests


def test_input_handler_methods_exist():
    ih = InputHandler()
    ih.detect_keyboard_input()
    ih.interpret_arrow_keys()
    ih.update_snake_direction()



# Subtask III – Collision detection tests


def test_collision_system_methods_exist():
    cs = CollisionSystem()
    cs.check_apple_collision()
    cs.check_wall_collision()
    cs.check_self_collision()



# Subtask IV – Apple effects tests


def test_apple_effects_methods_exist():
    ae = AppleEffects()
    ae.determine_apple_type()
    ae.apply_effect()
    ae.increase_length()
    ae.apply_special_effect()
    ae.remove_eaten_apple()
    ae.spawn_new_apple()

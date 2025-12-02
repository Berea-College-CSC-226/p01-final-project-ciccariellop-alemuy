class Snake:
    def __init__(self, start_x, start_y, length, direction):
        """ Create a snake starting at (start_x, start_y). """
        self.direction = direction
        self.queued_direction = direction
        self.body = []
        i = 0
        while i < length:       # build the body to the left of the head for a horizontal start
            self.body.append((start_x - i, start_y))
            i = i + 1

    def head(self):
        """Return the (x, y) of the snake's head"""
        return self.body[0]

    def set_direction(self, new_direction):
        self.queued_direction = new_direction

    def _apply_direction_change(self):
        """ Prevent a 180-degree turn (e.g., RIGHT → LEFT in one move). Only update direction if the new one isn't directly opposite """
        current = self.direction
        new = self.queued_direction

        if current == "UP" and new == "DOWN":
            return
        if current == "DOWN" and new == "UP":
            return
        if current == "LEFT" and new == "RIGHT":
            return
        if current == "RIGHT" and new == "LEFT":
            return
        self.direction = new

    def step(self, grow):
        """ Move the snake one cell in the current direction """
        self._apply_direction_change()
        dx = 0
        dy = 0

        if self.direction == "UP":
            dx = 0
            dy = -1
        elif self.direction == "DOWN":
            dx = 0
            dy = 1
        elif self.direction == "LEFT":
            dx = -1
            dy = 0
        elif self.direction == "RIGHT":
            dx = 1
            dy = 0

        head_x, head_y = self.head()
        new_head = (head_x + dx, head_y + dy)   # add new head to the front
        self.body.insert(0, new_head)    # remove tail unless we're growing
        if not grow:
            self.body.pop()

    def occupies(self):
        """ Return a copy of the list of (x, y) positions the snake is currently on"""
        return self.body[:]

    def hits_self(self, x, y):
        """ Return True if (x, y) is on the snake's body (excluding the current head)"""
        i = 1
        while i < len(self.body):
            if self.body[i] == (x, y):
                return True
            i = i + 1
        return False

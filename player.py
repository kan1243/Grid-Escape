TILE_SIZE = 60

class Player:
    def __init__(self, start_pos):
        self.start_pos = tuple(start_pos)
        self.pos = tuple(start_pos)
        self.last_dir = (0, 0)
        self.pixel_x = self.pos[1] * TILE_SIZE
        self.pixel_y = self.pos[0] * TILE_SIZE
        
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        
        self.move_speed = 600  # pixels per second

    def reset(self):
        self.pos = self.start_pos
        self.last_dir = (0, 0)

    def move(self, direction, level):
        dr, dc = direction
        self.last_dir = direction

        next_pos = (self.pos[0] + dr, self.pos[1] + dc)

        if not level.is_blocked(next_pos):
            self.pos = next_pos

            self.target_x = next_pos[1] * TILE_SIZE
            self.target_y = next_pos[0] * TILE_SIZE

    def update(self, dt):
        dx = self.target_x - self.pixel_x
        dy = self.target_y - self.pixel_y

        speed = self.move_speed * (dt / 1000)

        if abs(dx) > speed:
            self.pixel_x += speed if dx > 0 else -speed
        else:
            self.pixel_x = self.target_x

        if abs(dy) > speed:
            self.pixel_y += speed if dy > 0 else -speed
        else:
            self.pixel_y = self.target_y

    def next_pos(self):
        dr, dc = self.last_dir
        return (self.pos[0] + dr, self.pos[1] + dc)
    
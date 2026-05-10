class Level:
    def __init__(self, data):
        self.grid_size = tuple(data["grid_size"])
        self.start = tuple(data["start"])
        self.goal = tuple(data["goal"])

        self.glass = set(map(tuple, data.get("glass", [])))
        self.original_glass = set(self.glass)
        self.broken_glass = set()
        self.walls = set(map(tuple, data.get("walls", [])))
        self.ice = set(map(tuple, data.get("ice", [])))
        self.traps = set(map(tuple, data.get("traps", [])))
        self.spikes = set(map(tuple, data.get("spikes", [])))
        self.lava = set(map(tuple, data.get("lava", [])))

        self.teleporters = {
            k: [tuple(v[0]), tuple(v[1])]
            for k, v in data.get("teleporters", {}).items()
        }

        self.barriers = {
            k: set(map(tuple, v))
            for k, v in data.get("barriers", {}).items()
        }

        self.switches = {
            k: set(map(tuple, v))
            for k, v in data.get("switches", {}).items()
        }
        self.reset_state()

    def reset_state(self):
        self.barrier_active = {k: True for k in self.barriers}

    def reset_glass(self):
        self.glass = set(self.original_glass)
        self.broken_glass = set()

    def is_blocked(self, pos):
        r, c = pos

        # make player cannot move out grid
        if not (0 <= r < self.grid_size[0] and 0 <= c < self.grid_size[1]):
            return True

        if pos in self.walls:
            return True

        for k in self.barriers:
            if pos in self.barriers[k] and self.barrier_active[k]:
                return True

        return False
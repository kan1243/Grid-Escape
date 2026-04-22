class Mechanics:
    def __init__(self, level):
        self.level = level
        self.laser_timer = 0
        self.laser_on = True
        self.last_teleport_pos = None
        self.last_player_pos = None
        self.teleport_lock = False

    def update(self, dt):
        self.laser_timer += dt / 1000
        cycle = self.laser_timer % 3
        self.laser_on = cycle < 1

    def apply_all(self, player):

        if self.handle_trap(player):
            return "dead"

        prev_pos = self.last_player_pos  # mark the before move tile pos

        self.handle_ice(player)
        self.handle_teleport(player)
        self.handle_switch(player)
        self.handle_glass(player)

        if self.handle_lava(player):
            return "dead"
        
        if player.pos == self.level.goal:
            return "goal"

        # glass use prev_pos
        if prev_pos is not None:
            if prev_pos in self.level.glass and prev_pos != player.pos:
                self.level.glass.remove(prev_pos)
                self.level.broken_glass.add(prev_pos)

        # use last pos
        self.last_player_pos = player.pos

        if player.pos in self.level.broken_glass:
            return "dead"

        return "ok"

    def handle_trap(self, player):
        return player.pos in self.level.traps or player.pos in self.level.spikes

    def handle_ice(self, player):
        if player.pos in self.level.ice:
            next_pos = player.next_pos()
            
            if not self.level.is_blocked(next_pos):
                player.pos = next_pos

                # smooth movement
                player.target_x = next_pos[1] * 60
                player.target_y = next_pos[0] * 60

    def handle_teleport(self, player):

        # ===== CHECK LOCK =====
        if self.teleport_lock:
            # still on teleporter then still lock
            for pair in self.level.teleporters.values():
                if player.pos in pair:
                    return

            # move from teleporter then unlock
            self.teleport_lock = False
            return

        # ===== FIND MATCH FIRST =====
        for pair in self.level.teleporters.values():
            if player.pos == pair[0]:
                target = pair[1]
                break
            elif player.pos == pair[1]:
                target = pair[0]
                break
        else:
            return  # if no teleporter then end

        # ===== TELEPORT PART =====
        player.pos = target

        # set target pixel
        player.target_x = target[1] * 60
        player.target_y = target[0] * 60
        self.teleport_lock = True

    def handle_switch(self, player):
        for k in self.level.switches:
            if player.pos in self.level.switches[k]:
                self.level.barrier_active[k] = False

    def handle_glass(self, player):
        pos = player.pos

    # walk on glass step of then break
        if self.last_player_pos in self.level.glass and self.last_player_pos != pos:
            self.level.glass.remove(self.last_player_pos)
            self.level.broken_glass.add(self.last_player_pos)

    def handle_void(self, player):
        if player.pos in self.level.broken_glass:
            return True
        return False

    def handle_lava(self, player):
        if not self.laser_on:
            return False
        return player.pos in self.level.lava
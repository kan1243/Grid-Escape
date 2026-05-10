import json
import random
import pygame

from level import Level
from player import Player
from mechanics import Mechanics


class LevelManager:
    def __init__(self):
        # Store used variants for each level
        self.used_variants = {}

    def load_current_level(self, current_level):
        level_name = f"level{current_level + 1}"

        # Load level JSON
        with open(f"levels/{level_name}.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        variants = data["variants"]
        total_variants = len(variants)

        # Create used list if not exists
        if level_name not in self.used_variants:
            self.used_variants[level_name] = []

        # Find unused variants
        available = [
            i for i in range(total_variants)
            if i not in self.used_variants[level_name]
        ]

        # Reset if all variants were used
        if not available:
            self.used_variants[level_name] = []
            available = list(range(total_variants))

        # Select one variant randomly
        variant_index = random.choice(available)
        self.used_variants[level_name].append(variant_index)

        # Create objects
        level = Level(variants[variant_index])
        player = Player(level.start)
        mechanics = Mechanics(level)

        rows, cols = level.grid_size
        time_limit = data.get("time_limit", 15)

        # Initialize runtime values
        start_time = pygame.time.get_ticks()
        steps = 0
        death_count = 0

        print(
            "LEVEL", current_level + 1,
            "VARIANT", variant_index + 1
        )

        return {
            "level": level,
            "player": player,
            "mechanics": mechanics,
            "rows": rows,
            "cols": cols,
            "variant": variant_index,
            "time_limit": time_limit,
            "start_time": start_time,
            "steps": steps,
            "death_count": death_count
        }
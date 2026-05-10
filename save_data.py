import csv
import os
import pygame


class SaveData:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FILE = os.path.join(BASE_DIR, "stats.csv")

    FIELDNAMES = [
        "player_name",
        "level",
        "variant",
        "attempt",
        "steps",
        "time_used",
        "deaths",
        "result",
        "first_pass"
    ]

    def __init__(self):
        # Store latest attempt number for each
        # (player_name, level, variant)
        self.attempt_dict = {}

        # Store whether player has already
        # completed a level and variant
        self.first_pass_dict = {}

        # Load previous data from stats.csv
        self._load_existing_data()

    # ===== Load previous data =====
    def _load_existing_data(self):
        if not os.path.exists(self.FILE):
            return

        if os.path.getsize(self.FILE) == 0:
            return

        try:
            with open(self.FILE, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                if reader.fieldnames is None:
                    return

                for row in reader:
                    try:
                        player_name = row["player_name"]
                        level = int(row["level"]) - 1
                        variant = int(row["variant"]) - 1
                        attempt = int(row["attempt"])
                        result = row["result"]

                        key = (player_name, level, variant)

                        current = self.attempt_dict.get(key, 0)
                        self.attempt_dict[key] = max(current, attempt)

                        if result == "win":
                            self.first_pass_dict[key] = True

                    except (KeyError, ValueError):
                        continue

        except Exception as e:
            print("Error loading stats.csv:", e)

    # ===== Helper Methods =====
    def _get_key(self, player_name, level, variant):
        return (player_name, level, variant)

    def _get_attempt(self, player_name, level, variant):
        key = self._get_key(player_name, level, variant)
        return self.attempt_dict.get(key, 0) + 1

    def _save_attempt(self, player_name, level, variant, attempt):
        key = self._get_key(player_name, level, variant)
        self.attempt_dict[key] = attempt

    def _is_first_pass(self, player_name, level, variant):
        key = self._get_key(player_name, level, variant)
        return key not in self.first_pass_dict

    def _mark_first_pass(self, player_name, level, variant):
        key = self._get_key(player_name, level, variant)
        self.first_pass_dict[key] = True

    def _time_used(self, start_time):
        return round(
            (pygame.time.get_ticks() - start_time) / 1000,
            2
        )

    # ===== Save Data =====
    def save_stat(self, data):
        file_exists = os.path.exists(self.FILE)
        write_header = (
            not file_exists or
            os.path.getsize(self.FILE) == 0
        )
    
        try:
            # Add newline if the last line does not end with '\n'
            if file_exists and os.path.getsize(self.FILE) > 0:
                with open(self.FILE, "rb+") as f:
                    f.seek(-1, os.SEEK_END)
                    last_char = f.read(1)
    
                    if last_char != b"\n":
                        f.write(b"\n")
    
            with open(self.FILE, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=self.FIELDNAMES
                )
    
                if write_header:
                    writer.writeheader()
    
                writer.writerow(data)
    
        except Exception as e:
            print("Error saving stats:", e)

    # ===== Record Win =====
    def record_win(
        self,
        current_level,
        current_variant,
        player_name,
        start_time,
        steps,
        death_count
    ):
        attempt = self._get_attempt(
            player_name,
            current_level,
            current_variant
        )

        first_pass = self._is_first_pass(
            player_name,
            current_level,
            current_variant
        )

        data = {
            "player_name": player_name,
            "level": current_level + 1,
            "variant": current_variant + 1,
            "attempt": attempt,
            "steps": steps,
            "time_used": self._time_used(start_time),
            "deaths": death_count,
            "result": "win",
            "first_pass": first_pass
        }

        self.save_stat(data)

        self._save_attempt(
            player_name,
            current_level,
            current_variant,
            attempt
        )

        if first_pass:
            self._mark_first_pass(
                player_name,
                current_level,
                current_variant
            )

    # ===== Record Lose =====
    def record_lose(
        self,
        current_level,
        current_variant,
        player_name,
        start_time,
        steps,
        death_count
    ):
        attempt = self._get_attempt(
            player_name,
            current_level,
            current_variant
        )

        data = {
            "player_name": player_name,
            "level": current_level + 1,
            "variant": current_variant + 1,
            "attempt": attempt,
            "steps": steps,
            "time_used": self._time_used(start_time),
            "deaths": death_count,
            "result": "lose",
            "first_pass": False
        }

        self.save_stat(data)

        self._save_attempt(
            player_name,
            current_level,
            current_variant,
            attempt
        )
import csv
import os

FILE = "stats.csv"

def save_stat(data):
    file_exists = os.path.exists(FILE)

    with open(FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "player_name",
            "level",
            "variant",
            "attempt",
            "steps",
            "time_used",
            "deaths",
            "result",
            "first_pass"
        ])

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)
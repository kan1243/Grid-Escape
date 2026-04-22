import csv
from collections import defaultdict
import pygame

def get_summary():
    data = defaultdict(list)

    try:
        with open("stats.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                level = int(row["level"])
                time = float(row["time_used"])
                deaths = int(row["deaths"])

                data[level].append((time, deaths))
    except:
        return {}

    summary = {}

    for level in data:
        times = [t for t, d in data[level]]
        deaths = [d for t, d in data[level]]

        summary[level] = {
            "avg_time": sum(times)/len(times),
            "max_time": max(times),
            "min_time": min(times),
            "avg_death": sum(deaths)/len(deaths)
        }

    return summary


def draw_stat_screen(screen, font_big, font_small, page):
    screen.fill((20,20,20))

    center_x = screen.get_width() // 2

    title = font_big.render("STATISTICS", True, (255,255,255))
    screen.blit(title, (center_x - title.get_width()//2, 50))

    summary = get_summary()

    headers = ["Level", "Avg", "Max", "Min", "Deaths"]

    for i, h in enumerate(headers):
        text = font_small.render(h, True, (200,200,200))
        screen.blit(text, (100 + i*180, 150))

    # ===== pagination =====
    levels = sorted(summary)
    ROWS_PER_PAGE = 8

    start = page * ROWS_PER_PAGE
    end = start + ROWS_PER_PAGE

    y = 200

    for level in levels[start:end]:
        d = summary[level]

        row = [
            str(level),
            f"{d['avg_time']:.2f}",
            f"{d['max_time']:.2f}",
            f"{d['min_time']:.2f}",
            f"{d['avg_death']:.2f}"
        ]

        for i, val in enumerate(row):
            text = font_small.render(val, True, (255,255,255))
            screen.blit(text, (100 + i*180, y))

        y += 50

    # ===== border =====
    table_rect = pygame.Rect(80, 180, screen.get_width()-160, screen.get_height()-260)
    pygame.draw.rect(screen, (80,80,80), table_rect, 2)  

def get_win_rate():
    import csv
    from collections import defaultdict

    # group by player + level + variant
    data = defaultdict(list)

    with open("stats.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["player_name"], int(row["level"]), int(row["variant"]))
            data[key].append(row)

    level_rates = defaultdict(list)

    for (player, level, variant), attempts in data.items():

        count = 0
        for row in attempts:
            count += 1
            if row["first_pass"] == "True":
                rate = 1 / count
                level_rates[level].append(rate)
                break

    # average per level
    final = {}
    for level in level_rates:
        final[level] = sum(level_rates[level]) / len(level_rates[level])

    return final        
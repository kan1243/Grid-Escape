import csv
import os
from collections import defaultdict
import pygame


class StatScreen:
    def __init__(self, screen, font_big, font_small):
        self.screen = screen
        self.font_big = font_big
        self.font_small = font_small

        self.page = 0          # 0 = summary table, 1 = win rate
        self.scroll_y = 0

        # Smaller font for graph labels
        self.graph_font = pygame.font.Font(
            "C:/Windows/Fonts/arial.ttf",
            24
        )

    # ==================================================
    # Basic Controls
    # ==================================================
    def reset(self):
        self.page = 0
        self.scroll_y = 0

    def handle_event(self, event):
        # ===== Keyboard =====
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back"

            elif event.key == pygame.K_RIGHT:
                self.page = min(1, self.page + 1)
                self.scroll_y = 0

            elif event.key == pygame.K_LEFT:
                self.page = max(0, self.page - 1)
                self.scroll_y = 0

        # ===== Mouse Wheel (Pygame 2) =====
        elif event.type == pygame.MOUSEWHEEL:
            if self.page == 0:
                self.scroll_y += event.y * 30

                min_scroll = self._get_min_scroll()
                self.scroll_y = max(min_scroll, min(0, self.scroll_y))

        # ===== Mouse Wheel (Older Pygame) =====
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.page == 0:
                if event.button == 4:
                    self.scroll_y += 30
                elif event.button == 5:
                    self.scroll_y -= 30

                min_scroll = self._get_min_scroll()
                self.scroll_y = max(min_scroll, min(0, self.scroll_y))

        return None

    def draw(self):
        if self.page == 0:
            self._draw_summary_page()
        else:
            self._draw_win_rate_page()

    # ==================================================
    # Data Loading
    # ==================================================
    def _get_csv_path(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, "stats.csv")

    def _load_rows(self):
        rows = []

        try:
            with open(self._get_csv_path(), "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    rows.append(row)

        except FileNotFoundError:
            pass

        return rows

    # ==================================================
    # Summary Data
    # ==================================================
    def _get_summary(self):
        data = defaultdict(list)

        for row in self._load_rows():
            try:
                level = int(row["level"])
                variant = int(row["variant"])
                time_used = float(row["time_used"])
                deaths = int(row["deaths"])

                data[(level, variant)].append(
                    (time_used, deaths)
                )

            except (KeyError, ValueError):
                continue

        summary = {}

        for key, values in data.items():
            times = [t for t, d in values]
            death_list = [d for t, d in values]

            summary[key] = {
                "avg_time": sum(times) / len(times),
                "max_time": max(times),
                "min_time": min(times),
                "avg_death": sum(death_list) / len(death_list)
            }

        return summary

    # ==================================================
    # Win Rate Data
    # ==================================================
    def _get_win_rate(self):
        # Group by player + level + variant
        grouped = defaultdict(list)

        for row in self._load_rows():
            try:
                key = (
                    row["player_name"],
                    int(row["level"]),
                    int(row["variant"])
                )
                grouped[key].append(row)

            except (KeyError, ValueError):
                continue

        # Store scores by level
        level_rates = defaultdict(list)

        for (player, level, variant), attempts in grouped.items():
            # Sort by attempt number
            attempts.sort(
                key=lambda r: int(r["attempt"])
            )

            score = 0.0
            count = 0

            for row in attempts:
                count += 1

                if str(row["first_pass"]).lower() == "true":
                    score = 1 / count
                    break

            # If never wins, score remains 0.0
            level_rates[level].append(score)

        # Average score for each level
        final = {}

        for level, rates in level_rates.items():
            final[level] = sum(rates) / len(rates)

        return final

    # ==================================================
    # Drawing Helpers
    # ==================================================
    def _draw_title(self, title_text):
        self.screen.fill((20, 20, 20))

        hint = self.graph_font.render(
            "Mouse Wheel: Scroll | Left/Right: Change Page | ESC: Return",
            True,
            (180, 180, 180)
        )
        self.screen.blit(hint, (20, 20))

        title = self.font_big.render(
            title_text,
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            title,
            (
                self.screen.get_width() // 2
                - title.get_width() // 2,
                70
            )
        )

    # ==================================================
    # Page 1: Summary Table
    # ==================================================
    def _draw_summary_page(self):
        self._draw_title("STATISTICS (Time,Avg Death)")

        table_rect = pygame.Rect(
            80,
            140,
            self.screen.get_width() - 160,
            self.screen.get_height() - 240
        )

        pygame.draw.rect(
            self.screen,
            (80, 80, 80),
            table_rect,
            2
        )

        headers = [
            "Level",
            "Variant",
            "Avg",
            "Max",
            "Min",
            "Deaths"
        ]

        col_x = [100, 230, 380, 560, 740, 920]

        for i, header in enumerate(headers):
            text = self.font_small.render(
                header,
                True,
                (220, 220, 220)
            )
            self.screen.blit(text, (col_x[i], 150))

        summary = self._get_summary()
        keys = sorted(summary.keys())

        self.screen.set_clip(table_rect)

        y = 200 + self.scroll_y

        for key in keys:
            level, variant = key
            d = summary[key]

            row = [
                str(level),
                str(variant),
                f"{d['avg_time']:.2f}",
                f"{d['max_time']:.2f}",
                f"{d['min_time']:.2f}",
                f"{d['avg_death']:.2f}"
            ]

            for i, value in enumerate(row):
                text = self.font_small.render(
                    value,
                    True,
                    (255, 255, 255)
                )
                self.screen.blit(text, (col_x[i], y))

            y += 50

        self.screen.set_clip(None)

        label = self.font_small.render(
            "Page 1: Summary Table",
            True,
            (200, 200, 200)
        )

        self.screen.blit(
            label,
            (
                self.screen.get_width() // 2
                - label.get_width() // 2,
                self.screen.get_height() - 60
            )
        )

    # ==================================================
    # Page 2: Win Rate Graph
    # ==================================================
    def _draw_win_rate_page(self):
        self._draw_title("WIN RATE")

        rates = self._get_win_rate()

        chart_rect = pygame.Rect(
            100,
            120,
            self.screen.get_width() - 200,
            self.screen.get_height() - 220
        )

        pygame.draw.rect(
            self.screen,
            (80, 80, 80),
            chart_rect,
            2
        )

        if not rates:
            return

        levels = sorted(rates.keys())
        n = len(levels)

        gap = 20

        bar_width = min(
            60,
            max(
                30,
                (chart_rect.width - 80 - gap * (n - 1)) // n
            )
        )

        max_bar_height = chart_rect.height - 120
        base_y = chart_rect.bottom - 40

        for i, level in enumerate(levels):
            rate = rates[level]
            height = int(rate * max_bar_height)

            x = chart_rect.x + 40 + i * (bar_width + gap)
            y = base_y - height

            # Draw bar
            pygame.draw.rect(
                self.screen,
                (100, 200, 255),
                (x, y, bar_width, height)
            )

            # Draw percentage
            pct = self.graph_font.render(
                f"{rate * 100:.1f}%",
                True,
                (255, 255, 255)
            )

            pct_x = (
                x + bar_width // 2
                - pct.get_width() // 2
            )
            pct_y = max(
                chart_rect.y + 10,
                y - 28
            )

            self.screen.blit(
                pct,
                (pct_x, pct_y)
            )

            # Draw level number
            lvl = self.graph_font.render(
                str(level),
                True,
                (255, 255, 255)
            )

            lvl_x = (
                x + bar_width // 2
                - lvl.get_width() // 2
            )

            self.screen.blit(
                lvl,
                (lvl_x, base_y + 5)
            )

        label = self.font_small.render(
            "Page 2: Win Rate Graph",
            True,
            (200, 200, 200)
        )

        self.screen.blit(
            label,
            (
                self.screen.get_width() // 2
                - label.get_width() // 2,
                self.screen.get_height() - 60
            )
        )

    # ==================================================
    # Scroll Limit
    # ==================================================
    def _get_min_scroll(self):
        summary = self._get_summary()
        row_count = len(summary)

        content_height = row_count * 50
        visible_height = self.screen.get_height() - 300

        return min(
            0,
            visible_height - content_height
        )
    
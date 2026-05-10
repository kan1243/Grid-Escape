# Data Visualization

This folder contains screenshots of the statistical visualization features used in the Grid Escape project. The purpose of these visualizations is to summarize player performance and evaluate the difficulty of each level.

---

## 1. Summary Table (`summary_table.png`)

The Summary Table displays aggregated statistics for each level variant based on all recorded gameplay data.

### Columns Description

- **Level** – The level number.
- **Variant** – The variant number of that level.
- **Avg** – Average completion time (in seconds) for successful attempts.
- **Max** – Maximum completion time.
- **Min** – Minimum completion time.
- **Deaths** – Average number of deaths before completing the level.

### Purpose

This table helps compare the difficulty of different level variants.

For example:
- A higher average time suggests that the level is more difficult.
- A higher average death count indicates that players fail more frequently.
- A large difference between Min and Max values suggests inconsistent player performance.

---

## 2. Win Rate Graph (`win_rate_graph.png`)

The Win Rate Graph shows the percentage of players who successfully completed each level on their first successful attempt.

### Calculation Method

Win Rate is calculated as:

Win Rate = (Number of First-Pass Wins / Total Players Who Attempted the Level) × 100

Only records marked with `first_pass = True` are counted as successful first-pass completions.

### Purpose

This graph provides an overview of level difficulty.

- Higher percentages indicate easier levels.
- Lower percentages indicate more challenging levels.
- Comparing win rates across levels helps identify which levels may require balancing.

---

## 3. Interpretation

From the sample data:

- Levels 2, 4, 8, and 10 have a 100% first-pass win rate, indicating that these levels are relatively easy.
- Level 6 has the lowest win rate (50%), suggesting that it is the most challenging level.
- Levels with higher average completion times and lower win rates generally represent greater difficulty.

---

## 4. Data Source

All statistics are generated from the `stats.csv` file, which stores:

- Player name
- Level and variant
- Attempt number
- Number of steps
- Time used
- Death count
- Result (win or lose)
- First-pass success

---

## 5. Conclusion

The statistical visualization system provides meaningful insights into player performance and level design. By combining summary tables and win-rate graphs, the project demonstrates how gameplay data can be analyzed to evaluate and improve puzzle game difficulty.

## Important Notes

There still two graph missing from the poposal.
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Define member timelines (name, start date, end date, color)
members = [
    # AIQ period
    ("Futaba Momo", "2018-01-01", "2018-08-31", "gray"),
    ("Shion Rina", "2018-01-01", "2018-08-31", "gray"),
    ("Saki Scream", "2018-01-01", "2018-12-31", "gray"),

    # LEIWAN period
    ("Anaru Rairai", "2022-11-04", "2022-11-13", "brown"),
    ("Kuroi Mashiro", "2018-08-01", "2023-04-01", "yellow"),
    ("Nekono Nemuko", "2018-08-01", "2024-06-11", "purple"),

    # Current members
    ("Mio Monster", "2019-02-01", "2025-05-01", "blue"),
    ("Uzuki Ayaka", "2019-02-01", "2025-05-01", "pink"),
    ("Aguri Pico", "2023-07-04", "2025-05-01", "green"),
    ("Shibuya Ryuka", "2023-07-04", "2025-05-01", "red"),
]

# Convert dates
def to_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")

# Plotting
fig, ax = plt.subplots(figsize=(12, 6))

for i, (name, start, end, color) in enumerate(members):
    ax.hlines(i, to_date(start), to_date(end), color=color, linewidth=4)
    ax.text(to_date(start), i + 0.1, name, fontsize=8, verticalalignment='bottom')

# Formatting
ax.set_yticks([])
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.set_title("Member Activity Timeline")
ax.set_xlabel("Time")
plt.tight_layout()
plt.grid(axis='x', linestyle='--', alpha=0.5)

# plt.show()
plt.savefig("leiwan_timeline.svg")

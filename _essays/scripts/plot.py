import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import seaborn as sns

def to_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")

mirakuru_members = [
    ("Jiujiu", "2025-03-16", "2026-04-30", "yellow"),
    ("Itsume", "2025-03-16", "2026-04-30", "green"),
    ("Sakura", "2025-03-16", "2026-04-30", "pink"),
    ("Koyoi", "2025-10-01", "2026-04-30", "blue"),
    ("Kaori", "2025-03-16", "2026-01-18", "purple"),
    ("Yukikoo", "2025-03-16", "2026-01-18", "white"),
    ("Shimizu", "2025-03-16", "2025-07-27", "lightblue"),
    ("Mizuki", "2025-03-16", "2025-11-02", "red"),
]

# 设置 seaborn 风格
sns.set_theme(style="whitegrid")

# 绘图
fig, ax = plt.subplots(figsize=(12, 6))

# 设置背景为浅灰
fig.patch.set_facecolor('#f0f0f0')  # 整个图的背景
ax.set_facecolor('#f0f0f0')         # 坐标区域背景

for i, (name, start, end, color) in enumerate(mirakuru_members):
    ax.hlines(i, to_date(start), to_date(end), color=color, linewidth=4)
    ax.text(to_date(start), i + 0.1, name, fontsize=9, verticalalignment='bottom', color='black')

# 添加竖着的虚线和时间节点

milestones = [
    ("2025.03.16", "2025-03-16"),
    ("2025.07.27", "2025-07-27"),
    ("2025.11.02", "2025-11-02"),
    ("2026.01.18", "2026-01-18"),
    # ("2026.04.30", "2026-04-30"),
]

for label, date in milestones:
    milestone_date = to_date(date)
    ax.axvline(milestone_date, color='gray', linestyle='--', alpha=0.3)
    ax.text(milestone_date, -0.5, label, fontsize=9, color='black', rotation=0, verticalalignment='center')
# 格式设置
ax.set_yticks([])
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.set_title("MIRAKURU Member Activity Timeline", fontsize=14, weight='bold')
ax.set_xlabel("Time")
plt.tight_layout()
plt.grid(axis='x', linestyle='--', alpha=0.6, color='gray')

# 保存
plt.savefig("mirakuru_timeline.svg", facecolor=fig.get_facecolor())

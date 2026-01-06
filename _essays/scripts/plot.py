import plotly.express as px
import pandas as pd
from datetime import datetime

# 数据
data = [
    ("Jiujiu", "2025-03-16", "2026-02-01"),
    ("Itsume", "2025-03-16", "2026-02-01"),
    ("Sakura", "2025-03-16", "2026-02-01"),
    ("Koyoi", "2025-10-01", "2026-02-01"),
    ("Kaori", "2025-03-16", "2026-01-18"),
    ("Yukikoo", "2025-03-16", "2026-01-18"),
    ("Shimizu", "2025-03-16", "2025-07-27"),
    ("Mizuki", "2025-03-16", "2025-11-02"),
]

df = pd.DataFrame(data, columns=["Member", "Start", "End"])
df["Start"] = pd.to_datetime(df["Start"])
df["End"] = pd.to_datetime(df["End"])

# ========= 新增：open-ended 设置 =========
OPEN_END = pd.Timestamp("2026-02-01")
open_ended_members = {"Jiujiu", "Itsume", "Sakura", "Koyoi"}

df["IsOpen"] = df["Member"].isin(open_ended_members)
df.loc[df["IsOpen"], "End"] = OPEN_END
# =======================================

# 手动颜色映射
member_colors = {
    "Jiujiu":   "#F5F514",
    "Itsume":   "#10B981",
    "Sakura":   "#EC4899",
    "Koyoi":    "#3B82F6",
    "Kaori":    "#8B5CF6",
    "Yukikoo":  "#F9F9F9",
    "Shimizu":  "#38BDF8",
    "Mizuki":   "#EF4444",
}

fig = px.timeline(
    df,
    x_start="Start",
    x_end="End",
    y="Member",
    color="Member",
    color_discrete_map=member_colors,
    title="MIRAKURU Member Activity Timeline",
)

# 风格
fig.update_layout(
    height=520,
    font=dict(family="Inter, Arial", size=13, color="#6B5E57"),
    title=dict(x=0.02, font=dict(size=22, color="#6B5E57")),
    plot_bgcolor="#FDF1E6",
    paper_bgcolor="#FDECEF",
    margin=dict(l=50, r=40, t=70, b=40),
)


fig.update_xaxes(
    showgrid=True,
    gridcolor="#EADFD6",
    zeroline=False,
    tickfont=dict(color="#6B5E57"),
)

fig.update_yaxes(
    showgrid=False,
    tickfont=dict(color="#6B5E57"),
)


# ========= 新增：open-ended 视觉提示 =========
for _, row in df[df["IsOpen"]].iterrows():
    fig.add_annotation(
        x=row["End"],
        y=row["Member"],
        text="→",
        showarrow=False,
        font=dict(size=18, color=member_colors[row["Member"]]),
        xanchor="left",
        yanchor="middle",
    )


for m in open_ended_members:
    fig.update_traces(selector=dict(name=m), opacity=0.7)



# ==========================================

# Milestones
milestones = {
    "2025.03.16": "2025-03-16",
    "2025.07.27": "2025-07-27",
    "2025.11.02": "2025-11-02",
    "2026.01.18": "2026-01-18",
}

for label, date in milestones.items():
    x = datetime.fromisoformat(date)
    fig.add_vline(x=x, line_dash="dot", line_color="#F5D38E", opacity=0.6)
    fig.add_annotation(
        x=x,
        y=1.02,
        xref="x",
        yref="paper",
        text=label,
        showarrow=False,
        font=dict(size=11, color="#666"),
        align="center",
    )

fig.update_traces(marker_line_width=0, opacity=0.9)

fig.write_html("mirakuru_timeline.html")
print("已生成：mirakuru_timeline.html")


# import plotly.express as px
# import pandas as pd
# from datetime import datetime

# # 数据
# data = [
#     ("Jiujiu", "2025-03-16", "2026-02-01"),
#     ("Itsume", "2025-03-16", "2026-02-01"),
#     ("Sakura", "2025-03-16", "2026-02-01"),
#     ("Koyoi", "2025-10-01", "2026-02-01"),
#     ("Kaori", "2025-03-16", "2026-01-18"),
#     ("Yukikoo", "2025-03-16", "2026-01-18"),
#     ("Shimizu", "2025-03-16", "2025-07-27"),
#     ("Mizuki", "2025-03-16", "2025-11-02"),
# ]

# df = pd.DataFrame(data, columns=["Member", "Start", "End"])
# df["Start"] = pd.to_datetime(df["Start"])
# df["End"] = pd.to_datetime(df["End"])

# # 统一现代配色（柔和 Material 风格）
# # palette = px.colors.qualitative.Set2
# member_colors = {
#     "Jiujiu":   "#F59E0B",
#     "Itsume":   "#10B981",
#     "Sakura":   "#EC4899",
#     "Koyoi":    "#3B82F6",
#     "Kaori":    "#8B5CF6",
#     "Yukikoo":  "#64748B",
#     "Shimizu":  "#38BDF8",
#     "Mizuki":   "#EF4444",
# }

# fig = px.timeline(
#     df,
#     x_start="Start",
#     x_end="End",
#     y="Member",
#     color="Member",
#     color_discrete_map=member_colors,
#     title="MIRAKURU Member Activity Timeline",
# )

# # 风格微调
# fig.update_layout(
#     template="plotly_white",
#     height=500,
#     font=dict(family="Inter, Arial", size=13),
#     title=dict(x=0.02, font=dict(size=20)),
#     plot_bgcolor="white",
#     paper_bgcolor="white",
#     margin=dict(l=40, r=40, t=60, b=40),
# )

# # 网格和轴
# fig.update_xaxes(showgrid=True, gridcolor="#eaeaea", zeroline=False)
# fig.update_yaxes(showgrid=False)

# from datetime import datetime

# milestones = {
#     "2025.03.16": "2025-03-16",
#     "2025.07.27": "2025-07-27",
#     "2025.11.02": "2025-11-02",
#     "2026.01.18": "2026-01-18",
# }

# for label, date in milestones.items():
#     x = datetime.fromisoformat(date)

#     # 只画线，不带 annotation
#     fig.add_vline(
#         x=x,
#         line_dash="dot",
#         line_color="#999",
#         opacity=0.5,
#     )

#     # 手动加文字标注
#     fig.add_annotation(
#         x=x,
#         y=1.02,
#         xref="x",
#         yref="paper",
#         text=label,
#         showarrow=False,
#         font=dict(size=11, color="#666"),
#         align="center",
#     )


# # 保存为 HTML
# fig.write_html("mirakuru_timeline.html")

# print("已生成：mirakuru_timeline.html")


# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# from datetime import datetime
# import seaborn as sns

# def to_date(date_str):
#     return datetime.strptime(date_str, "%Y-%m-%d")

# mirakuru_members = [
#     ("Jiujiu", "2025-03-16", "2026-02-01", "yellow"),
#     ("Itsume", "2025-03-16", "2026-02-01", "green"),
#     ("Sakura", "2025-03-16", "2026-02-01", "pink"),
#     ("Koyoi", "2025-10-01", "2026-02-01", "blue"),
#     ("Kaori", "2025-03-16", "2026-01-18", "purple"),
#     ("Yukikoo", "2025-03-16", "2026-01-18", "white"),
#     ("Shimizu", "2025-03-16", "2025-07-27", "lightblue"),
#     ("Mizuki", "2025-03-16", "2025-11-02", "red"),
# ]

# # 设置 seaborn 风格
# sns.set_theme(style="whitegrid")

# # 绘图
# fig, ax = plt.subplots(figsize=(12, 6))

# # 设置背景为浅灰
# fig.patch.set_facecolor('#f0f0f0')  # 整个图的背景
# ax.set_facecolor('#f0f0f0')         # 坐标区域背景

# for i, (name, start, end, color) in enumerate(mirakuru_members):
#     ax.hlines(i, to_date(start), to_date(end), color=color, linewidth=4)
#     ax.text(to_date(start), i + 0.1, name, fontsize=9, verticalalignment='bottom', color='black')

# # 添加竖着的虚线和时间节点

# milestones = [
#     ("2025.03.16", "2025-03-16"),
#     ("2025.07.27", "2025-07-27"),
#     ("2025.11.02", "2025-11-02"),
#     ("2026.01.18", "2026-01-18"),
#     # ("2026.04.30", "2026-02-01"),
# ]

# for label, date in milestones:
#     milestone_date = to_date(date)
#     ax.axvline(milestone_date, color='gray', linestyle='--', alpha=0.3)
#     ax.text(milestone_date, -0.5, label, fontsize=9, color='black', rotation=0, verticalalignment='center')
# # 格式设置
# ax.set_yticks([])
# ax.xaxis.set_major_locator(mdates.YearLocator())
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
# ax.set_title("MIRAKURU Member Activity Timeline", fontsize=14, weight='bold')
# ax.set_xlabel("Time")
# plt.tight_layout()
# plt.grid(axis='x', linestyle='--', alpha=0.6, color='gray')

# # 保存
# plt.savefig("mirakuru_timeline.svg", facecolor=fig.get_facecolor())

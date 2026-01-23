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

# # ========= 新增：open-ended 设置 =========
# OPEN_END = pd.Timestamp("2026-02-01")
# open_ended_members = {"Jiujiu", "Itsume", "Sakura", "Koyoi"}

# df["IsOpen"] = df["Member"].isin(open_ended_members)
# df.loc[df["IsOpen"], "End"] = OPEN_END
# # =======================================

# # 手动颜色映射
# member_colors = {
#     "Jiujiu":   "#F5F514",
#     "Itsume":   "#10B981",
#     "Sakura":   "#EC4899",
#     "Koyoi":    "#3B82F6",
#     "Kaori":    "#8B5CF6",
#     "Yukikoo":  "#F9F9F9",
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

# # 风格
# fig.update_layout(
#     height=520,
#     font=dict(family="Inter, Arial", size=13, color="#6B5E57"),
#     title=dict(x=0.02, font=dict(size=22, color="#6B5E57")),
#     plot_bgcolor="#FDF1E6",
#     paper_bgcolor="#FDECEF",
#     margin=dict(l=50, r=40, t=70, b=40),
# )


# fig.update_xaxes(
#     showgrid=True,
#     gridcolor="#EADFD6",
#     zeroline=False,
#     tickfont=dict(color="#6B5E57"),
# )

# fig.update_yaxes(
#     showgrid=False,
#     tickfont=dict(color="#6B5E57"),
# )


# # ========= 新增：open-ended 视觉提示 =========
# for _, row in df[df["IsOpen"]].iterrows():
#     fig.add_annotation(
#         x=row["End"],
#         y=row["Member"],
#         text="→",
#         showarrow=False,
#         font=dict(size=18, color=member_colors[row["Member"]]),
#         xanchor="left",
#         yanchor="middle",
#     )


# for m in open_ended_members:
#     fig.update_traces(selector=dict(name=m), opacity=0.7)



# # ==========================================

# # Milestones
# milestones = {
#     "2025.03.16": "2025-03-16",
#     "2025.07.27": "2025-07-27",
#     "2025.11.02": "2025-11-02",
#     "2026.01.18": "2026-01-18",
# }

# for label, date in milestones.items():
#     x = datetime.fromisoformat(date)
#     fig.add_vline(x=x, line_dash="dot", line_color="#F5D38E", opacity=0.6)
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

# fig.update_traces(marker_line_width=0, opacity=0.9)

# fig.write_html("mirakuru_timeline.html")
# print("已生成：mirakuru_timeline.html")


import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

# =======================
# 数据
# =======================
data = [
    ("Jiujiu",   "2025-03-16", "2026-02-01"),
    ("Itsume",   "2025-03-16", "2026-02-01"),
    ("Sakura",   "2025-03-16", "2026-02-01"),
    ("Koyoi",    "2025-10-01", "2026-02-01"),
    ("Kaori",    "2025-03-16", "2026-01-18"),
    ("Yukikoo",  "2025-03-16", "2026-01-18"),
    ("Shimizu",  "2025-03-16", "2025-07-27"),
    ("Mizuki",   "2025-03-16", "2025-11-02"),
]

df = pd.DataFrame(data, columns=["Member", "Start", "End"])
df["Start"] = pd.to_datetime(df["Start"])
df["End"]   = pd.to_datetime(df["End"])

# =======================
# Open-ended
# =======================
OPEN_END = pd.Timestamp("2026-02-01")
open_ended_members = {"Jiujiu", "Itsume", "Sakura", "Koyoi"}

df["IsOpen"] = df["Member"].isin(open_ended_members)
df.loc[df["IsOpen"], "End"] = OPEN_END

# =======================
# 颜色
# =======================
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

# 保持成员原始顺序（你可以根据需要排序）
members = df["Member"].tolist()
n = len(members)
x_positions = {m: i for i, m in enumerate(members)}

# =======================
# 基础 Figure（不使用 px.timeline）
# =======================
fig = go.Figure()

# 用 shape 的 rect 绘制每个成员的区间（y 使用日期）
bar_half_width = 0.35  # 横向半宽度

shapes = []
hover_x = []
hover_y = []
hover_texts = []

for _, row in df.iterrows():
    i = x_positions[row["Member"]]
    x0 = i - bar_half_width
    x1 = i + bar_half_width
    y0 = row["Start"].strftime("%Y-%m-%d")
    y1 = row["End"].strftime("%Y-%m-%d")

    # rect shape
    shapes.append(
        dict(
            type="rect",
            xref="x",
            yref="y",
            x0=x0,
            x1=x1,
            y0=y0,
            y1=y1,
            fillcolor=member_colors[row["Member"]],
            line=dict(width=0),
            opacity=0.85 if not row["IsOpen"] else 0.7,
            layer="below",
        )
    )

    # 用隐形 scatter 提供 hover（放在矩形中央）
    mid = row["Start"] + (row["End"] - row["Start"]) / 2
    hover_x.append(i)
    hover_y.append(mid)
    hover_texts.append(
        f"<b>{row['Member']}</b><br>Start: {row['Start'].date()}<br>End: {row['End'].date()}"
    )

# 添加所有 shapes
fig.update_layout(shapes=shapes)

# 添加透明 scatter 用于 hover（marker 设置透明但 hover 可见）
fig.add_trace(
    go.Scatter(
        x=hover_x,
        y=hover_y,
        mode="markers",
        marker=dict(size=0.1, opacity=0),  # 视觉上不可见
        hoverinfo="text",
        hovertext=hover_texts,
        showlegend=False,
    )
)

# =======================
# Milestones（横线）
# =======================
milestones = {
    "2025.03.16": "2025-03-16",
    "2025.07.27": "2025-07-27",
    "2025.11.02": "2025-11-02",
    "2026.01.18": "2026-01-18",
}

# 为 milestones 添加 line shapes 与 annotation
for label, date in milestones.items():
    y = datetime.fromisoformat(date)
    shapes.append(
        dict(
            type="line",
            xref="x",
            yref="y",
            x0=-0.5,
            x1=n - 0.5,
            y0=y.strftime("%Y-%m-%d"),
            y1=y.strftime("%Y-%m-%d"),
            line=dict(color="#F5D38E", width=2, dash="dot"),
            opacity=0.7,
            layer="below",
        )
    )
    # annotation（放在右侧）
    fig.add_annotation(
        x=1.01,
        xref="paper",
        y=y,
        yref="y",
        text=label,
        showarrow=False,
        font=dict(size=16, color="#666"),
        align="left",
    )

# 将更新后的 shapes 写回 layout（包含 milestone lines）
fig.update_layout(shapes=shapes)

# =======================
# Open-ended 箭头（↓）
# =======================
for _, row in df[df["IsOpen"]].iterrows():
    i = x_positions[row["Member"]]
    fig.add_annotation(
        x=i,
        y=row["End"],
        xref="x",
        yref="y",
        text="↓",
        showarrow=False,
        font=dict(size=24, color=member_colors[row["Member"]]),
        xanchor="center",
        yanchor="top",
        yshift=-8,   # ← 向下移动（单位：像素）
    )

# =======================
# Layout / 轴设置（确保 Y 为日期）
# =======================
fig.update_layout(
    title="MIRAKURU Member Activity Timeline",
    height=900,
    font=dict(family="Inter, Arial", size=13, color="#6B5E57"),
    plot_bgcolor="#FDF1E6",
    paper_bgcolor="#FDECEF",
    margin=dict(l=60, r=80, t=80, b=40),
)

# X 轴：用数值位置，并把刻度替换为成员名字
fig.update_xaxes(
    showgrid=False,
    tickmode="array",
    tickvals=list(x_positions.values()),
    ticktext=list(x_positions.keys()),
    range=[-0.6, n - 0.4],
    tickfont=dict(color="#6B5E57"),
)

# Y 轴：日期轴，反转以便时间从上到下
fig.update_yaxes(
    type="date",
    autorange="reversed",
    showgrid=True,
    gridcolor="#EADFD6",
    # tickfont=dict(color="#6B5E57"),
    tickfont=dict(
        size=16,          # ← 这里调大（14 / 16 / 18 都可以）
        color="#6B5E57"
    ),
    title_text="Date",
)

# =======================
# 可选：在横向较窄时让标签旋转（如果需要）
# =======================
fig.update_xaxes(tickangle=0)

# =======================
# 导出
# =======================
fig.write_html("mirakuru_timeline.html")
print("已生成：mirakuru_timeline.html")







import matplotlib.pyplot as plt

# hist
# marks = [35,40,42,45,50,55,58,60,62,65,68,70,72,75,78,80,82,85,88,90,92,95]

# bins = 5
# 95 - 35 = 60 / 5 = 12
# bin1: 35 - 47 (4)
# bin2: 47 - 59 (3)
# bin3: 59 - 71 (5)
# bin4: 71 - 83 (5)
# bin5: 83 - 95 (5)

# plt.figure(figsize=(10,6))
# plt.hist(marks,bins=5,color='red',alpha=0.4,edgecolor='black')
# plt.title("Students Marks Distribution",fontsize=16)
# plt.xlabel("Marks Range",fontsize=12)
# plt.ylabel("Students",fontsize=12)
# plt.grid(True)
# plt.show()

# scatter
# plot dots on graph
# study_hours = [1,2,3,4,5,6,7,8]
# marks = [35,40,50,60,65,70,85,95]
# sizes = [100,120,140,160,180,200,220,240]
# colors = ['red','green','blue','orange','cyan','violet','indigo','yellow']
# plt.figure(figsize=(10,6))
# plt.scatter(study_hours,marks,s=sizes,c=colors,alpha=0.7,edgecolors='black',marker='o')
# plt.title("Hours vs Marks",fontsize=16)
# plt.xlabel("Hours",fontsize=12)
# plt.ylabel("Marks",fontsize=16)
# plt.grid(True)
# plt.annotate("Top Student",xy=(8,95), xytext=(7.5,80),arrowprops=dict(facecolor='black',shrink=0.01))
# plt.show()


# pie chart
# represent data in a circle
# extract portion from circle we can call "explode"
# subjects = ['Math','Science','English','Python','Java']
# marks = [95,88,76,98,85]
# colors = ['red','green','blue','orange','cyan']
# explode = (0,0,0,0.1,0)
# plt.figure(figsize=(10,10))
# plt.pie(marks,labels=subjects,colors=colors,explode=explode,autopct='%1.1f%%',shadow=True,startangle=90,
#         wedgeprops={'edgecolor':'black'},textprops={'fontsize':12})
# plt.title("Marks Vs Subects")
# plt.show()



# subplots
# collabrate multiple graps
plt.figure(figsize=(12,12))

plt.subplot(2,2,1)
plt.plot([1,2,3],[10,20,30])

plt.subplot(2,2,2)
subjects = ['Math','Science','English','Python','Java']
marks = [95,88,76,98,85]
colors = ['red','green','blue','orange','cyan']
explode = (0,0,0,0.1,0)
plt.pie(marks,labels=subjects,colors=colors,explode=explode,autopct='%1.1f%%',shadow=True,startangle=90,
        wedgeprops={'edgecolor':'black'},textprops={'fontsize':12})
plt.title("Marks Vs Subects")

plt.subplot(2,2,3)
marks = [35,40,42,45,50,55,58,60,62,65,68,70,72,75,78,80,82,85,88,90,92,95]
plt.hist(marks,bins=5,color='red',alpha=0.4,edgecolor='black')
plt.title("Students Marks Distribution",fontsize=16)
plt.xlabel("Marks Range",fontsize=12)
plt.ylabel("Students",fontsize=12)
plt.grid(True)


plt.subplot(2,2,4)
plt.bar(['std1','std2','std3'],[80,90,100])

plt.show()








# import matplotlib.pyplot as plt
# import matplotlib as mpl
# import matplotlib.patches as mpatches
# import numpy as np

# # ─────────────────────────────────────────
# # 1. DATA
# # ─────────────────────────────────────────
# subjects = ['Math', 'Science', 'English', 'Python', 'Java']
# marks    = [95, 88, 76, 98, 85]

# # ─────────────────────────────────────────
# # 2. GLOBAL rcPARAMS (dark academic theme)
# # ─────────────────────────────────────────
# mpl.rcParams.update({
#     "figure.facecolor":   "#0d1117",
#     "axes.facecolor":     "#0d1117",
#     "text.color":         "#e6edf3",
#     "font.family":        "DejaVu Sans",
#     "font.size":          11,
#     "savefig.dpi":        200,
#     "savefig.bbox":       "tight",
#     "savefig.facecolor":  "#0d1117",
# })

# # ─────────────────────────────────────────
# # 3. COLOR PALETTE  (vibrant on dark bg)
# # ─────────────────────────────────────────
# COLORS = ["#6c63ff", "#f7b731", "#e84393", "#00d4aa", "#ff6b6b"]

# # ─────────────────────────────────────────
# # 4. DERIVED METRICS
# # ─────────────────────────────────────────
# total        = sum(marks)
# percentages  = [m / total * 100 for m in marks]
# highest_idx  = marks.index(max(marks))

# # ─────────────────────────────────────────
# # 5. FIGURE LAYOUT  (pie + bar + stats)
# # ─────────────────────────────────────────
# fig = plt.figure(figsize=(16, 9))
# fig.patch.set_facecolor("#0d1117")

# # GridSpec: [pie | donut | bar-panel]
# from matplotlib.gridspec import GridSpec
# gs = GridSpec(2, 3,
#               figure=fig,
#               left=0.04, right=0.97,
#               top=0.88,  bottom=0.08,
#               hspace=0.45, wspace=0.38)

# ax_pie    = fig.add_subplot(gs[:, 0])   # full left col  – classic pie
# ax_donut  = fig.add_subplot(gs[:, 1])   # full mid col   – donut
# ax_bar    = fig.add_subplot(gs[0, 2])   # top-right      – bar
# ax_stats  = fig.add_subplot(gs[1, 2])   # bot-right      – stat table

# # ─────────────────────────────────────────
# # 6. SUPER TITLE & SUBTITLE
# # ─────────────────────────────────────────
# fig.text(0.5, 0.95, "📊  Student Marks Analysis",
#          ha="center", va="top",
#          fontsize=20, fontweight="bold", color="#f0f6fc")
# fig.text(0.5, 0.91,
#          f"Total Marks: {total}  |  Subjects: {len(subjects)}  |  "
#          f"Topper: {subjects[highest_idx]} ({marks[highest_idx]})",
#          ha="center", va="top",
#          fontsize=11, color="#8b949e")

# # ══════════════════════════════════════════
# # PLOT A – Classic Pie Chart
# # ══════════════════════════════════════════
# explode = [0.08 if i == highest_idx else 0.02 for i in range(len(subjects))]

# wedges, texts, autotexts = ax_pie.pie(
#     marks,
#     labels       = subjects,
#     colors       = COLORS,
#     explode      = explode,
#     autopct      = "%1.1f%%",
#     pctdistance  = 0.78,
#     startangle   = 140,
#     shadow       = True,
#     wedgeprops   = {"linewidth": 2, "edgecolor": "#0d1117",
#                     "antialiased": True},
#     textprops    = {"color": "#e6edf3", "fontsize": 10},
# )

# # Style percentage labels
# for i, autotext in enumerate(autotexts):
#     autotext.set_fontsize(9)
#     autotext.set_fontweight("bold")
#     autotext.set_color(COLORS[i])

# # Subject labels: bold + colored
# for i, text in enumerate(texts):
#     text.set_color(COLORS[i])
#     text.set_fontweight("bold")
#     text.set_fontsize(10)

# ax_pie.set_title("Classic Pie Chart", color="#f0f6fc",
#                  fontsize=13, fontweight="bold", pad=14)

# # Star marker on highest scorer
# ax_pie.annotate("★ Top",
#                 xy      = wedges[highest_idx].center,
#                 xytext  = (0, 0),
#                 ha      = "center", va      = "center",
#                 color   = "#f7b731", fontsize = 9,
#                 fontweight = "bold")

# # ══════════════════════════════════════════
# # PLOT B – Donut Chart
# # ══════════════════════════════════════════
# wedges2, texts2, autotexts2 = ax_donut.pie(
#     marks,
#     colors      = COLORS,
#     autopct     = "%1.1f%%",
#     pctdistance = 0.80,
#     startangle  = 140,
#     wedgeprops  = {"linewidth": 2.5, "edgecolor": "#0d1117",
#                    "width": 0.55, "antialiased": True},
#     textprops   = {"color": "#e6edf3"},
# )

# for i, at in enumerate(autotexts2):
#     at.set_fontsize(9)
#     at.set_fontweight("bold")
#     at.set_color("#0d1117")

# # Donut centre text
# ax_donut.text(0, 0.08, f"{total}", ha="center", va="center",
#               fontsize=22, fontweight="bold", color="#f0f6fc")
# ax_donut.text(0, -0.15, "Total", ha="center", va="center",
#               fontsize=10, color="#8b949e")

# ax_donut.set_title("Donut Chart", color="#f0f6fc",
#                    fontsize=13, fontweight="bold", pad=14)

# # Custom legend
# legend_patches = [
#     mpatches.Patch(facecolor=COLORS[i], edgecolor="#0d1117",
#                    label=f"{subjects[i]}  ({marks[i]} pts)")
#     for i in range(len(subjects))
# ]
# ax_donut.legend(
#     handles        = legend_patches,
#     loc            = "lower center",
#     bbox_to_anchor = (0.5, -0.22),
#     ncol           = 3,
#     fontsize       = 9,
#     framealpha     = 0.15,
#     edgecolor      = "#30363d",
#     labelcolor     = "#e6edf3",
# )

# # ══════════════════════════════════════════
# # PLOT C – Horizontal Bar (marks breakdown)
# # ══════════════════════════════════════════
# y_pos = np.arange(len(subjects))
# bars  = ax_bar.barh(y_pos, marks,
#                     color=COLORS, edgecolor="#0d1117",
#                     height=0.55, linewidth=1.2)

# # Value annotations
# for bar, mark, pct in zip(bars, marks, percentages):
#     ax_bar.text(bar.get_width() + 0.5,
#                 bar.get_y() + bar.get_height() / 2,
#                 f"{mark}  ({pct:.1f}%)",
#                 va="center", fontsize=9, color="#8b949e")

# # Grade lines
# for grade, val, col in [("A+", 90, "#00d4aa"), ("A", 80, "#f7b731")]:
#     ax_bar.axvline(val, color=col, linestyle="--",
#                    linewidth=1, alpha=0.6)
#     ax_bar.text(val + 0.3, len(subjects) - 0.5, grade,
#                 fontsize=8, color=col, va="top")

# ax_bar.set_yticks(y_pos)
# ax_bar.set_yticklabels(subjects, color="#e6edf3", fontsize=9)
# ax_bar.set_xlim(0, 115)
# ax_bar.set_xlabel("Marks", color="#8b949e", fontsize=9)
# ax_bar.set_title("Marks Breakdown", color="#f0f6fc",
#                  fontsize=11, fontweight="bold")
# ax_bar.tick_params(colors="#8b949e", labelsize=8)
# ax_bar.set_facecolor("#161b22")
# for spine in ax_bar.spines.values():
#     spine.set_edgecolor("#21262d")
# ax_bar.grid(axis="x", alpha=0.15, color="#8b949e")

# # Highlight top bar
# bars[highest_idx].set_edgecolor("#f7b731")
# bars[highest_idx].set_linewidth(2.5)

# # ══════════════════════════════════════════
# # PLOT D – Statistics Table
# # ══════════════════════════════════════════
# ax_stats.set_facecolor("#161b22")
# ax_stats.axis("off")

# # Compute stats
# _arr   = np.array(marks)
# stats  = [
#     ("Total Marks",   f"{total}"),
#     ("Average",       f"{_arr.mean():.1f}"),
#     ("Highest",       f"{_arr.max()}  ({subjects[_arr.argmax()]})"),
#     ("Lowest",        f"{_arr.min()}  ({subjects[_arr.argmin()]})"),
#     ("Std Deviation", f"{_arr.std():.2f}"),
#     ("Pass Rate",     "100%  (all ≥ 76)"),
# ]

# ax_stats.set_title("Statistics", color="#f0f6fc",
#                    fontsize=11, fontweight="bold", pad=8)

# col_labels = ["Metric", "Value"]
# table_data = [[k, v] for k, v in stats]

# tbl = ax_stats.table(
#     cellText    = table_data,
#     colLabels   = col_labels,
#     loc         = "center",
#     cellLoc     = "left",
# )
# tbl.auto_set_font_size(False)
# tbl.set_fontsize(9)
# tbl.scale(1, 1.55)

# # Style table cells
# for (row, col), cell in tbl.get_celld().items():
#     cell.set_facecolor("#1c2128" if row % 2 == 0 else "#161b22")
#     cell.set_edgecolor("#21262d")
#     cell.set_text_props(color="#8b949e" if col == 0 else "#e6edf3")
#     if row == 0:                          # header row
#         cell.set_facecolor("#21262d")
#         cell.set_text_props(color="#f0f6fc", fontweight="bold")

# # ─────────────────────────────────────────
# # 7. SAVE & SHOW
# # ─────────────────────────────────────────
# plt.savefig("pie_chart_full.png")
# print("✅  Saved: pie_chart_full.png")
# plt.show()



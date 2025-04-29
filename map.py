import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patheffects as pe
import matplotlib
from shapely.geometry import Point
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

# 设置使用TkAgg后端来支持交互
matplotlib.use('TkAgg')

# 设置中文显示支持
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']  # 中文字体
plt.rcParams['axes.unicode_minus'] = False

# 读取你的Excel文件
df = pd.read_excel('发货分布.xlsx')

# GeoJSON数据（提前下载）
us_states = gpd.read_file('us-states.json')

# 州简称到州名的映射表
state_abbrev_to_name = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
    'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
    'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
    'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
    'WI': 'Wisconsin', 'WY': 'Wyoming'
}

# 添加州名和缩写到DataFrame中
df['state_name'] = df['州'].map(state_abbrev_to_name)
df['state_abbrev'] = df['州']

# 合并地理数据和发货数据
merged = us_states.merge(df, left_on='name', right_on='state_name', how='left')

# 创建 Tkinter 窗口
root = tk.Tk()
root.title("美国各州发货数量分布图")

# 创建Matplotlib图形
fig, ax = plt.subplots(figsize=(20, 12))
ax.set_facecolor('#e9f0f7')  # 更亮的背景色

# 更现代的色图风格（可选：YlGnBu, viridis, plasma, coolwarm）
merged.plot(column='发货数量', ax=ax, legend=True, cmap='YlGnBu', edgecolor='#555', linewidth=0.6,
            legend_kwds={'label': "各州发货数量", 'orientation': "horizontal", 'shrink': 0.3, 'pad': 0.01, 'aspect': 30})

# 使用较细描边增强立体感
merged.boundary.plot(ax=ax, linewidth=1.2, edgecolor='gray')

# 标注信息，如果面积小则引出线条
for idx, row in merged.iterrows():
    if pd.notnull(row['发货数量']) and pd.notnull(row['发货量占比']):
        text = f"{int(row['发货数量'])}\n{row['发货量占比']:.1%}\n{row['state_abbrev']}"
        x, y = row['geometry'].centroid.x, row['geometry'].centroid.y
        bounds = row['geometry'].bounds
        area = row['geometry'].area

        # 对面积较小的州，将文字引出到右侧水平位置
        if area < 1:
            x_out, y_out = bounds[2] + 4, y
            ax.plot([x, x_out], [y, y], color='black', linewidth=0.5)
            ax.text(x_out, y_out, text, ha='left', va='bottom', fontsize=10, fontweight='bold', color='black', path_effects=[pe.withStroke(linewidth=1.5, foreground='white')])
        else:
            fontsize = 8 if row['state_abbrev'] in ['MD', 'CT', 'MA'] else 10
            ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, fontweight='bold', color='black', path_effects=[pe.withStroke(linewidth=1.5, foreground='white')])

# 设置地图的交互功能
plt.axis('on')  # 显示坐标轴和刻度
plt.grid(True)  # 显示网格

# 创建Canvas并嵌入到Tkinter窗口中
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

# 创建交互工具栏并将其嵌入到窗口
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
toolbar.pack()

# 启动Tkinter事件循环
root.mainloop()

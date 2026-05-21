import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os

os.makedirs('graphs', exist_ok=True)

# ── DARK THEME ──
plt.rcParams.update({
    'figure.facecolor': '#0D1117',
    'axes.facecolor': '#161B22',
    'axes.edgecolor': '#30363D',
    'axes.labelcolor': '#E6EDF3',
    'text.color': '#E6EDF3',
    'xtick.color': '#E6EDF3',
    'ytick.color': '#E6EDF3',
    'grid.color': '#21262D',
    'grid.linewidth': 0.8,
    'font.family': 'sans-serif',
})

COLORS = {
    'Python': '#3776AB',
    'JavaScript': '#F7DF1E',
    'TypeScript': '#3178C6',
    'Rust': '#FF4500',
    'Java': '#ED8B00',
    'Go': '#00ACD7',
}

print("=" * 60)
print("  TECH STACK REVOLUTION: Before & After AI Era")
print("=" * 60)

# Load your JSON
with open('Data/gh-push-event.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)
df['year'] = pd.to_numeric(df['year'])
df['count'] = pd.to_numeric(df['count'])
df = df[(df['year'] >= 2019) & (df['year'] <= 2024)]

languages = ['Python', 'JavaScript', 'TypeScript', 'Rust', 'Java', 'Go']
df = df[df['name'].isin(languages)]
yearly = df.groupby(['year', 'name'])['count'].sum().reset_index()

# ──────────────────────────────────────────────────────────────
# GRAPH 1: Simple Line Chart (What you have)
# ──────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(14, 7))
for lang in languages:
    d = yearly[yearly['name'] == lang].sort_values('year')
    ax.plot(d['year'], d['count'], marker='o', label=lang,
            linewidth=2.5, color=COLORS[lang], markersize=8)
    
    # Add value labels
    for _, row in d.iterrows():
        ax.annotate(f"{int(row['count']/1000)}K",
                   (row['year'], row['count']),
                   textcoords="offset points", xytext=(0, 10),
                   fontsize=7, color=COLORS[lang])

ax.axvline(x=2022.9, color='#FF0000', linestyle='--',
           linewidth=2, alpha=0.8, label='⚡ ChatGPT Launch')

ax.set_title('🚀 Programming Language Trends (2019-2024)',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('GitHub Pushes', fontsize=12)
ax.legend(loc='upper left', framealpha=0.3)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('graphs/01_language_trends.png', dpi=150, bbox_inches='tight',
            facecolor='#0D1117')
plt.show()
print("✅ Graph 1 saved!")

# ──────────────────────────────────────────────────────────────
# GRAPH 2: Before vs After (What you have)
# ──────────────────────────────────────────────────────────────

before = df[df['year'] <= 2022].groupby('name')['count'].sum().reset_index()
after = df[df['year'] >= 2023].groupby('name')['count'].sum().reset_index()
before.columns = ['Language', 'Before AI']
after.columns = ['Language', 'After AI']
comp = before.merge(after, on='Language')

fig, ax = plt.subplots(figsize=(13, 7))
x = range(len(comp))
w = 0.35

bars1 = ax.bar([i - w/2 for i in x], comp['Before AI'], w,
               label='Before AI (2019-2022)', color='#4682B4', alpha=0.85)
bars2 = ax.bar([i + w/2 for i in x], comp['After AI'], w,
               label='After AI (2023-2024)', color='#FF4500', alpha=0.85)

# Add labels
for bar in bars1:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height,
            f'{int(height/1000)}K', ha='center', fontsize=8)
for bar in bars2:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height,
            f'{int(height/1000)}K', ha='center', fontsize=8)

ax.set_title('⚡ Before AI vs After AI: GitHub Activity',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Programming Language', fontsize=12)
ax.set_ylabel('Total GitHub Pushes', fontsize=12)
ax.set_xticks(list(x))
ax.set_xticklabels(comp['Language'])
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('graphs/02_before_vs_after.png', dpi=150, bbox_inches='tight',
            facecolor='#0D1117')
plt.show()
print("✅ Graph 2 saved!")

# ──────────────────────────────────────────────────────────────
# NEW GRAPH 3: Growth Percentage (Simple!)
# ──────────────────────────────────────────────────────────────

comp['Growth %'] = ((comp['After AI'] - comp['Before AI']) / comp['Before AI'] * 100).round(1)
comp_sorted = comp.sort_values('Growth %', ascending=True)

fig, ax = plt.subplots(figsize=(12, 6))

# Change colors: red for negative, green for positive
colors = ['#FF4444' if x < 0 else '#00FF7F' for x in comp_sorted['Growth %']]

bars = ax.barh(comp_sorted['Language'], comp_sorted['Growth %'],
               color=colors, alpha=0.85, edgecolor='white', linewidth=0.5)

# Add percentage labels
for bar, val in zip(bars, comp_sorted['Growth %']):
    ax.text(val + 1 if val > 0 else val - 1, bar.get_y() + bar.get_height()/2,
            f'{val}%', va='center', fontsize=11, fontweight='bold',
            color='#00FF7F' if val > 0 else '#FF4444')

ax.axvline(x=0, color='white', linewidth=1.5, alpha=0.7)
ax.set_title('📊 Growth Rate: Post-AI vs Pre-AI',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Growth Percentage (%)', fontsize=12)
ax.set_ylabel('Programming Language', fontsize=12)
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('graphs/03_growth_rate.png', dpi=150, bbox_inches='tight',
            facecolor='#0D1117')
plt.show()
print("✅ Graph 3 saved!")

# ──────────────────────────────────────────────────────────────
# NEW GRAPH 4: Market Share Pie Chart (Simple!)
# ──────────────────────────────────────────────────────────────

data_2024 = df[df['year'] == 2024].groupby('name')['count'].sum()

fig, ax = plt.subplots(figsize=(10, 8))

# Colors for pie
pie_colors = [COLORS.get(lang, '#888888') for lang in data_2024.index]

wedges, texts, autotexts = ax.pie(
    data_2024.values,
    labels=data_2024.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=pie_colors,
    wedgeprops=dict(width=0.6, edgecolor='#0D1117', linewidth=2)
)

# Make text readable
for text in texts:
    text.set_color('#E6EDF3')
    text.set_fontsize(11)
    text.set_fontweight('bold')

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(9)
    autotext.set_fontweight('bold')

ax.text(0, 0, '2024\nMarket', ha='center', va='center',
        fontsize=14, fontweight='bold', color='#E6EDF3')

ax.set_title('🥧 2024 Market Share by Language',
             fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('graphs/04_2024_market_share.png', dpi=150, bbox_inches='tight',
            facecolor='#0D1117')
plt.show()
print("✅ Graph 4 saved!")

# ──────────────────────────────────────────────────────────────
# NEW: Print Key Insights (Simple analysis)
# ──────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("  📊 KEY INSIGHTS")
print("=" * 60 + "\n")

print("BEFORE vs AFTER AI (Nov 2022 - ChatGPT Launch):\n")

for idx, row in comp_sorted.iterrows():
    lang = row['Language']
    before = row['Before AI']
    after = row['After AI']
    growth = row['Growth %']
    
    if growth > 0:
        trend = "📈 GROWING"
    elif growth < -20:
        trend = "📉 DECLINING FAST"
    else:
        trend = "➡️ STABLE"
    
    print(f"{lang}:")
    print(f"  Before: {int(before/1000):,}K")
    print(f"  After:  {int(after/1000):,}K")
    print(f"  Change: {growth:+.1f}% {trend}\n")

print("=" * 60)
print("✅ All 4 graphs saved in 'graphs' folder!")
print("=" * 60 + "\n")
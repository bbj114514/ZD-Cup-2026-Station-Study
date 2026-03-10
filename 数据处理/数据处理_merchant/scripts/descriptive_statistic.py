import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '../data/merchant_final_encoded.csv')
df = pd.read_csv(file_path)

sns.set_theme(style="whitegrid", context="talk")
plt.rcParams['axes.unicode_minus'] = False

shop_loc_map = {0: 'Far', 1: 'Within 100m', 2: 'Community Entrance'}
rider_rate_map = {1: 'Rarely', 2: 'Occasionally', 3: 'Frequently'}
intent_map = {0: 'Unwilling', 1: 'Open to Consider', 2: 'Very Willing'}

fig, axes = plt.subplots(1, 2, figsize=(18, 8))

loc_counts = df['Shop_Loc_Code'].value_counts().sort_index()
sns.barplot(x=[shop_loc_map.get(i) for i in loc_counts.index], 
            y=loc_counts.values, ax=axes[0], palette='Blues_d')
axes[0].set_title('Shop Distance to Community', fontsize=20, pad=20)
axes[0].set_ylabel('Merchant Count')
axes[0].tick_params(axis='x', rotation=15)

rate_counts = df['Rider_Cust_Rate_Code'].value_counts().sort_index()
sns.barplot(x=[rider_rate_map.get(i) for i in rate_counts.index], 
            y=rate_counts.values, ax=axes[1], palette='Greens_d')
axes[1].set_title('Rider Visit Frequency', fontsize=20, pad=20)
axes[1].set_ylabel('Merchant Count')
axes[1].tick_params(axis='x', rotation=15)

plt.tight_layout()
plt.savefig(os.path.join(base_dir, '../image_chart/descriptive_statistic/merchant_v1_operational_fixed.png'), dpi=300, bbox_inches='tight')

plt.figure(figsize=(12, 7))
intent_counts = df['Collab_Intent_Code'].value_counts().sort_index()
ax2 = sns.barplot(x=[intent_map.get(i) for i in intent_counts.index], 
                  y=intent_counts.values, palette='magma')
plt.title('Merchant Collaboration Intent Distribution', fontsize=22, pad=25)
plt.ylabel('Count')
for i, v in enumerate(intent_counts.values):
    plt.text(i, v + 0.5, str(v), ha='center', va='bottom', fontweight='bold', fontsize=16)
plt.savefig(os.path.join(base_dir, '../image_chart/descriptive_statistic/merchant_v2_intent_fixed.png'), dpi=300, bbox_inches='tight')

concern_cols = [c for c in df.columns if c.startswith('Concern_')]
concern_counts = df[concern_cols].sum().sort_values(ascending=False)

concern_label_map = {
    'Concern_安全责任问题': 'Safety & Liability',
    'Concern_影响店面卫生': 'Hygiene & Cleanliness'
}
concern_labels = [concern_label_map.get(c, c.replace('Concern_', '')) for c in concern_counts.index]

plt.figure(figsize=(14, 8))
sns.barplot(x=concern_counts.values / len(df) * 100, y=concern_labels, palette='Reds_r')
plt.title('Merchant Main Concerns (%)', fontsize=22, pad=25)
plt.xlabel('Percentage of Merchants (%)')
plt.xlim(0, 110)
plt.savefig(os.path.join(base_dir, '../image_chart/descriptive_statistic/merchant_v3_concerns_fixed.png'), dpi=300, bbox_inches='tight')

inc_cols = [c for c in df.columns if c.startswith('Incentive_')]
inc_counts = df[inc_cols].sum().sort_values(ascending=False)

inc_label_map = {
    'Incentive_平台流量曝光': 'Platform Exposure',
    'Incentive_水电补贴': 'Utility Subsidies'
}
inc_labels = [inc_label_map.get(c, c.replace('Incentive_', '')) for c in inc_counts.index]

plt.figure(figsize=(14, 8))
sns.barplot(x=inc_counts.values / len(df) * 100, y=inc_labels, palette='YlGnBu_r')
plt.title('Preferred Incentives for Merchants (%)', fontsize=22, pad=25)
plt.xlabel('Percentage of Merchants (%)')
plt.xlim(0, 110)
plt.savefig(os.path.join(base_dir, '../image_chart/descriptive_statistic/merchant_v4_incentives_fixed.png'), dpi=300, bbox_inches='tight')

print(">>> 描述性统计图表已生成！")
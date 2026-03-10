import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import os

base_dir = os.path.dirname(__file__)
encoded_file_path = os.path.join(base_dir, '../data/resident_final_encoded.csv')
df = pd.read_csv(encoded_file_path)

sns.set_theme(style="whitegrid", context="talk")
plt.rcParams['axes.unicode_minus'] = False

nimby_labels = {0: 'Accept Near Home', 1: 'Reject Near Home'}
reside_labels = {1: 'Less than 1yr', 2: '1-5yrs', 3: 'More than 5yrs'}
attitude_labels = {1: 'Unsupportive', 3: 'Neutral', 4: 'Supportive', 5: 'Very Supportive'}

def check_significance(target_col):
    contingency_table = pd.crosstab(df[target_col], df['NIMBY_Sensitivity_Code'])
    chi2, p, dof, ex = stats.chi2_contingency(contingency_table)
    return p

stats_results = {
    'Age Group': check_significance('Age_Group_Code'),
    'Reside Duration': check_significance('Reside_Duration_Code'),
    'Visual Frequency': check_significance('See_Rider_Freq_Code')
}

print("--- 卡方检验 P值汇总 ---")
for k, v in stats_results.items():
    print(f"{k}: {v:.4f}")

plt.figure(figsize=(12, 7))
pivot_reside = pd.crosstab(df['Reside_Duration_Code'], df['NIMBY_Sensitivity_Code'], normalize='index') * 100
pivot_reside.index = [reside_labels.get(i) for i in pivot_reside.index]
pivot_reside.columns = ['Accept', 'Reject']

ax1 = pivot_reside.plot(kind='bar', stacked=True, color=['#3498db', '#e74c3c'], figsize=(12, 7))
plt.title('NIMBY Sensitivity by Residential Duration', fontsize=20, pad=20)
plt.ylabel('Percentage (%)')
plt.xlabel('Residential Duration')
plt.legend(title='Attitude Near Home', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=0)

for p in ax1.patches:
    width, height = p.get_width(), p.get_height()
    x, y = p.get_xy() 
    if height > 5:
        ax1.text(x+width/2, y+height/2, f'{height:.1f}%', ha='center', va='center', color='white', fontweight='bold')

plt.savefig(os.path.join(base_dir, '../image_chart/NIMBY/resident_nimby_by_duration.png'), dpi=300, bbox_inches='tight')

plt.figure(figsize=(12, 8))
valid_attitudes = [3, 4, 5] 
temp_df = df[df['Overall_Attitude_Code'].isin(valid_attitudes)]

pivot_att = pd.crosstab(df['Overall_Attitude_Code'], df['NIMBY_Sensitivity_Code'], normalize='index') * 100
pivot_att.index = [attitude_labels.get(i, 'Other') for i in pivot_att.index]
pivot_att.columns = ['Accept', 'Reject']

ax2 = pivot_att.plot(kind='bar', stacked=True, color=['#2ecc71', '#c0392b'], figsize=(12, 8))
plt.title('NIMBY Paradox: Overall Support vs. Local Acceptance', fontsize=20, pad=20)
plt.ylabel('Percentage (%)')
plt.xlabel('Overall Attitude towards Station')
plt.legend(title='Attitude Near Home', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=15)

for p in ax2.patches:
    width, height = p.get_width(), p.get_height()
    x, y = p.get_xy() 
    if height > 5:
        ax2.text(x+width/2, y+height/2, f'{height:.1f}%', ha='center', va='center', color='white', fontweight='bold')

plt.savefig(os.path.join(base_dir, '../image_chart/NIMBY/resident_nimby_paradox.png'), dpi=300, bbox_inches='tight')

pd.DataFrame.from_dict(stats_results, orient='index', columns=['p-value']).to_csv(os.path.join(base_dir, '../image_chart/NIMBY/resident_nimby_stats.csv'), index=False)
print("\n>>> 邻避效应分析图表及统计表已生成。")
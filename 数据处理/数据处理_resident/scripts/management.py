import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

base_dir = os.path.dirname(__file__)
encoded_file_path = os.path.join(base_dir, '../data/resident_final_encoded.csv')
df = pd.read_csv(encoded_file_path)

sns.set_theme(style="whitegrid", context="talk")
plt.rcParams['axes.unicode_minus'] = False

mgmt_cols = [c for c in df.columns if c.startswith('MgmtRule_')]

mgmt_map = {
    'MgmtRule_物业监督': 'Property Oversight',
    'MgmtRule_禁止吸烟': 'No Smoking',
    'MgmtRule_限时开放': 'Limited Hours',
    'MgmtRule_平台责任制': 'Platform Resp.'
}

mgmt_counts = df[mgmt_cols].sum().sort_values(ascending=False)
mgmt_perc = (mgmt_counts / len(df)) * 100
labels = [mgmt_map.get(c, c.replace('MgmtRule_', '')) for c in mgmt_counts.index]

plt.figure(figsize=(12, 8))
ax = sns.barplot(x=mgmt_perc.values, y=labels, hue=labels, palette='viridis', legend=False)

plt.title('Resident Preferences for Management Rules (%)', fontsize=20, pad=20)
plt.xlabel('Support Percentage (%)')
plt.xlim(0, 110)

for i, v in enumerate(mgmt_perc.values):
    ax.text(v + 1, i, f'{v:.1f}%', va='center', fontweight='bold')

plt.savefig(os.path.join(base_dir, '../image_chart/management/resident_mgmt_preference.png'), dpi=300, bbox_inches='tight')

print("\n--- 顾虑与管理对策交叉分析 ---")

concern_col = 'ResConcern_充电消防隐患'
rule_col = 'MgmtRule_物业监督'

if concern_col in df.columns and rule_col in df.columns:
    ct = pd.crosstab(df[concern_col], df[rule_col], normalize='index') * 100
    
    try:
        if 1 in ct.index and 1 in ct.columns:
            ratio = ct.loc[1, 1]
            print(f"担心消防隐患的居民中，支持物业监督的比例: {ratio:.2f}%")
        else:
            print("提示：样本在该维度上具有高度一致性（例如所有人均担心消防隐患），无法形成对比矩阵。")
            direct_ratio = df[rule_col].mean() * 100
            print(f"该群体对物业监督的总体支持率为: {direct_ratio:.2f}%")
            
    except Exception as e:
        print(f"统计计算跳过: {e}")

plt.figure(figsize=(10, 6))
sns.boxplot(x='Overall_Attitude_Code', y='Discussion_Will_Code', data=df, hue='Overall_Attitude_Code', palette='coolwarm', legend=False)
plt.title('Overall Attitude vs. Participation Willingness', fontsize=18)
plt.xlabel('Support Level (1-5)')
plt.ylabel('Participation Will (1-5)')
plt.savefig(os.path.join(base_dir, '../image_chart/management/resident_attitude_vs_participation.png'), dpi=300, bbox_inches='tight')

print("\n>>> 脚本运行完成。")
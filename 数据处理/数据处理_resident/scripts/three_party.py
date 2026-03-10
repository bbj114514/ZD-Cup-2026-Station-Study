import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

base_dir = os.path.dirname(__file__)
rider_file = os.path.join(base_dir, '../data/rider_final_encoded.csv')
merchant_file = os.path.join(base_dir, '../data/merchant_final_encoded.csv')
resident_file = os.path.join(base_dir, '../data/resident_final_encoded.csv')

rider_df = pd.read_csv(rider_file)
merchant_df = pd.read_csv(merchant_file)
resident_df = pd.read_csv(resident_file)

r_charge_need = rider_df['Q7_Charge_Issue'].mean() * 100
m_safety_risk = merchant_df['Concern_安全责任问题'].mean() * 100
res_fire_risk = resident_df['ResConcern_充电消防隐患'].mean() * 100

r_rest_need = rider_df['Q7_Rest_Issue'].mean() * 100
m_hygiene_risk = merchant_df['Concern_影响店面卫生'].mean() * 100
res_noise_risk = resident_df['ResConcern_噪音/卫生问题'].mean() * 100

res_mgmt_support = resident_df['MgmtRule_物业监督'].mean() * 100
m_base_intent = (merchant_df['Collab_Intent_Code'].mean() / 2.0) * 100

collision_data = [
    {'Theme': 'Power & Fire Safety', 'Stakeholder': 'Rider Demand', 'Score': r_charge_need},
    {'Theme': 'Power & Fire Safety', 'Stakeholder': 'Merchant Risk', 'Score': m_safety_risk},
    {'Theme': 'Power & Fire Safety', 'Stakeholder': 'Resident Risk', 'Score': res_fire_risk},
    
    {'Theme': 'Rest & Environment', 'Stakeholder': 'Rider Demand', 'Score': r_rest_need},
    {'Theme': 'Rest & Environment', 'Stakeholder': 'Merchant Risk', 'Score': m_hygiene_risk},
    {'Theme': 'Rest & Environment', 'Stakeholder': 'Resident Risk', 'Score': res_noise_risk},
    
    {'Theme': 'Management & Intent', 'Stakeholder': 'Merchant Intent', 'Score': m_base_intent},
    {'Theme': 'Management & Intent', 'Stakeholder': 'Resident Rule Support', 'Score': res_mgmt_support}
]

df_collision = pd.DataFrame(collision_data)

plt.figure(figsize=(14, 8))
sns.set_theme(style="whitegrid", context="talk")
plt.rcParams['axes.unicode_minus'] = False

palette = {'Rider Demand': '#3498db', 'Merchant Risk': '#e67e22', 'Resident Risk': '#e74c3c', 
           'Merchant Intent': '#f1c40f', 'Resident Rule Support': '#2ecc71'}

ax = sns.barplot(data=df_collision, x='Theme', y='Score', hue='Stakeholder', palette=palette)

plt.title('Three-party Stakeholder Collision Analysis', fontsize=22, pad=30, fontweight='bold')
plt.ylabel('Intensity Score (0-100)', fontsize=16)
plt.xlabel('')
plt.ylim(0, 120)

for p in ax.patches:
    height = p.get_height()
    if height > 0:
        ax.text(p.get_x() + p.get_width()/2., height + 2, f'{height:.1f}', ha="center", fontsize=12, fontweight='bold')

plt.legend(title='Stakeholder Perspective', bbox_to_anchor=(1.05, 1), loc='upper left')

output_img = os.path.join(base_dir, '../image_chart/three_party/stakeholder_collision_analysis.png')
output_csv = os.path.join(base_dir, '../image_chart/three_party/stakeholder_collision_results.csv')
plt.savefig(output_img, dpi=300, bbox_inches='tight')

df_pivot = df_collision.pivot(index='Theme', columns='Stakeholder', values='Score')
df_pivot.to_csv(output_csv)

print(f">>> 三方对撞分析完成！")
print(f">>> 对撞图表已保存至: {output_img}")
print(f">>> 汇总数据表已保存至: {output_csv}")

conflict_power = (r_charge_need + m_safety_risk + res_fire_risk) / 3
conflict_rest = (r_rest_need + m_hygiene_risk + res_noise_risk) / 3

print("-" * 30)
print(f"核心发现 - 充电/消防矛盾指数: {conflict_power:.2f}")
print(f"核心发现 - 休息/卫生矛盾指数: {conflict_rest:.2f}")
print("-" * 30)
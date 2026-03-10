import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

base_dir = os.path.dirname(__file__)
encoded_file_path = os.path.join(base_dir, '../data/resident_final_encoded.csv')
df = pd.read_csv(encoded_file_path, encoding='utf-8-sig')

sns.set_theme(style="whitegrid", context="talk")
plt.rcParams['axes.unicode_minus'] = False

attitude_labels = {1: 'Very Unsupportive', 2: 'Unsupportive', 3: 'Neutral', 4: 'Supportive', 5: 'Very Supportive'}
nimby_labels = {0: 'Accept Near Home', 1: 'Reject Near Home'}

translation_map = {
    'StreetRest_不希望聚集': 'Dislike Crowding',
    'StreetRest_影响美观': 'Aesthetics Issue',
    'StreetRest_没感觉': 'No Feeling',
    'StreetRest_觉得辛苦': 'Sympathy',
    'ResConcern_充电消防隐患': 'Fire Hazards',
    'ResConcern_充电消防隐患,噪音/卫生问题': 'Fire & Noise/Hygiene',
    'ResConcern_噪音/卫生问题': 'Noise & Hygiene',
    'ResConcern_噪音/卫生问题,充电消防隐患': 'Noise/Hygiene & Fire',
    'MgmtRule_物业监督': 'Property Management Oversight',
    'MgmtRule_物业监督,禁止吸烟': 'PM Oversight & No Smoking',
    'MgmtRule_禁止吸烟': 'No Smoking Policy',
    'MgmtRule_禁止吸烟,物业监督': 'No Smoking & PM Oversight'
}

plt.figure(figsize=(12, 7))
att_counts = df['Overall_Attitude_Code'].value_counts().sort_index()
x_labels = [attitude_labels.get(i, str(i)) for i in att_counts.index]
sns.barplot(x=x_labels, y=att_counts.values, palette='RdYlGn')
plt.title('Resident Overall Attitude towards Delivery Stations', fontsize=20, pad=20)
plt.ylabel('Resident Count')
plt.xlabel('Attitude Level')
for i, v in enumerate(att_counts.values):
    plt.text(i, v + 0.5, str(v), ha='center', fontweight='bold')
plt.savefig(os.path.join(base_dir, '../image_chart/descriptive/resident_1_attitude.png'), dpi=300, bbox_inches='tight')

plt.figure(figsize=(10, 7))
nimby_counts = df['NIMBY_Sensitivity_Code'].value_counts().sort_index()
plt.pie(nimby_counts.values, 
        labels=[nimby_labels.get(i, str(i)) for i in nimby_counts.index], 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=['#66b3ff','#ff9999'], 
        explode=(0.05, 0),
        textprops={'fontsize': 14})
plt.title('NIMBY Sensitivity: Acceptance Near Home', fontsize=20, pad=20)
plt.savefig(os.path.join(base_dir, '../image_chart/descriptive/resident_2_nimby.png'), dpi=300, bbox_inches='tight')

concern_cols = [c for c in df.columns if c.startswith('ResConcern_')]
concern_sum = df[concern_cols].sum().sort_values(ascending=False)
concern_labels = [translation_map.get(c, c) for c in concern_sum.index]
plt.figure(figsize=(14, 7))
sns.barplot(x=concern_sum.values / len(df) * 100, y=concern_labels, palette='Oranges_r')
plt.title('Primary Resident Concerns (%)', fontsize=22, pad=25)
plt.xlabel('Percentage of Residents (%)')
plt.xlim(0, 110)
plt.savefig(os.path.join(base_dir, '../image_chart/descriptive/resident_3_concerns.png'), dpi=300, bbox_inches='tight')

mgmt_cols = [c for c in df.columns if c.startswith('MgmtRule_')]
mgmt_sum = df[mgmt_cols].sum().sort_values(ascending=False)
mgmt_labels = [translation_map.get(c, c) for c in mgmt_sum.index]
plt.figure(figsize=(14, 7))
sns.barplot(x=mgmt_sum.values / len(df) * 100, y=mgmt_labels, palette='GnBu_r')
plt.title('Preferred Management Rules (%)', fontsize=22, pad=25)
plt.xlabel('Percentage of Residents (%)')
plt.xlim(0, 110)
plt.savefig(os.path.join(base_dir, '../image_chart/descriptive/resident_4_mgmt.png'), dpi=300, bbox_inches='tight')

key_vars = ['Overall_Attitude_Code', 'NIMBY_Sensitivity_Code', 'See_Rider_Freq_Code']
desc_stats = df[key_vars].describe().T
desc_stats.to_csv(os.path.join(base_dir, '../image_chart/descriptive/resident_descriptive_summary.csv'), index=False)
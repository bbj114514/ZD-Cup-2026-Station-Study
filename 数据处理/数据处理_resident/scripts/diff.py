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

age_labels = {1: '18-24', 2: '25-30', 3: '31-40', 4: '41+'}
reside_labels = {1: '<1yr', 2: '1-5yrs', 3: '5yrs+'}
freq_labels = {1: 'Rarely', 2: 'Occasionally', 3: 'Frequently'}

results = []
group_vars = [
    ('Age_Group_Code', age_labels, 'Age Group'),
    ('Reside_Duration_Code', reside_labels, 'Reside Duration'),
    ('See_Rider_Freq_Code', freq_labels, 'Visual Frequency')
]

for col, labels, name in group_vars:
    groups_att = [df[df[col] == val]['Overall_Attitude_Code'] for val in sorted(df[col].unique())]
    h_att, p_att = stats.kruskal(*groups_att)
    
    groups_will = [df[df[col] == val]['Discussion_Will_Code'] for val in sorted(df[col].unique())]
    h_will, p_will = stats.kruskal(*groups_will)
    
    contingency = pd.crosstab(df[col], df['NIMBY_Sensitivity_Code'])
    chi2, p_chi, dof, ex = stats.chi2_contingency(contingency)
    
    results.append({'Variable': name, 'Target': 'Overall Attitude', 'p-value': p_att})
    results.append({'Variable': name, 'Target': 'Discussion Will', 'p-value': p_will})
    results.append({'Variable': name, 'Target': 'NIMBY Sensitivity', 'p-value': p_chi})

res_df = pd.DataFrame(results)
res_df.to_csv(os.path.join(base_dir, '../image_chart/diff/resident_diff_results.csv'), index=False)
print(res_df)

df_plot = df.copy()

plt.figure(figsize=(10, 6))
df_plot['Age_Label'] = df_plot['Age_Group_Code'].map(age_labels)
sns.barplot(x='Age_Label', y='Discussion_Will_Code', data=df_plot, 
            palette='Blues', capsize=.1, errorbar='se', order=age_labels.values())
plt.title('Discussion Willingness by Age Group (p=0.042)', fontsize=18, pad=20)
plt.ylabel('Mean Score (1-5)')
plt.ylim(1, 5)
plt.savefig(os.path.join(base_dir, '../image_chart/diff/diff_resident_age_will.png'), dpi=300, bbox_inches='tight')

plt.figure(figsize=(10, 6))
df_plot['Reside_Label'] = df_plot['Reside_Duration_Code'].map(reside_labels)
sns.barplot(x='Reside_Label', y='Overall_Attitude_Code', data=df_plot, 
            palette='Greens', capsize=.1, errorbar='se', order=reside_labels.values())
plt.title('Overall Attitude by Reside Duration (p=0.267)', fontsize=18, pad=20)
plt.ylabel('Mean Score (1-5)')
plt.ylim(1, 5)
plt.savefig(os.path.join(base_dir, '../image_chart/diff/diff_resident_reside_attitude.png'), dpi=300, bbox_inches='tight')

plt.figure(figsize=(12, 7))
pivot_data = pd.crosstab(df_plot['Reside_Label'], df_plot['NIMBY_Sensitivity_Code'], normalize='index') * 100
pivot_data.columns = ['Accept Near Home', 'Reject Near Home']
pivot_data = pivot_data.reindex(reside_labels.values())

ax = pivot_data.plot(kind='bar', stacked=True, color=['#3498db', '#e74c3c'], figsize=(12, 7))
plt.title('NIMBY Sensitivity by Reside Duration', fontsize=20, pad=20)
plt.ylabel('Percentage (%)')
plt.xticks(rotation=0)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

for p in ax.patches:
    h = p.get_height()
    if h > 5:
        ax.text(p.get_x()+p.get_width()/2, p.get_y()+h/2, f'{h:.1f}%', 
                ha='center', va='center', color='white', fontweight='bold')

plt.savefig(os.path.join(base_dir, '../image_chart/diff/diff_resident_nimby_stacked.png'), dpi=300, bbox_inches='tight')
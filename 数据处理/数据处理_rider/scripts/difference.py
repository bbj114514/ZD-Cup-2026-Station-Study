import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

plt.rcParams['axes.unicode_minus'] = False
sns.set_context("talk")
sns.set_style("whitegrid")

def run_differentiation_analysis(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return
    df = pd.read_csv(file_path)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    group_ft = df[df['Delivery_Type'] == 1]['PU_Efficiency']
    group_cs = df[df['Delivery_Type'] == 2]['PU_Efficiency']
    t_stat, p_val_t = stats.ttest_ind(group_ft, group_cs)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Delivery_Type', y='PU_Efficiency', data=df, palette='muted', capsize=.1)
    plt.title(f'PU Difference by Delivery Type\n(p-value: {p_val_t:.3f})', fontsize=18)
    plt.xticks([0, 1], ['Full-time', 'Crowdsourced'])
    plt.savefig(os.path.join(base_dir, '../image/diff/diff_1_delivery_type.png'), dpi=300)

    groups_wh = [df[df['Work_Hours'] == i]['BI_Usage'] for i in [1, 2, 3, 4]]
    f_stat_wh, p_val_wh = stats.f_oneway(*groups_wh)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Work_Hours', y='BI_Usage', data=df, palette='Spectral', capsize=.1)
    plt.title(f'Usage Intent by Work Hours\n(p-value: {p_val_wh:.3f})', fontsize=18)
    plt.xticks([0, 1, 2, 3], ['<4h', '4-8h', '8-12h', '>12h'])
    plt.savefig(os.path.join(base_dir, '../image/diff/diff_2_work_hours.png'), dpi=300)

    groups_inc = [df[df['Monthly_Income'] == i]['BI_Usage'] for i in [1, 2, 3, 4]]
    f_stat_inc, p_val_inc = stats.f_oneway(*groups_inc)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Monthly_Income', y='BI_Usage', data=df, palette='YlOrBr', capsize=.1)
    plt.title(f'Usage Intent by Monthly Income\n(p-value: {p_val_inc:.3f})', fontsize=18)
    plt.xticks([0, 1, 2, 3], ['<5k', '5k-8k', '8k-12k', '>12k'])
    plt.savefig(os.path.join(base_dir, '../image/diff/diff_3_income_level.png'), dpi=300)

    groups_area = [df[df['Area_Type'] == i]['PU_Efficiency'] for i in [1, 2, 3]]
    f_stat_area, p_val_area = stats.f_oneway(*groups_area)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Area_Type', y='PU_Efficiency', data=df, palette='coolwarm', capsize=.1)
    plt.title(f'PU Difference by Area Type\n(p-value: {p_val_area:.3f})', fontsize=18)
    plt.xticks([0, 1, 2], ['Residential', 'Commercial', 'Mixed'])
    plt.savefig(os.path.join(base_dir, '../image/diff/diff_4_area_type.png'), dpi=300)
    
    print("-" * 30)
    print(f"Differentiation Analysis Summary:")
    print(f"1. Delivery Type (T-test) p: {p_val_t:.4f}")
    print(f"2. Work Hours (ANOVA)     p: {p_val_wh:.4f}")
    print(f"3. Monthly Income (ANOVA) p: {p_val_inc:.4f}")
    print(f"4. Area Type (ANOVA)      p: {p_val_area:.4f}")
    print("-" * 30)

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '../data/rider_encoded.csv') 

run_differentiation_analysis(file_path)
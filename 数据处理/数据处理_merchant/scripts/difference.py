import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '../data/merchant_final_encoded.csv')
df = pd.read_csv(file_path)

sns.set_theme(style="whitegrid", context="talk")
plt.rcParams['axes.unicode_minus'] = False

shop_type_map = {
    '便利店/小超市': 'Convenience Store',
    '餐饮店': 'Restaurant',
    '药店/诊所': 'Pharmacy',
    '其他服务店': 'Other Services'
}

concern_map = {
    '安全责任问题': 'Safety & Liability',
    '影响店面卫生': 'Hygiene & Cleanliness'
    
}

shop_cols = [c for c in df.columns if c.startswith('ShopType_')]
shop_data = []
for col in shop_cols:
    raw_type = col.replace('ShopType_', '')
    type_name = shop_type_map.get(raw_type, raw_type)
    
    vals = df[df[col] == 1]['Collab_Intent_Code']
    for v in vals:
        shop_data.append({'Type': type_name, 'Intent': v})
shop_df = pd.DataFrame(shop_data)

groups = [df[df[col] == 1]['Collab_Intent_Code'] for col in shop_cols]
f_stat, p_val_shop = stats.f_oneway(*groups)

plt.figure(figsize=(12, 7))
sns.barplot(x='Type', y='Intent', data=shop_df, palette='Set2', capsize=.1, errorbar='se')
plt.title(f'Collaboration Intent by Shop Type (p={p_val_shop:.3f})', fontsize=20, pad=20)
plt.xlabel('Shop Type')
plt.ylabel('Mean Intent Score (0-2)')
plt.xticks(rotation=15)
plt.savefig(os.path.join(base_dir, '../image_chart/diff/merchant_diff_shop_type.png'), dpi=300, bbox_inches='tight')

loc_labels = {0: 'Far', 1: '100m Radius', 2: 'At Entrance'}
loc_groups = [df[df['Shop_Loc_Code'] == i]['Collab_Intent_Code'] for i in [0, 1, 2]]
f_stat_loc, p_val_loc = stats.f_oneway(*loc_groups)

plt.figure(figsize=(10, 6))
sns.barplot(x=df['Shop_Loc_Code'].map(loc_labels), y=df['Collab_Intent_Code'], palette='coolwarm', capsize=.1)
plt.title(f'Intent Score by Location (p={p_val_loc:.3f})', fontsize=20, pad=20)
plt.xlabel('Location')
plt.ylabel('Mean Intent Score (0-2)')
plt.savefig(os.path.join(base_dir, '../image_chart/diff/merchant_diff_location.png'), dpi=300, bbox_inches='tight')

concern_cols = [c for c in df.columns if c.startswith('Concern_')]
cross_results = []

for s_col in shop_cols:
    raw_type = s_col.replace('ShopType_', '')
    type_name = shop_type_map.get(raw_type, raw_type)
    
    for c_col in concern_cols:
        raw_concern = c_col.replace('Concern_', '')
        concern_name = concern_map.get(raw_concern, raw_concern)
        
        ratio = df[df[s_col] == 1][c_col].mean() * 100
        cross_results.append({'ShopType': type_name, 'Concern': concern_name, 'Percentage': ratio})

cross_df = pd.DataFrame(cross_results)

plt.figure(figsize=(14, 8))
sns.barplot(x='ShopType', y='Percentage', hue='Concern', data=cross_df, palette='Reds')
plt.title('Specific Concerns across Different Shop Types (%)', fontsize=20, pad=20)
plt.xlabel('Shop Type')
plt.ylabel('Prevalence within Group (%)')
plt.legend(title='Concerns', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=15)
plt.savefig(os.path.join(base_dir, '../image_chart/diff/merchant_diff_concerns_cross.png'), dpi=300, bbox_inches='tight')

print(f"ANOVA Results: ShopType p={p_val_shop:.4f}, Location p={p_val_loc:.4f}")
print("Differentiation analysis charts (English version) have been generated successfully.")
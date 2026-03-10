import pandas as pd
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '../data/merchant_final_encoded.csv')
df = pd.read_csv(file_path)

df['Intent_Binary'] = (df['Collab_Intent_Code'] > 0).astype(int)

predictors = [
    'Age_Group_Code',
    'Shop_Loc_Code', 
    'Rider_Cust_Rate_Code',
    'ShopType_餐饮店', 
    'ShopType_便利店/小超市'
]

valid_predictors = [p for p in predictors if p in df.columns and df[p].nunique() > 1]

X = df[valid_predictors].astype(float)
X = sm.add_constant(X)
y = df['Intent_Binary']

model = sm.Logit(y, X).fit()
print(model.summary())

results_df = pd.DataFrame({
    'Variable': model.params.index,
    'Coefficient': model.params.values,
    'P-value': model.pvalues.values,
    'OR': np.exp(model.params.values)
}).drop('const', errors='ignore')

name_map = {
    'Age_Group_Code': 'Merchant Age',
    'Shop_Loc_Code': 'Proximity to Community',
    'Rider_Cust_Rate_Code': 'Rider Visit Freq',
    'ShopType_餐饮店': 'Is Restaurant',
    'ShopType_便利店/小超市': 'Is Convenience Store'
}
results_df['Variable'] = results_df['Variable'].map(lambda x: name_map.get(x, x))

plt.figure(figsize=(12, 7))
sns.set_theme(style="whitegrid", context="talk")

sns.pointplot(x='Coefficient', y='Variable', data=results_df, join=False, color='darkred', markers='D')
plt.axvline(0, color='gray', linestyle='--', alpha=0.7)

plt.title('Predictors of Merchant Collaboration Intent (Logit)', fontsize=20, pad=20)
plt.xlabel('Regression Coefficient (Beta)')
plt.ylabel('Predictor Factors')

output_img = os.path.join(base_dir, '../image_chart/driver_regression/merchant_intent_regression_forest.png')
plt.savefig(output_img, dpi=300, bbox_inches='tight')

results_df.to_csv(os.path.join(base_dir, '../image_chart/driver_regression/merchant_regression_results.csv'), index=False)

print(f">>> 意愿回归分析完成！森林图已保存至: {output_img}")
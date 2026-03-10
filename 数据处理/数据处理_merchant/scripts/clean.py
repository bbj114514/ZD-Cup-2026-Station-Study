import pandas as pd
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '../data/merchant.csv')

df = pd.read_csv(file_path)
print(f"读取原始数据，形状为: {df.shape}")

duration_threshold = df['Duration'].quantile(0.05)
mask_duration = df['Duration'] <= duration_threshold
print(f"1. 答题时长筛查：剔除时长 <= {duration_threshold:.2f}秒 的样本 {mask_duration.sum()} 份")

mask_conflict_stay = (df['Rider_Cust_Rate'] == '很少') & (df['Current_Stay_Status'] == '经常有')
print(f"2. 行为矛盾筛查：剔除‘到店极少但停留极多’样本 {mask_conflict_stay.sum()} 份")


invalid_mask = mask_duration | mask_conflict_stay
df_cleaned = df[~invalid_mask].copy()

print("-" * 30)
print(f"原始样本总数: {len(df)}")
print(f"总计剔除无效样本: {invalid_mask.sum()} 份")
print(f"最终有效样本总数: {len(df_cleaned)}")
print(f"有效率: {(len(df_cleaned)/len(df)*100):.2f}%")
print("-" * 30)

output_file = os.path.join(base_dir, '../data/merchant_cleaned_logic.csv')
df_cleaned.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"清洗后的数据已保存至: {output_file}")
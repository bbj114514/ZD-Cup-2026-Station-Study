import pandas as pd
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '../data/rider.csv')

df = pd.read_csv(file_path)
print(df.shape)

def cronbach_alpha(df):
    k = df.shape[1]  # 题目数量
    item_variances = df.var(axis=0, ddof=1)  # 每个题目的方差
    total_variance = df.sum(axis=1).var(ddof=1)  # 每个受访者总分的方差
    alpha = (k / (k - 1)) * (1 - item_variances.sum() / total_variance)
    return alpha

def get_citc(df_dimension):
    results = {}
    for col in df_dimension.columns:
        # 计算该项与其他项之和的相关系数
        other_sum = df_dimension.drop(columns=[col]).sum(axis=1)
        corr = df_dimension[col].corr(other_sum)
        results[col] = corr
    return results

pu_items = ['PU_Efficiency', 'PU_Safety', 'PU_Value']      # 感知有用性
peou_items = ['PEOU_Search', 'PEOU_Process', 'PEOU_Habit'] # 感知易用性
bi_items = ['BI_Usage', 'BI_Recommend']                   # 使用意愿

all_scale = pu_items + peou_items + bi_items
print(f"全量表总信度: {cronbach_alpha(df[all_scale]):.3f}")

df_cleaned = pd.read_csv(os.path.join(base_dir, '../data/rider_cleaned.csv'))
print(f"清洗后全量表总信度: {cronbach_alpha(df_cleaned[all_scale]):.3f}")
print(f"清洗前后全量表总信度变化: {cronbach_alpha(df_cleaned[all_scale]) - cronbach_alpha(df[all_scale]):.3f}")

print(f"清洗前 PU 信度: {cronbach_alpha(df[pu_items]):.3f}, 清洗后 PU 信度: {cronbach_alpha(df_cleaned[pu_items]):.3f}")
print(f"清洗前 PEOU 信度: {cronbach_alpha(df[peou_items]):.3f}, 清洗后 PEOU 信度: {cronbach_alpha(df_cleaned[peou_items]):.3f}")
print(f"清洗前 BI 信度: {cronbach_alpha(df[bi_items]):.3f}, 清洗后 BI 信度: {cronbach_alpha(df_cleaned[bi_items]):.3f}")

pu_items = ['PU_Efficiency', 'PU_Safety', 'PU_Value']
pu_citc = get_citc(df[pu_items])
print(pu_citc)

peou_items = ['PEOU_Search', 'PEOU_Process', 'PEOU_Habit']
peou_citc = get_citc(df[peou_items])
print(peou_citc)

bi_items = ['BI_Usage', 'BI_Recommend']
bi_citc = get_citc(df[bi_items])
print(bi_citc)

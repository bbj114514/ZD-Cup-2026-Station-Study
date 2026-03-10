import pandas as pd
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '../data/rider.csv')

df = pd.read_csv(file_path)

print(df.shape)
print(df.columns)

# 对骑手数据进行清洗

for index, row in df.iterrows():
    if row["Attention_Check"] != 1:
        print(f"注意力测试未通过，ID: {row['ID']}")
        df.drop(index, inplace=True)

print(df.shape)


duration_threshold = df["Duration"].quantile(0.05)
print(f"答题时间前5%分位数: {duration_threshold}秒")
for index, row in df.iterrows():
    if row["Duration"] < duration_threshold:
        print(f"答题时间过短，ID: {row['ID']}, Duration: {row['Duration']}秒")
        df.drop(index, inplace=True)

print(df.shape)

# 规律性作答排查（重点排查量表题
scale_cols = [
    'PU_Efficiency', 'PU_Safety', 'PU_Value', 
    'PEOU_Search', 'PEOU_Process', 'PEOU_Habit', 
    'BI_Usage', 'BI_Recommend'
]  # 避开质控题

df['Scale_Variance'] = df[scale_cols].var(axis=1)
variance_threshold = 0.3

for index, row in df.iterrows():
    if row['Scale_Variance'] == 0:
        print(f"方差为0，ID：{row['ID']}")
        df.drop(index, inplace=True)
    # if row['Scale_Variance'] < 0.3:
    #     if row['Duration'] < 60:
    #         print(f"方差小于0.3，且答题时间小于60s")
    #         df.drop(index, inplace=True)

print(df.shape)

# 逻辑一致性排查
# 年龄和工作年限的逻辑关系
# 投入产出悖论
# 初始化可疑度评分列
df['Suspicion_Score'] = 0

for index, row in df.iterrows():
    if row["Age_Group"] == "18-24" and row["Career_Duration"] == "3年以上":
        print(f"工作年限逻辑存疑，ID: {row['ID']}")
        # df.drop(index, inplace=True)
        # 可疑记录，暂不删除，可疑度加1
        df.at[index, 'Suspicion_Score'] += 1

    if row["Work_Hours"] == "少于4小时" and row["Monthly_Income"] == "5000-8000元":
        print(f"投入产出存疑，ID: {row['ID']}")
        # df.drop(index, inplace=True)
        # 可疑记录，暂不删除
        df.at[index, 'Suspicion_Score'] += 1
    if row["Work_Hours"] == "少于4小时" and row["Monthly_Income"] == "8000-12000元":
        print(f"投入产出悖论，ID: {row['ID']}")
        df.drop(index, inplace=True)
    if row["Work_Hours"] == "少于4小时" and row["Monthly_Income"] == "12000元以上":
        print(f"投入产出悖论，ID: {row['ID']}")
        df.drop(index, inplace=True)

    if row["Work_Hours"] == "4-8小时" and row["Monthly_Income"] == "12000元以上":
        print(f"投入产出存疑，ID: {row['ID']}")
        # df.drop(index, inplace=True)
        df.at[index, 'Suspicion_Score'] += 1
    
    if row["Work_Hours"] == "8-12小时" and row["Monthly_Income"] == "5000元以下":
        print(f"投入产出存疑，ID: {row['ID']}")
        df.at[index, 'Suspicion_Score'] += 1
    
    if row["Work_Hours"] == "超过12小时" and row["Monthly_Income"] == "5000元以下":
        print(f"投入产出存疑，ID: {row['ID']}")
        df.at[index, 'Suspicion_Score'] += 2

print(df.shape)

# 计算有效率
valid_rate = (df.shape[0] / 287) * 100
print(f"有效率: {valid_rate:.2f}%")

# 计算无效样本量
invalid_count = 287 - df.shape[0]
print(f"无效样本量: {invalid_count}")

df.to_csv(os.path.join(base_dir, '../data/rider_cleaned.csv'), index=False, encoding='utf-8-sig')
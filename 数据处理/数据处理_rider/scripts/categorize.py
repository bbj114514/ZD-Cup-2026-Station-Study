import pandas as pd
import os


base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '../data/data_renamed.csv')

df = pd.read_csv(file_path)

print(df.shape)
print(df.columns)

# 获取不同角色的列名
columns_rider = df.iloc[:, 0:27].columns.tolist()
columns_merchant = df.iloc[:, 0:4].columns.tolist() + df.iloc[:, 27:35].columns.tolist()
columns_resident = df.iloc[:, 0:4].columns.tolist() + df.iloc[:, 35:].columns.tolist()

# 使用列表收集数据
rider_data = [] 
merchant_data = []
resident_data = []

for index, row in df.iterrows():
    role = row["Role"]
    if role == "外卖骑手":
        rider_data.append(row[columns_rider])
    elif role == "社区周边商户":
        merchant_data.append(row[columns_merchant])
    elif role == "社区居民":
        resident_data.append(row[columns_resident])

# 创建DataFrame时指定列名
df_rider = pd.DataFrame(rider_data, columns=columns_rider)
df_merchant = pd.DataFrame(merchant_data, columns=columns_merchant)
df_resident = pd.DataFrame(resident_data, columns=columns_resident)

df_rider.to_csv(os.path.join(base_dir, '../data/rider.csv'), index=False, encoding='utf-8-sig')
df_merchant.to_csv(os.path.join(base_dir, '../data/merchant.csv'), index=False, encoding='utf-8-sig')
df_resident.to_csv(os.path.join(base_dir, '../data/resident.csv'), index=False, encoding='utf-8-sig')
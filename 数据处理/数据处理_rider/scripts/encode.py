import pandas as pd
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '../data/rider_cleaned.csv')

df = pd.read_csv(file_path)

encoding_rules = {
    'Age_Group': {'18-24岁': 1, '25-30岁': 2, '31-40岁': 3, '41岁及以上': 4},
    'Delivery_Type': {'专送': 1, '众包': 2},
    'Area_Type': {'住宅区/社区为主': 1, '商业区/写字楼为主': 2, '混合区域': 3},
    'Work_Hours': {'少于4小时': 1, '4-8小时': 2, '8-12小时': 3, '超过12小时': 4},
    'Career_Duration': {'不到6个月': 1, '6个月-1年': 2, '1-3年': 3, '3年以上': 4},
    'Monthly_Income': {'5000元以下': 1, '5000-8000元': 2, '8000-12000元': 3, '12000元以上': 4}
}

for column, mapping in encoding_rules.items():
    df[column] = df[column].map(mapping)

rename_map = {
    '找不到合适地方休息': 'Q7_Rest_Issue',
    '饮水不便': 'Q7_Water_Issue',
    '手机/电瓶车充电难': 'Q7_Charge_Issue',
    '上厕所不便': 'Q7_Toilet_Issue',
    '身体疲劳无处缓解': 'Q7_Fatigue_Issue',
    '应急庇护': 'Q8_Shelter',
    '便利服务': 'Q8_Service',
    '充足的电瓶车停车位': 'Q8_Parking',
    '基础休憩': 'Q8_Rest_Area',
    '充电续航': 'Q8_Battery',
    '向骑手收取少量费用': 'Q21_Pay_Rider',
    '广告收入': 'Q21_Pay_Ads',
    '由外卖平台承担': 'Q21_Pay_Platform',
    '完全由政府出资': 'Q21_Pay_Gov'
}

multi_select_cols = ['Inconvenience_M', 'Feature_Importance_M', 'Cost_Bearing_M']

for original_col in multi_select_cols:
    df[original_col] = df[original_col].astype(str).str.replace('，', ',')
    temp_dummies = df[original_col].str.get_dummies(sep=',')
    temp_dummies.columns = temp_dummies.columns.str.strip()
    temp_dummies.columns = [rename_map.get(col, f"{original_col}_{col}") for col in temp_dummies.columns]
    df = pd.concat([df, temp_dummies], axis=1)

additional_encoding = {
    'Usage_Exp': {'是，经常用': 3, '是，偶尔用': 2, '知道，但从没用过': 1, '完全不知道': 0},
    'Loc_Preference': {'小区大门/物业办公室旁': 1, '外卖柜集中点附近': 2, '社区便利店/超市内': 3, '社区内部公共活动中心': 4},
    'Scheme_Choice': {'A（高频便利型）': 1, 'B（综合保障型）': 2},
    'Pay_Willingness': {'愿意支付': 3, '视情况而定': 2, '不太愿意': 1, '完全不愿意': 0}
}

for col, mapping in additional_encoding.items():
    df[col] = df[col].map(mapping)

df['PU_Score'] = df[['PU_Efficiency', 'PU_Safety', 'PU_Value']].mean(axis=1)
df['PEOU_Score'] = df[['PEOU_Search', 'PEOU_Process', 'PEOU_Habit']].mean(axis=1)
df['BI_Score'] = df[['BI_Usage', 'BI_Recommend']].mean(axis=1)

q7_cols = [c for c in df.columns if 'Q7_' in c]
df['Urgency_Total'] = df[q7_cols].sum(axis=1)

df['Willing_To_Pay_Flag'] = df['Pay_Willingness'].apply(lambda x: 1 if x in [2, 3] else 0)
df['Pay_Propensity'] = df['Pay_Willingness'].apply(lambda x: 1 if x >= 2 else 0)
df['TAM_Total'] = df[['PU_Score', 'PEOU_Score', 'BI_Score']].mean(axis=1)

target_columns = [
    'Age_Group', 'Delivery_Type', 'Area_Type', 'Usage_Exp', 'Work_Hours', 
    'Loc_Preference', 'Scheme_Choice', 'PU_Efficiency', 'PU_Safety', 'PU_Value', 
    'PEOU_Search', 'PEOU_Process', 'PEOU_Habit', 'BI_Usage', 'BI_Recommend', 
    'Pay_Willingness', 'Ad_Acceptance', 'Career_Duration', 'Monthly_Income', 
    'Q7_Toilet_Issue', 'Q7_Charge_Issue', 'Q7_Rest_Issue', 'Q7_Fatigue_Issue', 'Q7_Water_Issue', 
    'Q8_Service', 'Q8_Battery', 'Q8_Parking', 'Q8_Rest_Area', 'Q8_Shelter', 
    'Q21_Pay_Rider', 'Q21_Pay_Gov', 'Q21_Pay_Ads', 'Q21_Pay_Platform', 
    'PU_Score', 'PEOU_Score', 'BI_Score', 'Urgency_Total', 
    'Willing_To_Pay_Flag', 'TAM_Total', 'Pay_Propensity'
]

df_final = df[target_columns]

out_path = os.path.join(base_dir, '../data/rider_encoded.csv')
df_final.to_csv(out_path, index=False, encoding='utf-8-sig')
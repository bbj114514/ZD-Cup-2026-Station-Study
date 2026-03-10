import pandas as pd
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '../primary_data/primary_data.csv')


df = pd.read_csv(file_path)

print(df.shape)
print(df.columns)

# Rename columns

# 基于《问卷04.pdf》的全量映射字典
rename_mapping = {
    "ID": "ID",
    "答题时间": "Duration",
    "Q1_身份": "Role",
    "Q2_年龄段": "Age_Group",
    
    # --- 骑手路径 (Path A: Q3-Q25) ---
    "Q3_配送类型": "Delivery_Type",
    "Q4_配送区域类型": "Area_Type",
    "Q5_是否用过驿站": "Usage_Exp",
    "Q6_跑单时长": "Work_Hours",
    "Q7_最不便方面_多选": "Inconvenience_M",
    "Q8_驿站重要功能_多选": "Feature_Importance_M",
    "Q9_驿站选址偏好": "Loc_Preference",
    "Q10_方案取舍": "Scheme_Choice",
    
    # TAM 核心量表 (Q11-Q19)
    "Q11_效率恢复_量表": "PU_Efficiency",     # 感知有用性 1
    "Q12_安全缓冲_量表": "PU_Safety",         # 感知有用性 2
    "Q13_价值感知_量表": "PU_Value",          # 感知有用性 3
    "Q14_寻找难易_量表": "PEOU_Search",       # 感知易用性 1
    "Q15_注意力测试_量表": "Attention_Check", # 质控项 (必须为1)
    "Q16_使用流程_量表": "PEOU_Process",      # 感知易用性 2
    "Q17_习惯难度_量表": "PEOU_Habit",        # 感知易用性 3
    "Q18_使用可能_量表": "BI_Usage",          # 行为意愿 1
    "Q19_推荐意愿_量表": "BI_Recommend",      # 行为意愿 2
    
    "Q20_运营费用承担_多选": "Cost_Bearing_M",
    "Q21_付费意愿": "Pay_Willingness",
    "Q22_广告接受度_量表": "Ad_Acceptance",
    "Q23_运营顾虑_开放": "Rider_Concern_Open",
    "Q24_从业时间": "Career_Duration",
    "Q25_月收入": "Monthly_Income",
    
    # --- 商户路径 (Path B: Q26-Q33) ---
    "Q26_商户店铺类型": "Shop_Type",
    "Q27_商户店址位置": "Shop_Loc",
    "Q28_骑手客源占比": "Rider_Cust_Rate",
    "Q29_目前骑手停留情况": "Current_Stay_Status",
    "Q30_参与合作意向": "Collab_Intent",
    "Q31_合作顾虑点_多选": "Merchant_Concern_M",
    "Q32_激励方式偏好_多选": "Incentive_Pref_M",
    "Q33_商户具体想法_开放": "Merchant_Idea_Open",
    
    # --- 居民路径 (Path C: Q34-Q42) ---
    "Q34_居民见骑手频率": "See_Rider_Freq",
    "Q35_对骑手露宿态度": "Attitude_Street_Rest",
    "Q36_对驿站总体态度": "Overall_Attitude",
    "Q37_50米内距离敏感度": "NIMBY_Sensitivity", # 邻避效应
    "Q38_居民主要担忧_多选": "Resident_Concern_M",
    "Q39_驿站管理原则_多选": "Mgmt_Principle_M",
    "Q40_参与讨论意愿": "Discussion_Will",
    "Q41_居民建议建议_开放": "Resident_Suggest_Open",
    "Q42_社区居住时长": "Reside_Duration"
}

df_renamed = df.rename(columns=rename_mapping)
new_path = os.path.join(base_dir, '../data/data_renamed.csv')
df_renamed.to_csv(new_path, index=False, encoding='utf-8-sig')
import semopy
import pandas as pd
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '../test_data/rider_cleaned.csv')

# 1. 定义模型逻辑 (依照编码手册)
model_desc = """
    PU =~ PU_Efficiency + PU_Safety + PU_Value
    PEOU =~ PEOU_Search + PEOU_Process + PEOU_Habit
    BI =~ BI_Usage + BI_Recommend
"""

# 2. 运行模型
df = pd.read_csv(file_path)
model = semopy.Model(model_desc)
model.fit(df)

# 3. 获取拟合指标
stats = semopy.calc_stats(model)
print(stats.T) # 查看 CFI, TLI, RMSEA 等

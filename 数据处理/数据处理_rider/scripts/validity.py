import pandas as pd
import os 
from factor_analyzer.factor_analyzer import calculate_kmo, calculate_bartlett_sphericity
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '../data/rider_cleaned.csv')

df = pd.read_csv(file_path)
print(df.shape)

scale_cols = ['PU_Efficiency', 'PU_Safety', 'PU_Value', 
              'PEOU_Search', 'PEOU_Process', 'PEOU_Habit', 
              'BI_Usage', 'BI_Recommend']

# KMO 检验
kmo_all, kmo_model = calculate_kmo(df[scale_cols])
print(f"KMO 检验结果: {kmo_model:.3f}") 

# Bartlett's 球形检验
chi_square_value, p_value = calculate_bartlett_sphericity(df[scale_cols])
print(f"Bartlett's 球形检验结果: chi-square={chi_square_value:.3f}, p-value={p_value:.3e}")

data = df[scale_cols]

scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

pca = PCA(n_components=3)
pca.fit(data_scaled)

# --- 指标 A: 计算累计方差解释率 ---
variance_ratio = pca.explained_variance_ratio_
cumulative_variance = np.sum(variance_ratio)
print(f"累计方差解释率: {cumulative_variance:.2%}")

# --- 指标 B: 计算因子负荷量 ---
# 负荷量 = 特征向量 * sqrt(特征值)
loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
loadings_df = pd.DataFrame(loadings, index=scale_cols, columns=['F1', 'F2', 'F3'])
print(loadings_df)
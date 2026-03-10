import pandas as pd
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_wtp_logistic_regression(file_path):
    df = pd.read_csv(file_path)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. 准备变量 (Feature Engineering)
    # 计算均值维度
    df['PU'] = df[['PU_Efficiency', 'PU_Safety', 'PU_Value']].mean(axis=1)
    df['PEOU'] = df[['PEOU_Search', 'PEOU_Process', 'PEOU_Habit']].mean(axis=1)
    
    # 选择预测变量：收入、工作时长、感知有用性、感知易用性、配送类型
    # 目标变量：Pay_Propensity (1=Yes, 0=No)
    X_cols = ['Monthly_Income', 'Work_Hours', 'PU', 'PEOU', 'Delivery_Type']
    X = df[X_cols]
    X = sm.add_constant(X)  # 添加常数项
    y = df['Pay_Propensity']
    
    # 2. 拟合 Logistic 模型
    model = sm.Logit(y, X).fit()
    
    # 3. 提取结果
    summary_df = pd.DataFrame({
        'Coefficient': model.params,
        'P-value': model.pvalues,
        'Odds_Ratio': np.exp(model.params) # 优势比：更有说服力的指标
    })
    
    print("\nLogistic Regression Results (Willingness to Pay):")
    print(summary_df)
    
    # 4. 绘制森林图 (Forest Plot)
    plt.figure(figsize=(12, 6))
    results_to_plot = summary_df.drop('const')
    
    # 绘制点和误差棒 (这里简化展示系数)
    sns.pointplot(x=results_to_plot['Coefficient'], y=results_to_plot.index, linestyles='none', color='darkred')
    plt.axvline(0, color='gray', linestyle='--') # 0线，左侧负相关，右侧正相关
    
    plt.title('Factors Influencing Willingness to Pay (Logistic Coefficients)', fontsize=18, pad=20)
    plt.xlabel('Regression Coefficient (Beta)')
    plt.ylabel('Predictors')
    plt.savefig(os.path.join(base_dir, '../image/willingness_to_pay/analysis_wtp_logistic_forest.png'), dpi=300, bbox_inches='tight')
    
    return model

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '../test_data/rider_encoded.csv')
# 运行
run_wtp_logistic_regression(file_path)
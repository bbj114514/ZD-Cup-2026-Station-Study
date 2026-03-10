import pandas as pd
import os

def clean_resident_data(file_path):
    df = pd.read_csv(file_path)
    initial_count = len(df)
    
    duration_threshold = df['Duration'].quantile(0.05)
    mask_duration = df['Duration'] > duration_threshold
    
    df['Resident_Suggest_Open'] = df['Resident_Suggest_Open'].fillna('未填写')
    
    invalid_keywords = ['无', '没有', '...', '123', 'aaa', 'ok']
    df['text_quality_bad'] = df['Resident_Suggest_Open'].apply(
        lambda x: len(str(x).strip()) < 2 or str(x).strip() in invalid_keywords
    )
    
    df_cleaned = df[mask_duration].copy()
    
    print(f"--- 居民卷清洗报告 ---")
    print(f"原始样本总数: {initial_count}")
    print(f"时长筛选阈值: {duration_threshold:.2f} 秒")
    print(f"因时长过短被剔除: {initial_count - len(df[mask_duration])} 份")
    print(f"最终有效样本数: {len(df_cleaned)}")
    print(f"有效率: {(len(df_cleaned)/initial_count*100):.2f}%")
    print("-" * 25)
    
    output_file = os.path.join(base_dir, '../data/resident_cleaned.csv')
    df_cleaned.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"清洗后的数据已保存至: {output_file}")
    print(f"无效样本量: {initial_count - len(df_cleaned)}")
    
    return df_cleaned

base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, '../data/resident.csv')

df_res_cleaned = clean_resident_data(file_path)
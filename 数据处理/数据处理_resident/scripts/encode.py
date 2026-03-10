import pandas as pd
import os

def encode_resident_data(file_path):
    df = pd.read_csv(file_path)
    
    duration_threshold = df['Duration'].quantile(0.05)
    df = df[df['Duration'] > duration_threshold].copy()
    
    age_map = {'18-24岁': 1, '25-30岁': 2, '31-40岁': 3, '41岁及以上': 4}
    freq_map = {'很少看到': 1, '偶尔看到': 2, '经常看到': 3}
    attitude_map = {'非常不支持': 1, '不太支持': 2, '中立': 3, '比较支持': 4, '非常支持': 5}
    nimby_map = {'否': 0, '是': 1}
    will_map = {'不愿意': 1, '不太愿意': 2, '无所谓': 3, '愿意': 4, '非常愿意': 5}
    duration_reside_map = {'少于1年': 1, '1-5年': 2, '5年以上': 3}
    
    df['Age_Group_Code'] = df['Age_Group'].map(age_map)
    df['See_Rider_Freq_Code'] = df['See_Rider_Freq'].map(freq_map)
    df['Overall_Attitude_Code'] = df['Overall_Attitude'].map(attitude_map)
    df['NIMBY_Sensitivity_Code'] = df['NIMBY_Sensitivity'].map(nimby_map)
    df['Discussion_Will_Code'] = df['Discussion_Will'].map(will_map)
    df['Reside_Duration_Code'] = df['Reside_Duration'].map(duration_reside_map)
    
    attitude_street_dummies = pd.get_dummies(df['Attitude_Street_Rest'], prefix='StreetRest')
    df = pd.concat([df, attitude_street_dummies], axis=1)
    
    concern_dummies = df['Resident_Concern_M'].str.get_dummies(sep=',').add_prefix('ResConcern_')
    mgmt_dummies = df['Mgmt_Principle_M'].str.get_dummies(sep=',').add_prefix('MgmtRule_')
    
    df = pd.concat([df, concern_dummies, mgmt_dummies], axis=1)
    
    original_cols = [
        'Age_Group', 'See_Rider_Freq', 'Attitude_Street_Rest', 
        'Overall_Attitude', 'NIMBY_Sensitivity', 'Resident_Concern_M', 
        'Mgmt_Principle_M', 'Discussion_Will', 'Reside_Duration'
    ]
    useless_cols = ['ID', 'Duration', 'Role']
    
    cols_to_drop = original_cols + useless_cols
    df_final = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
    
    output_dir = os.path.dirname(file_path)
    output_file = os.path.join(output_dir, '../data/resident_final_encoded.csv')
    df_final.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f">>> 居民卷编码完成！")
    print(f">>> 已处理样本数: {len(df_final)}")
    return df_final

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '../data/resident.csv')
    df_res_final = encode_resident_data(file_path)
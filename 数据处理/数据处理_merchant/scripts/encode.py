import pandas as pd
import os

def finalize_merchant_encoding(file_path):
    df = pd.read_csv(file_path)
    
    mappings = {
        'Age_Group': {'18-24岁': 1, '25-30岁': 2, '31-40岁': 3, '41岁及以上': 4},
        'Shop_Loc': {'否': 0, '是，在100米内': 1, '是，就在小区门口': 2},
        'Rider_Cust_Rate': {'很少': 1, '偶尔来': 2, '是，经常来': 3},
        'Current_Stay_Status': {'从未有过': 0, '很少有': 1, '偶尔有': 2, '经常有': 3},
        'Collab_Intent': {'不愿意': 0, '可以考虑': 1, '非常愿意': 2}
    }
    
    for col, mapping in mappings.items():
        if col in df.columns:
            df[col + '_Code'] = df[col].map(mapping)
    
    concern_dummies = df['Merchant_Concern_M'].str.get_dummies(sep=',').add_prefix('Concern_')
    incentive_dummies = df['Incentive_Pref_M'].str.get_dummies(sep=',').add_prefix('Incentive_')
    
    df = pd.concat([df, concern_dummies, incentive_dummies], axis=1)
    
    shop_type_dummies = pd.get_dummies(df['Shop_Type'], prefix='ShopType')
    df = pd.concat([df, shop_type_dummies], axis=1)
    
    original_cols = [
        'Age_Group', 'Shop_Loc', 'Rider_Cust_Rate', 
        'Current_Stay_Status', 'Collab_Intent',
        'Merchant_Concern_M', 'Incentive_Pref_M', 'Shop_Type'
    ]
    
    useless_cols = ['ID', 'Duration', 'Role']
    
    cols_to_drop = original_cols + useless_cols
    df_final = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
    
    output_dir = os.path.dirname(file_path)
    output_file = os.path.join(output_dir, 'merchant_final_encoded.csv')
    df_final.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f">>> 编码与清理任务完成！")
    print(f">>> 已删除列: {cols_to_drop}")
    print(f">>> 当前数据集列数: {len(df_final.columns)}")
    return df_final

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cleaned_file_path = os.path.join(base_dir, '../data/merchant_cleaned_logic.csv')
    df_final = finalize_merchant_encoding(cleaned_file_path)
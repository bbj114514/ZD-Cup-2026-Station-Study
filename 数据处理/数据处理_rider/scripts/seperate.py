import pandas as pd
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(base_dir, '../primary_data/primary_data(open.csv')

df = pd.read_csv(input_file)

open_cols = ['Q23_运营顾虑_开放', 'Q33_商户具体想法_开放', 'Q41_居民建议建议_开放']

open_data = df[open_cols].copy()
open_data.to_csv(os.path.join(base_dir, '../../open/open_data.csv'), index=False, encoding='utf-8-sig')

df[open_cols] = None
df.to_csv(os.path.join(base_dir, '../primary_data/primary_data.csv'), index=False, encoding='utf-8-sig')
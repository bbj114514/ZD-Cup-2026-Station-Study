import pandas as pd
import matplotlib.pyplot as plt
import os

base_dir = os.path.dirname(__file__)
encoded_file_path = os.path.join(base_dir, '../data/resident_final_encoded.csv')
df = pd.read_csv(encoded_file_path, encoding='utf-8-sig')

concern_cols = [c for c in df.columns if c.startswith('ResConcern_')]

concern_map = {
    'ResConcern_充电消防隐患': 'Fire Hazards',
    'ResConcern_充电消防隐患,噪音/卫生问题': 'Fire & Noise/Hygiene',
    'ResConcern_噪音/卫生问题': 'Noise & Hygiene',
    'ResConcern_噪音/卫生问题,充电消防隐患': 'Noise/Hygiene & Fire'
}

concern_sum = df[concern_cols].sum().sort_values(ascending=False)
concern_df = pd.DataFrame({
    'Concern': [concern_map.get(c, c) for c in concern_sum.index], 
    'Frequency': concern_sum.values
})

concern_df['CumulativePercentage'] = concern_df['Frequency'].cumsum() / concern_df['Frequency'].sum() * 100

fig, ax1 = plt.subplots(figsize=(12, 8))

ax1.bar(concern_df['Concern'], concern_df['Frequency'], color='steelblue', alpha=0.8)
ax1.set_xlabel('Resident Concerns', fontsize=14)
ax1.set_ylabel('Frequency (Count)', fontsize=14)

ax2 = ax1.twinx()
ax2.plot(concern_df['Concern'], concern_df['CumulativePercentage'], color='red', marker='D', ms=7, label='Cumulative %')
ax2.axhline(80, color='orange', linestyle='--', alpha=0.6)
ax2.set_ylabel('Cumulative Percentage (%)', fontsize=14)
ax2.set_ylim(0, 110)

plt.title('Pareto Analysis of Resident Concerns', fontsize=18, pad=20)
plt.savefig('resident_pareto_concerns.png', dpi=300, bbox_inches='tight')
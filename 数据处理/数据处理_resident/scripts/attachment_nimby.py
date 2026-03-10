import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '../data/resident_final_encoded.csv')
df_res = pd.read_csv(file_path)

sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = ['Arial'] 
plt.rcParams['axes.unicode_minus'] = False
sns.set_context("paper", font_scale=1.2)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

duration_map = {1: '<1 Year', 2: '1-5 Years', 3: '>5 Years'}
counts = df_res['Reside_Duration_Code'].map(duration_map).value_counts().sort_index()

colors = sns.color_palette('pastel')[0:3]
ax1.pie(counts, labels=counts.index, autopct='%1.1f%%', 
        startangle=140, colors=colors, wedgeprops={'edgecolor': 'white', 'linewidth': 1})
ax1.set_title('(a) Sample Residence Duration', fontsize=14, fontweight='bold', pad=15)

df_plot = df_res.copy()
df_plot['jitter_x'] = df_plot['Reside_Duration_Code'] + np.random.uniform(-0.15, 0.15, size=len(df_plot))
df_plot['jitter_y'] = df_plot['NIMBY_Sensitivity_Code'] + np.random.uniform(-0.1, 0.1, size=len(df_plot))

sns.regplot(x='jitter_x', y='jitter_y', data=df_plot, ax=ax2, 
            scatter_kws={'alpha': 0.4, 'color': '#5D6D7E', 's': 40}, 
            line_kws={'color': '#E74C3C', 'lw': 2.5, 'label': 'Trend Line'})

ax2.set_xticks([1, 2, 3])
ax2.set_xticklabels(['<1 Year', '1-5 Years', '>5 Years'])
ax2.set_yticks([0, 1])
ax2.set_yticklabels(['Low (0)', 'High (1)'])

ax2.set_title('(b) Tenure vs. NIMBY Sensitivity', fontsize=14, fontweight='bold', pad=15)
ax2.set_xlabel('Length of Residence', fontsize=12)
ax2.set_ylabel('NIMBY Sensitivity Score', fontsize=12)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend(loc='upper left')

plt.tight_layout()
plt.savefig(os.path.join(base_dir, '../image_chart/figure_5_2_resident_analysis_en.png'), dpi=300, bbox_inches='tight')
print("Figure 5-2 has been generated and saved as: figure_5_2_resident_analysis_en.png")
# plt.show()
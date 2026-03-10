import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def generate_tam_path_diagram(file_path):
    df = pd.read_csv(file_path)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    df['PU'] = df[['PU_Efficiency', 'PU_Safety', 'PU_Value']].mean(axis=1)
    df['PEOU'] = df[['PEOU_Search', 'PEOU_Process', 'PEOU_Habit']].mean(axis=1)
    df['BI'] = df[['BI_Usage', 'BI_Recommend']].mean(axis=1)

    res1 = sm.OLS(df['PU'], sm.add_constant(df['PEOU'])).fit()
    b_peou_pu = res1.params['PEOU']
    p_peou_pu = res1.pvalues['PEOU']
    r2_pu = res1.rsquared

    res2 = sm.OLS(df['BI'], sm.add_constant(df[['PEOU', 'PU']])).fit()
    b_peou_bi = res2.params['PEOU']
    p_peou_bi = res2.pvalues['PEOU']
    b_pu_bi = res2.params['PU']
    p_pu_bi = res2.pvalues['PU']
    r2_bi = res2.rsquared

    def get_stars(p):
        if p < 0.001: return "***"
        if p < 0.01: return "**"
        if p < 0.05: return "*"
        return "ns"

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')

    pos = {'PEOU': (2, 4), 'PU': (5, 6), 'BI': (8, 4)}

    for label, (x, y) in pos.items():
        node_text = label
        if label == 'PU': node_text += f"\n(R²={r2_pu:.2f})"
        if label == 'BI': node_text += f"\n(R²={r2_bi:.2f})"
        
        box = patches.FancyBboxPatch((x-0.8, y-0.6), 1.6, 1.2, boxstyle="round,pad=0.1", 
                                     ec="black", fc="white", lw=2)
        ax.add_patch(box)
        ax.text(x, y, node_text, ha='center', va='center', fontsize=14, fontweight='bold')

    ax.annotate("", xy=(pos['PU'][0]-0.5, pos['PU'][1]-0.2), xytext=(pos['PEOU'][0]+0.5, pos['PEOU'][1]+0.2),
                arrowprops=dict(arrowstyle="->", lw=2, color='blue'))
    ax.text(3.2, 5.3, f"β={b_peou_pu:.3f}{get_stars(p_peou_pu)}", color='blue', rotation=30)

    ax.annotate("", xy=(pos['BI'][0]-0.5, pos['BI'][1]+0.2), xytext=(pos['PU'][0]+0.5, pos['PU'][1]-0.2),
                arrowprops=dict(arrowstyle="->", lw=2, color='green'))
    ax.text(6.8, 5.3, f"β={b_pu_bi:.3f}{get_stars(p_pu_bi)}", color='green', rotation=-30)

    ax.annotate("", xy=(pos['BI'][0]-0.8, pos['BI'][1]), xytext=(pos['PEOU'][0]+0.8, pos['PEOU'][1]),
                arrowprops=dict(arrowstyle="->", lw=2, color='red', ls='--'))
    ax.text(5, 3.7, f"β={b_peou_bi:.3f}{get_stars(p_peou_bi)}", color='red', ha='center')

    plt.title("TAM Structural Model Path Analysis", fontsize=18, pad=20)
    plt.savefig(os.path.join(base_dir, '../image/TAM/tam_path_diagram.png'), dpi=300, bbox_inches='tight')
    print(">>> Path diagram generated: tam_path_diagram.png")

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '../data/rider_encoded.csv')
generate_tam_path_diagram(file_path)
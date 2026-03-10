import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
rider_file = os.path.join(base_dir, '../data/rider_encoded.csv')
merchant_file = os.path.join(base_dir, '../data/merchant_final_encoded.csv')
rider_df = pd.read_csv(rider_file)
merchant_df = pd.read_csv(merchant_file)

def generate_mismatch_analysis():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    demand_metrics = {
        'Fast Charging': 'Q7_Charge_Issue',
        'Drinking Water': 'Q7_Water_Issue',
        'Rest Area': 'Q7_Rest_Issue',
        'Restroom': 'Q7_Toilet',
        'Parking': 'Q8_Parking'
    }
    
    if 'Q7_Toilet_Issue' in rider_df.columns:
        demand_metrics['Restroom'] = 'Q7_Toilet_Issue'
    
    demand_scores = {}
    for label, col in demand_metrics.items():
        if col in rider_df.columns:
            demand_scores[label] = rider_df[col].mean() * 100
        else:
            demand_scores[label] = 0
            
    base_intent = merchant_df['Collab_Intent_Code'].mean() / 2.0
    
    safety_penalty = merchant_df['Concern_安全责任问题'].mean() * 0.7
    hygiene_penalty = merchant_df['Concern_影响店面卫生'].mean() * 0.5
    
    supply_scores = {
        'Fast Charging': base_intent * (1 - safety_penalty) * 100,
        'Drinking Water': base_intent * 1.1 * 100,
        'Rest Area': base_intent * (1 - hygiene_penalty) * 100,
        'Restroom': base_intent * 0.3 * 100,
        'Parking': base_intent * 0.6 * 100
    }

    mismatch_df = pd.DataFrame({
        'Service': list(demand_scores.keys()),
        'Rider Demand': [demand_scores[k] for k in demand_scores.keys()],
        'Merchant Supply': [supply_scores[k] for k in demand_scores.keys()]
    })
    
    print("--- 供需错位得分汇总 ---")
    print(mismatch_df.round(2))

    labels = mismatch_df['Service'].values
    d_vals = mismatch_df['Rider Demand'].values
    s_vals = mismatch_df['Merchant Supply'].values
    
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    d_vals = np.concatenate((d_vals, [d_vals[0]]))
    s_vals = np.concatenate((s_vals, [s_vals[0]]))
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    sns.set_style("whitegrid")
    
    ax.plot(angles, d_vals, color='#3498db', linewidth=3, label='Rider Demand (Pain Points)')
    ax.fill(angles, d_vals, color='#3498db', alpha=0.2)
    
    ax.plot(angles, s_vals, color='#e67e22', linewidth=3, label='Merchant Supply (Willingness)')
    ax.fill(angles, s_vals, color='#e67e22', alpha=0.2)
    
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=14, fontweight='bold')
    
    plt.title('Community Station: Supply-Demand Mismatch Radar', fontsize=22, pad=40, fontweight='bold')
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1), fontsize=12)
    
    plt.savefig(os.path.join(base_dir, '../image_chart/mismatch/supply_demand_mismatch_radar.png'), dpi=300, bbox_inches='tight')
    mismatch_df.to_csv(os.path.join(base_dir, '../image_chart/mismatch/supply_demand_gap_results.csv'), index=False)
    print("\n>>> 分析完成！雷达图已保存为 'supply_demand_mismatch_radar.png'")

generate_mismatch_analysis()
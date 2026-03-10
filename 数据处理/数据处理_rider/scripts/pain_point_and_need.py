import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.rcParams['axes.unicode_minus'] = False
sns.set_context("talk")
sns.set_style("whitegrid")

def analyze_multi_select(df, prefix, title_name):
    cols = [c for c in df.columns if c.startswith(prefix)]
    
    counts = df[cols].sum().sort_values(ascending=False)
    
    counts.index = [i.replace(prefix, '') for i in counts.index]
    
    case_pct = (counts / len(df) * 100).round(2)
    
    return counts, case_pct

def run_needs_analysis(file_path):
    df = pd.read_csv(file_path)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    counts_q7, pct_q7 = analyze_multi_select(df, 'Q7_', 'Pain Points')
    
    fig, ax1 = plt.subplots(figsize=(14, 8))
    sns.barplot(x=pct_q7.index, y=pct_q7.values, ax=ax1, palette='OrRd_r')
    ax1.set_title('Analysis of Rider Pain Points (Q7)', fontsize=20, pad=20)
    ax1.set_ylabel('Case Percentage (%)')
    plt.xticks(rotation=45, ha='right')
    
    ax2 = ax1.twinx()
    cum_pct = pct_q7.cumsum() / pct_q7.sum() * 100
    ax2.plot(pct_q7.index, cum_pct, color='darkblue', marker='D', ms=7, label='Cumulative %')
    ax2.set_ylabel('Cumulative Percentage (%)')
    ax2.set_ylim(0, 105)
    
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, '../image/pain_point_and_need/analysis_q7_pareto.png'), dpi=300)
    
    q8_cols = [c for c in df.columns if c.startswith('Q8_')]
    needs_diff = df.groupby('Delivery_Type')[q8_cols].mean() * 100
    needs_diff.index = ['Full-time', 'Crowdsourced']
    needs_diff.columns = [c.replace('Q8_', '') for c in needs_diff.columns]
    
    needs_diff = needs_diff.T
    
    plt.figure(figsize=(14, 10))
    needs_diff.plot(kind='barh', figsize=(14, 10), color=['#4C72B0', '#DD8452'])
    plt.title('Feature Importance: Full-time vs Crowdsourced (%)', fontsize=20, pad=20)
    plt.xlabel('Importance Percentage (%)')
    plt.legend(title='Rider Type')
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, '../image/pain_point_and_need/analysis_q8_comparison.png'), dpi=300)
    
    print(">>> Pain point and Needs analysis completed!")
    print("\nTop 3 Pain Points (Case %):\n", pct_q7.head(3))


base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '../data/rider_encoded.csv')
run_needs_analysis(file_path)
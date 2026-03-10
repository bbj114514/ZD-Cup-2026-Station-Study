import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.rcParams['axes.unicode_minus'] = False
sns.set_context("talk")
sns.set_style("whitegrid")

def run_full_portrait_analysis(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return
    df = pd.read_csv(file_path)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    mappings = {
        'Age_Group': {1: '18-24', 2: '25-30', 3: '31-40', 4: '41+'},
        'Delivery_Type': {1: 'Full-time', 2: 'Crowdsourced'},
        'Work_Hours': {1: '<4h', 2: '4-8h', 3: '8-12h', 4: '>12h'},
        'Career_Duration': {1: '<6m', 2: '6m-1y', 3: '1-3y', 4: '>3y'},
        'Monthly_Income': {1: '<5k', 2: '5k-8k', 3: '8k-12k', 4: '>12k'},
        'Usage_Exp': {0: 'Unaware', 1: 'Aware/Unused', 2: 'Occasional', 3: 'Frequent'}
    }

    def safe_map(val, mapping_dict):
        if pd.isna(val): return "N/A"
        return mapping_dict.get(val, str(val))

    fig1, axes1 = plt.subplots(3, 2, figsize=(18, 22))
    fig1.suptitle('Sample Portrait Overview', fontsize=24, y=1.02)
    basic_cols = ['Age_Group', 'Delivery_Type', 'Work_Hours', 'Monthly_Income', 'Career_Duration', 'Usage_Exp']
    
    for i, col in enumerate(basic_cols):
        ax = axes1[i//2, i%2]
        plot_data = df[col].apply(lambda x: safe_map(x, mappings.get(col, {})))
        counts = plot_data.value_counts().sort_index()
        
        sns.barplot(x=counts.index, y=counts.values, ax=ax, palette='viridis')
        ax.set_title(f'Distribution of {col}', fontsize=18)
        ax.set_ylabel('Count')
        ax.tick_params(axis='x', rotation=15)
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, '../image/portrait/portrait_1_basic_overview.png'), dpi=300)
    print("Saved: portrait_1_basic_overview.png")
    
    plt.figure(figsize=(12, 7))
    temp_df = df.copy()
    temp_df['Delivery_Type'] = temp_df['Delivery_Type'].apply(lambda x: safe_map(x, mappings['Delivery_Type']))
    temp_df['Monthly_Income'] = temp_df['Monthly_Income'].apply(lambda x: safe_map(x, mappings['Monthly_Income']))
    
    ct_income = pd.crosstab(temp_df['Delivery_Type'], temp_df['Monthly_Income'], normalize='index') * 100
    sns.heatmap(ct_income, annot=True, fmt='.1f', cmap='YlGnBu', cbar_kws={'label': 'Percentage (%)'})
    plt.title('Income Structure by Delivery Type (%)', fontsize=20, pad=20)
    plt.xlabel('Monthly Income Range')
    plt.ylabel('Delivery Type')
    plt.savefig(os.path.join(base_dir, '../image/portrait/portrait_2_income_cross_pct.png'), dpi=300)
    print("Saved: portrait_2_income_cross_pct.png")
    
    plt.figure(figsize=(14, 8))
    temp_df['Work_Hours'] = temp_df['Work_Hours'].apply(lambda x: safe_map(x, mappings['Work_Hours']))
    temp_df['Usage_Exp'] = temp_df['Usage_Exp'].apply(lambda x: safe_map(x, mappings['Usage_Exp']))
    
    ct_usage = pd.crosstab(temp_df['Work_Hours'], temp_df['Usage_Exp'], normalize='index') * 100
    usage_order = ['Unaware', 'Aware/Unused', 'Occasional', 'Frequent']
    actual_order = [o for o in usage_order if o in ct_usage.columns]
    
    ct_usage[actual_order].plot(kind='barh', stacked=True, color=sns.color_palette("RdYlGn_r", len(actual_order)), ax=plt.gca())
    plt.title('Usage Experience by Daily Work Hours', fontsize=20, pad=20)
    plt.xlabel('Percentage (%)')
    plt.ylabel('Work Hours')
    plt.legend(title='Exp Level', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, '../image/portrait/portrait_3_usage_stacked.png'), dpi=300)
    print("Saved: portrait_3_usage_stacked.png")
    
    if 'Pay_Propensity' in df.columns:
        plt.figure(figsize=(10, 6))
        temp_df['Age_Group'] = temp_df['Age_Group'].apply(lambda x: safe_map(x, mappings['Age_Group']))
        age_pay = (temp_df.groupby('Age_Group')['Pay_Propensity'].mean() * 100)
        sns.barplot(x=age_pay.index, y=age_pay.values, palette='magma')
        plt.title('Pay Propensity by Age Group (%)', fontsize=20, pad=20)
        plt.ylabel('Willing to Pay (%)')
        plt.xlabel('Age Group')
        for i, v in enumerate(age_pay):
            plt.text(i, v + 1, f"{v:.1f}%", ha='center', fontweight='bold')
        plt.savefig(os.path.join(base_dir, '../image/portrait/portrait_4_age_pay_propensity.png'), dpi=300)
        print("Saved: portrait_4_age_pay_propensity.png")

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '../data/rider_encoded.csv')

run_full_portrait_analysis(file_path)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_preprocess_data(filepath):
    df = pd.read_csv(filepath)
    df['is_capital_cluster'] = df['city'].isin(['Astana', 'Almaty']).astype(int)
    return df

def generate_comprehensive_report(df):
    capital_group = df[df['is_capital_cluster'] == 1]
    regional_group = df[df['is_capital_cluster'] == 0]
    
    report = {
        'Capital_Avg_Mentors': capital_group['industry_mentors'].mean(),
        'Regional_Avg_Mentors': regional_group['industry_mentors'].mean(),
        'Capital_Avg_Grants_USD': capital_group['international_grants_usd'].mean(),
        'Regional_Avg_Grants_USD': regional_group['international_grants_usd'].mean(),
        'Capital_Avg_R_and_D': capital_group['r_and_d_projects_count'].mean(),
        'Regional_Avg_R_and_D': regional_group['r_and_d_projects_count'].mean(),
        'Capital_Retention_Rate_%': capital_group['talent_retention_rate_pct'].mean(),
        'Regional_Retention_Rate_%': regional_group['talent_retention_rate_pct'].mean(),
        'Mentors_Disparity_Ratio': capital_group['industry_mentors'].mean() / regional_group['industry_mentors'].mean(),
        'Funding_Disparity_Ratio': capital_group['international_grants_usd'].mean() / regional_group['international_grants_usd'].mean()
    }
    return pd.Series(report)

def generate_visualizations(df):
    sns.set_theme(style="whitegrid", palette="muted")
    fig, axes = plt.subplots(2, 2, figsize=(16, 11))
    
    # Chart 1: Funding vs Mentors Scatter with Hub Labels
    sns.scatterplot(
        data=df, x='industry_mentors', y='international_grants_usd', 
        hue='has_coworking', style='advanced_ai_labs', s=200, ax=axes[0,0], palette='deep'
    )
    for idx, row in df.iterrows():
        axes[0,0].text(row['industry_mentors']+0.8, row['international_grants_usd']+3000, row['city'], fontsize=9)
    axes[0,0].set_title('Figure 1: Capital Disparity (Mentors vs. International Grants)', fontsize=11, fontweight='bold')
    axes[0,0].set_xlabel('Industry Mentors')
    axes[0,0].set_ylabel('Grant Funding (USD)')
    
    # Chart 2: R&D Projects Count by City
    sns.barplot(data=df.sort_values('r_and_d_projects_count', ascending=False), x='city', y='r_and_d_projects_count', ax=axes[0,1], palette='Blues_r')
    axes[0,1].set_title('Figure 2: Active AI & Software R&D Projects per IT Hub', fontsize=11, fontweight='bold')
    axes[0,1].set_xlabel('City')
    axes[0,1].set_ylabel('R&D Projects Count')
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # Chart 3: Talent Retention Rate Comparison
    sns.barplot(data=df.sort_values('talent_retention_rate_pct', ascending=False), x='city', y='talent_retention_rate_pct', ax=axes[1,0], palette='Greens_r')
    axes[1,0].set_title('Figure 3: Regional Youth Talent Retention Rate (%)', fontsize=11, fontweight='bold')
    axes[1,0].set_xlabel('City')
    axes[1,0].set_ylabel('Retention Rate (%)')
    axes[1,0].tick_params(axis='x', rotation=45)
    
    # Chart 4: Correlation Heatmap
    numeric_cols = ['industry_mentors', 'international_grants_usd', 'r_and_d_projects_count', 'talent_retention_rate_pct', 'advanced_ai_labs']
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=axes[1,1])
    axes[1,1].set_title('Figure 4: Correlation Matrix of Infrastructure Variables', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('kazakhstan_ai_infrastructure_comprehensive.png', dpi=300)
    print("[SUCCESS] Multi-panel analytics visualization saved.")

if __name__ == '__main__':
    data_path = 'data/regional_hubs.csv'
    df = load_and_preprocess_data(data_path)
    
    print("=== KAZAKHSTAN REGIONAL IT HUBS ADVANCED DATA REPORT ===")
    summary = generate_comprehensive_report(df)
    print(summary)
    print("\nRendering analytical dashboards...")
    generate_visualizations(df)

#!/usr/bin/env python3
"""
Step 6: Time Trend Analysis and Visualizations
E-commerce Sales Optimization Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (15, 10)

def load_data():
    """Load the cleaned dataset"""
    try:
        df = pd.read_csv('data/superstore_sales_cleaned.csv')
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        print(f"✅ Loaded dataset: {df.shape}")
        return df
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def create_time_trend_visualizations(df):
    """Create comprehensive time trend visualizations"""
    print("\n" + "="*60)
    print("📈 CREATING TIME TREND VISUALIZATIONS")
    print("="*60)
    
    # 1. Monthly Sales and Profit Trends
    monthly_data = df.groupby(df['Order Date'].dt.to_period('M')).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Profit_Margin': 'mean',
        'Order ID': 'nunique'
    }).reset_index()
    
    monthly_data['Order Date'] = monthly_data['Order Date'].dt.to_timestamp()
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 12))
    
    # Monthly Sales Trend
    ax1.plot(monthly_data['Order Date'], monthly_data['Sales'], marker='o', linewidth=2, color='blue')
    ax1.set_title('Monthly Sales Trend', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Sales ($)')
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # Monthly Profit Trend
    ax2.plot(monthly_data['Order Date'], monthly_data['Profit'], marker='s', linewidth=2, color='green')
    ax2.set_title('Monthly Profit Trend', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Profit ($)')
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=45)
    
    # Monthly Profit Margin Trend
    ax3.plot(monthly_data['Order Date'], monthly_data['Profit_Margin'], marker='^', linewidth=2, color='red')
    ax3.set_title('Monthly Profit Margin Trend', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Profit Margin (%)')
    ax3.grid(True, alpha=0.3)
    ax3.tick_params(axis='x', rotation=45)
    
    # Monthly Order Count
    ax4.bar(monthly_data['Order Date'], monthly_data['Order ID'], color='orange', alpha=0.7)
    ax4.set_title('Monthly Order Count', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Number of Orders')
    ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('visualizations/monthly_trends.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Monthly trends visualization saved")
    
    return monthly_data

def create_category_performance_charts(df):
    """Create category performance visualizations"""
    print("\n📊 Creating category performance charts...")
    
    # Category analysis
    category_data = df.groupby('Category').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Profit_Margin': 'mean',
        'Order ID': 'nunique'
    }).reset_index()
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 12))
    
    # Sales by Category
    bars1 = ax1.bar(category_data['Category'], category_data['Sales'], color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    ax1.set_title('Total Sales by Category', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Sales ($)')
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}', ha='center', va='bottom')
    
    # Profit by Category
    bars2 = ax2.bar(category_data['Category'], category_data['Profit'], color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    ax2.set_title('Total Profit by Category', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Profit ($)')
    ax2.tick_params(axis='x', rotation=45)
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}', ha='center', va='bottom')
    
    # Profit Margin by Category
    bars3 = ax3.bar(category_data['Category'], category_data['Profit_Margin'], color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    ax3.set_title('Average Profit Margin by Category', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Profit Margin (%)')
    ax3.tick_params(axis='x', rotation=45)
    
    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom')
    
    # Order Count by Category
    bars4 = ax4.bar(category_data['Category'], category_data['Order ID'], color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    ax4.set_title('Order Count by Category', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Number of Orders')
    ax4.tick_params(axis='x', rotation=45)
    
    for bar in bars4:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:,.0f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('visualizations/category_performance.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Category performance charts saved")

def create_regional_analysis_charts(df):
    """Create regional performance visualizations"""
    print("\n🌍 Creating regional analysis charts...")
    
    # Regional analysis
    regional_data = df.groupby('Region').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Profit_Margin': 'mean'
    }).reset_index()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Sales by Region
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99']
    bars1 = ax1.bar(regional_data['Region'], regional_data['Sales'], color=colors)
    ax1.set_title('Total Sales by Region', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Sales ($)')
    ax1.tick_params(axis='x', rotation=45)
    
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}', ha='center', va='bottom')
    
    # Profit Margin by Region
    bars2 = ax2.bar(regional_data['Region'], regional_data['Profit_Margin'], color=colors)
    ax2.set_title('Average Profit Margin by Region', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Profit Margin (%)')
    ax2.tick_params(axis='x', rotation=45)
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('visualizations/regional_performance.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Regional performance charts saved")

def create_profitability_scatter_plot(df):
    """Create sales vs profit scatter plot by sub-category"""
    print("\n💰 Creating profitability scatter plot...")
    
    # Sub-category analysis
    subcategory_data = df.groupby('Sub-Category').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Profit_Margin': 'mean',
        'Category': 'first'
    }).reset_index()
    
    plt.figure(figsize=(14, 10))
    
    # Create scatter plot with different colors for each category
    categories = subcategory_data['Category'].unique()
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    for i, category in enumerate(categories):
        cat_data = subcategory_data[subcategory_data['Category'] == category]
        plt.scatter(cat_data['Sales'], cat_data['Profit'], 
                   c=colors[i], label=category, s=100, alpha=0.7)
    
    # Add trend line
    z = np.polyfit(subcategory_data['Sales'], subcategory_data['Profit'], 1)
    p = np.poly1d(z)
    plt.plot(subcategory_data['Sales'], p(subcategory_data['Sales']), 
             "r--", alpha=0.8, linewidth=2)
    
    # Annotate top performers
    top_profit = subcategory_data.nlargest(5, 'Profit')
    for idx, row in top_profit.iterrows():
        plt.annotate(row['Sub-Category'], 
                    (row['Sales'], row['Profit']),
                    xytext=(5, 5), textcoords='offset points',
                    fontsize=9, alpha=0.8)
    
    plt.xlabel('Total Sales ($)', fontsize=12)
    plt.ylabel('Total Profit ($)', fontsize=12)
    plt.title('Sales vs Profit by Sub-Category', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('visualizations/sales_vs_profit_scatter.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Profitability scatter plot saved")

def create_seasonal_analysis(df):
    """Analyze and visualize seasonal patterns"""
    print("\n🗓️ Creating seasonal analysis...")
    
    # Quarterly analysis
    quarterly_data = df.groupby(['Year', 'Quarter']).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    
    quarterly_data['Period'] = quarterly_data['Year'].astype(str) + '-Q' + quarterly_data['Quarter'].astype(str)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10))
    
    # Quarterly Sales
    ax1.bar(quarterly_data['Period'], quarterly_data['Sales'], color='skyblue', alpha=0.8)
    ax1.set_title('Quarterly Sales Performance', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Sales ($)')
    ax1.tick_params(axis='x', rotation=45)
    
    # Quarterly Profit
    ax2.bar(quarterly_data['Period'], quarterly_data['Profit'], color='lightcoral', alpha=0.8)
    ax2.set_title('Quarterly Profit Performance', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Profit ($)')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('visualizations/seasonal_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Day of week analysis
    dow_data = df.groupby('Day_of_Week').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    
    # Reorder by weekday
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_data['Day_of_Week'] = pd.Categorical(dow_data['Day_of_Week'], categories=day_order, ordered=True)
    dow_data = dow_data.sort_values('Day_of_Week')
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(dow_data['Day_of_Week'], dow_data['Sales'], color='lightgreen', alpha=0.8)
    plt.title('Sales by Day of Week', fontsize=14, fontweight='bold')
    plt.ylabel('Sales ($)')
    plt.xticks(rotation=45)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('visualizations/day_of_week_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Seasonal analysis charts saved")

def create_customer_segment_charts(df):
    """Create customer segment visualizations"""
    print("\n👥 Creating customer segment charts...")
    
    # Segment analysis
    segment_data = df.groupby('Segment').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Profit_Margin': 'mean',
        'Order ID': 'nunique'
    }).reset_index()
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Sales Distribution Pie Chart
    ax1.pie(segment_data['Sales'], labels=segment_data['Segment'], autopct='%1.1f%%', 
            startangle=90, colors=['#FF9999', '#66B2FF', '#99FF99'])
    ax1.set_title('Sales Distribution by Customer Segment', fontsize=12, fontweight='bold')
    
    # Profit Distribution Pie Chart
    ax2.pie(segment_data['Profit'], labels=segment_data['Segment'], autopct='%1.1f%%', 
            startangle=90, colors=['#FF9999', '#66B2FF', '#99FF99'])
    ax2.set_title('Profit Distribution by Customer Segment', fontsize=12, fontweight='bold')
    
    # Order Count by Segment
    bars3 = ax3.bar(segment_data['Segment'], segment_data['Order ID'], 
                    color=['#FF9999', '#66B2FF', '#99FF99'])
    ax3.set_title('Order Count by Customer Segment', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Number of Orders')
    ax3.tick_params(axis='x', rotation=45)
    
    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:,.0f}', ha='center', va='bottom')
    
    # Profit Margin by Segment
    bars4 = ax4.bar(segment_data['Segment'], segment_data['Profit_Margin'], 
                    color=['#FF9999', '#66B2FF', '#99FF99'])
    ax4.set_title('Average Profit Margin by Customer Segment', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Profit Margin (%)')
    ax4.tick_params(axis='x', rotation=45)
    
    for bar in bars4:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('visualizations/customer_segment_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Customer segment charts saved")

def create_summary_dashboard(df):
    """Create a comprehensive summary dashboard"""
    print("\n📊 Creating summary dashboard...")
    
    # Key metrics
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    avg_margin = df['Profit_Margin'].mean()
    total_orders = df['Order ID'].nunique()
    
    fig = plt.figure(figsize=(20, 12))
    
    # Create a 3x3 grid
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Key metrics text
    ax_metrics = fig.add_subplot(gs[0, :])
    ax_metrics.text(0.1, 0.7, f'Total Sales: ${total_sales:,.0f}', fontsize=16, fontweight='bold')
    ax_metrics.text(0.1, 0.5, f'Total Profit: ${total_profit:,.0f}', fontsize=16, fontweight='bold')
    ax_metrics.text(0.1, 0.3, f'Average Margin: {avg_margin:.1f}%', fontsize=16, fontweight='bold')
    ax_metrics.text(0.1, 0.1, f'Total Orders: {total_orders:,}', fontsize=16, fontweight='bold')
    ax_metrics.set_xlim(0, 1)
    ax_metrics.set_ylim(0, 1)
    ax_metrics.axis('off')
    ax_metrics.set_title('KEY PERFORMANCE METRICS', fontsize=18, fontweight='bold', pad=20)
    
    # Category performance
    ax1 = fig.add_subplot(gs[1, 0])
    category_sales = df.groupby('Category')['Sales'].sum()
    ax1.pie(category_sales.values, labels=category_sales.index, autopct='%1.1f%%')
    ax1.set_title('Sales by Category')
    
    # Regional performance
    ax2 = fig.add_subplot(gs[1, 1])
    regional_sales = df.groupby('Region')['Sales'].sum()
    ax2.bar(regional_sales.index, regional_sales.values, color=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99'])
    ax2.set_title('Sales by Region')
    ax2.tick_params(axis='x', rotation=45)
    
    # Monthly trend
    ax3 = fig.add_subplot(gs[1, 2])
    monthly_sales = df.groupby(df['Order Date'].dt.to_period('M'))['Sales'].sum()
    ax3.plot(range(len(monthly_sales)), monthly_sales.values, marker='o')
    ax3.set_title('Monthly Sales Trend')
    ax3.set_xlabel('Months')
    
    # Profit margin by category
    ax4 = fig.add_subplot(gs[2, 0])
    category_margin = df.groupby('Category')['Profit_Margin'].mean()
    ax4.bar(category_margin.index, category_margin.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    ax4.set_title('Profit Margin by Category')
    ax4.tick_params(axis='x', rotation=45)
    
    # Customer segments
    ax5 = fig.add_subplot(gs[2, 1])
    segment_sales = df.groupby('Segment')['Sales'].sum()
    ax5.pie(segment_sales.values, labels=segment_sales.index, autopct='%1.1f%%')
    ax5.set_title('Sales by Customer Segment')
    
    # Top sub-categories
    ax6 = fig.add_subplot(gs[2, 2])
    top_subcats = df.groupby('Sub-Category')['Sales'].sum().nlargest(5)
    ax6.barh(range(len(top_subcats)), top_subcats.values)
    ax6.set_yticks(range(len(top_subcats)))
    ax6.set_yticklabels(top_subcats.index)
    ax6.set_title('Top 5 Sub-Categories')
    
    plt.suptitle('E-COMMERCE SALES OPTIMIZATION DASHBOARD', fontsize=20, fontweight='bold')
    plt.savefig('visualizations/summary_dashboard.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Summary dashboard saved")

def main():
    """Main visualization execution function"""
    print("🚀 E-COMMERCE SALES OPTIMIZATION - VISUALIZATION ANALYSIS")
    print("="*60)
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Create all visualizations
    monthly_data = create_time_trend_visualizations(df)
    create_category_performance_charts(df)
    create_regional_analysis_charts(df)
    create_profitability_scatter_plot(df)
    create_seasonal_analysis(df)
    create_customer_segment_charts(df)
    create_summary_dashboard(df)
    
    print(f"\n✅ STEP 6 COMPLETED SUCCESSFULLY!")
    print(f"📊 All visualizations saved to visualizations/ folder")
    print(f"🎯 Ready for Step 7: Final Insights & Recommendations")
    
    return df

if __name__ == "__main__":
    main()

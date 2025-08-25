#!/usr/bin/env python3
"""
Step 4: Exploratory Data Analysis (EDA)
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
plt.rcParams['figure.figsize'] = (12, 8)

def load_cleaned_data():
    """Load the cleaned dataset"""
    try:
        # First run data cleaning if cleaned file doesn't exist
        import os
        if not os.path.exists('data/superstore_sales_cleaned.csv'):
            print("🔧 Running data cleaning first...")
            from data_cleaning import clean_and_prepare_data
            df = clean_and_prepare_data()
        else:
            df = pd.read_csv('data/superstore_sales_cleaned.csv')
            df['Order Date'] = pd.to_datetime(df['Order Date'])
            df['Ship Date'] = pd.to_datetime(df['Ship Date'])
            print(f"✅ Loaded cleaned dataset: {df.shape}")
        
        return df
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def analyze_category_performance(df):
    """Analyze performance by category and sub-category"""
    print("\n" + "="*60)
    print("📊 CATEGORY PERFORMANCE ANALYSIS")
    print("="*60)
    
    # Category-level analysis
    category_analysis = df.groupby('Category').agg({
        'Sales': ['count', 'sum', 'mean'],
        'Profit': ['sum', 'mean'],
        'Profit_Margin': 'mean'
    }).round(2)
    
    category_analysis.columns = ['Order_Count', 'Total_Sales', 'Avg_Sales', 
                               'Total_Profit', 'Avg_Profit', 'Avg_Profit_Margin']
    
    print("\n🏆 CATEGORY SUMMARY:")
    print(category_analysis.sort_values('Total_Sales', ascending=False))
    
    # Sub-category analysis (top 10)
    subcategory_analysis = df.groupby('Sub-Category').agg({
        'Sales': ['sum', 'count'],
        'Profit': 'sum',
        'Profit_Margin': 'mean'
    }).round(2)
    
    subcategory_analysis.columns = ['Total_Sales', 'Order_Count', 'Total_Profit', 'Avg_Profit_Margin']
    
    print(f"\n🥇 TOP 10 SUB-CATEGORIES BY SALES:")
    top_subcategories = subcategory_analysis.sort_values('Total_Sales', ascending=False).head(10)
    print(top_subcategories)
    
    print(f"\n💰 TOP 10 SUB-CATEGORIES BY PROFIT:")
    top_profit_subcategories = subcategory_analysis.sort_values('Total_Profit', ascending=False).head(10)
    print(top_profit_subcategories)
    
    return category_analysis, subcategory_analysis

def analyze_regional_performance(df):
    """Analyze performance by region and state"""
    print("\n" + "="*60)
    print("🌍 REGIONAL PERFORMANCE ANALYSIS")
    print("="*60)
    
    # Regional analysis
    regional_analysis = df.groupby('Region').agg({
        'Sales': ['count', 'sum', 'mean'],
        'Profit': ['sum', 'mean'],
        'Profit_Margin': 'mean'
    }).round(2)
    
    regional_analysis.columns = ['Order_Count', 'Total_Sales', 'Avg_Sales', 
                               'Total_Profit', 'Avg_Profit', 'Avg_Profit_Margin']
    
    print("\n🗺️ REGIONAL SUMMARY:")
    print(regional_analysis.sort_values('Total_Sales', ascending=False))
    
    # Top states analysis
    state_analysis = df.groupby('State').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Profit_Margin': 'mean'
    }).round(2)
    
    print(f"\n🏙️ TOP 10 STATES BY SALES:")
    top_states = state_analysis.sort_values('Sales', ascending=False).head(10)
    print(top_states)
    
    return regional_analysis, state_analysis

def analyze_customer_segments(df):
    """Analyze performance by customer segments"""
    print("\n" + "="*60)
    print("👥 CUSTOMER SEGMENT ANALYSIS")
    print("="*60)
    
    # Segment analysis
    segment_analysis = df.groupby('Segment').agg({
        'Sales': ['count', 'sum', 'mean'],
        'Profit': ['sum', 'mean'],
        'Profit_Margin': 'mean',
        'Customer ID': 'nunique'
    }).round(2)
    
    segment_analysis.columns = ['Order_Count', 'Total_Sales', 'Avg_Sales', 
                              'Total_Profit', 'Avg_Profit', 'Avg_Profit_Margin', 'Unique_Customers']
    
    print("\n👤 SEGMENT SUMMARY:")
    print(segment_analysis.sort_values('Total_Sales', ascending=False))
    
    # Customer value analysis
    customer_value = df.groupby('Customer ID').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique'
    }).round(2)
    
    customer_value.columns = ['Customer_Sales', 'Customer_Profit', 'Order_Count']
    
    print(f"\n💎 TOP 10 CUSTOMERS BY VALUE:")
    top_customers = customer_value.sort_values('Customer_Sales', ascending=False).head(10)
    print(top_customers)
    
    return segment_analysis, customer_value

def analyze_time_trends(df):
    """Analyze sales and profit trends over time"""
    print("\n" + "="*60)
    print("📈 TIME TREND ANALYSIS")
    print("="*60)
    
    # Monthly trends
    monthly_trends = df.groupby(['Year', 'Month']).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Profit_Margin': 'mean',
        'Order ID': 'nunique'
    }).round(2)
    
    monthly_trends.columns = ['Monthly_Sales', 'Monthly_Profit', 'Monthly_Margin', 'Monthly_Orders']
    
    print(f"\n📅 MONTHLY TRENDS (Last 12 months):")
    print(monthly_trends.tail(12))
    
    # Quarterly trends
    quarterly_trends = df.groupby(['Year', 'Quarter']).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Profit_Margin': 'mean'
    }).round(2)
    
    quarterly_trends.columns = ['Quarterly_Sales', 'Quarterly_Profit', 'Quarterly_Margin']
    
    print(f"\n📊 QUARTERLY TRENDS:")
    print(quarterly_trends)
    
    # Day of week analysis
    dow_analysis = df.groupby('Day_of_Week').agg({
        'Sales': ['sum', 'mean'],
        'Profit': 'sum',
        'Order ID': 'nunique'
    }).round(2)
    
    dow_analysis.columns = ['Total_Sales', 'Avg_Sales', 'Total_Profit', 'Order_Count']
    
    # Reorder by weekday
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_analysis = dow_analysis.reindex(day_order)
    
    print(f"\n📆 SALES BY DAY OF WEEK:")
    print(dow_analysis)
    
    return monthly_trends, quarterly_trends, dow_analysis

def create_summary_insights(df, category_analysis, regional_analysis, segment_analysis):
    """Generate key insights summary"""
    print("\n" + "="*60)
    print("🎯 KEY INSIGHTS SUMMARY")
    print("="*60)
    
    # Overall metrics
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    avg_margin = df['Profit_Margin'].mean()
    total_orders = df['Order ID'].nunique()
    
    print(f"\n📈 OVERALL PERFORMANCE:")
    print(f"   • Total Sales: ${total_sales:,.2f}")
    print(f"   • Total Profit: ${total_profit:,.2f}")
    print(f"   • Average Profit Margin: {avg_margin:.1f}%")
    print(f"   • Total Orders: {total_orders:,}")
    
    # Top performers
    top_category = category_analysis.loc[category_analysis['Total_Sales'].idxmax()]
    top_region = regional_analysis.loc[regional_analysis['Total_Sales'].idxmax()]
    top_segment = segment_analysis.loc[segment_analysis['Total_Sales'].idxmax()]
    
    print(f"\n🏆 TOP PERFORMERS:")
    print(f"   • Best Category: {top_category.name} (${top_category['Total_Sales']:,.2f})")
    print(f"   • Best Region: {top_region.name} (${top_region['Total_Sales']:,.2f})")
    print(f"   • Best Segment: {top_segment.name} (${top_segment['Total_Sales']:,.2f})")
    
    # Profitability insights
    best_margin_category = category_analysis.loc[category_analysis['Avg_Profit_Margin'].idxmax()]
    worst_margin_category = category_analysis.loc[category_analysis['Avg_Profit_Margin'].idxmin()]
    
    print(f"\n💰 PROFITABILITY INSIGHTS:")
    print(f"   • Highest Margin Category: {best_margin_category.name} ({best_margin_category['Avg_Profit_Margin']:.1f}%)")
    print(f"   • Lowest Margin Category: {worst_margin_category.name} ({worst_margin_category['Avg_Profit_Margin']:.1f}%)")
    
    # Loss analysis
    loss_orders = df[df['Profit'] < 0]
    loss_count = len(loss_orders)
    loss_percentage = (loss_count / len(df)) * 100
    
    print(f"\n⚠️ LOSS ANALYSIS:")
    print(f"   • Loss-making Orders: {loss_count:,} ({loss_percentage:.1f}%)")
    print(f"   • Total Loss Amount: ${loss_orders['Profit'].sum():,.2f}")

def save_eda_results(df, category_analysis, regional_analysis, segment_analysis, monthly_trends):
    """Save EDA results to files"""
    
    # Save summary tables
    with pd.ExcelWriter('eda_summary_tables.xlsx', engine='openpyxl') as writer:
        category_analysis.to_excel(writer, sheet_name='Category_Analysis')
        regional_analysis.to_excel(writer, sheet_name='Regional_Analysis')
        segment_analysis.to_excel(writer, sheet_name='Segment_Analysis')
        monthly_trends.to_excel(writer, sheet_name='Monthly_Trends')
    
    print(f"\n💾 EDA summary tables saved to: eda_summary_tables.xlsx")

def main():
    """Main EDA execution function"""
    print("🚀 E-COMMERCE SALES OPTIMIZATION - EDA ANALYSIS")
    print("="*60)
    
    # Load data
    df = load_cleaned_data()
    if df is None:
        return
    
    # Run analyses
    category_analysis, subcategory_analysis = analyze_category_performance(df)
    regional_analysis, state_analysis = analyze_regional_performance(df)
    segment_analysis, customer_value = analyze_customer_segments(df)
    monthly_trends, quarterly_trends, dow_analysis = analyze_time_trends(df)
    
    # Generate insights
    create_summary_insights(df, category_analysis, regional_analysis, segment_analysis)
    
    # Save results
    save_eda_results(df, category_analysis, regional_analysis, segment_analysis, monthly_trends)
    
    print(f"\n✅ STEP 4 COMPLETED SUCCESSFULLY!")
    print(f"📊 EDA analysis complete - ready for Step 5: Profitability Analysis")
    
    return df, category_analysis, regional_analysis, segment_analysis

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Step 5: Profitability Analysis
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

def analyze_high_sales_low_profit(df):
    """Identify high sales, low profit items - the profit traps"""
    print("\n" + "="*60)
    print("⚠️ HIGH SALES, LOW PROFIT ANALYSIS")
    print("="*60)
    
    # Sub-category analysis
    subcategory_profit = df.groupby('Sub-Category').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Profit_Margin': 'mean',
        'Order ID': 'nunique'
    }).round(2)
    
    subcategory_profit.columns = ['Total_Sales', 'Total_Profit', 'Avg_Profit_Margin', 'Order_Count']
    
    # Define high sales threshold (top 50% by sales)
    sales_threshold = subcategory_profit['Total_Sales'].median()
    
    # Identify profit traps: High sales but low margins
    profit_traps = subcategory_profit[
        (subcategory_profit['Total_Sales'] > sales_threshold) & 
        (subcategory_profit['Avg_Profit_Margin'] < 20)
    ].sort_values('Total_Sales', ascending=False)
    
    print(f"\n🚨 PROFIT TRAPS (High Sales, Low Margins < 20%):")
    if len(profit_traps) > 0:
        print(profit_traps)
        
        total_trap_sales = profit_traps['Total_Sales'].sum()
        total_trap_profit = profit_traps['Total_Profit'].sum()
        print(f"\n📊 Profit Trap Impact:")
        print(f"   • Total Sales in Traps: ${total_trap_sales:,.2f}")
        print(f"   • Total Profit from Traps: ${total_trap_profit:,.2f}")
        print(f"   • Average Margin in Traps: {profit_traps['Avg_Profit_Margin'].mean():.1f}%")
    else:
        print("   ✅ No significant profit traps identified!")
    
    # Identify profit stars: High sales AND high margins
    profit_stars = subcategory_profit[
        (subcategory_profit['Total_Sales'] > sales_threshold) & 
        (subcategory_profit['Avg_Profit_Margin'] > 30)
    ].sort_values('Total_Profit', ascending=False)
    
    print(f"\n⭐ PROFIT STARS (High Sales, High Margins > 30%):")
    if len(profit_stars) > 0:
        print(profit_stars)
    else:
        print("   No profit stars in high-sales categories")
    
    return profit_traps, profit_stars, subcategory_profit

def analyze_customer_profitability(df):
    """Analyze customer profitability patterns"""
    print("\n" + "="*60)
    print("👥 CUSTOMER PROFITABILITY ANALYSIS")
    print("="*60)
    
    # Customer-level profitability
    customer_profit = df.groupby('Customer ID').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Profit_Margin': 'mean',
        'Order ID': 'nunique'
    }).round(2)
    
    customer_profit.columns = ['Total_Sales', 'Total_Profit', 'Avg_Profit_Margin', 'Order_Count']
    customer_profit['Profit_Per_Order'] = customer_profit['Total_Profit'] / customer_profit['Order_Count']
    
    # Segment customers by profitability
    customer_profit['Profitability_Tier'] = pd.cut(
        customer_profit['Total_Profit'], 
        bins=[-np.inf, 0, 100, 500, np.inf],
        labels=['Loss', 'Low', 'Medium', 'High']
    )
    
    # Customer segment analysis
    segment_profit = df.groupby(['Segment', 'Customer ID']).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Profit_Margin': 'mean'
    }).reset_index()
    
    segment_summary = segment_profit.groupby('Segment').agg({
        'Sales': 'mean',
        'Profit': 'mean',
        'Profit_Margin': 'mean',
        'Customer ID': 'count'
    }).round(2)
    
    segment_summary.columns = ['Avg_Customer_Sales', 'Avg_Customer_Profit', 'Avg_Profit_Margin', 'Customer_Count']
    
    print(f"\n📊 CUSTOMER SEGMENT PROFITABILITY:")
    print(segment_summary)
    
    # Top and bottom customers
    print(f"\n🏆 TOP 10 MOST PROFITABLE CUSTOMERS:")
    top_customers = customer_profit.nlargest(10, 'Total_Profit')
    print(top_customers[['Total_Sales', 'Total_Profit', 'Avg_Profit_Margin', 'Order_Count']])
    
    print(f"\n📉 BOTTOM 10 CUSTOMERS (Losses):")
    loss_customers = customer_profit[customer_profit['Total_Profit'] < 0].nsmallest(10, 'Total_Profit')
    if len(loss_customers) > 0:
        print(loss_customers[['Total_Sales', 'Total_Profit', 'Avg_Profit_Margin', 'Order_Count']])
    else:
        print("   No customers with overall losses")
    
    return customer_profit, segment_summary

def analyze_regional_profitability(df):
    """Analyze profitability by region and identify optimization opportunities"""
    print("\n" + "="*60)
    print("🌍 REGIONAL PROFITABILITY ANALYSIS")
    print("="*60)
    
    # Regional profitability matrix
    regional_matrix = df.groupby(['Region', 'Category']).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Profit_Margin': 'mean',
        'Order ID': 'nunique'
    }).round(2)
    
    regional_matrix.columns = ['Sales', 'Profit', 'Avg_Margin', 'Orders']
    
    print(f"\n📊 REGIONAL-CATEGORY PERFORMANCE MATRIX:")
    print(regional_matrix)
    
    # Regional efficiency analysis
    regional_efficiency = df.groupby('Region').agg({
        'Sales': ['sum', 'mean'],
        'Profit': ['sum', 'mean'],
        'Profit_Margin': 'mean',
        'Order ID': 'nunique'
    }).round(2)
    
    regional_efficiency.columns = ['Total_Sales', 'Avg_Order_Sales', 'Total_Profit', 
                                 'Avg_Order_Profit', 'Avg_Profit_Margin', 'Total_Orders']
    
    regional_efficiency['Sales_Per_Order'] = regional_efficiency['Total_Sales'] / regional_efficiency['Total_Orders']
    regional_efficiency['Profit_Per_Order'] = regional_efficiency['Total_Profit'] / regional_efficiency['Total_Orders']
    
    print(f"\n🎯 REGIONAL EFFICIENCY METRICS:")
    print(regional_efficiency)
    
    # Identify underperforming regions
    avg_margin = df['Profit_Margin'].mean()
    underperforming = regional_efficiency[regional_efficiency['Avg_Profit_Margin'] < avg_margin]
    
    print(f"\n⚠️ UNDERPERFORMING REGIONS (Below {avg_margin:.1f}% avg margin):")
    if len(underperforming) > 0:
        print(underperforming[['Avg_Profit_Margin', 'Total_Sales', 'Total_Profit']])
    else:
        print("   All regions performing above average!")
    
    return regional_matrix, regional_efficiency

def analyze_product_profitability_matrix(df):
    """Create product profitability matrix for portfolio optimization"""
    print("\n" + "="*60)
    print("📦 PRODUCT PROFITABILITY MATRIX")
    print("="*60)
    
    # Product performance matrix
    product_matrix = df.groupby('Sub-Category').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Profit_Margin': 'mean',
        'Order ID': 'nunique'
    }).round(2)
    
    product_matrix.columns = ['Total_Sales', 'Total_Profit', 'Avg_Margin', 'Order_Count']
    
    # Categorize products into BCG-style matrix
    sales_median = product_matrix['Total_Sales'].median()
    margin_median = product_matrix['Avg_Margin'].median()
    
    def categorize_product(row):
        if row['Total_Sales'] > sales_median and row['Avg_Margin'] > margin_median:
            return 'Stars'  # High sales, high margin
        elif row['Total_Sales'] > sales_median and row['Avg_Margin'] <= margin_median:
            return 'Cash Cows'  # High sales, low margin
        elif row['Total_Sales'] <= sales_median and row['Avg_Margin'] > margin_median:
            return 'Question Marks'  # Low sales, high margin
        else:
            return 'Dogs'  # Low sales, low margin
    
    product_matrix['Category_Type'] = product_matrix.apply(categorize_product, axis=1)
    
    # Summary by category type
    category_summary = product_matrix.groupby('Category_Type').agg({
        'Total_Sales': ['sum', 'count'],
        'Total_Profit': 'sum',
        'Avg_Margin': 'mean'
    }).round(2)
    
    print(f"\n🎯 PRODUCT PORTFOLIO ANALYSIS:")
    print(f"Sales Median: ${sales_median:,.2f}")
    print(f"Margin Median: {margin_median:.1f}%")
    print(f"\n📊 Portfolio Categories:")
    
    for category in ['Stars', 'Cash Cows', 'Question Marks', 'Dogs']:
        products = product_matrix[product_matrix['Category_Type'] == category]
        if len(products) > 0:
            print(f"\n{category} ({len(products)} products):")
            print(products.sort_values('Total_Sales', ascending=False))
    
    return product_matrix

def generate_profitability_recommendations(df, profit_traps, customer_profit, regional_efficiency, product_matrix):
    """Generate actionable profitability recommendations"""
    print("\n" + "="*60)
    print("💡 PROFITABILITY OPTIMIZATION RECOMMENDATIONS")
    print("="*60)
    
    recommendations = []
    
    # 1. Product recommendations
    if len(profit_traps) > 0:
        trap_sales = profit_traps['Total_Sales'].sum()
        recommendations.append(f"🔧 PRODUCT OPTIMIZATION:")
        recommendations.append(f"   • Focus on {len(profit_traps)} profit trap categories (${trap_sales:,.0f} sales)")
        recommendations.append(f"   • Consider price increases or cost reductions for low-margin items")
    
    # 2. Customer recommendations
    loss_customers = len(customer_profit[customer_profit['Total_Profit'] < 0])
    if loss_customers > 0:
        recommendations.append(f"\n👥 CUSTOMER OPTIMIZATION:")
        recommendations.append(f"   • Review {loss_customers} loss-making customers")
        recommendations.append(f"   • Implement minimum order values or service fees")
    
    # 3. Regional recommendations
    best_region = regional_efficiency.loc[regional_efficiency['Avg_Profit_Margin'].idxmax()]
    worst_region = regional_efficiency.loc[regional_efficiency['Avg_Profit_Margin'].idxmin()]
    
    recommendations.append(f"\n🌍 REGIONAL OPTIMIZATION:")
    recommendations.append(f"   • Replicate {best_region.name} success model ({best_region['Avg_Profit_Margin']:.1f}% margin)")
    recommendations.append(f"   • Improve {worst_region.name} operations ({worst_region['Avg_Profit_Margin']:.1f}% margin)")
    
    # 4. Portfolio recommendations
    stars = product_matrix[product_matrix['Category_Type'] == 'Stars']
    dogs = product_matrix[product_matrix['Category_Type'] == 'Dogs']
    
    if len(stars) > 0:
        recommendations.append(f"\n⭐ PORTFOLIO OPTIMIZATION:")
        recommendations.append(f"   • Invest more in {len(stars)} 'Star' products")
    
    if len(dogs) > 0:
        recommendations.append(f"   • Consider discontinuing {len(dogs)} 'Dog' products")
    
    # 5. Overall profit improvement potential
    current_margin = df['Profit_Margin'].mean()
    target_margin = 35  # Industry benchmark
    
    if current_margin < target_margin:
        improvement_potential = (target_margin - current_margin) / 100 * df['Sales'].sum()
        recommendations.append(f"\n💰 PROFIT IMPROVEMENT POTENTIAL:")
        recommendations.append(f"   • Current margin: {current_margin:.1f}%")
        recommendations.append(f"   • Target margin: {target_margin}%")
        recommendations.append(f"   • Potential profit increase: ${improvement_potential:,.0f}")
    
    print("\n".join(recommendations))
    
    return recommendations

def save_profitability_analysis(profit_traps, customer_profit, regional_efficiency, product_matrix, recommendations):
    """Save profitability analysis results"""
    
    # Save to Excel
    with pd.ExcelWriter('profitability_analysis.xlsx', engine='openpyxl') as writer:
        if len(profit_traps) > 0:
            profit_traps.to_excel(writer, sheet_name='Profit_Traps')
        customer_profit.to_excel(writer, sheet_name='Customer_Profitability')
        regional_efficiency.to_excel(writer, sheet_name='Regional_Efficiency')
        product_matrix.to_excel(writer, sheet_name='Product_Matrix')
    
    # Save recommendations
    with open('profitability_recommendations.txt', 'w', encoding='utf-8') as f:
        f.write("E-COMMERCE PROFITABILITY OPTIMIZATION RECOMMENDATIONS\n")
        f.write("="*60 + "\n\n")
        f.write("\n".join(recommendations))
    
    print(f"\n💾 Analysis saved to:")
    print(f"   • profitability_analysis.xlsx")
    print(f"   • profitability_recommendations.txt")

def main():
    """Main profitability analysis execution"""
    print("🚀 E-COMMERCE SALES OPTIMIZATION - PROFITABILITY ANALYSIS")
    print("="*60)
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Run analyses
    profit_traps, profit_stars, subcategory_profit = analyze_high_sales_low_profit(df)
    customer_profit, segment_summary = analyze_customer_profitability(df)
    regional_matrix, regional_efficiency = analyze_regional_profitability(df)
    product_matrix = analyze_product_profitability_matrix(df)
    
    # Generate recommendations
    recommendations = generate_profitability_recommendations(
        df, profit_traps, customer_profit, regional_efficiency, product_matrix
    )
    
    # Save results
    save_profitability_analysis(profit_traps, customer_profit, regional_efficiency, product_matrix, recommendations)
    
    print(f"\n✅ STEP 5 COMPLETED SUCCESSFULLY!")
    print(f"💡 Profitability analysis complete - ready for Step 6: Time Trends & Visualizations")
    
    return df, profit_traps, customer_profit, product_matrix

if __name__ == "__main__":
    main()

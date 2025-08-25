import pandas as pd
import numpy as np
from datetime import datetime
import os

def load_data():
    """Load the cleaned dataset and analysis results"""
    try:
        df = pd.read_csv('data/superstore_sales_cleaned.csv')
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        print(f"Loaded dataset: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def generate_executive_summary(df):
    """Generate executive summary with key metrics"""
    print("\nGenerating executive summary...")
    
    # Key metrics
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    avg_margin = df['Profit_Margin'].mean()
    total_orders = df['Order ID'].nunique()
    unique_customers = df['Customer ID'].nunique()
    
    # Performance by category
    category_performance = df.groupby('Category').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Profit_Margin': 'mean'
    }).sort_values('Sales', ascending=False)
    
    # Top performers
    top_category = category_performance.index[0]
    top_region = df.groupby('Region')['Sales'].sum().idxmax()
    top_segment = df.groupby('Segment')['Sales'].sum().idxmax()
    
    summary = f"""
EXECUTIVE SUMMARY
================

OVERALL PERFORMANCE:
• Total Sales: ${total_sales:,.2f}
• Total Profit: ${total_profit:,.2f}
• Average Profit Margin: {avg_margin:.1f}%
• Total Orders: {total_orders:,}
• Unique Customers: {unique_customers:,}

TOP PERFORMERS:
• Best Category: {top_category} (${category_performance.loc[top_category, 'Sales']:,.2f})
• Best Region: {top_region}
• Best Segment: {top_segment}

KEY FINDINGS:
• {len(df[df['Profit'] < 0]):,} loss-making orders ({len(df[df['Profit'] < 0])/len(df)*100:.1f}%)
• Profit margin varies significantly across categories ({category_performance['Profit_Margin'].min():.1f}% - {category_performance['Profit_Margin'].max():.1f}%)
• Regional performance gaps present optimization opportunities
"""
    
    return summary

def identify_profit_optimization_opportunities(df):
    """Identify specific profit optimization opportunities"""
    print("Identifying profit optimization opportunities...")
    
    opportunities = []
    
    # 1. Product-level opportunities
    subcategory_analysis = df.groupby('Sub-Category').agg({
        'Sales': ['sum', 'count'],
        'Profit': 'sum',
        'Profit_Margin': 'mean'
    }).round(2)
    
    subcategory_analysis.columns = ['Total_Sales', 'Order_Count', 'Total_Profit', 'Avg_Profit_Margin']
    
    # High sales, low margin products (profit traps)
    profit_traps = subcategory_analysis[
        (subcategory_analysis['Total_Sales'] > subcategory_analysis['Total_Sales'].median()) &
        (subcategory_analysis['Avg_Profit_Margin'] < 20)
    ]
    
    if len(profit_traps) > 0:
        opportunities.append({
            'category': 'Product Optimization',
            'opportunity': f'Profit Trap Products',
            'description': f'{len(profit_traps)} sub-categories with high sales but low margins (<20%)',
            'impact': f'${profit_traps["Total_Sales"].sum():,.0f} in sales at risk',
            'action': 'Review pricing strategy, negotiate better supplier terms, or consider product mix changes'
        })
    
    # 2. Customer-level opportunities
    customer_analysis = df.groupby('Customer ID').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique'
    })
    
    loss_customers = customer_analysis[customer_analysis['Profit'] < 0]
    
    if len(loss_customers) > 0:
        opportunities.append({
            'category': 'Customer Optimization',
            'opportunity': 'Loss-Making Customers',
            'description': f'{len(loss_customers)} customers generating losses',
            'impact': f'${abs(loss_customers["Profit"].sum()):,.0f} in losses',
            'action': 'Implement minimum order values, service fees, or customer tier pricing'
        })
    
    # 3. Regional opportunities
    regional_analysis = df.groupby('Region').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Profit_Margin': 'mean'
    })
    
    best_region = regional_analysis.loc[regional_analysis['Profit_Margin'].idxmax()]
    worst_region = regional_analysis.loc[regional_analysis['Profit_Margin'].idxmin()]
    
    margin_gap = best_region['Profit_Margin'] - worst_region['Profit_Margin']
    
    if margin_gap > 5:  # Significant gap
        opportunities.append({
            'category': 'Regional Optimization',
            'opportunity': 'Regional Performance Gap',
            'description': f'{margin_gap:.1f}% margin difference between best and worst regions',
            'impact': f'Potential to improve {worst_region.name} region performance',
            'action': f'Replicate {best_region.name} best practices in {worst_region.name}'
        })
    
    return opportunities

def create_strategic_recommendations(df, opportunities):
    """Create strategic recommendations with timelines"""
    print("Creating strategic recommendations...")
    
    recommendations = {
        'immediate': [],  # 0-3 months
        'short_term': [], # 3-6 months
        'long_term': []   # 6-12 months
    }
    
    # Immediate actions (0-3 months)
    recommendations['immediate'].extend([
        {
            'action': 'Pricing Review',
            'description': 'Review and adjust pricing for low-margin, high-volume products',
            'expected_impact': '2-5% margin improvement',
            'resources': 'Pricing team, 2 weeks'
        },
        {
            'action': 'Minimum Order Implementation',
            'description': 'Implement minimum order values for loss-making customer segments',
            'expected_impact': 'Eliminate customer losses',
            'resources': 'Operations team, 1 month'
        },
        {
            'action': 'Cost Reduction Initiative',
            'description': 'Negotiate better terms with suppliers for profit trap categories',
            'expected_impact': '1-3% margin improvement',
            'resources': 'Procurement team, 6 weeks'
        }
    ])
    
    # Short-term initiatives (3-6 months)
    recommendations['short_term'].extend([
        {
            'action': 'Regional Best Practice Rollout',
            'description': 'Implement successful regional strategies across underperforming regions',
            'expected_impact': '3-7% regional margin improvement',
            'resources': 'Regional managers, 4 months'
        },
        {
            'action': 'Customer Segmentation Enhancement',
            'description': 'Develop tiered pricing and service models based on customer profitability',
            'expected_impact': '5-10% customer profit improvement',
            'resources': 'Marketing & Sales teams, 3 months'
        },
        {
            'action': 'Product Portfolio Optimization',
            'description': 'Phase out or reposition low-performing products',
            'expected_impact': '2-4% overall margin improvement',
            'resources': 'Product management, 5 months'
        }
    ])
    
    # Long-term strategy (6-12 months)
    recommendations['long_term'].extend([
        {
            'action': 'Category Expansion',
            'description': 'Expand high-margin categories and reduce dependency on low-margin ones',
            'expected_impact': '5-15% profit growth',
            'resources': 'Strategic planning, 8 months'
        },
        {
            'action': 'Private Label Development',
            'description': 'Develop private label products in high-volume, low-margin categories',
            'expected_impact': '10-20% margin improvement in target categories',
            'resources': 'Product development, 12 months'
        },
        {
            'action': 'Advanced Analytics Implementation',
            'description': 'Implement dynamic pricing and demand forecasting systems',
            'expected_impact': '3-8% revenue optimization',
            'resources': 'IT & Analytics teams, 10 months'
        }
    ])
    
    return recommendations

def calculate_financial_impact(df, recommendations):
    """Calculate potential financial impact of recommendations"""
    print("Calculating financial impact scenarios...")
    
    current_sales = df['Sales'].sum()
    current_profit = df['Profit'].sum()
    current_margin = (current_profit / current_sales) * 100
    
    scenarios = {
        'conservative': {
            'margin_improvement': 2.0,  # 2% points
            'sales_impact': 0.0,        # No sales impact
            'description': 'Conservative implementation with minimal risk'
        },
        'moderate': {
            'margin_improvement': 4.5,  # 4.5% points
            'sales_impact': 2.0,        # 2% sales growth
            'description': 'Moderate implementation with balanced risk/reward'
        },
        'aggressive': {
            'margin_improvement': 7.0,  # 7% points
            'sales_impact': 5.0,        # 5% sales growth
            'description': 'Aggressive implementation with higher risk but maximum reward'
        }
    }
    
    impact_analysis = {}
    
    for scenario_name, scenario in scenarios.items():
        new_margin = current_margin + scenario['margin_improvement']
        new_sales = current_sales * (1 + scenario['sales_impact'] / 100)
        new_profit = new_sales * (new_margin / 100)
        
        profit_increase = new_profit - current_profit
        roi_percentage = (profit_increase / current_profit) * 100
        
        impact_analysis[scenario_name] = {
            'new_margin': new_margin,
            'new_sales': new_sales,
            'new_profit': new_profit,
            'profit_increase': profit_increase,
            'roi_percentage': roi_percentage,
            'description': scenario['description']
        }
    
    return impact_analysis

def create_implementation_roadmap():
    """Create detailed implementation roadmap"""
    print("Creating implementation roadmap...")
    
    roadmap = {
        'Month 1': [
            'Conduct comprehensive pricing review',
            'Identify loss-making customers and products',
            'Begin supplier negotiations for key categories'
        ],
        'Month 2': [
            'Implement minimum order values',
            'Launch cost reduction initiatives',
            'Start regional performance analysis'
        ],
        'Month 3': [
            'Complete immediate pricing adjustments',
            'Finalize supplier contract renegotiations',
            'Develop customer segmentation strategy'
        ],
        'Month 4-6': [
            'Roll out regional best practices',
            'Implement tiered customer pricing',
            'Begin product portfolio optimization',
            'Launch customer profitability programs'
        ],
        'Month 7-9': [
            'Execute product line rationalization',
            'Develop private label strategy',
            'Implement advanced customer analytics',
            'Monitor and adjust pricing strategies'
        ],
        'Month 10-12': [
            'Launch private label products',
            'Implement dynamic pricing systems',
            'Complete category expansion initiatives',
            'Conduct comprehensive performance review'
        ]
    }
    
    return roadmap

def save_comprehensive_report(df, executive_summary, opportunities, recommendations, financial_impact, roadmap):
    """Save comprehensive business recommendations report"""
    print("Saving comprehensive business recommendations report...")
    
    report_content = f"""
BUSINESS RECOMMENDATIONS REPORT
==============================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{executive_summary}

PROFIT OPTIMIZATION OPPORTUNITIES
=================================

"""
    
    for i, opp in enumerate(opportunities, 1):
        report_content += f"""
{i}. {opp['opportunity'].upper()}
Category: {opp['category']}
Description: {opp['description']}
Impact: {opp['impact']}
Recommended Action: {opp['action']}
"""
    
    report_content += f"""

STRATEGIC RECOMMENDATIONS
========================

IMMEDIATE ACTIONS (0-3 months):
"""
    
    for i, rec in enumerate(recommendations['immediate'], 1):
        report_content += f"""
{i}. {rec['action']}
   Description: {rec['description']}
   Expected Impact: {rec['expected_impact']}
   Resources Required: {rec['resources']}
"""
    
    report_content += f"""

SHORT-TERM INITIATIVES (3-6 months):
"""
    
    for i, rec in enumerate(recommendations['short_term'], 1):
        report_content += f"""
{i}. {rec['action']}
   Description: {rec['description']}
   Expected Impact: {rec['expected_impact']}
   Resources Required: {rec['resources']}
"""
    
    report_content += f"""

LONG-TERM STRATEGY (6-12 months):
"""
    
    for i, rec in enumerate(recommendations['long_term'], 1):
        report_content += f"""
{i}. {rec['action']}
   Description: {rec['description']}
   Expected Impact: {rec['expected_impact']}
   Resources Required: {rec['resources']}
"""
    
    report_content += f"""

FINANCIAL IMPACT ANALYSIS
=========================

"""
    
    for scenario_name, impact in financial_impact.items():
        report_content += f"""
{scenario_name.upper()} SCENARIO:
{impact['description']}
• New Profit Margin: {impact['new_margin']:.1f}%
• Projected Sales: ${impact['new_sales']:,.2f}
• Projected Profit: ${impact['new_profit']:,.2f}
• Profit Increase: ${impact['profit_increase']:,.2f}
• ROI: {impact['roi_percentage']:.1f}%

"""
    
    report_content += f"""
IMPLEMENTATION ROADMAP
=====================

"""
    
    for month, tasks in roadmap.items():
        report_content += f"""
{month}:
"""
        for task in tasks:
            report_content += f"• {task}\n"
        report_content += "\n"
    
    report_content += f"""

SUCCESS METRICS & KPIs
=====================

Key Performance Indicators to track:
• Overall profit margin improvement
• Revenue per customer increase
• Regional performance convergence
• Product portfolio optimization success
• Customer profitability enhancement
• Loss-making order reduction

Monitoring Schedule:
• Weekly: Pricing and margin tracking
• Monthly: Customer and regional performance
• Quarterly: Strategic initiative progress
• Annually: Comprehensive business review

CONCLUSION
==========

This comprehensive analysis identifies significant opportunities for profit optimization
across product pricing, customer management, and regional operations. The recommended
strategies provide a clear path to improve profitability while maintaining sales growth.

Conservative estimates suggest ${financial_impact['conservative']['profit_increase']:,.0f} in additional profit,
while aggressive implementation could yield ${financial_impact['aggressive']['profit_increase']:,.0f} or more.

Success depends on systematic execution of the implementation roadmap and continuous
monitoring of key performance indicators.
"""
    
    # Save to file
    with open('business_recommendations_report.txt', 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print("Business recommendations report saved to: business_recommendations_report.txt")

def main():
    """Main business recommendations execution"""
    print("E-COMMERCE SALES OPTIMIZATION - BUSINESS RECOMMENDATIONS")
    print("="*60)
    
    # Load data
    df = load_data()
    if df is None:
        print("Failed to load data. Please run previous analysis steps first.")
        return
    
    # Generate comprehensive business recommendations
    executive_summary = generate_executive_summary(df)
    opportunities = identify_profit_optimization_opportunities(df)
    recommendations = create_strategic_recommendations(df, opportunities)
    financial_impact = calculate_financial_impact(df, recommendations)
    roadmap = create_implementation_roadmap()
    
    # Save comprehensive report
    save_comprehensive_report(df, executive_summary, opportunities, recommendations, financial_impact, roadmap)
    
    print(f"\nSTEP 7 COMPLETED SUCCESSFULLY!")
    print(f"Business recommendations complete. Ready for final deliverables.")
    
    return df, opportunities, recommendations, financial_impact

if __name__ == "__main__":
    main()

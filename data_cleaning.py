#!/usr/bin/env python3
"""
Step 3: Data Cleaning and Synthetic Profit Generation
E-commerce Sales Optimization Analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def create_synthetic_profit_data(df):
    """Makes fake profit data"""
    print("Creating synthetic profit data...")
    
    # Industry-realistic profit margins by category (as percentages)  # TODO: fix this later
    category_margins={
        'Technology': {
            'base_margin': 15,  # Technology typically has lower margins
            'subcategory_adjustments': {
                'Phones': 12,
                'Accessories': 25,
                'Machines': 10,
                'Copiers': 8
            }
        },
        'Furniture': {
            'base_margin': 22,  # Furniture has moderate margins
            'subcategory_adjustments': {
                'Chairs': 20,
                'Tables': 18,
                'Bookcases': 25,
                'Furnishings': 30
            }
        },
        'Office Supplies': {
            'base_margin': 35,  # Office supplies have higher margins
            'subcategory_adjustments': {
                'Paper': 40,
                'Binders': 45,
                'Art': 50,
                'Storage': 30,
                'Appliances': 25,
                'Labels': 55,
                'Envelopes': 45,
                'Fasteners': 50
            }
        }
    }
    
    # Customer segment adjustments (Corporate gets discounts, affecting margins)
    segment_adjustments = {
        'Consumer': 1.0,      # Base margin
        'Corporate': 0.85,    # 15% lower margins due to volume discounts
        'Home Office': 1.05   # 5% higher margins
    }
    
    # Regional cost adjustments (some regions have higher operational costs)
    regional_adjustments = {
        'West': 0.95,    # Higher costs, lower margins
        'East': 1.0,     # Base
        'Central': 1.05, # Lower costs, higher margins  
        'South': 1.02    # Slightly lower costs
    }
    
    profits = []
    
    for idx, row in df.iterrows():
        sales = row['Sales']
        category = row['Category']
        subcategory = row['Sub-Category']
        segment = row['Segment']
        region = row['Region']
        
        # Get base margin for category  # Note to self: remember to update this
        if category in category_margins:
            base_margin = category_margins[category]['base_margin']
            
            # Adjust for subcategory if available
            subcategory_adjustments = category_margins[category]['subcategory_adjustments']
            if subcategory in subcategory_adjustments:
                margin_percent = subcategory_adjustments[subcategory]
            else:
                margin_percent = base_margin
        else:
            margin_percent = 20  # Default margin
        
        # Apply segment adjustment
        segment_adj=segment_adjustments.get(segment, 1.0)
        margin_percent *= segment_adj
        
        # Apply regional adjustment
        regional_adj = regional_adjustments.get(region, 1.0)
        margin_percent *= regional_adj
        
        # Add some realistic variation (±3% random variation)
        variation = np.random.normal(0, 3)
        final_margin = margin_percent + variation
        
        # Ensure margin is within realistic bounds (5% to 60%)
        final_margin = max(5, min(60, final_margin))
        
        # Create profit based on sales and calculated margin - hack for now
        profit = sales * (final_margin / 100)
        
        # Add some products with losses (realistic business scenario)
        if np.random.random() < 0.05:  # 5% chance of loss
            profit = sales * np.random.uniform(-0.1, 0.02)  # Loss between -10% and +2%
        
        profits.append(profit)
    
    return profits

def clean_and_prepare_data():
    """
    Main data cleaning and preparation function
    """
    print("="*60)
    print("STEP 3: DATA CLEANING AND PREPARATION")
    print("="*60)
    
    # Load the dataset
    try:
        df = pd.read_csv('data/superstore_sales.csv', encoding='latin-1')
        print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    except FileNotFoundError:
        print("Dataset not found in data/ folder")
        return None
    
    # Create a copy for cleaning
    df_clean = df.copy()
    
    print(f"\nINITIAL DATA ANALYSIS:")
    print(f"Shape: {df_clean.shape}")
    print(f"Missing values: {df_clean.isnull().sum().sum()}")
    
    # 1. Convert date columns
    print(f"\nConverting date columns...")
    date_columns = ['Order Date', 'Ship Date']
    for col in date_columns:
        if col in df_clean.columns:
            df_clean[col] = pd.to_datetime(df_clean[col], format='%d/%m/%Y')
            print(f"   Converted {col}")
    
    # 2. Clean text columns
    print(f"\nCleaning text columns...")
    text_columns = ['Customer Name', 'Product Name', 'City', 'State']
    for col in text_columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].str.strip()
    
    # 3. Handle missing values
    print(f"\nHandling missing values...")
    missing_before = df_clean.isnull().sum().sum()
    
    # Fill missing postal codes with 0
    if 'Postal Code' in df_clean.columns:
        df_clean['Postal Code'] = df_clean['Postal Code'].fillna(0)
    
    missing_after = df_clean.isnull().sum().sum()
    print(f"   Missing values: {missing_before} → {missing_after}")
    
    # 4. Create synthetic profit data
    print(f"\nGenerating synthetic profit data...")
    np.random.seed(42)  # For reproducible results
    profits = create_synthetic_profit_data(df_clean)
    df_clean['Profit'] = profits
    
    # 5. Create calculated fields
    print(f"\nCreating calculated fields...")
    
    # Profit Margin
    df_clean['Profit_Margin'] = (df_clean['Profit'] / df_clean['Sales']) * 100
    
    # Date-based features
    df_clean['Year'] = df_clean['Order Date'].dt.year
    df_clean['Month'] = df_clean['Order Date'].dt.month
    df_clean['Quarter'] = df_clean['Order Date'].dt.quarter
    df_clean['Day_of_Week'] = df_clean['Order Date'].dt.day_name()
    df_clean['Month_Name'] = df_clean['Order Date'].dt.month_name()
    
    # Sales performance categories
    df_clean['Sales_Category'] = pd.cut(df_clean['Sales'], 
                                       bins=[0, 100, 500, 1000, float('inf')],
                                       labels=['Low', 'Medium', 'High', 'Very High'])
    
    # Profit performance categories
    df_clean['Profit_Category'] = pd.cut(df_clean['Profit'], 
                                        bins=[-float('inf'), 0, 50, 200, float('inf')],
                                        labels=['Loss', 'Low Profit', 'Medium Profit', 'High Profit'])
    
    print(f"   Created profit margins, date features, and performance categories")
    
    # 6. Data quality summary
    print(f"\nCLEANED DATA SUMMARY:")
    print(f"Final shape: {df_clean.shape}")
    print(f"Date range: {df_clean['Order Date'].min()} to {df_clean['Order Date'].max()}")
    print(f"Sales range: ${df_clean['Sales'].min():.2f} to ${df_clean['Sales'].max():.2f}")
    print(f"Profit range: ${df_clean['Profit'].min():.2f} to ${df_clean['Profit'].max():.2f}")
    print(f"Average profit margin: {df_clean['Profit_Margin'].mean():.1f}%")
    
    # Category breakdown
    print(f"\nCATEGORY BREAKDOWN:")
    category_summary = df_clean.groupby('Category').agg({
        'Sales': ['count', 'sum', 'mean'],
        'Profit': ['sum', 'mean'],
        'Profit_Margin': 'mean'
    }).round(2)
    print(category_summary)
    
    # 7. Save cleaned dataset
    output_file = 'data/superstore_sales_cleaned.csv'
    df_clean.to_csv(output_file, index=False)
    print(f"\nCleaned dataset saved to: {output_file}")
    
    # 8. Save data dictionary
    save_data_dictionary(df_clean)
    
    return df_clean

def save_data_dictionary(df):
    """Save data dictionary explaining all columns"""
    
    data_dict = {
        'Row ID': 'Unique identifier for each row',
        'Order ID': 'Unique identifier for each order',
        'Order Date': 'Date when the order was placed',
        'Ship Date': 'Date when the order was shipped',
        'Ship Mode': 'Shipping method used',
        'Customer ID': 'Unique identifier for each customer',
        'Customer Name': 'Name of the customer',
        'Segment': 'Customer segment (Consumer, Corporate, Home Office)',
        'Country': 'Country where order was placed',
        'City': 'City where order was placed',
        'State': 'State where order was placed',
        'Postal Code': 'Postal code of delivery location',
        'Region': 'Geographic region (West, East, Central, South)',
        'Product ID': 'Unique identifier for each product',
        'Category': 'Product category (Furniture, Office Supplies, Technology)',
        'Sub-Category': 'Product sub-category',
        'Product Name': 'Name of the product',
        'Sales': 'Revenue generated from the sale',
        'Profit': 'Profit generated (synthetic data based on industry margins)',
        'Profit_Margin': 'Profit as percentage of sales',
        'Year': 'Year extracted from Order Date',
        'Month': 'Month extracted from Order Date',
        'Quarter': 'Quarter extracted from Order Date',
        'Day_of_Week': 'Day of week when order was placed',
        'Month_Name': 'Month name when order was placed',
        'Sales_Category': 'Sales amount category (Low, Medium, High, Very High)',
        'Profit_Category': 'Profit amount category (Loss, Low, Medium, High)'
    }
    
    with open('data_dictionary.txt', 'w') as f:
        f.write("E-COMMERCE SALES DATA DICTIONARY\n")
        f.write("="*50 + "\n\n")
        for col, desc in data_dict.items():
            f.write(f"{col}: {desc}\n")
    
    print(f"Data dictionary saved to: data_dictionary.txt")

if __name__ == "__main__":
    df_cleaned = clean_and_prepare_data()
    
    if df_cleaned is not None:
        print(f"\nSTEP 3 COMPLETED SUCCESSFULLY!")
        print(f"Ready for Step 4: Exploratory Data Analysis")
        print(f"Synthetic profit data created using realistic industry margins")
    else:
        print(f"\nSTEP 3 FAILED!")
        print(f"Please check the dataset location")

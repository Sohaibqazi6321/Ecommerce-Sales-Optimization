#!/usr/bin/env python3
"""
Step 2: Data Loading and Exploration
E-commerce Sales Optimization Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_and_explore_data():
    """
    Load the Superstore dataset and perform initial exploration
    """
    print("="*60)
    print("STEP 2: DATA LOADING AND EXPLORATION")
    print("="*60)
    
    # Load the dataset
    try:
        # Try different possible filenames
        possible_files = [
            'data/superstore_sales.csv',
            'data/Sample - Superstore.csv', 
            'data/superstore.csv',
            'data/train.csv'
        ]
        
        df = None
        for file_path in possible_files:
            try:
                df = pd.read_csv(file_path, encoding='latin-1')
                print(f"Dataset loaded from: {file_path}")
                break
            except FileNotFoundError:
                continue
        
        if df is None:
            print("Dataset not found. Please check the data/ folder.")
            print("Expected files: superstore_sales.csv, Sample - Superstore.csv, or train.csv")
            return None
            
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None
    
    # Basic dataset information
    print(f"\nDATASET OVERVIEW")
    print(f"Shape: {df.shape}")
    print(f"Columns: {len(df.columns)}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Display column names
    print(f"\nCOLUMN NAMES:")
    for i, col in enumerate(df.columns, 1):
        print(f"{i:2d}. {col}")
    
    # Data types
    print(f"\nDATA TYPES:")
    print(df.dtypes)
    
    # First few rows
    print(f"\nFIRST 5 ROWS:")
    print(df.head())
    
    # Missing values analysis
    print(f"\nMISSING VALUES ANALYSIS:")
    missing_data = df.isnull().sum()
    missing_percent = (missing_data / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'Column': df.columns,
        'Missing_Count': missing_data.values,
        'Missing_Percent': missing_percent.values
    })
    
    # Only show columns with missing values
    missing_summary = missing_df[missing_df['Missing_Count'] > 0]
    if len(missing_summary) > 0:
        print(missing_summary.to_string(index=False))
    else:
        print("No missing values found!")
    
    # Basic statistics for numeric columns
    print(f"\nNUMERIC COLUMNS SUMMARY:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print(df[numeric_cols].describe())
    
    # Categorical columns summary
    print(f"\nCATEGORICAL COLUMNS SUMMARY:")
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        unique_count = df[col].nunique()
        print(f"{col}: {unique_count} unique values")
        if unique_count <= 10:
            print(f"  Values: {list(df[col].unique())}")
        else:
            print(f"  Sample values: {list(df[col].unique()[:5])}...")
    
    # Identify key columns for analysis
    print(f"\nKEY COLUMNS IDENTIFIED:")
    
    # Find sales/revenue column
    sales_cols = [col for col in df.columns if any(word in col.lower() for word in ['sales', 'revenue'])]
    print(f"Sales columns: {sales_cols}")
    
    # Find profit column
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    print(f"Profit columns: {profit_cols}")
    
    # Find date columns
    date_cols = [col for col in df.columns if any(word in col.lower() for word in ['date', 'time'])]
    print(f"Date columns: {date_cols}")
    
    # Find category columns
    category_cols = [col for col in df.columns if 'category' in col.lower()]
    print(f"Category columns: {category_cols}")
    
    # Find region/location columns
    location_cols = [col for col in df.columns if any(word in col.lower() for word in ['region', 'state', 'city', 'country'])]
    print(f"Location columns: {location_cols}")
    
    # Find customer/segment columns
    customer_cols = [col for col in df.columns if any(word in col.lower() for word in ['customer', 'segment'])]
    print(f"Customer columns: {customer_cols}")
    
    return df

def analyze_data_quality(df):
    """
    Analyze data quality issues
    """
    print(f"\nDATA QUALITY ANALYSIS:")
    
    # Check for duplicates
    duplicate_count = df.duplicated().sum()
    print(f"Duplicate rows: {duplicate_count}")
    
    # Check for negative values in sales/profit columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        negative_count = (df[col] < 0).sum()
        if negative_count > 0:
            print(f"Negative values in {col}: {negative_count}")
    
    # Check date ranges
    date_cols = df.select_dtypes(include=['datetime64']).columns
    for col in date_cols:
        try:
            date_series = pd.to_datetime(df[col], errors='coerce')
            print(f"{col} range: {date_series.min()} to {date_series.max()}")
        except:
            pass

def save_exploration_summary(df):
    """
    Save exploration summary to file
    """
    summary = {
        'dataset_shape': df.shape,
        'columns': list(df.columns),
        'data_types': df.dtypes.to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'numeric_summary': df.describe().to_dict() if len(df.select_dtypes(include=[np.number]).columns) > 0 else {}
    }
    
    # Save as text file
    with open('data_exploration_summary.txt', 'w') as f:
        f.write("E-COMMERCE SALES DATA EXPLORATION SUMMARY\n")
        f.write("="*50 + "\n\n")
        f.write(f"Dataset Shape: {summary['dataset_shape']}\n\n")
        f.write("Columns:\n")
        for i, col in enumerate(summary['columns'], 1):
            f.write(f"{i:2d}. {col}\n")
        f.write(f"\nData Types:\n")
        for col, dtype in summary['data_types'].items():
            f.write(f"{col}: {dtype}\n")
    
    print(f"\nExploration summary saved to: data_exploration_summary.txt")

if __name__ == "__main__":
    # Run the exploration
    df = load_and_explore_data()
    
    if df is not None:
        analyze_data_quality(df)
        save_exploration_summary(df)
        
        print(f"\nSTEP 2 COMPLETED!")
        print(f"Dataset loaded with {df.shape[0]} rows and {df.shape[1]} columns")
        print(f"Ready for Step 3: Data Cleaning")
    else:
        print(f"\nPlease download the dataset first!")
        print(f"See data_download_instructions.md for details")

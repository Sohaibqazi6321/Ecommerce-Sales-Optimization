#!/usr/bin/env python3
"""
Main script to run the E-commerce Sales Optimization Analysis
Execute each step of the analysis pipeline
"""

import sys
import os
from data_exploration import load_and_explore_data, analyze_data_quality, save_exploration_summary

def main():
    """Main execution function"""
    print("E-COMMERCE SALES OPTIMIZATION PROJECT")
    print("="*60)
    
    # Step 2: Data Loading and Exploration
    print("\nExecuting Step 2: Data Loading and Exploration...")
    
    df = load_and_explore_data()
    
    if df is not None:
        analyze_data_quality(df)
        save_exploration_summary(df)
        
        print(f"\nDataset exploration completed successfully!")
        print(f"Dataset: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"Summary saved to: data_exploration_summary.txt")
        
        return df
    else:
        print(f"\nDataset exploration failed!")
        print(f"Please ensure the dataset is downloaded to the data/ folder")
        return None

if __name__ == "__main__":
    df = main()
    
    if df is not None:
        print(f"\nNEXT STEPS:")
        print(f"1. Review the exploration summary")
        print(f"2. Push code to repository")
        print(f"3. Ready for Step 3: Data Cleaning")
    else:
        print(f"\nTO DO:")
        print(f"1. Download dataset from Kaggle")
        print(f"2. Place CSV file in data/ folder")
        print(f"3. Re-run this script")

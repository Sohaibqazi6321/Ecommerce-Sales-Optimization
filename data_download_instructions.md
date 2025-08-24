# Dataset Download Instructions

## Kaggle Dataset: Sample Superstore Sales Dataset
**URL**: https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting

## Download Steps:
1. Go to the Kaggle URL above
2. Click "Download" button (requires Kaggle account)
3. Extract the CSV file to the `data/` folder in this project
4. Rename the file to `superstore_sales.csv` if needed

## Expected File Structure:
```
Ecommerce-Sales-Optimization/
├── data/
│   └── superstore_sales.csv
├── notebooks/
│   └── ecommerce_analysis.ipynb
├── visualizations/
├── requirements.txt
└── README.md
```

## Alternative: Use Kaggle API
If you have Kaggle API set up:
```bash
kaggle datasets download -d rohitsahoo/sales-forecasting
```

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
df = pd.read_excel('argentina_flcannabis_investments.xlsx')

print("Columns in the DataFrame:")
print(df.columns)

print("\nFirst few rows of the DataFrame:")
print(df.head())

# Clean the data
df = df.dropna(how='all')  # Remove any completely empty rows
df['Current Price'] = pd.to_numeric(df['Current Price'], errors='coerce')
df['Allocation'] = pd.to_numeric(df['Allocation'], errors='coerce')

# Calculate total value for each stock
df['Total Value'] = df['Current Price'] * df['Allocation']

# Plotting
plt.figure(figsize=(12, 6))
plt.bar(df['Name'], df['Total Value'])
plt.title('Investment Value by Stock')
plt.xlabel('Stock Name')
plt.ylabel('Total Value')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Print summary statistics
print("\nSummary Statistics:")
print(df[['Name', 'Current Price', 'Allocation', 'Total Value']].describe())

# Identify best and worst performing stocks based on current price
best_stock = df.loc[df['Current Price'].idxmax()]
worst_stock = df.loc[df['Current Price'].idxmin()]

print(f"\nBest performing stock: {best_stock['Name']} (${best_stock['Current Price']:.2f})")
print(f"Worst performing stock: {worst_stock['Name']} (${worst_stock['Current Price']:.2f})")

# Calculate and print total portfolio value
total_portfolio_value = df['Total Value'].sum()
print(f"\nTotal Portfolio Value: ${total_portfolio_value:.2f}")
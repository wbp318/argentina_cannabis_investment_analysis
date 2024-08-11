import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

# Load the data
df = pd.read_excel('argentina_flcannabis_investments.xlsx')

# Convert date to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Calculate total value for each stock
df['Total Value'] = df['Price'] * df['Shares']

# Group by date and sum the total value
portfolio_value = df.groupby('Date')['Total Value'].sum().reset_index()

# Perform simple future projection (linear trend)
last_date = portfolio_value['Date'].max()
future_dates = pd.date_range(start=last_date, periods=30)  # Project 30 days into future
X = np.arange(len(portfolio_value)).reshape(-1, 1)
y = portfolio_value['Total Value'].values

from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X, y)

future_X = np.arange(len(portfolio_value), len(portfolio_value) + 30).reshape(-1, 1)
future_y = model.predict(future_X)

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(portfolio_value['Date'], portfolio_value['Total Value'], label='Actual')
plt.plot(future_dates, future_y, label='Projected', linestyle='--')
plt.title('Portfolio Value Over Time with Future Projection')
plt.xlabel('Date')
plt.ylabel('Total Value')
plt.legend()
plt.grid(True)
plt.show()

# Calculate potential returns
current_value = portfolio_value['Total Value'].iloc[-1]
projected_value = future_y[-1]
potential_return = (projected_value - current_value) / current_value * 100

print(f"Potential 30-day return: {potential_return:.2f}%")

# Identify best and worst performing stocks
stock_performance = df.groupby('Ticker').apply(lambda x: (x['Price'].iloc[-1] - x['Price'].iloc[0]) / x['Price'].iloc[0] * 100)
print("\nBest performing stock:", stock_performance.idxmax())
print("Worst performing stock:", stock_performance.idxmin())
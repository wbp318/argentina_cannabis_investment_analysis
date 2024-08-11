library(readxl)
library(dplyr)
library(ggplot2)
library(forecast)

# Load the data
df <- read_excel("investment_spreadsheet.xlsx")

# Convert date to proper date format
df$Date <- as.Date(df$Date)

# Calculate total value for each stock
df$TotalValue <- df$Price * df$Shares

# Group by date and sum the total value
portfolio_value <- df %>%
  group_by(Date) %>%
  summarise(TotalValue = sum(TotalValue))

# Perform future projection using ARIMA
ts_data <- ts(portfolio_value$TotalValue, frequency = 365)
fit <- auto.arima(ts_data)
future_forecast <- forecast(fit, h = 30)  # Forecast 30 days into future

# Plotting
ggplot() +
  geom_line(data = portfolio_value, aes(x = Date, y = TotalValue), color = "blue") +
  geom_line(aes(x = seq(max(portfolio_value$Date), by = "day", length.out = 30),
                y = future_forecast$mean), color = "red", linetype = "dashed") +
  geom_ribbon(aes(x = seq(max(portfolio_value$Date), by = "day", length.out = 30),
                  ymin = future_forecast$lower[,2],
                  ymax = future_forecast$upper[,2]),
              fill = "pink", alpha = 0.3) +
  labs(title = "Portfolio Value Over Time with Future Projection",
       x = "Date", y = "Total Value") +
  theme_minimal()

# Calculate potential returns
current_value <- tail(portfolio_value$TotalValue, 1)
projected_value <- tail(future_forecast$mean, 1)
potential_return <- (projected_value - current_value) / current_value * 100

cat("Potential 30-day return:", round(potential_return, 2), "%\n")

# Identify best and worst performing stocks
stock_performance <- df %>%
  group_by(Ticker) %>%
  summarise(Return = (last(Price) - first(Price)) / first(Price) * 100)

cat("Best performing stock:", stock_performance$Ticker[which.max(stock_performance$Return)], "\n")
cat("Worst performing stock:", stock_performance$Ticker[which.min(stock_performance$Return)], "\n")
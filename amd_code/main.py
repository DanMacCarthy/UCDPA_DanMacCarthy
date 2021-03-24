# Python Tool for calculating the value of a stock using fundamental financial analysis

# import pandas package
import pandas as pd

# YahooQuery API is used to extract the information from Yahoo Finance website

# Create an empty DataFrame to hold our metrics of stock value
# Use year-end dates as index for the DataFrame
index = ['2017-12-31', '2018-12-31', '2019-12-31']
amd = pd.DataFrame(index = index)
print (amd)

# Import Ticker Module of yahooQuery
from yahooquery import Ticker

symbol = 'amd'
# Assign the target stock ticker to a new variable called tick
tick = Ticker(symbol)

# Use yahooquery to retrieve the Financial Statements for the target stock from yahoofinance.com
income_statement = tick.income_statement(frequency='a').set_index('asOfDate')
cash_flow_statement = tick.cash_flow(frequency='a').set_index('asOfDate')
balance_sheet = tick.balance_sheet(frequency='a').set_index('asOfDate')


# Moat Analysis
# For Moat analysis we are looking for measures of competitive advantage
# Companies that have been able to sustain compound annual growth rates of 10% per year across 4 measures,
# are considered to have a durable moat.
# The 4 Growth Measures are: # Earnings growth, Cash Flow growth, Sales growth and growth in Book Value

# Moat Analysis - First of our growth rate measures is Earnings per Share

# Extract Earnings per share (EPS) history from 2017 to 2020
eps = income_statement[['DilutedEPS']].dropna()
amd['DilutedEPS'] = eps['DilutedEPS'].values
print (amd)
# YahooFinance is missing EPS for 2020
# Calculate earnings_per_share from quaterly results in 2020
income_statement = tick.income_statement(frequency='q').set_index('asOfDate')
eps_qtr_2020 = income_statement['DilutedEPS'].dropna()
# Sum the eps for each quarter of 2020 to get the annual eps for 2020
eps_2020 = eps_qtr_2020.loc['2020-03-31':'2020-12-31'].sum()
# Insert the 2020 eps into the results dataframe under a new index '2020-12-31'
amd.loc['2020-12-31'] = [eps_2020]
print (amd)

# calculate eps growth rate
# The year on year eps growth rate is calculated using the percent change function
# The results are posted to a new column 'EPS_growth' in the results dataframe
amd['EPS_growth'] = amd['DilutedEPS'].pct_change()
print (amd)

# Moat Analysis - Second of our growth measures is growth in CashFlow per Share
# Extract Cashflow from operations from 2017 to 2020
operating_cashflow = (cash_flow_statement['OperatingCashFlow']/balance_sheet['OrdinarySharesNumber'])
operating_cashflow = operating_cashflow[~operating_cashflow.index.duplicated()]
# The results are posted to a new column 'operating_cashflow' in the results dataframe
amd['operating_cashflow'] = operating_cashflow.values

# Calculate the year on year growth rate for Operations CashFlow
amd['opcashflow_growth'] = amd['operating_cashflow'].pct_change()
print(amd)

# Extract Free Cashflow history from 2017 to 2020 and post to results DataFrame
free_cashflow = (cash_flow_statement['FreeCashFlow']/balance_sheet['OrdinarySharesNumber'])
free_cashflow = free_cashflow[~free_cashflow.index.duplicated()]
amd['free_cashflow'] = free_cashflow.values
#Estimate the Cashflow growth rate for Free CashFlow per Share
amd['free_cashflow_growth'] = amd['free_cashflow'].pct_change()
print (amd)

# Moat Analysis - Third of our growth measures is Sales Growth
# Extract top-line annual sales revenue from 2017 to 2020 from income statement
income_statement = tick.income_statement(frequency='a').set_index('asOfDate')
sales = income_statement['OperatingRevenue']
sales = sales[~sales.index.duplicated()]
# post annual sales data to results DataFrame
amd['Sales_Revenue'] = sales.values
# Estimate the Sales growth rate from annual sales 2017 to 2020
amd['Sales_growth'] = amd['Sales_Revenue'].pct_change()
print (amd)

# Moat Analysis - Fourth of our growth measures is growth in Book Value per share (BVPS)
# Extract Book Value and Book Value per Share information from 2017 to 2020
book_value = (balance_sheet['NetTangibleAssets']/balance_sheet['OrdinarySharesNumber'])
book_value = book_value[~book_value.index.duplicated()]
amd['book_value'] = book_value.values
# Estimate the Book Value per Share growth rate from 2017 to 2020 BVPS data
amd['book_value_growth'] = amd['book_value'].pct_change()
print(amd)

# Management Analysis
# Here we are looking for measures of management effectiveness

# Return on Invested Capital (ROIC) and Return on Equity (ROE) will be calculated
# Companies that have a high ROIC efficiently use the capital that they raised to grow the business
# ROIC is Net Operating Profit after tax / (Debt and Equity)
# Extract data, from income statement and balance sheet from 2017 to 2020
roic = (income_statement['NetIncomeCommonStockholders']/(balance_sheet['TotalDebt']+balance_sheet['CommonStockEquity']))
roic = roic[~roic.index.duplicated()]
amd['ROIC']=roic.values
# calculate the Book Value per share growth rate year to year
# and post to results DataFrame
amd['ROIC_growth'] = amd['ROIC'].pct_change()
print (amd)

# Management Analysis - ROE
# Extract Information to calculate Return on Equity (ROE) 2017 - 2020
# ROE = Net Income / Shareholder's Equity
roe = (income_statement['OperatingIncome']/balance_sheet['CommonStockEquity'])
roe = roe[~roe.index.duplicated()]
amd['ROE']=roe.values
# look at year to year change in ROE
amd['ROE_growth'] = amd['ROE'].pct_change()
print (amd)

# Debt Analysis - How much Debt is the company carrying ?
# The debt-to-earnings measures the time in years to pay off current debt at current level of earnings
# debt to earnings = (Long Term Debt / Net Income)
debt_to_earnings =(income_statement['OperatingIncome']/balance_sheet['TotalDebt'])
debt_to_earnings = debt_to_earnings[~debt_to_earnings.index.duplicated()]
amd['debt_to_earnings'] = debt_to_earnings.values


# The final stage - putting it all together to put a value on the stock
# First we need an estimate for the future price to earnings (future PE estimate)
# The forward PE is available on the key statistics tab on yahoo finance
forward_PE_estimate = tick.key_stats[symbol]['forwardPE']
print (forward_PE_estimate)
amd['forward_PE_estimate'] = forward_PE_estimate

# We need an estimate for earnings_per_share
# The forward EPS is availible on the key statistics tab on Yahoo finance
forward_eps_estimate = tick.key_stats[symbol]['forwardEps']
amd['forward_eps_estimate'] = forward_eps_estimate
print (amd)

# We need an estimate for longterm earnings per share growth rate
# We get the analyst's forward price to earnings (PE) and price-to-earnings growth (PEG) figures from Yahoo finance
# Estimate of long-term earnings per share growth = PE / PEG

growth_rate_estimate_analysts = tick.key_stats[symbol]['forwardPE']/tick.key_stats[symbol]['pegRatio']
amd['growth_rate_estimate']= growth_rate_estimate_analysts
print (growth_rate_estimate_analysts)

# import numpy financial model using alias npf
import numpy_financial as npf
# calculate future earnings per share
# We need to use numpy future value function
# future_eps = np.fv(interestRate,numberOfYears,-initialInvestment(current eps),when='begin')
# In the formula we use the estimate for growth rate as the 'interestRate'
# In the formula we use number of years = 10, as we are long term investors looking for value
# In the formula the 'InitialInvestment' is the current EPS (earnings per share)
future_eps = npf.fv(growth_rate_estimate_analysts/100,10.0,0,-forward_eps_estimate)
amd['future_EPS'] = future_eps
print (amd)
# Calculate future stock price
# The future stock price is the estimated (future) eps multiplied by the estimated forward PE
future_stock_price = future_eps * forward_PE_estimate
amd['future_stock_price'] = future_stock_price
print (amd)
# Calculate the target stock price
# We need to use numpy present value function
# target_stock_price = np.pvnumpy.pv(rate, nper, pmt, fv=0, when='end')
# rate: an interest rate which is my minimum acceptable rate of return (MAAR) of 15%
# nper = investment period in years, wew are using 10 years
# a (fixed) payment, pmt, which we set to zero
# a future value, fv, which is the future stock price determined above
target_stock_price = npf.pv(0.15, 10, 0, future_stock_price)*-1
amd['target_stock_price'] = target_stock_price
amd['margin_of_safety'] = amd['target_stock_price']/2
print (amd)

# Export our DataFrame of Results as a csv file to the current working directory
amd.to_csv(r'C:\Users\DanMacCarthy\Desktop\amd.csv')

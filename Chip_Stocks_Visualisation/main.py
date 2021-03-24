# Visualisation of the Stock Data

import matplotlib.pyplot as plt
import pandas as pd

adi = pd.read_csv('adi.csv', parse_dates=['Year'], index_col=['Year'])
amd = pd.read_csv('amd.csv', parse_dates=['Year'], index_col=['Year'])
intc = pd.read_csv('intc.csv',parse_dates=['Year'], index_col=['Year'])
nvda = pd.read_csv('nvda.csv',parse_dates=['Year'], index_col=['Year'])
qcom = pd.read_csv('qcom.csv',parse_dates=['Year'], index_col=['Year'])

# compare sales revenue by company for 2020
# using a barchart

fig, ax = plt.subplots()
ax.bar('adi', adi.loc['31-10-2020']['Sales_Revenue'])
ax.bar('amd', amd.loc['31-12-2020']['Sales_Revenue'])
ax.bar('intc',intc.loc['31-12-2020']['Sales_Revenue'])
ax.bar('nvda', nvda.loc['31-12-2020']['Sales_Revenue'])
ax.bar('qcom', qcom.loc['30-09-2020']['Sales_Revenue'])
ax.tick_params(axis='x', rotation=70)
ax.set_ylabel('Annual Sales Revenue $')
plt.show()
#fig.savefig('annual_sales_revenue', dpi=250)

# plot sales revenue by company

fig, ax = plt.subplots()
ax.plot(adi.index, adi['Sales_Revenue'], marker='o')
ax.set_xlabel('Year')
ax.tick_params(axis='x', rotation=70)
ax.set_ylabel('Sales revenue')
ax.set_title('Analog Devices sales revenue')
plt.show()

fig, ax = plt.subplots()
ax.plot(amd.index, amd['Sales_Revenue'], marker='o')
ax.set_xlabel('Year')
ax.tick_params(axis='x', rotation=70)
ax.set_ylabel('Sales revenue')
ax.set_title('Advanced Micro Devices sales revenue')
plt.show()

fig, ax = plt.subplots()
ax.plot(intc.index, intc['Sales_Revenue'], marker='o')
ax.set_xlabel('Year')
ax.tick_params(axis='x', rotation=70)
ax.set_ylabel('Sales revenue')
ax.set_title('Intel sales revenue')
plt.show()

fig, ax = plt.subplots()
ax.plot(nvda.index, nvda['Sales_Revenue'], marker='o')
ax.set_xlabel('Year')
ax.tick_params(axis='x', rotation=70)
ax.set_ylabel('Sales revenue')
ax.set_title('NVIDIA sales revenue')
plt.show()

fig, ax = plt.subplots()
ax.plot(qcom.index, qcom['Sales_Revenue'], marker='o')
ax.set_xlabel('Year')
ax.tick_params(axis='x', rotation=70)
ax.set_ylabel('Sales revenue')
ax.set_title('QUALCOMM sales revenue')
plt.show()

# Analog Devices (adi) and Qualcomm (qcom) have declining sales trend
# We delete them from our watchlist

# Earnings per share is not directly comparable between the stcoks
# we will plot earnings per share to visualise the growth rate

fig, ax = plt.subplots()
ax.plot(adi.index, amd['DilutedEPS'], marker='o')
ax.set_xlabel('Year')
ax.tick_params(axis='x', rotation=70)
ax.set_ylabel('earnings per share $')
ax.set_title('AMD eps')
plt.show()

fig, ax = plt.subplots()
ax.plot(adi.index, intc['DilutedEPS'], marker='o')
ax.set_xlabel('Year')
ax.tick_params(axis='x', rotation=70)
ax.set_ylabel('earnings per share $')
ax.set_title('Intel eps')
plt.show()

fig, ax = plt.subplots()
ax.plot(adi.index, nvda['DilutedEPS'], marker='o')
ax.set_xlabel('Year')
ax.tick_params(axis='x', rotation=70)
ax.set_ylabel('earnings per share')
ax.set_title('NVIDIA eps')
plt.show()

# Debt to Equity Comparison
fig, ax = plt.subplots()
ax.plot(amd.index, amd['debt_to_earnings'], marker='o', color='red')
ax.plot(intc.index, intc['debt_to_earnings'], marker='o',color='green')
ax.plot(nvda.index, nvda['debt_to_earnings'], marker='o', color='blue')
ax.set_ylabel('debt_to_earnings ratio')
ax.tick_params(axis='x', rotation=70)
ax.legend()
plt.show()





